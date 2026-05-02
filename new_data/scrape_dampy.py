"""
Scrape DamPy (https://spl.gov.py/dampy/) — Comida, Fauna, Flora categories.

For each entry page saves:
  - Castellano (Spanish) label
  - Guaraní label
  - All main-content images (skips assets_dampy/brand logos)
  - Page URL, category, h2 title

Output:
  <out_dir>/dampy_metadata.csv
  <out_dir>/images/<Category>/<entry_slug>/<filename>

Usage:
  python3 scrape_dampy.py                          # full scrape
  python3 scrape_dampy.py --dry-run --max-entries 2
  python3 scrape_dampy.py --timeout 240 --delay 2.0 --retries 10
  python3 scrape_dampy.py --out-dir /path/to/output
"""

import argparse
import csv
import http.cookiejar
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

BASE_URL = "https://spl.gov.py/dampy/"

LISTINGS = [
    ("Comida", "Comida/comidas.html"),
    ("Fauna",  "Fauna/fauna.html"),
    ("Flora",  "Flora/flora.html"),
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-PY,es;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "identity",  # avoid gzip so we can read raw bytes easily
    "Connection": "keep-alive",
}

CSV_FIELDS = [
    "category", "page_url", "title_h2",
    "spanish", "guarani",
    "image_count", "image_paths",
]


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def make_opener(jar):
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    opener.addheaders = list(HEADERS.items())
    return opener


def fetch(opener, url, timeout, retries, delay):
    """Fetch URL, return bytes. Raises on permanent failure."""
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with opener.open(req, timeout=timeout) as resp:
                return resp.read()
        except (urllib.error.URLError, OSError) as e:
            last_err = e
            wait = delay * attempt
            print(f"  [warn] attempt {attempt}/{retries} failed for {url}: {e}. "
                  f"Retrying in {wait:.1f}s …", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"All {retries} attempts failed for {url}: {last_err}")


def download_image(opener, url, dest_path, timeout, retries, delay):
    """Download image to dest_path. Skip if already exists. Returns True if saved."""
    if dest_path.exists():
        return False
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    data = fetch(opener, url, timeout, retries, delay)
    dest_path.write_bytes(data)
    return True


# ---------------------------------------------------------------------------
# HTML parsers
# ---------------------------------------------------------------------------

class LinkCollector(HTMLParser):
    """Collect all <a href="*.html"> from a listing page."""

    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        attrs = dict(attrs)
        href = attrs.get("href", "")
        if href.endswith(".html") and "://" not in href:
            full = urllib.parse.urljoin(self.base_url, href)
            if full not in self.links:
                self.links.append(full)


class EntryParser(HTMLParser):
    """
    Parse a DamPy entry page.

    Extracts:
      title_h2   — text of first <h2>
      spanish    — text after a label containing "Castellano"
      guarani    — text after a label containing "Guaraní" or "Guarani"
      img_srcs   — src of <img> tags not under assets_dampy/brand
    """

    def __init__(self):
        super().__init__()
        self.title_h2 = ""
        self.spanish = ""
        self.guarani = ""
        self.img_srcs = []

        # state
        self._in_h2 = False
        self._h2_done = False
        self._current_text = []

        # bilingual label detection
        # Strategy: scan all text nodes; when we see a label keyword, the
        # NEXT non-empty text sibling is the value.
        self._all_text_nodes = []   # list of str in document order
        self._pending_label = None  # "castellano" | "guarani"

        # img tracking
        self._tag_stack = []

    def handle_starttag(self, tag, attrs):
        self._tag_stack.append(tag)
        attrs = dict(attrs)

        if tag == "h2" and not self._h2_done:
            self._in_h2 = True
            self._current_text = []

        if tag == "img":
            src = attrs.get("src", "")
            if src and "assets_dampy/brand" not in src and "logo" not in src.lower():
                self.img_srcs.append(src)

    def handle_endtag(self, tag):
        if self._tag_stack and self._tag_stack[-1] == tag:
            self._tag_stack.pop()
        if tag == "h2" and self._in_h2:
            self._in_h2 = False
            self._h2_done = True
            self.title_h2 = " ".join(self._current_text).strip()

    def handle_data(self, data):
        text = data.strip()

        if self._in_h2:
            if text:
                self._current_text.append(text)
            return

        if not text:
            return

        # Check if this text node is a label keyword
        low = text.lower().rstrip(":").strip()
        if low == "castellano":
            self._pending_label = "castellano"
            return
        if low in ("guaraní", "guarani"):
            self._pending_label = "guarani"
            return

        # Otherwise it may be the value for the pending label
        if self._pending_label == "castellano" and not self.spanish:
            self.spanish = text
            self._pending_label = None
            return
        if self._pending_label == "guarani" and not self.guarani:
            self.guarani = text
            self._pending_label = None
            return

        # Reset pending label if we hit unrelated content
        # (only reset after non-empty, non-label text)
        self._pending_label = None


def parse_entry(html_bytes, page_url):
    """Return dict with title_h2, spanish, guarani, img_srcs."""
    try:
        html = html_bytes.decode("utf-8", errors="replace")
    except Exception:
        html = html_bytes.decode("latin-1", errors="replace")

    parser = EntryParser()
    parser.feed(html)

    # Resolve relative image URLs
    resolved = []
    for src in parser.img_srcs:
        resolved.append(urllib.parse.urljoin(page_url, src))

    return {
        "title_h2": parser.title_h2,
        "spanish":  parser.spanish,
        "guarani":  parser.guarani,
        "img_srcs": resolved,
    }


def collect_links(html_bytes, listing_url):
    try:
        html = html_bytes.decode("utf-8", errors="replace")
    except Exception:
        html = html_bytes.decode("latin-1", errors="replace")
    collector = LinkCollector(listing_url)
    collector.feed(html)
    return collector.links


# ---------------------------------------------------------------------------
# Slug helpers
# ---------------------------------------------------------------------------

def url_to_slug(url):
    """Turn an entry URL into a filesystem-safe slug."""
    name = urllib.parse.urlparse(url).path.rstrip("/").split("/")[-1]
    name = re.sub(r"\.html?$", "", name, flags=re.I)
    name = re.sub(r"[^a-zA-Z0-9_\-]", "_", name)
    return name or "entry"


def img_filename(img_url, idx):
    """Derive a filename from an image URL, with index fallback."""
    path = urllib.parse.urlparse(img_url).path
    name = path.split("/")[-1]
    if not name or "." not in name:
        name = f"image_{idx:03d}.jpg"
    return name


# ---------------------------------------------------------------------------
# Main scrape logic
# ---------------------------------------------------------------------------

def scrape(args):
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "dampy_metadata.csv"

    # Load already-scraped URLs to allow resuming
    scraped_urls = set()
    if csv_path.exists():
        with csv_path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                scraped_urls.add(row.get("page_url", ""))
        print(f"Resuming — {len(scraped_urls)} entries already in CSV.")

    jar = http.cookiejar.CookieJar()
    opener = make_opener(jar)

    # Warm up session with root page
    try:
        print("Warming up session …")
        fetch(opener, BASE_URL, args.timeout, 2, args.delay)
        time.sleep(args.delay)
    except Exception as e:
        print(f"[warn] Root warmup failed: {e}", file=sys.stderr)

    write_header = not csv_path.exists() or csv_path.stat().st_size == 0
    csv_file = csv_path.open("a", newline="", encoding="utf-8")
    writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
    if write_header:
        writer.writeheader()

    total_entries = 0
    total_images = 0

    for category, listing_rel in LISTINGS:
        listing_url = BASE_URL + listing_rel
        print(f"\n=== {category} — fetching listing: {listing_url}")

        try:
            listing_html = fetch(opener, listing_url, args.timeout, args.retries, args.delay)
        except Exception as e:
            print(f"[error] Could not fetch listing for {category}: {e}", file=sys.stderr)
            continue

        time.sleep(args.delay)

        links = collect_links(listing_html, listing_url)
        print(f"  Found {len(links)} entry links.")

        if args.max_entries:
            links = links[: args.max_entries]
            print(f"  (capped to {args.max_entries} for --max-entries)")

        for i, entry_url in enumerate(links, 1):
            if entry_url in scraped_urls:
                print(f"  [{i}/{len(links)}] skip (already scraped): {entry_url}")
                continue

            print(f"  [{i}/{len(links)}] {entry_url}")

            if args.dry_run:
                writer.writerow({
                    "category": category,
                    "page_url": entry_url,
                    "title_h2": "(dry-run)",
                    "spanish": "(dry-run)",
                    "guarani": "(dry-run)",
                    "image_count": 0,
                    "image_paths": "",
                })
                csv_file.flush()
                scraped_urls.add(entry_url)
                total_entries += 1
                time.sleep(args.delay)
                continue

            try:
                entry_html = fetch(opener, entry_url, args.timeout, args.retries, args.delay)
            except Exception as e:
                print(f"    [error] fetch failed: {e}", file=sys.stderr)
                time.sleep(args.delay)
                continue

            entry = parse_entry(entry_html, entry_url)
            slug = url_to_slug(entry_url)
            img_dir = out_dir / "images" / category / slug

            saved_paths = []
            for idx, img_url in enumerate(entry["img_srcs"]):
                fname = img_filename(img_url, idx)
                dest = img_dir / fname
                rel_path = dest.relative_to(out_dir)
                try:
                    saved = download_image(opener, img_url, dest, args.timeout, args.retries, args.delay)
                    if saved:
                        print(f"    img saved: {rel_path}")
                    else:
                        print(f"    img exists: {rel_path}")
                    saved_paths.append(str(rel_path))
                    total_images += saved
                except Exception as e:
                    print(f"    [warn] image download failed {img_url}: {e}", file=sys.stderr)
                time.sleep(args.delay * 0.5)

            writer.writerow({
                "category":    category,
                "page_url":    entry_url,
                "title_h2":    entry["title_h2"],
                "spanish":     entry["spanish"],
                "guarani":     entry["guarani"],
                "image_count": len(saved_paths),
                "image_paths": "|".join(saved_paths),
            })
            csv_file.flush()
            scraped_urls.add(entry_url)
            total_entries += 1

            print(f"    title={entry['title_h2']!r}  "
                  f"es={entry['spanish']!r}  "
                  f"gn={entry['guarani']!r}  "
                  f"imgs={len(saved_paths)}")

            time.sleep(args.delay)

    csv_file.close()
    print(f"\nDone. {total_entries} entries, {total_images} new images.")
    print(f"CSV: {csv_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    default_out = str(Path(__file__).parent / "dampy_output")

    p = argparse.ArgumentParser(
        description="Scrape DamPy (spl.gov.py/dampy/) — Comida, Fauna, Flora."
    )
    p.add_argument("--out-dir",    default=default_out,
                   help=f"Output directory (default: {default_out})")
    p.add_argument("--dry-run",    action="store_true",
                   help="Fetch listing pages only; do not download images or entry pages")
    p.add_argument("--max-entries", type=int, default=0,
                   help="Cap entries per category (0 = all)")
    p.add_argument("--timeout",    type=int, default=120,
                   help="Per-request timeout in seconds (default: 120)")
    p.add_argument("--retries",    type=int, default=5,
                   help="Max retries per request (default: 5)")
    p.add_argument("--delay",      type=float, default=1.0,
                   help="Seconds between requests (default: 1.0)")
    args = p.parse_args()

    if "/path/to" in args.out_dir:
        p.error("--out-dir contains placeholder '/path/to'; supply a real path or omit it.")

    print(f"Output dir : {args.out_dir}")
    print(f"Dry-run    : {args.dry_run}")
    print(f"Max entries: {args.max_entries or 'all'}")
    print(f"Timeout    : {args.timeout}s  Retries: {args.retries}  Delay: {args.delay}s")

    scrape(args)


if __name__ == "__main__":
    main()

# Guarani Culture Visual Dataset

A multimodal dataset of images paired with bilingual Spanish/Guarani labels and cultural metadata, built to support fine-tuning of culturally aware visual language models (VLMs) for Guarani and Paraguayan cultural contexts.

---

## Project Structure

```
new_data/
├── README.md                        # This file
├── scrape_dampy.py                  # DamPy scraper script
├── dampy_output/
│   ├── dampy_metadata.csv           # One row per entry (111 rows)
│   └── images/
│       ├── Comida/{entry}/          # Food images (42 entries)
│       ├── Fauna/{entry}/           # Animal images (47 entries)
│       └── Flora/{entry}/           # Plant images (22 entries)
└── ia_output/
    ├── ia_metadata.csv              # One row per item (17 items)
    └── images/
        └── {identifier}/           # Images per IA item
            ├── {image}.jpg          # Full-size images (keep)
            ├── {image}_thumb.jpg    # IA thumbnails (filter before training)
            └── __ia_thumb.jpg       # IA auto-thumb (filter before training)
```

---

## Dataset Summary

| Source | Entries | Images | Bilingual Labels | Date Scraped |
|---|---|---|---|---|
| DamPy (spl.gov.py) | 111 | 112 | Spanish + Guarani | April 2026 |
| Internet Archive | 18 | ~42 full-size | Metadata only | April 2026 |
| **Total** | **129** | **~154** | | |

---

## Source 1: DamPy — Diccionario Audiovisual Multilingüe del Paraguay

### What It Is
DamPy is an official audiovisual multilingual dictionary published by the Secretaría de Políticas Lingüísticas (SPL) of Paraguay at `spl.gov.py/dampy/`. It contains curated entries for Paraguayan food, fauna, and flora, each with a photograph and bilingual labels in Spanish (Castellano) and Guarani.

### Dataset Contents
- **111 entries** across three categories (1 entry was a broken link on the site: `empanada`)
- **112 images** (one image per entry; a small number of entries have multiple)
- **Categories:**
  - `Comida` (Food) — 42 entries: traditional Paraguayan dishes, ingredients, and preparations
  - `Fauna` (Animals) — 47 entries: birds, mammals, reptiles native to Paraguay
  - `Flora` (Plants) — 22 entries: trees, fruits, and plants of the Paraguayan ecosystem
- **Bilingual labels:** Spanish name from the "Castellano" field and Guarani name from the "Guaraní" field on each page. ~16 of 111 entries have a Guarani label; the remainder either have no Guarani term listed on the site or use a format the parser did not capture.

### CSV Schema (`dampy_metadata.csv`)

| Column | Description | Example |
|---|---|---|
| `category` | Comida, Fauna, or Flora | `Fauna` |
| `page_url` | Full URL of the entry page | `https://spl.gov.py/dampy/Fauna/yaguarete/yaguarete.html` |
| `title_h2` | Page heading (`<h2>`) | `yaguareté` |
| `spanish` | Spanish label from "Castellano" field | `yaguareté` |
| `guarani` | Guarani label from "Guaraní" field | `jaguarete` |
| `image_count` | Number of images downloaded | `1` |
| `image_paths` | Pipe-separated relative paths under `dampy_output/` | `images/Fauna/yaguarete/yaguarete_0.jpg` |

### Scraping Methodology

#### 1. Listing Pages
The scraper fetches three category listing pages:
- `https://spl.gov.py/dampy/Comida/comidas.html` → 43 links
- `https://spl.gov.py/dampy/Fauna/fauna.html` → 47 links
- `https://spl.gov.py/dampy/Flora/flora.html` → 22 links

Entry URLs are extracted from `<li><a href="...html">` elements. URLs containing spaces or non-ASCII characters in the path are normalized with `urllib.parse.unquote` followed by `urllib.parse.quote` to avoid double-encoding.

#### 2. Entry Page Parsing
For each entry page, the scraper uses regex to extract:
- **Title:** first `<h2>` inside `<main>`
- **Spanish label:** content of `<b>` following `Castellano:`
- **Guarani label:** content of `<b>` following `Guaraní:` (handles variant spellings `Guarani`/`Guaraní` and a leading colon artifact in some entries)

#### 3. Image Download
All `<img src="...">` tags are collected, excluding:
- Site logos under `assets_dampy/brand/` or `/brand/`
- `data:` URIs (inline images)

Images are saved as `images/{Category}/{slug}/{slug}_{index}{ext}`. Non-ASCII characters in image filenames (e.g. `ñ`) are percent-encoded before download.

#### 4. Reliability
- 0.5-second delay between requests
- Up to 8 retries on network errors with exponential backoff (1s → 17s)
- HTTP 401, 403, 404 errors fail immediately without retry
- 1 entry skipped due to a server-side 404 (`empanada`)

#### Reproducing the Scrape

```bash
# Requires Python 3.9+ and network access to spl.gov.py (site can be slow)
# Test connectivity first:
curl -I --connect-timeout 30 --max-time 60 -A "Mozilla/5.0" \
  "https://spl.gov.py/dampy/Comida/comidas.html"

# Dry run (no downloads, first 5 entries)
python3 scrape_dampy.py --dry-run --max-entries 5

# Full scrape
python3 scrape_dampy.py

# If site is slow, increase timeout and retries
python3 scrape_dampy.py --timeout 240 --retries 10
```

---

## Source 2: Internet Archive

### What It Is
The Internet Archive (`archive.org`) is a non-profit digital library hosting freely accessible cultural heritage materials. No API key is required. Items are searched via the Advanced Search API and images downloaded directly.

### Dataset Contents
- **18 items** curated from 25 raw search results
- **~42 full-size images** (plus IA-generated thumbnails `_thumb.jpg` and audio spectrograms `_spectrogram.png`)
- Content covers:

| Theme | Example Items |
|---|---|
| Indigenous rights & land defense | Guarani-Kaiowá demarcation protests in Brazil |
| Music in Guarani language | Paraguayan folk songs by Edgar Galeano Domínguez |
| Indigenous community media | Rádio Araça-i (Guarani community radio) |
| Cultural events | First Indigenous Culture Conference of Curitiba (Guarani-Kaiowá) |
| Guarani mythology | Ao Ao monster digital art |
| Guarani poetry | Interview with poet Susy Delgado (jopara: Spanish/Guarani mix) |
| Paraguay material culture | Banknotes denominated in Guaraní currency (1952–2007) |
| Folklore and dance | Festival Internacional de la Tierra Guaraní; Bolivian Guarani dances |
| Geography | Satellite imagery of South America including Paraguay |

### CSV Schema (`ia_metadata.csv`)

| Column | Description |
|---|---|
| `identifier` | Internet Archive item ID |
| `page_url` | Full URL to the IA item page |
| `title` | Item title |
| `creator` | Author or uploader |
| `date` | Publication date (if available) |
| `subject` | Tags/subjects from IA metadata |
| `mediatype` | IA mediatype (all `image`) |
| `description` | Item description (truncated to 500 chars) |
| `image_count` | Number of image files downloaded |
| `image_paths` | Pipe-separated relative paths under `ia_output/` |

### Scraping Methodology

#### 1. Search
The IA Advanced Search API was queried with `guarani AND mediatype:image`, which returned **25 items**. A broader query (`guarani`) returns ~8,500 items but the vast majority are Wikimedia dump files, audio recordings, and texts with no images.

#### 2. File Discovery
For each item, the metadata API (`/metadata/{identifier}/files`) returns a file list. Files are selected if their `format` field matches known image types (JPEG, PNG, GIF, TIFF, JPEG 2000, etc.) or their filename has an image extension. Files whose names contain encoded external URLs (pattern `https3A2F2F`) are excluded — these point to third-party CDN content requiring authentication.

#### 3. Download
Images are downloaded from `https://archive.org/download/{identifier}/{filename}` with:
- 0.5-second delay between requests
- Up to 6 retries on network errors
- Immediate failure on HTTP 401/403/404

#### 4. Manual Curation
7 of the 25 items were removed after inspection:

| Removed Item | Reason |
|---|---|
| `guia_inscripcion_examen_siu_guarani` | SIU Guaraní = Argentine university admin software, not Guarani people |
| `guia_dcto_medio_boleto` | Argentine student bus pass guide (same software) |
| `guia_general_uso_SIU-Guarani` | SIU software user guide |
| `cert_alumn_regular_siu_guarani` | SIU software tutorial |
| `pileofpapyrus` | The Sims 3 game content |
| `jukah-art-by-the_enigma_69420` | Speculative evolution art; no Guarani cultural connection |
| `restored-album-art-05` | Generic folk album art; no Guarani content |

#### Reproducing the Scrape

```bash
# No API key required. Python 3.9+ stdlib only.

# Dry run
python3 scrape_ia.py --dry-run --max-items 10

# Full scrape
python3 scrape_ia.py

# Custom query
python3 scrape_ia.py --query "guarani AND mediatype:image"
```

---

## Intended Use

This dataset is designed for:
- **Fine-tuning visual language models (VLMs)** on culturally underrepresented content
- **Bilingual image captioning** in Spanish and Guarani (DamPy entries)
- **Cultural recognition tasks** — identifying Paraguayan food, fauna, flora, and indigenous cultural contexts
- **Multimodal research** on indigenous South American languages and cultures

### Joining the Two Datasets
The two CSVs can be used independently or merged. They share no common key, but both provide `page_url` as a stable identifier. For VLM training, DamPy entries are the higher-quality source because each image has structured bilingual labels. Internet Archive items provide broader cultural context but lack per-image labels.

---

## Known Limitations

| Limitation | Details |
|---|---|
| Small size | ~154 images total. Wikimedia Commons alone could provide 500–2,000+ additional images. |
| Missing Guarani labels (DamPy) | 95 of 111 DamPy entries have no Guarani label — either the site itself has no Guarani term for that entry, or the HTML structure variant was not captured by the parser. |
| Thumbnails mixed in (IA) | Filter out `_thumb.jpg` and `_spectrogram.png` files before training. |
| License varies (IA) | Check each item's `page_url` for specific license terms before redistribution. |
| DamPy availability | `spl.gov.py` can be slow or unreachable outside business hours (Paraguay time, UTC-4). |
| 1 broken entry (DamPy) | `empanada` returns HTTP 404 on the server; skipped automatically. |

---

## Next Steps for Expanding the Dataset

| Source | Expected Images | Notes |
|---|---|---|
| Wikimedia Commons | 500–2,000+ | Categories: `Guaraní people`, `Guaraní language`, `Indigenous peoples of Paraguay`; free API, no key needed |
| DamPy (re-scrape) | Same 112 | Fix Guarani label parser to capture more HTML variants |
| Internet Archive (broader) | 100–300 | Query `guarani Paraguay` without `mediatype:image`; most items will still have 0 images |

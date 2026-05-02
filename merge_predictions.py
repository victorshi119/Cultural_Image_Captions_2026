import json
from pathlib import Path
#utils to merge the generated captions (in TSV format) with the original JSONL file containing image metadata.
#so we can have a single JSONL file with both metadata and generated captions ready for submission.

def load_tsv_predictions(tsv_path: str) -> dict:
    """
    Returns: {image_id_or_filename: caption}
    """
    preds = {}
    with open(tsv_path, "r", encoding="utf-8") as f:
        for line in f:
            if "\t" not in line:
                continue
            img_id, caption = line.strip().split("\t", 1)
            preds[img_id] = caption
    return preds


def merge_jsonl_with_predictions(jsonl_path: str, tsv_path: str, output_path: str):
    preds = load_tsv_predictions(tsv_path)

    with open(jsonl_path, "r", encoding="utf-8") as fin, \
         open(output_path, "w", encoding="utf-8") as fout:

        for line in fin:
            if not line.strip():
                continue

            obj = json.loads(line)

            # match key: filename OR id (depending on your TSV)
            filename = Path(obj["filename"]).name  # e.g. grn_051.jpg
            stem = Path(obj["filename"]).stem      # e.g. grn_051

            # try both matching strategies
            caption = None
            if filename in preds:
                caption = preds[filename]
            elif stem in preds:
                caption = preds[stem]

            if caption is not None:
                obj["predicted_caption"] = caption
            else:
                obj["predicted_caption"] = None  # or skip if you prefer

            fout.write(json.dumps(obj, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonl", required=True, help="input jsonl file")
    parser.add_argument("--tsv", required=True, help="generated captions tsv")
    parser.add_argument("--output", default="merged.jsonl")

    args = parser.parse_args()

    merge_jsonl_with_predictions(
        jsonl_path=args.jsonl,
        tsv_path=args.tsv,
        output_path=args.output
    )
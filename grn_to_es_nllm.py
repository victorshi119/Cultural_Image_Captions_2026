#!/usr/bin/env python3
"""
Translate Guaraní captions to Spanish using NLLB.
"""

from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL = "facebook/nllb-200-3.3B"
SRC_LANG = "grn_Latn"
TGT_LANG = "spa_Latn"

BATCH_SIZE = 4
MAX_NEW_TOKENS = 256

# Load model once 
device = "cuda"
tok = AutoTokenizer.from_pretrained(MODEL)
tok.src_lang = SRC_LANG

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL, torch_dtype=torch.float16
).to(device)

model.eval()


def translate(caps):
    out = []

    for i in range(0, len(caps), BATCH_SIZE):
        batch = [c.strip() for c in caps[i:i+BATCH_SIZE]]

        enc = tok(batch, return_tensors="pt", padding=True, truncation=True).to(device)

        gen = model.generate(
            **enc,
            forced_bos_token_id=tok.convert_tokens_to_ids(TGT_LANG),
            max_new_tokens=MAX_NEW_TOKENS,
        )

        out.extend(tok.batch_decode(gen, skip_special_tokens=True))

    return out


def main():
    # Input/output paths: currently working as single file translation
    in_path = Path("outputs/v4_ablation/ablation_add1_all.tsv")
    out_path = Path("outputs/v4_ablation_es/ablation_add1_all_es.tsv")

    imgs = []
    caps = []

    # Read TSV
    for line in in_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        # Image id and caption are separated by a tap
        img, cap = line.split("\t", 1)
        imgs.append(img)
        caps.append(cap)

    # Translate
    es_caps = translate(caps)

    # Write output
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for img, cap in zip(imgs, es_caps):
            f.write(f"{img}\t{cap}\n")


if __name__ == "__main__":
    main()
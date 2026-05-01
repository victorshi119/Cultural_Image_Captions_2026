#!/usr/bin/env python3
"""
Upload Guarani cultural image dataset to Hugging Face.
Repo: victorgo119/Guarani_cultural_images (dataset)
"""

import os
import sys
from pathlib import Path
from huggingface_hub import HfApi, create_repo

REPO_ID = "victorgo119/Guarani_cultural_images"
BASE    = Path(__file__).parent

api = HfApi()

# Create repo (no-op if already exists)
print(f"Creating dataset repo {REPO_ID} ...")
create_repo(REPO_ID, repo_type="dataset", exist_ok=True, private=False)
print("Repo ready.")

# ── Upload metadata CSVs ──────────────────────────────────────────────────────
for csv in ["dampy_output/dampy_metadata.csv", "ia_output/ia_metadata.csv"]:
    src = BASE / csv
    dest = csv  # same relative path in repo
    print(f"Uploading {dest} ...")
    api.upload_file(path_or_fileobj=str(src), path_in_repo=dest,
                    repo_id=REPO_ID, repo_type="dataset")

# ── Upload DamPy images (all 112, keep folder structure) ─────────────────────
print("Uploading dampy_output/images/ ...")
api.upload_folder(
    folder_path=str(BASE / "dampy_output" / "images"),
    path_in_repo="dampy_output/images",
    repo_id=REPO_ID,
    repo_type="dataset",
    ignore_patterns=[],
)
print("DamPy images done.")

# ── Upload IA images (full-size only, skip thumbnails/spectrograms) ───────────
ia_images = BASE / "ia_output" / "images"
full_size = [
    p for p in ia_images.rglob("*")
    if p.is_file()
    and "_thumb" not in p.name
    and "__ia_thumb" not in p.name
    and "_spectrogram" not in p.name
]
print(f"Uploading {len(full_size)} full-size IA images ...")
api.upload_folder(
    folder_path=str(ia_images),
    path_in_repo="ia_output/images",
    repo_id=REPO_ID,
    repo_type="dataset",
    ignore_patterns=["*_thumb.jpg", "__ia_thumb.jpg", "*_spectrogram.png"],
)
print("IA images done.")

print(f"\nAll done. View at: https://huggingface.co/datasets/{REPO_ID}")

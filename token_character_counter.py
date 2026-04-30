#!/usr/bin/env python3
"""
Token and Character counter for a text file
(approximate: splits on whitespace)
"""

from pathlib import Path

# FILE = Path("apertium_grn_summary.txt")

# text = FILE.read_text(encoding="utf-8")

# # Tokenization 
# # split by whitespace
# tokens = text.split()

# print(f"File: {FILE}")
# print(f"Characters: {len(text):,}")
# print(f"Tokens (approx): {len(tokens):,}")

# Target directory
BASE = Path("/N/project/CoRSAL/Cultural_Image_Captions_2026/resources")

# Get all .txt and .json files
files = list(BASE.glob("*.txt")) + list(BASE.glob("*.json"))

total_chars = 0
total_tokens = 0

for FILE in files:
    # Read the file
    text = FILE.read_text(encoding="utf-8")

    # just split on whitespace
    tokens = text.split()

    chars = len(text)
    toks = len(tokens)

    total_chars += chars
    total_tokens += toks

    print(f"\nFile: {FILE}")
    print(f"Characters: {chars:,}")
    print(f"Tokens (approx): {toks:,}")

# Print totals if there are multiple files
if len(files) > 1:
    print("\nTOTAL")
    print(f"Characters: {total_chars:,}")
    print(f"Tokens (approx): {total_tokens:,}")
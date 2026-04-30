#!/usr/bin/env python3
"""
Simple token counter for a text file
(approximate: splits on whitespace)
"""

from pathlib import Path

FILE = Path("apertium_grn_summary.txt")

text = FILE.read_text(encoding="utf-8")

# Tokenization 
# split by whitespace
tokens = text.split()

print(f"File: {FILE}")
print(f"Characters: {len(text):,}")
print(f"Tokens (approx): {len(tokens):,}")
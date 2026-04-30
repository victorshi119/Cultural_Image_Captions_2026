#!/usr/bin/env python3
"""
Condensed Apertium Guaraní Summary
The objective is to create a condensed version of Apertium Morphological Transducer.
Reasoning: 
    for an agglutinative language like Guarani, a morphological transudcer is the most
pseudo-code like input that might be the easiest for an LLM to understand/internalize.

We extract the MOST important information following the README the README (https://github.com/apertium/apertium-grn/blob/master/README):
Files and data
===============================================================================

* `apertium-grn.grn.lexc`           - Lexicon
* `apertium-grn.grn.twol`           - Phonological rules
* `grn.prob`                        - Tagger model (WE CANNOT FIND IT, EXCLUDE)
* `apertium-grn.grn.rlx`            - Constraint Grammar disambiguation rules
* `modes.xml`                       - Translation modes

Based on current https://github.com/apertium/apertium-grn/blob/master/,
we add:


"""
import os
from pathlib import Path
from openai import OpenAI
from time import sleep
# current structure:
# build_apertium_sum.py
# ../apertium/
# Files directory
FILES = [
    ("LEXICON (.lexc)", "apertium/apertium-grn.grn.lexc"),
    ("PHONOLOGY (.twol)","apertium/apertium-grn.grn.twol"),
    ("CONSTRAINT GRAMMAR (.rlx)", "apertium/apertium-grn.grn.rlx"),
    ("TRANSLATION MODES (xml)",  "apertium/modes.xml"),
]
reallms_base_url = "https://reallms.rescloud.iu.edu/direct/v1"
sys_prompt = "You are an expert in Guarani, summary each file for me"
# Output file (also relative → replicable)
OUT = Path("apertium_grn_summary.txt")

# Build output
output_parts = []

header = """\
GUARANÍ MORPHOLOGICAL REFERENCE (condensed from Apertium-GRN)
Source: https://github.com/apertium/apertium-grn
Language: Paraguayan Guaraní (ISO 639-3: grn)

Guaraní is an agglutinative, polysynthetic language with:
- Active/inactive (agentive/patientive) verb agreement
- Nasal harmony: nasality spreads across morpheme boundaries
- Glottal stop (ʼ) as a phoneme, written with apostrophe
- No grammatical gender
- Verb-initial or verb-final word order (SVO also attested)
- Rich postpositional system (postpositions, not prepositions)
- Person agreement encoded on verbs as prefixes (not suffixes)

"""
api_key = os.environ.get("REALLMS_API_KEY")
client = OpenAI(api_key=api_key,base_url=reallms_base_url)
for title, path in FILES:
    path = Path(path)  
    content = path.read_text(encoding="utf-8")

    # Add a clean section header
    section = f"\n\n{'='*60}\n{title}\n{'='*60}\n\n{content}"
    # This is for input
    max_chars = 100000
    # This is for output
    max_token = 10000
    inputs = section[:max_chars]
    # call api to help summarize
    response = client.chat.completions.create(
        model="gemma-4-31B-it",
        messages = [
            {"role":"system","content":sys_prompt},
            {"role":"user","content":inputs}
            ],
    )
    model_res = response.choices[0].message.content.strip()
    sleep(0.5)
    output_parts.append(model_res)

# Write everything
OUT.write_text(header + "".join(output_parts), encoding="utf-8")

print(f"Done. Written to: {OUT}")
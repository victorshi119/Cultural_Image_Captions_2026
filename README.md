# IUHoosier's Official Submission to the AmericasNLP 2026 Cultural Image Captioning Shared Task

This is IUHoosier's Official Submission to the AmericasNLP 2026 Cultural Image Captioning shared task — Guarani (Avañe'ẽ), a language spoken by people in Paraguay, Brazil, Bolivia, and Argentina.

## Setup

```bash
uv pip install -r requirements.txt
export REALLMS_API_KEY=<your-key>
```

To lock versions for reproducibility:

```bash
uv pip compile requirements.txt -o requirements.lock
uv pip install -r requirements.lock
```

## Usage

`main.py` takes a folder of images and generates Guaraní captions via the REaLLMs VLM API.

```bash
python main.py <image_dir> [options]
```

### Minimal run

```bash
python main.py data/dev/guarani/images --output outputs/captions.tsv
```

### With all resources

```bash
python main.py data/dev/guarani/images \
    --model gemma-4-31B-it \
    --prompt_version v4 \
    --culture_knowledge  resources/guarani_culture_knowledge.txt \
    --interlinear        resources/gug_para.txt --num_interlinear 60 \
    --grammar_parallel   resources/gua_parallel.txt --num_grammar_parallel 30 \
    --apertium           resources/apertium_grn_summary.txt \
    --parallel_examples  resources/flores_dev_examples_en-gn.json --num_parallel 10 \
    --code_rules         resources/grammar_code_rules_gemma_4_31B_it.py --retrieval_top_k 10 \
    --output outputs/captions_all.tsv
```

### Arguments

| Argument | Default | Description |
|---|---|---|
| `image_dir` | required | Folder of input images (jpg/png/webp/bmp) |
| `--model` | `gemma-4-31B-it` | Model name on REaLLMs |
| `--prompt_version` | `v2` | Base system prompt: `v2` (English rules), `v3`/`v4` (Spanish guidelines) |
| `--culture_knowledge` | — | Guaraní cultural knowledge file |
| `--interlinear` / `--num_interlinear` | — / 8 | Interlinear glossed examples injected into prompt |
| `--grammar_parallel` / `--num_grammar_parallel` | — / 5 | Grammar-book parallel sentence pairs |
| `--apertium` / `--apertium_chars` | — / 15000 | Apertium morphology summary (truncated to N chars) |
| `--parallel_examples` / `--num_parallel` | — / 10 | FLORES EN→GN parallel examples |
| `--code_rules` / `--retrieval_top_k` | — / 10 | Code-format grammar rules with BM25 retrieval per image |
| `--output` | `generated_captions.tsv` | Output file (`image_name\tcaption` per line) |

### Evaluation

```bash
python eval_chrf.py --dataframe data/dev/guarani/guarani.jsonl --generated outputs/captions.tsv
```

Reports mean chrF++ score per image within each respective 

## Resource Character and Token Count
Gemma 4 31B Max Token Input: 250k
File: /N/project/CoRSAL/Cultural_Image_Captions_2026/resources/gua_parallel.txt
Characters: 280,442
Tokens (approx): 41,497

File: /N/project/CoRSAL/Cultural_Image_Captions_2026/resources/prompt-para1311-nosum.txt
Characters: 134,035
Tokens (approx): 19,642

File: /N/project/CoRSAL/Cultural_Image_Captions_2026/resources/guarani_culture_knowledge.txt
Characters: 6,347
Tokens (approx): 890

File: /N/project/CoRSAL/Cultural_Image_Captions_2026/resources/apertium_grn_summary.txt
Characters: 9,530
Tokens (approx): 1,361

File: /N/project/CoRSAL/Cultural_Image_Captions_2026/resources/gug_para.txt
Characters: 201,863
Tokens (approx): 28,205

File: /N/project/CoRSAL/Cultural_Image_Captions_2026/resources/flores_dev_examples_en-gn.json
Characters: 300,114
Tokens (approx): 41,664

TOTAL
Characters: 932,331
Tokens (approx): 133,259

## Ablation Results (dev set, Gemma 4 31B, prompt v3, 3 runs averaged)

Add-one-forward ablation — each resource added to the base prompt in isolation. Scores are mean chrF++ averaged over 3 independent runs (jobs 6966213, 6966221, 6966222).

Resources evaluated:
- `ck` — culture knowledge (`Claude_2step_guarani_cultural_knowledge.txt`)
- `il` — interlinear examples (`guarani_grammar_primer_claude.md`, full)
- `gp` — grammar parallel (`guarani_exemplar_bank_claude.md`, full)
- `ap` — apertium (`apertium-grn-caption-cheatsheet.md`)
- `pe` — FLORES parallel examples (`flores_dev_examples_en-gn.json`, full)
- `dampy` — DAMPY cultural caption exemplars (`dampy_gemma_claude_caption.txt`, full)

| Condition | r0 | r1 | r2 | Avg |
|---|---|---|---|---|
| none | 20.15 | 20.13 | 20.55 | **20.28** |
| +pe | 23.37 | 22.65 | 23.18 | **23.07** |
| +ck | 21.02 | 20.86 | 20.78 | **20.89** |
| +il | 21.76 | 20.94 | 20.84 | **21.18** |
| +dampy | 21.33 | 20.70 | 20.69 | **20.91** |
| +gp | 19.28 | 19.37 | 19.54 | **19.40** |
| +ap | 17.51 | 17.27 | 18.02 | **17.60** |
| all | 22.14 | 22.20 | 21.96 | **22.10** |

## Conclusion

v3 consistently outperforms v4 across almost all conditions. FLORES parallel examples (`pe`) is the strongest single augmentation for both prompts. Grammar parallel (`gp`) hurts performance for both. Code rules (`cr`) is the only condition where v4 edges out v3.
# Cultural Image Captions 2026

AmericasNLP 2026 Cultural Image Captioning shared task — Guarani (Avañe'ẽ), a language spoken by people in Paraguay, Brazil, Bolivia, and Argentina.

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

`+pe` (FLORES parallel examples) is the strongest single resource at 23.07 avg chrF++. `+il` (21.18) and `+dampy` (20.91) both improve over the baseline. `+gp` and `+ap` hurt performance — `all` (22.10) falls short of `+pe` alone, likely dragged down by those two resources.

---

## Finale Experiments (Test Set)

All finale runs use **gemma-4-31B-it**, **prompt v3**, and the full **test set** (101 images). Fixed across all runs: grammar book (`guarani_ref.md`, 157 lines) and interlinear (`guarani_grammar_primer_claude.md`, 144 lines).

Submitted to AmericasNLP 2026. Submission files: `submissions/final/guarani-{0-5}.jsonl` (corresponding to `finale_text_{0-5}.tsv`).

---

### Text BM25 Runs — `finale_text_{0-5}.tsv`

**Mode:** All resources retrieved via BM25 per image (text-only, no visual shots). Resources:
- `--culture_bm25` → `Claude_2step_guarani_cultural_knowledge.txt` (top-K chunks)
- `--dampy_captions` + `--dampy_spanish_captions_dir` → DAMPY Guaraní + Spanish captions, BM25 top-K
- `--flores_bm25` → `flores_dev_examples_en-gn.json`, BM25 top-K EN→GN pairs
- `--dev_bm25_text_top_k` → dev set image/caption pairs retrieved by text BM25

| File | DAMPY\_K | FLORES\_K | DEV\_K | CULTURE\_K |
|---|---|---|---|---|
| `finale_text_0.tsv` | 5 | 100 | 5 | 5 |
| `finale_text_1.tsv` | 10 | 100 | 10 | 5 |
| `finale_text_2.tsv` | 15 | 100 | 10 | 5 |
| `finale_text_3.tsv` | 20 | 100 | 10 | 6 |
| `finale_text_4.tsv` | 15 | 120 | 10 | 8 |
| `finale_text_5.tsv` | 15 | 150 | 10 | 10 |

The sweep tests the effect of increasing BM25 retrieval depth: `finale_text_0` uses the smallest context (FLORES\_K=100, DAMPY\_K=5); `finale_text_5` uses the largest (FLORES\_K=150, DAMPY\_K=15, CULTURE\_K=10).

---

### Static Text Run — `finale_static_text_1.tsv` *(pending/not yet produced)*

Planned text-only static run using fixed (non-BM25) resources mirroring the static visual config below, but without visual shots injected. Config based on `finale_static.slurm` minus the `--dampy_images` visual argument.

---

### Static Visual Run — `finale_static_visual_15shot_dev50.tsv`

**Mode:** Static (non-BM25) resource injection with visual DAMPY few-shot pairs.

| Argument | Value |
|---|---|
| `--culture_knowledge` | `Claude_2step_guarani_cultural_knowledge.txt` (full file) |
| `--parallel_examples` | `flores_dev_examples_en-gn.json`, 50 examples (static) |
| `--dampy_images` | `new_data/dampy_output/images` |
| `--dampy_captions` | `dampy_gemma_claude_caption.txt` |
| `--num_dampy_shots` | 15 visual image–caption pairs |
| `--dev_bm25_visual_top_k` | 50 dev pairs retrieved by visual BM25 |

---

### Static Visual 10-shot Run — `finale_static_visual_10shot.tsv` *(pending/not yet produced)*

Planned reduced-shot variant of the static visual run above, using 10 DAMPY visual shots instead of 15. Config mirrors the 10-shot entry from `finale_quick.slurm` (ID=8: FLORES\_K=25, DEV\_K=8).

---

### Dev BM25 Visual Run — `finale_dampy_bm25_visual5_dev.tsv` *(dev set only)*

Validation run on the 50-image dev set to test BM25-based visual DAMPY retrieval.

| Argument | Value |
|---|---|
| `--culture_knowledge` | `Claude_2step_guarani_cultural_knowledge.txt` (full file) |
| `--parallel_examples` | `flores_dev_examples_en-gn.json`, 50 examples (static) |
| `--dampy_images` + `--dampy_captions` | DAMPY visual BM25, top-5 visually similar pairs |
| `--dampy_spanish_captions_dir` | DAMPY Spanish caption directory for BM25 scoring |
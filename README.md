# Cultural Image Captions 2026

AmericasNLP 2026 Cultural Image Captioning shared task — Paraguayan Guaraní (Avañe'ẽ).

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
python eval_chrf.py --dataframe data/dev/guarani/captions.jsonl --generated outputs/captions.tsv
```

Reports mean chrF++ score.

## Ablation Results (dev set, Gemma 4 31B, prompt v4)

Add-one-forward ablation — each resource added to the base prompt in isolation.

| Resource | chrF++ |
|---|---|
| none (base prompt only) | 19.09 |
| +culture knowledge (`ck`) | 20.89 |
| +interlinear examples (`il`) | 20.33 |
| +apertium morphology (`ap`) | 19.63 |
| +code rules / BM25 (`cr`) | 19.81 |
| +grammar parallel (`gp`) | 17.56 |
| +FLORES parallel examples (`pe`) | **21.84** |
| all combined | 21.61 |

# Results Summary — Guaraní Caption Generation (Dev Set)

Evaluated on `data/dev/guarani/guarani.jsonl` (50 images) using chrF++ (word_order=2).  
Model: **gemma-4-31B-it**

---

## Ablation Study — prompt v4, old resources (3 runs avg)

Resources: culture knowledge (`guarani_culture_knowledge.txt`), interlinear (`gug_para.txt`, n=60), grammar parallel (`gua_parallel.txt`, n=30), apertium (`apertium_grn_summary.txt`), parallel examples (`flores_dev_examples_en-gn.json`, n=10), code rules (`grammar_code_rules_gemma_4_31B_it.py`).

| Condition | r0 | r1 | r2 | Avg |
|-----------|----|----|-----|-----|
| none | 18.90 | 19.28 | 20.21 | **19.46** |
| +ck | 20.19 | 19.84 | 19.22 | **19.75** |
| +il | 20.16 | 20.98 | 20.39 | **20.51** |
| +gp | 14.56 | 15.14 | 15.12 | **14.94** |
| +ap | 20.70 | 20.83 | 20.36 | **20.63** |
| +pe | 21.73 | 22.17 | 22.17 | **22.02** |
| +cr | 18.76 | 19.36 | 19.63 | **19.25** |
| all | 21.41 | 21.37 | 21.19 | **21.32** |

**Key finding:** parallel examples (+pe) gives the largest gain. Grammar parallel (+gp) and code rules (+cr) hurt relative to none.

---

## Ablation Study — prompt v3, old resources (3 runs avg)

Same resources as above but with prompt version v3.

| Condition | r0 | r1 | r2 | Avg |
|-----------|----|----|-----|-----|
| none | 20.15 | 20.45 | 21.27 | **20.62** |
| +ck | 20.80 | 21.69 | 20.72 | **21.07** |
| +il | 21.26 | 21.48 | 21.48 | **21.41** |
| +gp | 16.29 | 16.01 | 15.87 | **16.06** |
| +ap | 21.28 | 20.69 | 21.17 | **21.05** |
| +pe | 23.26 | 22.18 | 23.06 | **22.83** |
| +cr | 18.42 | 18.67 | 18.83 | **18.64** |
| all | 21.71 | 21.18 | 22.35 | **21.75** |

**Key finding:** prompt v3 baseline is higher than v4 baseline. +pe remains strongest. +gp and +cr still hurt. +il performs well under v3.

---

## Main Test Configurations

| Output file | Description | chrF++ |
|-------------|-------------|--------|
| `main_test_v3_flores100` | prompt v3, 100 FLORES examples | **23.45** |
| `main_test_v3_flores200` | prompt v3, 200 FLORES examples | **23.34** |
| `main_test_v3_ck_il_flores` | prompt v3, CK + IL + FLORES | **22.45** |
| `main_test_v4_claude_grammar_exemplar` | prompt v4, Claude grammar exemplar | **21.25** |
| `main_test_v4_claude2step_ck` | prompt v4, Claude 2-step CK | **20.45** |
| `main_test_v4_visual_lexicon` | prompt v4, visual lexicon | **17.65** |
| `main_test_v4_all_resources` | prompt v4, all resources | N/A (eval error) |

**Best so far:** `main_test_v3_flores100` at 23.45.

---

## Experimental — BM25 / LLM Retrieval

| Output file | Description | chrF++ |
|-------------|-------------|--------|
| `experimental` | base experimental | 19.12 |
| `experimental_all_bm25` | BM25 over all resources (flores k=10, resource k=3) | 17.50 |
| `experimental_bm25flores` | BM25 for FLORES retrieval | 18.03 |
| `experimental_bm25flores_k10` | BM25 FLORES k=10 | 17.61 |
| `experimental_llm_retrieval` | LLM-based retrieval | 16.38 |
| `experimental_llm_retrieval_vision` | LLM retrieval + vision | 16.48 |
| `experimental_no_flores` | no FLORES examples | 15.76 |

**Finding:** BM25/LLM retrieval strategies underperform direct FLORES inclusion. FLORES examples are critical.

---

## Ablation v2 (new resources, prompt v4) — pending

Job 6965487 submitted 2026-05-01. Resources: grammar parallel → `guarani_exemplar_bank_claude.md` (n=30), interlinear → `guarani_grammar_primer_claude.md` (n=60), apertium → `apertium-grn-caption-cheatsheet.md`, parallel examples → `flores_dev_examples_en-gn.json` (n=200). Code rules removed.

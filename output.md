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

---

## Ablation v3prompt+dampy — prompt v3, updated resources + dampy captions (3 runs avg)

Resources: 
1. culture knowledge (`Claude_2step_guarani_cultural_knowledge.txt`) - ck
2. interlinear (`guarani_grammar_primer_claude.md`, full) - il
3. grammar parallel (`guarani_exemplar_bank_claude.md`, full) - gp
4. apertium (`apertium-grn-caption-cheatsheet.md`) - ap
5. parallel examples (`flores_dev_examples_en-gn.json`, full) - pe
6. dampy cultural caption exemplars (`dampy_gemma_claude_caption.txt`, full). - dampy
Jobs: 6966213 (r0), 6966221 (r1), 6966222 (r2).

| Condition | r0 | r1 | r2 | Avg |
|-----------|----|----|-----|-----|
| none | 20.15 | 20.13 | 20.55 | **20.28** |
| +pe | 23.37 | 22.65 | 23.18 | **23.07** |
| +ck | 21.02 | 20.86 | 20.78 | **20.89** |
| +ap | 17.51 | 17.27 | 18.02 | **17.60** |
| +il | 21.76 | 20.94 | 20.84 | **21.18** |
| +gp | 19.28 | 19.37 | 19.54 | **19.40** |
| +dampy | 21.33 | 20.70 | 20.69 | **20.91** |
| all | 22.14 | 22.20 | 21.96 | **22.10** |

**Key finding:** +pe remains the strongest single resource (23.07 avg). +il (21.18) and +dampy (20.91) both outperform the none baseline. +ap continues to hurt. `all` (22.10) falls short of +pe alone, suggesting +ap and/or +gp drag it down.

---

## Ablation v3prompt+dampy — updated apertium (`apertium-grn-caption-cheatsheet.txt`), single run

Same setup as above but with updated apertium resource (`.txt`). Job 6967979 (r3).

| Condition | r3 |
|-----------|-----|
| none | 19.91 |
| +ap | 19.81 |
| all | 21.62 |

---

## Ablation — dampy visual few-shot (2 per category: Comida, Fauna, Flora), single run

Visual few-shot: 6 image-caption pairs injected as prior conversation turns (not text in system prompt).
`all` = ck + il + gp + ap + pe + 6 visual dampy shots. Job 6968211.

| Condition | score |
|-----------|-------|
| none | 21.38 |
| +dampy_vis | 21.71 |
| all | 22.69 |

## Conclusion: Upon manual check, the apertium was deemed helpful. However, it seems like the improved apertium did not help with the performance. 

---

## Ablation — dampy visual few-shot (5 per category: Comida, Fauna, Flora), single run

Visual few-shot: 15 image-caption pairs injected as prior conversation turns.
`all` = ck + il + gp + ap + pe + 15 visual dampy shots. Job 6969327.

| Condition | score |
|-----------|-------|
| none | 20.76 |
| +dampy_vis (5×3) | 22.48 |
| all | 23.39 |

## Observation: It seems like incrementing the visual few-shot pairs significantly help with the result, might be best if we can do RAG to get the k-most-similar images (to the target image) while considering their captions while generating the caption for the target image.
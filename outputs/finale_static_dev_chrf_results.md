# finale_static Dev chrF++ Results
Gold labels: `data/dev/guarani/guarani.jsonl`
Metric: chrF++ (word_order=2, sacrebleu)

## Text-only configs

| File | flores | dampy_text_cat | chrF++ |
|------|--------|----------------|--------|
| finale_static_dev_text_0.tsv | 20  | 2 | 21.80 |
| finale_static_dev_text_1.tsv | 30  | 3 | 22.49 |
| finale_static_dev_text_2.tsv | 50  | 3 | 21.43 |
| finale_static_dev_text_3.tsv | 50  | 5 | 22.09 |
| finale_static_dev_text_4.tsv | 80  | 3 | 22.21 |
| finale_static_dev_text_5.tsv | 100 | 5 | 23.02 |

## Visual few-shot configs

| File | shots | flores | chrF++ |
|------|-------|--------|--------|
| finale_static_dev_visual_5shot.tsv  |  5 | 30 | 23.49 |
| finale_static_dev_visual_10shot.tsv | 10 | 30 | 24.17 |
| finale_static_dev_visual_15shot.tsv | 15 | 50 | **24.43** |

## Summary
- Best overall: `visual_15shot` at **24.43**
- Best text-only: `text_5` (flores=100, dampy_text_cat=5) at **23.02**
- Visual few-shot consistently outperforms text-only across all configs

# Finale Submission Analysis — AmericasNLP 2026 Guaraní Captioning

## Overview

This document describes the motivation for our 9 finale submission configurations, the limitations of chrF++ as an evaluation metric for this task, and a qualitative analysis of the first 10 test captions (grn_051–grn_060) across all models.

---

## The 9 Submission Configurations

We submitted 9 configurations covering two retrieval strategies:

### Text BM25 Runs (`finale_text_0` – `finale_text_5`)

All 6 runs use the same base: Gemma 4 31B, prompt v3, full grammar book (157 lines) and interlinear (144 lines), with **BM25 dynamic retrieval** per image across four resource types. The sweep varies retrieval depth:

| Run | DAMPY\_K | FLORES\_K | DEV\_K | CULTURE\_K | Rationale |
|---|---|---|---|---|---|
| `text_0` | 5 | 100 | 5 | 5 | Conservative baseline — smaller, tighter context |
| `text_1` | 10 | 100 | 10 | 5 | Doubled DAMPY and DEV retrieval |
| `text_2` | 15 | 100 | 10 | 5 | Increased DAMPY further |
| `text_3` | 20 | 100 | 10 | 6 | Maximum DAMPY, slight culture bump |
| `text_4` | 15 | 120 | 10 | 8 | More FLORES examples, more culture chunks |
| `text_5` | 15 | 150 | 10 | 10 | Largest context — maximum FLORES and culture |

**DAMPY\_K**: top-K Guaraní + Spanish DAMPY caption pairs retrieved by BM25 from image text  
**FLORES\_K**: top-K EN→GN FLORES parallel sentence pairs retrieved by BM25  
**DEV\_K**: top-K dev set image-caption pairs retrieved by text BM25  
**CULTURE\_K**: top-K chunks from the cultural knowledge file retrieved by BM25

### Static Visual Run (`finale_static_visual_15shot_dev50`)

Uses **static (non-BM25) injection** of 15 DAMPY image–caption pairs as visual few-shot turns, plus 50 static FLORES examples, full culture knowledge text, and top-50 dev pairs retrieved by **visual** BM25 (image similarity rather than text). This is the only run that injects actual images into the prompt and retrieves dev exemplars visually.

### Two Pending Configurations (not yet produced)

- `finale_static_text_1`: planned text-only version of the static run (same resources, no visual shots)
- `finale_static_visual_10shot`: planned reduced-shot visual run (10 DAMPY shots)

---

## Why Submit Both Despite chrF++ Limitations

chrF++ measures character n-gram overlap between the generated caption and the gold reference. It is fast, language-agnostic, and correlates moderately with translation quality, but it has two key blind spots for this task:

1. **No semantic sensitivity**: Two captions that describe the same image content in different valid Guaraní phrasings can score very differently if they use different surface forms. A correct, culturally precise caption that paraphrases the gold label may score lower than a formulaic caption that happens to share n-gram fragments.

2. **No cultural accuracy signal**: chrF++ cannot distinguish between a caption that correctly identifies a cultural item (e.g., calling a *mate* setup *mate*) and one that gets the cultural nuance wrong (calling the same image *tereré*). The two words do not share character n-grams, so a wrong cultural identification is penalized the same as any other lexical mismatch.

We submitted multiple configurations across both retrieval strategies because:
- The BM25 runs (text_0–text_5) optimize for context breadth and retrieval diversity — more likely to hit vocabulary and phrasing overlap with gold labels, which benefits chrF++.
- The static visual run prioritizes **semantic and visual grounding**: it retrieves the most visually similar dev examples and injects real image–caption pairs as context, which improves cultural item recognition even when the surface form differs from the gold label.

Submitting both strategies gives us coverage: the BM25 runs are more likely to score well on chrF++; the static visual run is more likely to produce culturally accurate and well-grounded captions.

---

## Qualitative Analysis — First 10 Test Captions (grn_051–grn_060)

### Dev Gold Label Style

Before evaluating the model outputs, it is useful to characterize the expected style from the 50 dev gold labels. Gold captions are:
- **Concise**: typically 1–2 sentences
- **Visually specific**: name the object, its material or color, and what it is doing/showing
- **Culturally grounded without editorializing**: a short cultural note is acceptable, but captions avoid generic phrases like "oñemoingove ñane retã reko" (representing our cultural heritage) tacked on as a closing formula
- **Grammatically natural**: they do not repeat the same closing boilerplate across images

Example gold labels from dev:
- grn_001: *"Tereré ekípo oĩva poyvi ári peteĩ korapy yvýrayty mbytépe: peteĩ térmo vakapíregui mbojegua pyre, guámpa yvyragui ojejapopyréva ha vombílla kuarepotigui."*  
  → Describes specific objects, materials, and setting. No generic cultural closing.
- grn_009: *"Peteĩ chípa, ojejapóva aramirõ ha kesúgui, oĩva kuatia jurukytyha ári, ha'e hína ñane rembi'u teete, ojehayhuvéva ha omohe'ẽva ñande reko."*  
  → Short, clear, one modest cultural note ("beloved, represents our way of life").

### Observations by Criterion

#### 1. Style: Does the caption match the gold label register?

Most BM25 text runs (especially `text_0`, `text_1`, `text_3`) heavily overuse the closing formula *"Ko tembi'u ha'e peteĩ rembiapokue tee Paraguáigui, ojekuaáva heta torypópe"* (this dish is a true cultural product of Paraguay, known at many celebrations). This phrase appears verbatim in multiple images regardless of whether the image actually depicts a celebratory context. The gold labels use culturally grounded closings, but they vary the phrasing and keep it specific to the image.

`text_2` and `text_5` are somewhat better: they vary their closings and occasionally add image-specific detail. The **static visual run** most consistently matches the gold label register — its captions are concise, image-specific, and avoid boilerplate.

Selected comparison for grn_053 (ñandutí lace on clothing):

| Source | Caption |
|---|---|
| `text_0` | *"Ko mba'e ha'e peteĩ mba'e imbaretéva ñande reko Paraguáipe, ojejapóva mborayhu ha tembiapo katuirã."* — generic cultural statement |
| `text_2` | *"Ko mba'eporã ohechauka ñande reko ha ñande yvy rembiapo tee."* — still generic |
| `text_5` | *"Ko enkáhe ha'e peteĩ mba'e porãite ojejapóva Itauguápe, ha ohechauka ñande reko Paraguáipe."* — better: names Itauguá (the town) |
| static visual | *"Ñandutí porãite ha sa'yju, ojejapóva pópe pe ikatupyry Paraguáigui. Ko rembiapo oñemomba'epu'avo ao ári, ohechauka ñane retã reko ha ñande rekojera."* — specific color (gold/yellow), hand-made detail, clothing context |

#### 2. Cultural nuance: Does the caption correctly identify the cultural item?

This is where the models diverge most clearly. **grn_052** is the critical test case.

**What is in grn_052?**  
The image shows a mate setup: a **mate gourd**, a **bombilla**, and a **pava** (metal kettle for heating water). This is *mate* — the hot drink. The key discriminating visual cue is the **kettle (pava)** in the background. Tereré, the cold version of the drink, uses a **térmo** (cold thermos) and is served in a **guampa** (often a bull-horn or carved wooden cup), not a gourd.

| Model | Caption for grn_052 | Correct? |
|---|---|---|
| `text_0` | *"Mokõi guampa ha peteĩ pava oĩva peteĩ poyvi sa'y hetáva ári. Ko'ãva ojeipuru tereré ha mate oñu'u hag̃ua."* | Partial — sees the pava, mentions both drinks but calls the vessels "guampa" (tereré cup) |
| `text_1` | *"Tereré ekípo oĩva peteĩ ao sa'yitáva ári: mokõi guámpa yvyrágui, peteĩ pava kuarepotígui ha peteĩ pava yvyra ha peteĩ térmo."* | Wrong — labels it tereré equipment |
| `text_2` | *"Mate ha tereré ekípo oĩva peteĩ ao poyvi ári: oĩva guampa yvyragui, bombilla kuarepotigui ha peteĩ pava."* | Partial — hedges ("mate ha tereré"), sees the pava |
| `text_3` | *"Tereré ekípo oĩva peteĩ ao pyporéva ári: guámpa yvyrágui, vombílla ha peteĩ térmo."* | Wrong — labels as tereré, mentions térmo (cold thermos) |
| `text_4` | *"Tereré ekípo oĩva poyvi isañyju ári: guámpa yvyrágui, vombílla ha térmo."* | Wrong — tereré, térmo |
| `text_5` | *"Tereré ekípo oĩva peteĩ ao po'i ári: guámpa yvyragui, bombílla ha peteĩ pava."* | Partial — still labels as tereré but correctly sees the pava (kettle) |
| static visual | *"Mate pytã ha pava oĩva poyvi ári; tembi'u ha y'u ojekuaavéva ñane retãme oñembojoaju hag̃ua tapichakuéra pyhareve."* | **Correct** — identifies as mate, names the pava, notes it is for gathering in the morning |

The static visual run is the **only model** that correctly identifies grn_052 as a *mate* setup. The reason is likely that the visual BM25 retrieval found a dev image depicting mate equipment, and its gold caption provided the right vocabulary and framing (*"mate pytã"*, *"pava"*) as a few-shot example. The BM25 text runs, lacking visual retrieval, defaulted to the more statistically common term *tereré* and the vessel *guampa*, which are more frequently referenced in the text training resources.

#### 3. Further nuances in the first 10 images

- **grn_054 (Victoria water lily)**: All models correctly identify this as *Jakare Yrupe (Victoria cruziana)* and note it grows in the rivers of Paraguay and Paraná. No major differences. The static visual run adds *"ijyvoty morotĩva oñemomba'erate y'águi"* (its white flower strengthened by the water) — image-specific detail absent from the text runs.

- **grn_055 (folkloric dance)**: Most models correctly describe male/female dancers with their traditional attire (pollera, sombrero, poncho). `text_4` uses the unusual phrase *"umi kavaju ijao ryguasu"* (those with horse feather costumes), which seems to be a hallucination. The static visual run stays grounded.

- **grn_057 (chipa cooking on fire)**: The text runs disagree: `text_0` says *chipa sopy'a* (chipa cooked on coals), `text_1` says *chipa lopi*, `text_2` says *Sopa Paraguaya* (clearly wrong — sopa paraguaya is a baked corn bread, not grilled chipa), `text_3` and `text_4` say *chipa lopi*, `text_5` says *mbohapy chipa lopi*. The static visual run says *"Mbeju oñembochyryrýva tataypýpe"* — recognizing it as **mbeju** (cassava flatbread grilled on a pan). Given the image context (flat dough on a fire), mbeju is a plausible identification, and the static visual run's visual grounding may be correct here over the text runs' consensus for *chipa lopi*.

- **grn_059 (soup)**: `text_2`, `text_3`, `text_4`, `text_5` all identify this as *locro*, a corn-and-meat stew. `text_0` calls it *vori vori* (cornmeal dumplings in broth) and `text_1` calls it *vori vori* as a "caldo." *Locro* and *vori vori* are visually similar — both are chunky soups. The static visual run says *"Locro, tembi'u Paraguái tee"*, agreeing with the text_2–5 majority. `text_0`'s confidence in *vori vori* for this image may be a retrieval artifact.

---

## Selection Recommendation

Based on this qualitative review, the **static visual run** (`finale_static_visual_15shot_dev50`) is the strongest overall:
- Matches the gold label register (concise, specific, no boilerplate)
- Correctly identifies the mate/tereré distinction (grn_052) — the only model to do so
- Produces image-specific detail (water lily flower, mbeju on fire) that the text runs miss

Among the text BM25 runs, **`text_2`** and **`text_5`** are the strongest:
- `text_2` hedges correctly on grn_052 (names both mate and tereré), uses more specific ingredient lists
- `text_5` uses the largest FLORES context and varies its closings more than `text_0`–`text_3`

`text_0` is the weakest: it defaults most aggressively to boilerplate closings and misidentifies grn_052 entirely (calls vessels "guampa" while also mentioning a pava, suggesting retrieval confusion).

For the final submission ranking, we recommend: **static\_visual\_15shot > text\_2 ≈ text\_5 > text\_4 > text\_3 > text\_1 > text\_0**, weighted primarily by cultural accuracy and style, not chrF++ alone.

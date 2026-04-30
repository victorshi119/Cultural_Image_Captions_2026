
You said: I'm participating in americasnlp challenge where we take an image then generate a caption in target langauge (in our case guarani).
I'm participating in americasnlp challenge where we take an image then generate a caption in target langauge (in our case guarani). I'm thinking about feeding a condensed version of Apertium Guarani Morphological Transducer with website https://github.com/apertium/apertium-grn along with the image so that langauge model knows about guarani culture (hopefully). can you help me articulate my prompt to my speicalized LLM to look into this file and then confirm with the internet what part of the grammar we should prioritize and what part are more just nitty gritty detailed that we can ignore? I want you to give me the best prompt possible for this, and here is the github repo for the comeptition: __https://github.com/AmericasNLP/americasnlp2026#important-dates__, and we are competing on the Guarani track only.

4:25 PM
Claude responded: Here's a prompt designed to get the most out of a specialist LLM.

Architected specialized prompt for grammar prioritization analysis
Architected specialized prompt for grammar prioritization analysis
Here's a prompt designed to get the most out of a specialist LLM. A few choices worth flagging up front so you can adjust:

It enforces a tiered output (Tier 1 must-keep / Tier 2 useful / Tier 3 drop), which is what you actually need rather than a flat "summary."
It seeds the model with the Guarani-specific phenomena that LLMs reliably get wrong (nasal harmony, active/inactive "chendal/areal" verbs, inclusive/exclusive 1pl, obligatory possession, nominal tense). Naming these explicitly makes it harder for the model to skip them, but doesn't tell it the answer.
It distinguishes Apertium-internal artifacts from real grammar. Transducer files have a lot of compile-time machinery you don't want bleeding into your captioning prompt.
It demands web verification on Tier 1/2 items only, so the model doesn't waste effort double-checking trivia.
It caps the final cheat-sheet at ~600 tokens so the output is actually usable as a system prompt for your captioning model. Adjust this number to your real context budget.
It flags the Yopará vs. standard Guarani register question, which is a known issue in AmericasNLP submissions.
Copy-paste below:

markdown
You are an expert in Guarani (Avañe'ẽ) linguistics and computational morphology, with working familiarity with the Apertium platform and finite-state transducer design. You are advising a team competing in the **AmericasNLP 2026 Image Captioning Shared Task, Guarani track** (https://github.com/AmericasNLP/americasnlp2026). The objective is to generate fluent, culturally appropriate Guarani captions for input images.

## Task

The team is building a system prompt for a multimodal LLM that will receive (a) an image and (b) a compact grammar/morphology cheat-sheet distilled from the Apertium Guarani Morphological Transducer (https://github.com/apertium/apertium-grn). Your job is to decide what goes into that cheat-sheet and what gets cut.

## Inputs

1. The condensed Apertium transducer content I will paste below this prompt.
2. The web. Verify your conclusions against authoritative external sources: descriptive grammars of Guarani (e.g., Velázquez-Castillo, Gregores & Suárez, Krivoshein de Canese, Estigarribia), the Apertium documentation, prior AmericasNLP shared-task papers, the Wikipedia entry on Guarani grammar, and any image-captioning literature for low-resource or morphologically rich languages.
3. The shared-task page itself — please skim the AmericasNLP 2026 README for the actual evaluation metric, training data source, and any register/orthography guidance, and let those constraints shape your priorities.

## How to prioritize

Image captions are short, descriptive utterances naming entities, attributes, spatial relations, and actions visible in a picture. Rank every Apertium category, tag, and morphological process by how often it will appear in a 1–2-sentence caption AND how badly its misuse damages output quality.

**Tier 1 — must keep (caption-critical).** Categories that:
- Appear in essentially every caption (e.g., basic verbal agreement, plural marking, demonstratives).
- Are obligatory and whose absence is ungrammatical (e.g., possession marking on body parts and kin terms).
- Distinguish Guarani from Spanish/English in ways an LLM trained mostly on those will default-violate. Pay particular attention to: **nasal harmony**, the **active/inactive (chendal vs. areal) split-intransitive system**, **inclusive vs. exclusive 1pl (ñande vs. ore)**, **obligatory possessive prefixes on inalienable nouns**, and **nominal tense (-kue, -rã)**.

**Tier 2 — useful context.** Common but not omnipresent: aspect markers, frequent postpositions, evidentials, classifier-like elements, closed-class enumerations (pronouns, demonstratives, common adpositions).

**Tier 3 — drop or compress to one line.**
- Rare derivational suffixes, archaic or strongly dialectal forms, low-frequency lexicon.
- Apertium-internal machinery: twol diacritics, compile-time flags, paradigm names, internal symbols, lexc continuation classes — anything that's about transducer engineering rather than grammar an LLM needs to know.
- Pure orthographic-normalization rules the LLM will handle implicitly.

## Verification requirement

For every Tier 1 and Tier 2 item, briefly confirm with an external source that (a) it really is high-frequency or obligatory and (b) you've described it correctly. Cite the source. Where Apertium's analysis diverges from descriptive grammars — this happens, since Apertium sometimes reflects implementation choices over linguistic ones — flag the divergence and pick the version that helps captioning.

## Register

Note explicitly whether you're targeting standard/literary Paraguayan Guarani, Yopará (Spanish-influenced everyday Guarani), or Jopará-tolerant output. The choice affects which lexicon and morphology to surface. Recommend the register that best matches the AmericasNLP training data and say why.

## Deliverable

1. **Executive summary** (3–5 bullets): the features the captioning LLM must respect or fail.
2. **Tiered table** of Apertium categories. Columns: category, one-line description, tier, justification, minimal Guarani example with interlinear gloss.
3. **The cheat-sheet itself** (≤ ~600 tokens) — the actual condensed text, ready to paste into the captioning model's system prompt. Write it for an LLM consumer, not a human linguist: short rules, schematic patterns, and 3–6-word examples with glosses, not prose paragraphs.
4. **Drop list**: what you cut from Apertium and why, so the team can sanity-check no critical category was lost.
5. **Risks & open questions**: anywhere Apertium and external grammars disagree, anywhere you're uncertain, and 1–2 ablations worth running (e.g., "does including evidentials actually change BLEU/chrF on dev?").

## Style

Be concrete and example-driven. Prefer "rule + 4-word Guarani example with gloss" over abstract description. Don't hedge where evidence is solid; flag genuine uncertainty plainly. Use Guarani orthography with the puso (apostrophe) and tilde correctly throughout.

---

CONDENSED APERTIUM CONTENT FOLLOWS:

[paste your condensed transducer file here]
One small suggestion: when you paste the condensed Apertium content, also paste a 5–10 caption sample from the AmericasNLP training set if you have access to it. That gives the model real distributional evidence rather than a priori guesses about what's frequent — and you'll get a noticeably tighter cheat-sheet back.

You said: There are actually three apertium files that we will send the LLM along with this prompt and they are uploaded here, help me adjust the prompt again

apertium-grn.grn.lexc
lexc


apertium-grn.grn.rlx
rlx


apertium-grn.grn.twol
twol


modes.xml
xml

There are actually three apertium files that we will send the LLM along with this prompt and they are uploaded here, help me adjust the prompt again

4:31 PM
Claude responded: Heads up before the prompt: when I check the four files in the upload directory, all four are 0 bytes — they appear to have failed to upload.

Analyzed four Apertium file types and restructured prompt guidance accordingly
Analyzed four Apertium file types and restructured prompt guidance accordingly
Heads up before the prompt: when I check the four files in the upload directory, all four are 0 bytes — they appear to have failed to upload. You'll want to re-upload before sending this off. That said, I can still tailor the prompt around what these four file types are in Apertium, which is what matters for the instructions.

Quick orientation on the four files, since how the specialist LLM weights them should be baked into the prompt:

.lexc — the lexicon and morphotactics. Stems, paradigms, the full inventory of morphological tags, and which affixes can attach to which stems. This is your primary source for what categories exist.
.twol — two-level phonological/orthographic rules. This is where nasal harmony lives — exactly the Tier 1 phenomenon you can't afford to miss.
.rlx — Constraint Grammar disambiguation rules. Tells you which analyses are preferred in which contexts; encodes a lot of implicit syntactic and collocational knowledge.
modes.xml — pipeline plumbing. Pure engineering, no linguistic content. Should be acknowledged and dropped.
You mentioned "three files" but uploaded four — the prompt below explicitly tells the LLM that modes.xml is engineering-only, which matches that intuition.

Here's the revised prompt:

markdown
You are an expert in Guarani (Avañe'ẽ) linguistics and computational morphology, with working familiarity with the Apertium platform, finite-state transducers (lexc/twol), and Constraint Grammar (CG-3 / .rlx). You are advising a team competing in the **AmericasNLP 2026 Image Captioning Shared Task, Guarani track** (https://github.com/AmericasNLP/americasnlp2026). The objective is to generate fluent, culturally appropriate Guarani captions for input images.

## Task

The team is building a system prompt for a multimodal LLM that will receive (a) an image and (b) a compact grammar/morphology cheat-sheet distilled from the Apertium Guarani resources (https://github.com/apertium/apertium-grn). Your job is to decide what goes into that cheat-sheet and what gets cut.

## Inputs

You are given **four files** from `apertium-grn`. Treat them differently — they encode different kinds of information and should be mined accordingly:

1. **`apertium-grn.grn.lexc`** — Lexicon and morphotactics in lexc format. **Primary source.** Mine this for: the inventory of morphological tags, the paradigm classes, which affixes attach to which stems, closed-class items (pronouns, demonstratives, postpositions), and the overall shape of nominal vs. verbal inflection. The set of tags here essentially defines what Apertium thinks Guarani morphology is.

2. **`apertium-grn.grn.twol`** — Two-level phonological/orthographic alternation rules. **This is where nasal harmony rules live**, along with any vowel/consonant alternations at morpheme boundaries. Extract the *linguistic generalizations* the rules encode (e.g., "nasal feature spreads leftward through a domain"); ignore the rule notation itself. Nasal harmony is Tier 1 — do not skip this file.

3. **`apertium-grn.grn.rlx`** — Constraint Grammar disambiguation rules. **Secondary source for syntax and collocation.** When .rlx says "prefer reading X when followed by Y," that is implicit evidence about Guarani word order, agreement, and frequent constructions. Use this to validate which tags from .lexc are actually used in practice and to surface common syntactic patterns. Don't reproduce CG syntax in the cheat-sheet — translate it to plain rules.

4. **`modes.xml`** — Pipeline configuration. **Engineering machinery, not linguistics.** Acknowledge that you've read it (one line: what pipelines are defined) and otherwise drop it entirely. Nothing from this file should appear in the cheat-sheet.

Cross-reference the files: a tag declared in .lexc but never referenced in .rlx is probably low-frequency or vestigial and is a Tier 3 candidate. A phenomenon mentioned in .twol but absent from .lexc tags (or vice versa) is worth flagging.

5. **The web.** Verify your conclusions against authoritative external sources: descriptive grammars of Guarani (e.g., Velázquez-Castillo, Gregores & Suárez, Krivoshein de Canese, Estigarribia), Apertium documentation, prior AmericasNLP shared-task papers, the Wikipedia entry on Guarani grammar, and image-captioning literature for low-resource and morphologically rich languages.

6. **The shared-task page itself.** Skim the AmericasNLP 2026 README for the actual evaluation metric, the training data source, and any register/orthography guidance. Let those constraints shape your priorities — don't optimize for features the metric won't reward.

## How to prioritize

Image captions are short, descriptive utterances naming entities, attributes, spatial relations, and actions visible in a picture. Rank every Apertium category, tag, and morphological process by how often it will appear in a 1–2-sentence caption AND how badly its misuse damages output quality.

**Tier 1 — must keep (caption-critical).** Categories that:
- Appear in essentially every caption (e.g., basic verbal agreement, plural marking, demonstratives).
- Are obligatory and whose absence is ungrammatical (e.g., possession marking on body parts and kin terms).
- Distinguish Guarani from Spanish/English in ways an LLM trained mostly on those will default-violate. Pay particular attention to: **nasal harmony** (cross-check .twol and external sources), the **active/inactive (chendal vs. areal) split-intransitive system**, **inclusive vs. exclusive 1pl (ñande vs. ore)**, **obligatory possessive prefixes on inalienable nouns**, and **nominal tense (-kue, -rã)**.

**Tier 2 — useful context.** Common but not omnipresent: aspect markers, frequent postpositions, evidentials, classifier-like elements, closed-class enumerations (pronouns, demonstratives, common adpositions). .rlx is especially useful for spotting Tier 2 items — things the disambiguator cares about are usually things that show up.

**Tier 3 — drop or compress to one line.**
- Rare derivational suffixes, archaic or strongly dialectal forms, low-frequency lexicon.
- Tags declared in .lexc but unused in .rlx.
- Apertium-internal machinery: lexc continuation-class names, twol diacritics and rule operators, CG rule syntax, paradigm-internal symbols, anything in modes.xml.
- Pure orthographic-normalization rules the LLM will handle implicitly.

## Verification requirement

For every Tier 1 and Tier 2 item, briefly confirm with an external source that (a) it really is high-frequency or obligatory and (b) you've described it correctly. Cite the source. Where Apertium's analysis diverges from descriptive grammars — this happens, since Apertium sometimes reflects implementation choices over linguistic ones — flag the divergence and pick the version that helps captioning.

## Register

Note explicitly whether you're targeting standard/literary Paraguayan Guarani, Yopará (Spanish-influenced everyday Guarani), or Jopará-tolerant output. The choice affects which lexicon and morphology to surface. Check whether Apertium's lexicon leans toward one register (the proportion of Spanish loans in .lexc is a good signal) and whether that matches the AmericasNLP training data. Recommend the register that best fits and say why.

## Deliverable

1. **Executive summary** (3–5 bullets): the features the captioning LLM must respect or fail.
2. **Tiered table** of Apertium categories. Columns: category, source file(s), one-line description, tier, justification, minimal Guarani example with interlinear gloss.
3. **The cheat-sheet itself** (≤ ~600 tokens) — the actual condensed text, ready to paste into the captioning model's system prompt. Write it for an LLM consumer, not a human linguist: short rules, schematic patterns, and 3–6-word examples with glosses, not prose paragraphs.
4. **Drop list**: what you cut from Apertium and why, organized by file (lexc / twol / rlx / modes.xml), so the team can sanity-check no critical category was lost.
5. **Risks & open questions**: anywhere Apertium and external grammars disagree, anywhere the four files disagree with each other, anywhere you're uncertain, and 1–2 ablations worth running (e.g., "does including evidentials actually change BLEU/chrF on dev?").

## Style

Be concrete and example-driven. Prefer "rule + 4-word Guarani example with gloss" over abstract description. Don't hedge where evidence is solid; flag genuine uncertainty plainly. Use Guarani orthography with the puso (apostrophe) and tilde correctly throughout.

---

FILES ATTACHED: apertium-grn.grn.lexc, apertium-grn.grn.twol, apertium-grn.grn.rlx, modes.xml
Two small things worth considering:

The "tags declared in .lexc but unused in .rlx" heuristic for spotting Tier 3 items is genuinely powerful for Apertium-derived grammars — it's the closest thing you'll get to corpus-frequency evidence without actually running the analyzer over a corpus. If you have time, running the analyzer over the AmericasNLP training captions and counting tag frequencies would be even better, but the lexc/rlx cross-check is a decent proxy.

And again — please confirm your file uploads went through before sending. The four files in /mnt/user-data/uploads/ are all 0 bytes on my end.


Claude works directly with your codebase

Let Claude edit files, run commands, and ship changes right inside your terminal or IDE.




Claude is AI and can make mistakes. Please double-check responses.


You said: Follow the instructions in the pasted text and reference the other files as instructed by the pasted text.

apertium-grn.grn.lexc
lexc


apertium-grn.grn.rlx
rlx


apertium-grn.grn.twol
twol


modes.xml
xml


You are an expert in Guarani (Avañe'ẽ) linguistics and computational morphology, with working familiarity with the Apertium platform, finite-state transducers (lexc/twol), and Constraint Grammar (CG-3 / .rlx). You are advising a team competing in the **AmericasNLP 2026 Image Captioning Shared Task,

pasted

Follow the instructions in the pasted text and reference the other files as instructed by the pasted text.

4:34 PM
Claude responded: Now I have a solid picture of all four files.

Reconciling linguistic notation systems and tag conventions
Reconciling linguistic notation systems and tag conventions
Now I have a solid picture of all four files. Let me verify a few key linguistic claims against external sources before writing up the deliverable.


Synthesized Guarani grammar rules and prepared comprehensive linguistic deliverable
Synthesized Guarani grammar rules and prepared comprehensive linguistic deliverable
I have enough to write the deliverable. Let me compose it now.

Apertium Guarani → Captioning Cheat-Sheet: Analysis & Recommendation
0. What's in the four files (one-line each)
apertium-grn.grn.lexc (17,341 lines, ≈9,200 lemmas): full morphotactics with 6 active and 6 inactive person prefixes, tense/voice/case suffixes, ~4,450 nouns, ~2,560 verbs (Tv/Iv), ~1,660 adjectives, ~555 Spanish-origin items tagged <barb>. Defines the tag inventory I'll mine.
apertium-grn.grn.twol (245 lines): regressive nasal-harmony rule ({J}:ñ), progressive nasal allomorphy in suffixes/postpositions ({N}{K} for plural, {m} for locative -pe/-me), 3p-possessive allomorphs {H}{I} (h-/i-/j-/ñ-/iʼ-), negative circumfix n(d)-…-i allomorphy, glottal-stop epenthesis ({P}), aireal -i- insertion ({i}), tonal-vowel shifting before atonal suffixes.
apertium-grn.grn.rlx (375 lines): CG disambiguator. Cares about: noun/verb selection, transitivity, dat/acc cases, plural agreement, demonstrative+N concord, copula haʼe<vbser>, postposition selection (-pe, -gua, -guarã, -rõ), nominal tense -kue/-rã, peteĩ numeral. Implicitly never references most fine tense/aspect tags from lexc — implementation cares more about big morphosyntactic categories than fine TAM.
modes.xml: defines 6 HFST/lt-proc/vislcg3 pipelines (grn-morph, grn-trace, grn-segment, grn-gener, grn-tagger, grn-disam). Pure plumbing — dropped from cheat-sheet.
1. Executive summary
The metric (ChrF++) rewards getting the surface form right, not just the lemma. Every wrong allomorph (oral vs. nasal prefix, -pe vs. -me, -kuéra vs. -nguéra) is a chunk of chrF lost. Morphology cannot be skipped.
Five non-Spanish/English-default features dominate caption quality: (i) regressive nasal harmony across prefixes, (ii) the active (areal) / inactive (chendal) split, (iii) inclusive vs. exclusive 1pl (ñande vs. ore), (iv) obligatory possessor on inalienable nouns with the t-/r-/h- triformes alternation, (v) nominal tense -kue (ex-) and -rã (future).
Captions are short. Most useful tags collapse to: person prefix on V (areal or chendal proclitic), demonstrative + N, postposition (esp. locative -pe/-me), plural -kuéra/-nguéra only on definite/animate, present tense (no marker). Almost nothing else is per-caption obligatory.
Register: target standard Paraguayan Guarani in Academia (ALG-2018) orthography. Apertium's lexicon and prior AmericasNLP Guarani training data (legal/health/educational; Estigarribia 2020; Wikipedia-grn) are all in this register. Suppress jopará code-switching unless the dev set shows otherwise; keep the puso ʼ, the tilde g̃, and nasal vowels ã ẽ ĩ õ ũ ỹ.
Apertium ↔ descriptive grammar divergences worth knowing: Apertium uses <ac>/<in> (active/inactive) where descriptions use areal/chendal; Apertium hides the aireal subclass inside the {i} archiphoneme rather than giving it a tag; Apertium analyses some chendal-class transitives as plain <tv>. Use Apertium's tags internally, but explain to the LLM in standard Guaranist terms.
2. Tiered table of categories
(Source codes: L=lexc, T=twol, R=rlx)

#	Category	Src	One-line description	Tier	Justification	Example
1	Areal subject prefixes a-/re-/o-/ja-/ro-/pe-	L,R	Active-class person/number marker on most verbs	1	Every verb with an active subject. Wrong prefix = wrong agreement.	a-guata "1SG-walk" = I walk
2	Chendal proclitics che/nde/i-/ñande/ore/pende	L,T,R	Inactive-class proclitic for stative V's & possessors	1	Used for stative predicates ("I'm sick", "it's red") and for ALL possession.	che-rasy "1SG-sick" = I am sick
3	Inclusive vs. exclusive 1pl	L,R	ja-/ñande include addressee; ro-/ore exclude	1	A photo of "us" requires choosing. LLMs default to one form.	ja-guata we (incl.) walk / ro-guata we (excl.) walk
4	Regressive nasal harmony	T	Nasal stem nasalises prefixes leftward; voiceless stops transparent	1	Wrong allomorph on every nasal-stem verb. ChrF-critical.	o-mboʼe (oral) vs. o-ñe-mongeta (nasal stem ⇒ je-→ñe-)
5	3p possessive allomorphy i-/ij-/iñ-/h-/iʼ-	L,T,R	3p prefix shape depends on stem onset & nasality	1	Picks the form before ñ-/vowel/consonant.	i-jagua his dog / h-óga his house / iñ-akã his head
6	Triformes / Biformes (t-/r-/h-)	L	Body parts & kin terms have 3 stem forms by possessor	1	Body parts can never appear bare. tesa/resa/hesa = absolute/1-2poss/3poss "eye".	che resa hovy my eyes are blue / hesa his eye(s)
7	Plural -kuéra / -nguéra	L,T,R	Animate/definite plural; nasal allomorph after nasal stems	1	Optional but ubiquitous in scenes with multiple people/animals.	mitã-nguéra children (nasal stem mitã) vs. jagua-kuéra dogs
8	Locative -pe / -me	L,T,R	"in/at/to"; nasal allomorph after nasal stem	1	Spatial relations are caption-defining.	óga-pe at home / tetã-me in the country
9	Nominal tense -kue / -rã	L,R	-kue = ex-, former; -rã = future, prospective	1	Distinguishes "former president" from "future president"; used in descriptive captions ("his former house").	mboʼehára-kue ex-teacher / tembiʼu-rã food-to-be
10	Demonstratives ko / pe / amo + pl ã/koʼã/umi	L,R	3-way deictic (proximal/medial/distal); pl uses pl form	1	Captions point: "this man", "those mountains".	ko kuña this woman / umi yvyra those trees
11	Negation circumfix nd(a)-…-i	L,T	nd- prefix + -i suffix on V; allomorphy by stem	1	A photo not showing X gets negation.	nda-ha-i I'm not going / nda-i-porã-i it's not pretty
12	Copula haʼe<vbser>	L,R	Equational "is/are"; SELECT rule in .rlx triggers it for "X is Y"	1	"X is a cat" is a frequent caption shape. Copula haʼe ≠ pronoun haʼe (3sg).	haʼe peteĩ jagua (it) is a dog
13	Future -ta / -vaʼerã	L	-ta = imminent; -vaʼerã = prospective/should	2	Less common in pure descriptions; appears in instructive/intentional captions.	o-jahu-ta (s)he will bathe
14	Past -vaʼekue / -kuri	L	Aux-like perfective and recent past	2	Captions narrating past scenes; less common than present.	o-guata vaʼekue (s)he walked (past)
15	Progressive -hína	L	Aux for ongoing action; very common in image-as-snapshot captions	2	A picture often is a snapshot of an ongoing action.	o-puka hína (s)he is laughing
16	Causative mbo-/mo- (Voices)	L,T	Adds an agent: "make X V"	2	Common in scenes of caregiving, herding, teaching.	o-mbo-puka (s)he makes (someone) laugh
17	Reflexive je- / Reciprocal jo-	L,T	je-/ñe- = REFL (nasal alt.); jo-/ño- = RECIP	2	Action-on-self captions ("she is washing herself").	o-ñe-mongeta (s)he is talking (to themselves) / o-jo-hayhu they love each other
18	Postpositions ndive, gui, rehe, gotyo, guarã, ári, pype	L,R	Comitative/ablative/topical/directional/benefactive/super/in	2	Caption spatial logic ("with X", "on top of Y").	mesa ári on the table / tape rupi along the road
19	Numerals 1–10 peteĩ, mokõi, mbohapy, irundy, po, poteĩ, pokõi, poapy, porundy, pa	L,R	Native count system (vigesimal-ish, with -pa for 10s)	2	Counted-entity captions.	mokõi mitã two children
20	Substantivising / relative -va	L,R	Turns V into participle/relativiser ("the one who Vs")	2	Useful for describing roles in a scene ("a man who is reading").	o-mbaʼapo-va (one) who works
21	Imperative prefix e-/pe- (+-na/-ke)	L	2sg/2pl imperative + politeness; in didactic captions	3	Almost never in descriptive captions.	e-juhu find! — cut
22	Optative t(a)-/tere-/to-	L	Hortative/jussive ("let me/them V")	3	Tag declared in lexc; unused in rlx.	drop
23	Diminutive -mi/-ʼi/-mimi	L	Affectionate/small	3	Not declared in rlx; very low yield.	one-line mention
24	Evidentials/discourse particles niko<nar>, piko<qst>, nipo, katu	L	Narrative/interrogative/contrastive markers	3	Rare in image captions; risky to over-use.	drop except if dev set shows them
25	Fine past tense subdivision <ifi>/<pii>/<pmp>/<past>	L	Several past markers Apertium distinguishes	3	rlx mostly ignores them; collapse to one "past" bucket.	compress
26	Caritive -ỹ (<car>)	L	"Without" suffix on N	3	Rare; unused in rlx.	drop
27	Object pronominal proclitics che/nde/ro/po/i- on V	L	Marks O when prefix already marks S	3	Hierarchical/portmanteau system; complex. Limit to one note.	one-line ("ro- = I→2sg portmanteau")
28	Apertium-internal machinery	L,T	Continuation-class names (POS-COMPL, CASE-INFL…), archiphonemes ({N}, {K}, {P}, {i}…), CG syntax (SELECT, BARRIER), modes.xml	3	Helps no LLM.	drop entirely
3. THE CHEAT-SHEET (paste into system prompt)
GUARANI (Avañeʼẽ) – CAPTION-CRITICAL GRAMMAR. Use standard Paraguayan
Guarani orthography: nasal vowels ã ẽ ĩ õ ũ ỹ, g̃, puso ʼ. NEVER drop diacritics.

== VERB FORM = PREFIX + STEM (+ optional suffixes) ==

Two prefix sets — pick by verb class (active = action; inactive = state/feeling):

ACTIVE (areal):  a- 1SG | re- 2SG | o- 3 | ja- 1PL.INCL | ro- 1PL.EXCL | pe- 2PL
                 a-guata "I walk", o-puka "(s)he laughs", ja-jahu "we (incl) bathe"

INACTIVE (chendal, written separate or hyphenated):
                 che 1SG | nde 2SG | i-/ij-/iñ-/h- 3 | ñande 1PL.INCL | ore 1PL.EXCL | pende 2PL
                 che-rasy "I am sick", h-aku "it is hot", ñande-vyʼa "we (incl) are happy"

INCL vs EXCL is OBLIGATORY for "we": ñande/ja- includes the addressee; ore/ro- excludes them.

== NASAL HARMONY (regressive, very common, ChrF-critical) ==

If the stem has any nasal segment (ã ẽ ĩ õ ũ ỹ, m, n, ñ, mb, nd, ng, g̃),
the prefix takes its nasal allomorph:
  ja- → ña-     (ja-mboʼe ✗ → ña-mboʼe ✓ "we teach")
  je- → ñe-     (reflexive/passive: o-ñe-monge "he sleeps himself = sleeps")
  mbo- → mo-    (causative on nasal stem: mo-ñembyahýi "make hungry")
  i- (3POSS) → iñ- before vowel-initial nasal stem (iñ-akã "his head")
            → h-  before tonal vowel (h-óga "his house", h-esa "his eye")
            → ij- before atonal vowel-initial oral stem (ij-ao "his clothes")
Voiceless stops (p, t, k, ch, s) are TRANSPARENT and do not block harmony.

== INALIENABLE NOUNS (body parts, kin) — possessor is OBLIGATORY ==

Triformes alternate t- (no possessor) / r- (1-2 poss) / h- (3 poss):
  tesa "an eye"  → che resa "my eye"  → hesa "his/her eye(s)"
  tape "path"    → che rape "my path" → hape "his path"
  túva "father"  → che ru   "my father" → itúva / túva  (3p uses i- elsewhere)
Biformes (e.g. óga "house"): bare for 3 with h-, with r- for 1-2: che róga / hóga.
NEVER write a body part or kin term bare if the picture shows whose it is.

== NUMBER ==

Plural is marked with -kuéra ONLY on definite/animate plurals; -nguéra after nasal stem.
  mitã-nguéra "the children", jagua-kuéra "the dogs", umi yvyra "those trees".
3rd person verb is unmarked for number; use "hikuái" auxiliary to force "they": o-puka hikuái "they laugh".

== NOMINAL TENSE (very Guarani; Spanish/English have nothing like it) ==

-kue = former, ex-, used-up:  mboʼehára-kue "ex-teacher", tembiʼu-kue "leftovers"
-rã  = future, prospective:    tembiʼu-rã "food-to-be", che ru-rã "my future husband"

== TENSE/ASPECT (verbal, all suffixes) ==

PRESENT = bare verb (default for image captions of ongoing scenes).
PROGRESSIVE = add hína:           o-puka hína "he is laughing"
PAST: -kuri (recent), -vaʼekue (perfective), -akue, -mi (imperfective long-ago)
FUTURE: -ta (imminent: o-ho-ta "he will go"), -vaʼerã (prospective/should)
NEGATION: circumfix nd(a)-…-i:    nd-a-ha-i "I am not going",  nda-i-porã-i "it is not pretty"
                                  (n- before nasal stems: na-ñe-mongeta-i)

== POSTPOSITIONS (Guarani has no prepositions) ==

-pe / -me (after nasal): "in, at, to"     óga-pe "at home", tetã-me "in the country"
-gui  "from"        -rehe / -re  "about, on, onto"     -ndive  "with"
-gua  "of, from"    -guarã  "for (purpose)"            -ári  "on top of"
-pype "inside"      -gotyo  "toward"                   -rupi  "through, along"

== DEMONSTRATIVES ==

ko "this" | pe "that" | amo "that yonder"  (sg)
ã / koʼã "these" | umi "those"             (pl)
Word order: DEM N — ko jagua "this dog", umi mitã-nguéra "those children".

== WORD ORDER & MODIFIERS ==

Default: prefix on V already encodes subject; explicit S optional and usually first.
Adjective FOLLOWS noun:    jagua hũ "black dog", kuña porã "pretty woman".
Possessor PRECEDES possessed:  mitã sy "the child's mother", che jagua "my dog".
Copula "is/are" = haʼe (different from 3sg pronoun haʼe):  haʼe peteĩ jagua "it is a dog".

== FREQUENT LEXICAL ANCHORS FOR CAPTIONS ==

people: kuimbaʼe "man", kuña "woman", mitã "child", karai "Mr/elder",
        tapicha "person", mboʼehára "teacher", tetãygua "compatriot"
body:   akã "head", tĩ "nose", juru "mouth", tesa "eye", po "hand", py "foot",
        hete "body", áva "hair"
animals: jagua "dog", mbarakaja "cat", kavaju "horse", guyra "bird", pira "fish",
         mbói "snake", tymba "(domestic) animal"
nature: kuarahy "sun", jasy "moon", mbyja "star", ára "day/sky", yvága "sky",
        yvy "earth/ground", y "water", kaʼaguy "forest"
objects/places: óga "house", tape "path", tenda "place", aranduka "book",
                ao "clothing", tembiʼu "food", mesa "table"
colors: pytã "red", hovy "blue", aky "green", saʼyju "yellow", morotĩ "white",
        hũ "black"
size/quality: tuicha "big", michĩ/mirĩ "small", puku "long", mbyky "short",
              porã "beautiful/good", vai "bad/ugly", pyahu "new", tuja "old"
numerals: peteĩ 1, mokõi 2, mbohapy 3, irundy 4, po 5
4. Drop list (what was cut and why)
From .lexc
All continuation-class names (POS-COMPL, CASE-INFL, IRR-INFL, DEM-PRN-INFL, V-INFL, MODES, MODES-AUX, etc.). Apertium plumbing.
Archiphonemes as visible symbols ({N}, {K}, {P}, {H}, {I}, {i}, {m}, {b}, {a}, {e}, {Y}, {p}, {r}, {d}, {D}, {J}, {T}, {t}, {o}, {g}, {E}, •). Replaced by plain-language allomorphy notes for the four cases that matter: i-/ij-/iñ-/h-, -pe/-me, -kuéra/-nguéra, ja-/ña-.
Fine past-tense distinctions (<ifi> pretérito perfecto, <pii> imperfecto, <pmp> pluperfect, separate <past>). The .rlx never disambiguates among them; collapsed to "past suffixes."
Fine future (<fts> subjunctive future, <fti> indicative future). Collapsed.
Voice subdistinctions <obj> (objective), <sub> (subsumptive), <recip>. Kept only causative + reflexive/reciprocal.
Modal/discourse tags <vol>, <nar>, <car>, <emph>, <dist> (distributive -ve). Apertium-only; rare in captions.
Diminutive <dim> (-mi, -ʼi). Mentioned in cheat-sheet only as note-worthy if seen.
Imperative <imp> and optative <opt>. Captions describe; they don't command.
Question particle <qst> (-pa, -piko, -po). Captions are not questions.
<incp> (incorporation): Apertium's CG explicitly REMOVEs every Incp reading. This is a noun-verb-compounding analysis Apertium produces but doesn't trust; captions don't need it.
Punctuation/symbol/abbreviation tags (<sym>, <abbr>, <percent>, <sent>, <guio>, <cm>, <apos>, <rquot>, <lquot>, <rpar>, <lpar>). Trivia.
The Spanish loan lexicon (SpaNouns, SpaAdjectives, BARB, Barbarismes, ~555 items tagged <barb>). Cut from cheat-sheet — but flagged: see Risks §5.
Roman numerals, digits, proper-noun lists (~600 toponyms incl. Indianapolis, Wisconsin, Wyoming…). The LLM already knows world geography.
From .twol
The rule notation itself (alphabet declarations, archiphoneme realisations, <=> operators, where … matched clauses). Translated to four plain-language rules: regressive nasal harmony; -kuéra/-nguéra; -pe/-me; 3-poss prefix allomorphy. Glottal-stop epenthesis ({P}) is also kept implicitly through correct lexical forms.
Tonal-vowel/atonal-vowel shifting before suffixes (the Va:Vt rule). The LLM should use lexical forms verbatim; this rule fires automatically inside the FST. Mentioning it would invite over-correction.
The -rehe → -re reduction, the -ndive → -ndie orthographic variant, Err/Orth Dir/LR variants (these are surface-spelling alternatives Apertium generates for tolerance, not what to produce).
From .rlx
CG syntax (SELECT, REMOVE, MAP, BARRIER, subreadings SUB:0, etc.). Translated to plain-language rules where they bear on captioning (e.g., "after peteĩ the next noun is the head" → not even mentioned because numerals already precede N).
@nsubj/@dobj/@iobj/@amod/@compound/@ccomp/@advmod/@conj/@cc/@advcl/@acl syntactic-relation labels. Useful only for downstream parsing.
Heuristic REMOVEs of low-frequency analyses (Incp, Guess, A+Prn, Re+Prn, Top near Cog/Ant).
Ñandejára-specific rule (a hardcoded selector for "Our Lord"). Not generalisable.
From modes.xml
Everything. Six pipeline definitions (grn-morph, grn-trace, grn-segment, grn-gener, grn-tagger, grn-disam) describe how to invoke hfst-proc/lt-proc/vislcg3. None of it is linguistic.
5. Risks, open questions, ablations
Disagreements between Apertium and descriptive grammars
Active/inactive labelling. Apertium uses <ac>/<in>; Estigarribia (2020), Velázquez-Castillo, the Wikipedia entry, and the LING073 Apertium-style materials use areal/chendal/aireal. The cheat-sheet uses Apertium's <ac>/<in> only internally; the LLM-facing text uses the descriptive terms because they are more searchable and more linguistically transparent. Not a real conflict — just terminology.
Aireal subclass is invisible in Apertium's tags. In descriptive grammar, aireal verbs (a-i-ko, a-i-pota, a-i-kuaa) are a third subclass with an /-i-/ between prefix and stem. Apertium implements them via the {i} archiphoneme set on individual lemmas (e.g., poriahuvereko:%{i%}poriahuvereko V in lexc). This means the LLM, given Apertium tags only, cannot tell aireal from areal. In the cheat-sheet I've described the consequence at the level of attested forms (a-iko, not a-ko) rather than as a class label.
Apertium's analysis of ñe- as a 1pl.incl pronominal accusative (lexc line 7031: ñande<prn>…<acc>:ñe Verbs) is suspicious. In descriptive grammar ñe- is the nasal allomorph of the reflexive/passive je-. This is a place where Apertium's lexicon will mis-tag forms; for captioning we should treat ñe- as REFL-after-nasal-stem, full stop.
<tv> vs. <iv> does not equal active vs. inactive. Apertium's transitivity tag splits verbs by valence, while areal/chendal class is a separate (and partly orthogonal) split. Several lemmas tagged <tv> are chendal (e.g., poriahuvereko<v><tv> 'pity', which inflects with che/nde/i-, not a/re/o-). The cheat-sheet handles this by describing prefix sets in semantic terms ("active = action; inactive = state/feeling") rather than by transitivity.
Disagreements among the four files
The -niko/<nar> particle is declared in lexc and twol allomorphy rules, but rlx never references the <nar> tag. Either nar is rare or the disambiguator simply doesn't need to disambiguate it. Either way, low priority.
The aireal class is not named in lexc tags, yet twol has a dedicated rule "Add [i] for aireales." A genuine cross-file inconsistency: the rule exists but the tag does not.
Plural marking discrepancy. lexc has both <det><pl> kuéra (a separate post-nominal "plural determiner") and SUF-PL -ita<adj><ind><pl>. rlx only uses the <pl> tag. The -ita plural is probably a Spanish-loan adjective plural and unlikely to occur in native captions; cut from cheat-sheet.
Other open questions
Register / loan tolerance. Apertium tags ~555 items as <barb> (Spanish loans like trabajo, colegio, hospital, familia). The AmericasNLP 2023 Guarani training data spans legal/health/educational domains where such loans appear naturally. Whether the 2026 image-caption gold uses standard ALG-2018 forms (e.g., mboʼehao for school, not escuela) or jopará-tolerant forms is unknown until the dev set is read. Recommended: target standard PG; if dev captions show Spanish-origin tokens, allow <barb> words verbatim but never mix orthographies (don't write jaha-mos or anything jopará).
Orthographic variation in the wild. The Apertium lexicon contains many Err/Orth entries (e.g., paragu•ái:paragu•ái and paraguái:paraguái, accent placement differing). The dev/test set will probably be normalised, but if it isn't, chrF++ will sting on accent placement. Verify on dev before final submission.
Word segmentation of person prefix + verb. Apertium represents these joined (o-puka written opuka, no hyphen). The conventional written form omits the hyphen; the cheat-sheet shows hyphens for clarity. Important: tell the LLM to OUTPUT joined forms (opuka, cherasy, not o-puka, che-rasy) — otherwise chrF++ punishes every prefix.
Suggested ablations on the dev set
Nasal-harmony block. Run the LLM with vs. without the harmony rule paragraph. Hypothesis: removing it costs ≥1 chrF++ point on captions whose images have ≥1 nasal-stem verb. If so, keep it; otherwise inspect why the model ignored it.
Inalienable-possession block. Remove the triformes/biformes paragraph and the body-part lexical anchors. Captions of people/animals where body parts are visible should degrade; if they don't, the LLM is already handling this via patterns from training data and the block is redundant.
Inclusive/exclusive 1pl. Captions describing groups including the (implicit) viewer ("us at the festival") vs. excluding them ("the men working") should differ. Test whether explicit incl/excl guidance changes the model's choice. If the dev set rarely uses 1pl, drop the paragraph entirely.
Loan-word policy. Two prompts: (a) "use only native Guarani lexicon"; (b) "Spanish-origin words are acceptable when standard." Compare chrF++. Set the policy that wins; the difference will tell you the dev set's register without you needing to read all 50 examples manually.
-kue / -rã block. These are unique to Guarani and Spanish-defaulting LLMs almost never produce them. If the dev set captions never use them (likely for static images of present-time scenes), the block can be cut. Otherwise it's the highest-leverage Tier-1 instruction.
You said: Can you give me the full .
Can you give me the full .md file that contains the cheat sheet (all the information requested)?

4:44 PM
Claude responded: The full deliverable is in apertium-grn-caption-cheatsheet.

Consolidated cheat sheet content into downloadable markdown format
Consolidated cheat sheet content into downloadable markdown format
The full deliverable is in apertium-grn-caption-cheatsheet.md — all five sections (file overview, executive summary, tiered table, the paste-ready cheat-sheet itself, drop list by file, and risks/ablations).


Apertium grn caption cheatsheet
Document · MD 

Claude works directly with your codebase

Let Claude edit files, run commands, and ship changes right inside your terminal or IDE.




Claude is AI and can make mistakes. Please double-check responses.










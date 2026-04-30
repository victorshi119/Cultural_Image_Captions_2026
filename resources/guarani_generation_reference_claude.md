# Guarani Generation Reference
*A production grammar guide for generating grammatically valid Paraguayan Guarani*

Source: Estigarribia, B. (2020). *A Grammar of Paraguayan Guarani*. UCL Press.

---

## 1. Word Order

The most frequent surface order is **V** (verb alone) or **VO** (verb-object). The canonical full-sentence order when all constituents are present is **SVO**, but word order is flexible. Common patterns:

| Pattern | Example | Gloss |
|---------|---------|-------|
| V | `Aha.` | I go/went. |
| VO | `Ojuka so'o.` | He kills/killed meat. |
| SVO | `Mitã oho óga gotyo.` | The child goes towards the house. |
| OVS | `So'o ojuka.` | Meat he kills. (focus on object) |

**Key rules for generation:**
- Subjects are very frequently **omitted** (subject drop is the norm). The verb prefix encodes person/number.
- When a subject NP or pronoun appears overtly, it often signals **contrastive focus**.
- Focused constituents prefer **sentence-initial position**.
- Interrogative words (`mba'e` 'what', `moõ` 'where') appear sentence-initially.

### 1.1 Noun Phrase Internal Order

```
(Demonstrative/Numeral) + (Possessor) + HEAD NOUN + (Adjective) + (Relative Clause)
```

| Guarani | Gloss | English |
|---------|-------|---------|
| `ko jagua ñarõ` | prox.sg dog ferocious | this ferocious dog |
| `mitã'i po ky'a` | child-dim hand dirty | the small child's dirty hand |

> Adjectives **follow** the noun (opposite of English). Possessors **precede** the noun.

---

## 2. Verb Morphology

This is the most critical section. Guarani is **head-marking**: person and number are always **prefixed** to the verb. There is no infinitive form. Every predicate — including nouns and adjectives used predicatively — takes person prefixes.

### 2.1 Split Intransitivity: Active vs. Inactive Prefixes

Intransitive verbs split into two classes with different subject prefixes. **Membership must be memorized** — it is not always predictable from meaning.

**Active verbs** (subjects are typically agents in control): `ho` 'go', `guata` 'walk', `ñani` 'run', `puka` 'laugh', `ñe'ẽ` 'speak', `karu` 'eat', `ake` 'sleep', `purahéi` 'sing', `jeroky` 'dance', `mba'apo` 'work', `juga` 'play'.

**Inactive verbs** (subjects typically experience a state): `kane'õ` 'be tired', `porã` 'be beautiful', `rasy` 'be sick', `vare'a` 'be hungry', `pochy` 'be angry', `tuja` 'be old', `katupyry` 'be skillful'. All adjectives/states take inactive prefixes.

#### Active subject prefixes (standard verbs)

| Prefix | Person | Example |
|--------|--------|---------|
| `a-` | 1sg | `a-guata` → `aguata` 'I walk' |
| `re-` | 2sg | `re-guata` → `reguata` 'you walk' |
| `o-` | 3 | `o-guata` → `oguata` 's/he walks' |
| `ja-` | 1pl.incl | `ja-guata` → `jaguata` 'we (incl.) walk' |
| `ro-` | 1pl.excl | `ro-guata` → `roguata` 'we (excl.) walk' |
| `pe-` | 2pl | `pe-guata` → `peguata` 'you (pl.) walk' |

**Aireal active verbs** add `-i-` to the prefix: `ai-`, `rei-`, `oi-`, `jai-`, `roi-`, `pei-`. Examples: `kuaa` 'know', `pytyvõ` 'help', `poru` 'use', `pota` 'want'. E.g., `aikuaa` 'I know', `reikuaa` 'you know'.

#### Inactive subject prefixes (states/properties)

| Prefix | Person | Example |
|--------|--------|---------|
| `che-` | 1sg | `che-porã` → `cheporã` 'I am beautiful' |
| `nde-` / `ne-` (nasal) | 2sg | `nde-tuja` → `ndetuja` 'you are old' |
| `i-` / `iñ-` (nasal) | 3 | `i-porã` → `iporã` 's/he is beautiful' |
| `ñande-` / `ñane-` (nasal) | 1pl.incl | `ñane-rasy` 'we are sick' |
| `ore-` | 1pl.excl | `ore-kane'õ` 'we are tired' |
| `pende-` / `pene-` (nasal) | 2pl | `pene-porã` 'you (pl.) are beautiful' |

### 2.2 Transitive Verbs

The prefix encodes the participant **higher in the person hierarchy (1 > 2 > 3)**. If the AGENT is higher-ranked, use ACTIVE prefixes. If the PATIENT is higher-ranked, use INACTIVE prefixes on the patient.

| Guarani | Gloss | English |
|---------|-------|---------|
| `a-juka ichupe` | 1sg.act-kill to.him/her | I kill(ed) him/her [agent=1 > patient=3, active] |
| `che-juka ha'e` | 1sg.inact-kill s/he | S/he kill(ed) me [patient=1 > agent=3, inactive on patient] |

**Portmanteau prefixes:** When 1st person acts on 2nd person, use `ro-` (1→2sg) or `po-` (1→2pl):

| Guarani | Gloss | English |
|---------|-------|---------|
| `ro-h-ayhu` | 1>2sg-possm3-love | I love you (sg.) |
| `po-h-ayhu` | 1>2pl-possm3-love | I love you (pl.) |

### 2.3 Tense Marking

**Present / Past:** Bare verb forms are **non-future**. Context and time adverbs distinguish present from past. Telic verbs (with natural endpoints) default to past; atelic (states, activities) default to present.

| Guarani | Gloss | English |
|---------|-------|---------|
| `o-guata` | 3.act-walk | s/he walks (present — atelic) |
| `ho-'a` | 3.act-fall | s/he fell (past — telic) |

**Future:** Suffix `-ta` (unstressed) marks definite future.

| Guarani | Gloss | English |
|---------|-------|---------|
| `a-mba'apo-ta` | 1sg.act-work-fut | I will work |
| `o-guata-ta` | 3.act-walk-fut | s/he will walk |

**Explicit past:** Suffix `-va'ekue` (or reduced `-'akue`) marks remote/explicit past.

| Guarani | Gloss | English |
|---------|-------|---------|
| `a-ha-va'ekue` | 1sg.act-go-past | I went (explicit/remote past) |

**Progressive:** Particle `hína` marks ongoing action (post-verbal, semi-free).

| Guarani | Gloss | English |
|---------|-------|---------|
| `o-guata hína` | 3.act-walk prog | s/he is walking |

**Completive:** Suffix `-ma` marks 'already / completed'.

| Guarani | Gloss | English |
|---------|-------|---------|
| `og̃uahẽ-ma` | 3.act-arrive-already | s/he has already arrived |

### 2.4 Negation

All predicates are negated by the circumfix **`nd-…-i`** (oral bases) or **`n-…-i`** (nasal bases). The suffix becomes `-ri` if the stem ends in `-i` or `-ĩ`. Future negation uses `-mo'ã` instead of `-ta`.

| Guarani | Gloss | English |
|---------|-------|---------|
| `nd-a-guata-i` | neg-1sg.act-walk-neg | I do not walk |
| `n-o-porã-i` | neg-3.inact-beautiful-neg | s/he is not beautiful [nasal base → n-] |
| `n-a-mba'apo-mo'ã-i` | neg-1sg.act-work-neg.fut-neg | I will not work |

**Negation prefix rules:**
- Oral base → `nd-` prefix; nasal base → `n-` prefix
- Active prefix beginning in vowel (`a-`, `o-`) → `n(d)-` precedes person prefix directly: `nd-a-`, `nd-o-`
- Active prefix beginning in consonant → epenthetic vowel matching the prefix vowel: `nd-are-` (2sg), `nd-aja-` (1pl.incl)
- Exception: 2pl.act `pe-` takes `nda-pe-`
- Inactive prefixes always take `nda-` (oral) or `na-` (nasal)

| Form | Meaning |
|------|---------|
| `nd-a-japo-i` | I don't do it (1sg.act oral) |
| `nd-o-ho-i` | s/he doesn't go (3.act oral) |
| `nd-are-ho-i` | you don't go (2sg.act oral) |
| `nda-che-porã-i` | I am not beautiful (1sg.inact oral) |
| `n-a-purahéi-i` | I don't sing (nasal base) |
| `n-o-mano-i` | s/he doesn't die (nasal base) |

### 2.5 Conjugated Sentence Examples

**Present:**
```
Mitã o-karu.
child 3.act-eat
'The child eats / is eating.'
```

**Present progressive:**
```
Kuña o-guata hína óga gotyo.
woman 3.act-walk prog house towards
'The woman is walking toward the house.'
```

**Past (bare telic verb):**
```
Ha'e o-'a yvýpe.
s/he 3.act-fall earth-in
'S/he fell to the ground.'
```

**Explicit past:**
```
A-ha-va'ekue Asuncionpe.
1sg.act-go-past Asuncion-in
'I went to Asunción (past).'
```

**Future:**
```
Ko'ẽro a-mba'apo-ta.
tomorrow 1sg.act-work-fut
'Tomorrow I will work.'
```

**Negation:**
```
Nd-a-guata-i.
neg-1sg.act-walk-neg
'I don't walk.'
```

---

## 3. Noun Phrases & Possession

### 3.1 Relational (Multiform) Nouns

A large class of nouns (and some verbs) have a shape-shifting initial consonant. You **must** use the correct form:

| Form | Condition | Example |
|------|-----------|---------|
| `t-` | non-possessed / absolute | `t-esa` 'an eye (in general)' |
| `r-` | possessed by NP or 1st/2nd person inactive prefix | `che-r-esa` 'my eye', `nde-r-esa` 'your eye' |
| `h-` | possessed by 3rd person pronominal | `h-esa` 'his/her/their eye' |

More examples:

| Absolute | 1sg possessed | 3sg possessed |
|----------|--------------|---------------|
| `t-óga` 'a house' | `che-r-óga` 'my house' | `h-óga` 'his/her house' |
| `t-ayhu` 'love' | `che-r-ayhu` 'my love' | `h-ayhu` 'his/her love' |
| `t-ova` 'face' | `che-r-ova` 'my face' | `h-ova` 'his/her face' |
| `t-esa` 'eye' | `che-r-esa` 'my eye' | `h-esa` 'his/her eye' |

### 3.2 Possessive Noun Phrases

Possessor **precedes** possessum. When possessor is a full NP, simple juxtaposition — no special marking:

```
María ajaka
María basket
'María's basket'
```

When possessor is pronominal, inactive person prefixes are used (+ relational consonant if applicable):

| Guarani | Gloss | English |
|---------|-------|---------|
| `che-r-óga` | 1sg.inact-possm-house | my house |
| `nde-r-esa` | 2sg.inact-possm-eye | your eye |
| `h-óga` | possm3-house | his/her/their house |

### 3.3 Adjectives and Modifiers

Adjectives **follow** the noun. Most roots can function as adjective, noun, or verb with no change in form.

| Guarani | Gloss | English |
|---------|-------|---------|
| `óga tuicha` | house big | a big house |
| `kuña porã` | woman beautiful | a beautiful woman |

Adjectives used predicatively take inactive prefixes: `iporã` 's/he/it is beautiful'; `cheporã` 'I am beautiful'.

### 3.4 Plurality

Number is **not obligatorily marked**. For animate nouns, the enclitic `=kuéra` (nasal variant `=nguéra`) marks plural. Omit when a numeral or other plural indicator is present.

| Guarani | Gloss | English |
|---------|-------|---------|
| `mitã=nguéra` | child=pl | children |
| `mokõi mitã` | two child | two children [no =kuéra needed] |

---

## 4. Nasal Harmony

Guarani has pervasive nasal harmony: a nasal vowel in the root causes nasalization of adjacent sounds, so oral morphemes take nasal allomorphs when attached to nasal bases.

**Single rule:** if a root is nasal (contains ã, ẽ, ĩ, õ, ũ, ỹ), all attached affixes shift to their nasal allomorphs.

| Allomorph alternation | Example |
|-----------------------|---------|
| `nd-` → `n-` (nasal base) | `nomañái` 'he doesn't look' (vs. `ndojoguái` oral) |
| `=kuéra` → `=nguéra` (nasal base) | `mitã=nguéra` 'children' |
| `=pe` → `=me` (nasal base) | `táva=me` 'in the village' |
| `ñande-` → `ñane-` (nasal base) | `ñane-rasy` 'we are sick' |
| `pende-` → `pene-` (nasal base) | `pene-porã` 'you (pl.) are beautiful' |

> **Practical tip:** identify the nasal quality of the root first, then apply the appropriate allomorphs to all attached suffixes and enclitics.

---

## 5. Postpositions (Case Marking)

Guarani has no case suffixes. Grammatical relations are marked by **postpositions** (enclitics on the NP).

| Postposition | Meaning & Use |
|-------------|---------------|
| `=pe` / `=me` (nasal) | locative 'in/at/to'; direct object marker for human/animate objects |
| `=gui` | 'from' (source/ablative) |
| `=rehe` / `=re` | 'about/at' (postpositional complement for some verbs) |
| `=ndive` / `=ndi` | 'with' (comitative) |
| `=rupi` | 'through/around/because' |
| `=gotyo` / `=ngotyo` (nasal) | 'towards' |
| `='ári` | 'on top of' |
| `=peve` / `=meve` (nasal) | 'until' |
| `=guive` | 'since' (from a starting point) |
| `=haguã` / `=g̃uarã` | 'for/in order to' (purpose) |

> Human direct objects are marked with `=pe`: `Ajuka la mitãme` 'I kill the boy'. Inanimate objects have **no marker**.

---

## 6. Core Vocabulary for Image Captioning

### 6.1 Verbs

| Guarani | Meaning & Usage |
|---------|----------------|
| `h-echa` (relational) | to see / look at → `ahecha ichupe` 'I see him' |
| `'u` / `ha'u` | to eat/drink (transitive) — 1sg: `ha'u`, 3: `ho'u` |
| `karu` | to eat (intransitive, active) → `okaru` 's/he eats' |
| `guata` | to walk (active) → `oguata` 's/he walks' |
| `guapy` | to sit (active) → `oguapy` 's/he sits' |
| `'a` / `ha'a` | to fall — 1sg: `ha'a`, 3: `ho'a` |
| `pyhy` | to hold/grab (aireal) → `oipyhy` 's/he grabs it' |
| `ñemonde` | to wear/dress → `oñemonde` 's/he wears' |
| `juga` | to play (active) → `ojuga` 's/he plays' |
| `mba'apo` | to work (active) → `omba'apo` 's/he works' |
| `ñe'ẽ` | to speak (active) → `oñe'ẽ` 's/he speaks' |
| `ñani` | to run (active) → `oñani` 's/he runs' |
| `puka` | to laugh (active) → `opuka` 's/he laughs' |
| `pu'ã` | to get up/stand (active) → `opu'ã` 's/he stands' |
| `pyta` | to stay/remain (active) → `opyta` 's/he stays' |
| `juhu` | to find → `ojuhu` 's/he finds' |
| `me'ẽ` | to give → `ome'ẽ` 's/he gives' |
| `ru` / `aru` | to bring → `aru` 'I bring', `oru` 's/he brings' |
| `h-endu` (relational) | to hear/listen → `ahendu` 'I hear' |
| `ike` | to enter → `oike` 's/he enters' |
| `sẽ` | to exit/go out → `osẽ` 's/he goes out' |
| `y'u` / `hay'u` | to drink water → `hay'u` 'I drink water' |
| `ma'ẽ` | to look at (with `=re`) → `oma'ẽ hese` 's/he looks at him' |

### 6.2 Nouns

| Guarani | Meaning |
|---------|---------|
| `ava` / `kuimba'e` | person / man |
| `kuña` | woman |
| `mitã` | child |
| `mitã kuimba'e` | boy |
| `mitã kuña` | girl |
| `óga` / `t-óga` | house (relational: `hóga` 'his house') |
| `yvyra` | tree |
| `y` | water, river |
| `tembi'u` / `rembi'u` / `hembi'u` | food (relational) |
| `mymba` / `t-ymba` | animal (relational: `t-ymba` 'wild animal') |
| `po` | hand |
| `t-ova` | face (relational: `rova`, `hova` 'his face') |
| `t-esa` | eye (relational: `hesa` 'his/her eye', `chesa` 'my eye') |
| `akã` | head |
| `tape` | road, path |
| `ka'aguy` | forest |
| `ñu` | field, meadow |
| `táva` | town, village |
| `pira` | fish |
| `ryguasu` | chicken |
| `jagua` | dog |
| `mbarakaja` | cat |
| `ao` / `ij-ao` | clothes (relational: `ijao` 'his/her clothes') |
| `kuarahy` | sun |
| `jasy` | moon |
| `yvoty` | flower |
| `so'o` | meat |

### 6.3 Descriptors / Adjectives / Adverbs

| Guarani | Meaning |
|---------|---------|
| `tuicha` / `guasu` | big, large |
| `michĩ` / `piru` | small, thin |
| `tuja` | old (of animate beings) |
| `pyahu` / `karia'y` | new / young (person) |
| `pytã` | red |
| `morotĩ` | white |
| `hũ` | black |
| `tovy` / `hovy` | blue / green |
| `sa'yju` | yellow |
| `aky` | green |
| `heta` | many, numerous |
| `peteĩ` | one |
| `mokõi` | two |
| `mbohapy` | three |
| `irundy` | four |
| `porã` | beautiful, good |
| `vai` | bad, ugly |
| `pya'e` | fast, quickly |
| `mbegue` | slow, slowly |
| `ko'ápe` | here |
| `ko` / `ko'ã` | this (sg.) / these (pl.) — proximal demonstrative |
| `pe` / `umi` | that (sg.) / those (pl.) — medial/distal |

---

## 7. Annotated Caption Examples

### Caption 1: 'The child is eating fruit.'
```
Mitã o-karu yva hína.
child 3.act-eat fruit prog
'The child is eating fruit.'
```
*Notes: `karu` = active intransitive 'eat'; `o-` = 3rd person active; `hína` = progressive; `yva` = 'fruit/apple'. No object marking needed for inanimate.*

---

### Caption 2: 'A woman is walking near the house.'
```
Kuña o-guata hína óga renondépe.
woman 3.act-walk prog house front-in
'A woman is walking in front of/near the house.'
```
*Notes: `renonde` + `=pe` = 'in front of/near'; no article needed — nouns are unspecified for definiteness.*

---

### Caption 3: 'Two men are playing.'
```
Mokõi kuimba'e o-juga hína.
two man 3.act-play prog
'Two men are playing.'
```
*Notes: numeral precedes the noun; no `=kuéra` needed with a numeral; 3rd person prefix `o-` covers both singular and plural.*

---

### Caption 4: 'The boy holds a dog.'
```
Mitã kuimba'e oi-pyhy jagua.
child man 3.act-grab dog
'The boy grabs/holds a dog.'
```
*Notes: `pyhy` is an aireal transitive verb → `oi-` (not `o-`); `jagua` = inanimate-treated, no `=pe` marking.*

---

### Caption 5: 'She is wearing a red dress.'
```
O-ñemonde ao pytã.
3.act-dress clothes red
'She is wearing red clothes/a red dress.'
```
*Notes: adjective `pytã` follows the noun `ao`; bare form reads as present for atelic states.*

---

### Caption 6: 'A man is working in the field.'
```
Kuimba'e o-mba'apo hína ñúpe.
man 3.act-work prog field-in
'A man is working in the field.'
```
*Notes: `=pe` locative marks 'in the field'; `mba'apo` = active verb.*

---

### Caption 7: 'The children are running towards the river.'
```
Mitã=nguéra o-ñani hína y=gotyo.
child=pl 3.act-run prog water=towards
'The children are running towards the river.'
```
*Notes: `=nguéra` (nasal variant of `=kuéra`) marks plural of nasal noun `mitã`; `=gotyo` = 'towards'; `y` = 'water/river'.*

---

### Caption 8: 'An old woman is sitting near the house.'
```
Kuña tuja o-guapy hína óga renondépe.
woman old 3.act-sit prog house front-in
'An old woman is sitting near the house.'
```
*Notes: `tuja` follows the noun as adjective; `guapy` = active verb 'sit'.*

---

## 8. Relational Verbs (Critical for Common Vocabulary)

Several of the most common verbs are relational: their root begins with a consonant that changes based on person prefix. Active prefixes trigger `h-` on the root; inactive prefixes trigger `r-`; the absolute/nominal form uses `t-`.

| Relational Verb | Example Forms |
|----------------|---------------|
| `-echa` 'to see' | `a-h-echa ichupe` 'I see him'; `nde che-r-echa` 'you see me' |
| `-endu` 'to hear' | `a-h-endu` 'I hear it'; `che-r-endu` 'I am heard' |
| `-ayhu` 'to love' | `a-h-ayhu ichupe` 'I love him'; `che-r-ayhu` 'I am loved' |
| `-eka` 'to seek' | `a-h-eka` 'I seek it'; `che-r-eka` 'someone seeks me' |
| `-eja` 'to leave' | `a-h-eja` 'I leave it'; `t-eja` 'abandonment' (abs.) |
| `-enói` 'to call' | `ro-h-enói` 'I call you'; `che-r-enói` 'I am called' |

**Generation rule:** active subject + 3rd person object → `PERSON.ACT + h- + root` (e.g., `a-h-echa`). Patient marking → `PERSON.INACT + r- + root` (e.g., `che-r-echa`).

---

## 9. Common Pitfalls

- **Don't make subjects obligatory.** `Okaru hína.` 'S/he is eating.' is more natural than `Ha'e okaru hína.` Subject pronouns appear for contrast/focus only.

- **Don't ignore the active/inactive split.** Every intransitive verb must be stored with its class. Using `*ndeho` (inactive prefix for 'go') instead of `reho` is ungrammatical. States like 'be tired', 'be hungry', 'be beautiful' take inactive prefixes: `chekane'õ`, `chevare'a`, `cheporã`.

- **Don't omit relational prefixes.** When a noun like `-esa` 'eye', `-óga` 'house', `-ova` 'face', or a relational verb like `-echa` 'see' appears with a possessor or person prefix, the relational initial consonant is MANDATORY. `*cheesa` is wrong; correct form is `che-r-esa` 'my eye'.

- **Don't use `-ta` for future negation.** Future negative uses `-mo'ã`: `namba'apomo'ãi` 'I will not work' — NOT `*namba'apotai`.

- **Don't over-mark plural.** Plural is not obligatory. With numerals, demonstratives, or clear context, omit `=kuéra`. Overusing it sounds unnatural.

- **Watch nasal harmony on all affixes.** A nasal root like `mitã` requires `=nguéra` not `=kuéra`, `=me` not `=pe`, `n-` not `nd-` in negation. Failure to apply nasal harmony is one of the most detectable generation errors.

---

## 10. Irregular Verbs (High-Frequency)

| Verb | 1sg | 2sg | 3 |
|------|-----|-----|---|
| `ho` 'to go' | `aha` | `reho` | `oho` |
| `ju` 'to come' | `aju` | `reju` | `ou` |
| `'e` 'to say' | `ha'e` | `ere` | `he'i` |
| `'u` 'to eat/drink' (trans.) | `ha'u` | `re'u` | `ho'u` |
| `y'u` 'to drink water' | `hay'u` | `rey'u` | `hoy'u` |

---

*— End of Reference —*

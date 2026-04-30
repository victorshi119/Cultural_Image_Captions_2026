# Guaraní (gug) Captioning Pack

This file contains two artifacts intended to be fed to a vision-language model alongside images, to help it generate Guaraní captions:

1. A grammar primer covering the patterns attested in the source corpus.
2. An exemplar bank of corpus sentences that look like plausible image captions.

---

## Artifact 1 — Grammar primer

Guaraní (ISO: gug) is the Paraguayan variety of Guaraní. Words are mostly built by stringing prefixes and suffixes onto a root; an interlinear segmentation will typically show a person prefix, a root, and one or more aspect/mood/postposition suffixes. What follows describes only the patterns visibly attested in the accompanying corpus.

### Person marking on verbs: active vs. inactive

Guaraní verbs and predicative nouns/adjectives take one of two sets of person prefixes. The active set marks the subject of agentive verbs and most actions. The inactive set marks the subject of stative predicates ("be tired," "be tall," "be hungry"), the possessor of body parts and kin, and the patient/object of a transitive verb when the subject is third person.

Active prefixes: `a-` 1sg, `re-` 2sg, `o-` 3, `ja-` / `ña-` 1pl.incl, `ro-` 1pl.excl, `pe-` 2pl. Plural third person is usually `o-...` plus the free pronoun `hikuái` "they" or the enclitic `=kuéra` on a noun. The 1pl.incl prefix is `ña-` before nasal stems, `ja-` elsewhere.

- `aguata` — `a-guata` — 1sg.act-walk — "I walk / walked"
- `reho` — `re-ho` — 2sg.act-go — "you (sg.) go / went"
- `opuka` — `o-puka` — 3.act-laugh — "s/he laughs / laughed"
- `jakaru` — `ja-karu` — 1pl.incl.act-eat — "we (and you) eat"
- `rokaru` — `ro-karu` — 1pl.excl.act-eat — "we (not you) eat"
- `peguata peína` — `pe-guata pe-ína` — 2pl.act-walk 2pl.act-prog — "you (pl.) are walking"
- `ofarrea hikuái` — `o-farrea hikuái` — 3.act-party they — "they party / partied"

Inactive prefixes: `che-` 1sg, `nde-` / `ne-` 2sg, `i-` / `h-` / `iñ-` 3, `ñande-` / `ñane-` 1pl.incl, `ore-` 1pl.excl, `pende-` / `pene-` 2pl. The third-person inactive surfaces as `h-` on certain "biform" nouns (see Possession), as `iñ-` before a nasal stem, and as plain `i-` elsewhere.

- `chevare'a` — `che-vare'a` — 1sg.inact-hunger — "I am hungry"
- `ndekatupyry` — `nde-katupyry` — 2sg.inact-efficient — "you (sg.) are skilful"
- `ipochy` — `i-pochy` — 3.inact-anger — "s/he is angry"
- `iporã` — `i-porã` — 3.inact-beautiful — "s/he/it is pretty"
- `iñakã` — `iñ-akã` — 3.inact-head — "his/her head"
- `ñanerasẽ` — `ñane-r-asẽ` — 1pl.incl.inact-cry — "we (and you) cry"
- `oreare` — `ore-are` — 1pl.excl.inact-late — "we (not you) are late"
- `pendeyvate` — `pende-yvate` — 2pl.inact-tall — "you (pl.) are tall"

The same inactive prefixes mark the patient of a transitive verb when the subject is third person:

- `chenupã ha'e` — `che-nupã ha'e` — 1sg.inact-hit s/he — "s/he hit me"
- `oresy orenupã` — `ore-sy ore-nupã` — 1pl.excl.inact-mother 1pl.excl.inact-beat — "our mother beats us"

When a 1st person acts on a 2nd person, special portmanteau prefixes are used: `ro-` (1 → 2sg) and `po-` (1 → 2pl):

- `rohayhu` — `ro-h-ayhu` — 1>2sg-love — "I/we love you (sg.)"
- `pohayhu` — `po-h-ayhu` — 1>2pl-love — "I/we love you (pl.)"

### Tense, aspect, mood suffixes

Guaraní does not obligatorily mark past or present; bare verbs are read from context. Several stressed and unstressed suffixes add temporal or modal information.

- `-ta` future. `osẽta` — `o-sẽ-ta` — 3.act-go.out-fut — "s/he will go out"
- `-va'ekue` distant/definite past. `Ahava'ekue la Chákope.` — `a-ha-va'ekue la Cháko=pe` — 1sg.act-go-past det.sg Chaco=in — "I went to the Chaco."
- `-kue` / `-ngue` post-stative ("ex-", "former"). `cherogakue` — `che-r-óga-kue` — 1sg.inact-possm-house-post — "my former house"
- `-rã` destinative ("future-thing", "to-be"). `cherogarã` — `che-r-óga-rã` — 1sg.inact-possm-house-dest — "my future house"
- `-va'erã` deontic / "must, have to". `Rejuva'erã cherógape.` — `re-ju-va'erã che-r-óga=pe` — 2sg.act-come-must 1sg.inact-possm-house=in — "You must come to my house."
- `-ma` "already" (completive). `aháma` — `a-ha-ma` — 1sg.act-go-already — "I have gone already"; `ogũahẽma` — `o-gũahẽ-ma` — 3.act-arrive-already — "s/he has already arrived"
- `-mi` habitual / "used to". `Py'ỹi ahami penderógape.` — `py'ỹi a-ha-mi pende-r-óga=pe` — often 1sg.act-go-used.to 2pl.inact-possm-house=in — "I used to go to your house often."
- `-se` "want". `ahase` — `a-ha-se` — 1sg.act-go-want — "I want to go"
- `hína` (free word) progressive. `rehai hína` — `re-h-ai hína` — 2sg.act-write prog — "you are writing"
- `t-` (with active prefix) optative / hortative. `tamba'apo` — `t-a-mba'apo` — opt-1sg.act-work — "let me work"; `topurahéi` — `t-o-purahéi` — opt-3.act-sing — "may s/he sing"
- `e-` 2sg imperative. `Eju ko'ãga!` — `e-ju ko'ãga` — imp-come now — "Come now!"
- `-pa` totalitive ("all"). `Tahyikuéra omanomba.` — `tahýi=kuéra o-mano-mba` — ant=pl 3.act-die-all — "The ants all died."

### Postpositions

Most case-like relations are encoded by enclitics or particles after the noun. Stress falls on the postposition itself for the stressed ones.

- `=pe` / `=me` "in, on, at, to". `Aiko Paraguáipe` — `a-iko Paraguái=pe` — 1sg.act-be Paraguay=in — "I live in Paraguay." Also marks human direct objects: `aikuaa amo kuñáme` — `ai-kuaa amo kuña=me` — 1sg.act-know dist.sg woman=in — "I know that woman."
- `=gui` "from, out of, because of". `Aha Luquegui` — `a-ha Luque=gui` — 1sg.act-go Luque=from — "I go from Luque."
- `=rehe` / `=re` "at, about, with (instrument)" and the oblique object of certain verbs. `chemandu'áta nderehe` — `che-mandu'a-ta nde=rehe` — 1sg.inact-remember-fut 2sg.inact=at — "I will remember you."
- `=guarã` "for, intended for". `Ajapo chesýpeguarã.` — `a-japo che-sy=pe=guarã` — 1sg.act-make 1sg.inact-mother=in=for — "I made (it) for my mother."
- `=ndive` / `=ndi` comitative "with". `Eho Peru jarýindive.` — `e-ho Peru jarýi=ndive` — imp-go Peru grandmother=with — "Go with Pedro's grandmother."
- `=gua` / `=ygua` provenance "from, of". `Che paraguáigua.` — `che paraguái=gua` — I Paraguay=from — "I am from Paraguay."
- `=icha` "like, as". `yvotyicha` — `yvoty-icha` — flower-as — "like a flower." `Nde sy iporã yvotyicha.` — `nde-sy i-porã yvoty-icha` — 2sg.inact-mother 3.inact-beautiful flower-as — "Your mother is beautiful like a flower."

Other useful postpositions in the corpus include `=ári` "upon, on top of," `=guy` / `=guýpe` "below, under," `jerére` "around," `rendápe` "next to," and `-vo` "while."

### Negation: `nd(a)-…-i` and variants

Negation of a finite verb is a circumfix: `nd(a)-` (or `n-` before a nasal vowel) at the front and `-i` at the end. Allomorphs of the front element include `nda-`, `nde-`, `ndo-`, `ne-`, `na-`, `n-`. The future negation replaces `-i` with `-mo'ã-i`. The imperative negation is `ani` plus the verb (with optional `-tei`).

- `ndaguatasevéi` — `nd-a-guata-se-ve-i` — neg-1sg.act-walk-want-more-neg — "I don't want to walk more"
- `ndajapói` — `nd-a-japo-i` — neg-1sg.act-make-neg — "I didn't do it"
- `ndaikuaái` — `nd-ai-kuaa-i` — neg-1sg.act-know-neg — "I don't know"
- `nasẽi` — `n-a-sẽ-i` — neg-1sg.act-go.out-neg — "I don't go out"
- `ndachepochýi` — `nda-che-pochy-i` — neg-1sg.inact-anger-neg — "I am not angry"
- `namba'apomo'ãi` — `n-a-mba'apo-mo'ã-i` — neg-1sg.act-work-neg.fut-neg — "I will not work"
- `ani reho` — `ani re-ho` — neg.imp 2sg.act-go — "do not go"

### Possession

Pronominal possession on a noun uses the inactive prefix series. A subset of "biform" relational nouns insert an `r-` "possessm" before the root when they have a 1st/2nd person possessor, and use `h-` for the 3rd person possessor. Without any possessor at all, the root takes the prefix `t-` (npossm).

- `cheróga` — `che-r-óga` — 1sg.inact-possm-house — "my house"
- `nderóga` — `nde-r-óga` — 2sg.inact-possm-house — "your house"
- `hóga` — `h-óga` — possm3-house — "his/her house"
- `ñanderetã` — `ñande-r-etã` — 1pl.incl.inact-possm-country — "our country"
- `cheru` — `che-r-u` — 1sg.inact-possm-father — "my father"
- `itúva` — `i-t-úva` — 3.inact-npossm-father — "his/her father"

For ordinary (non-biform) nouns, the prefix attaches directly: `ipo` "his hand" (`i-po`), `ijao` "his clothes" (`ij-ao`), `iñakã` "his head" (`iñ-akã`), `imbarakaja` "his cat" (`i-mbarakaja`).

Possession by a full noun phrase is by simple juxtaposition, possessor before possessed: `María ajaka` — María basket — "María's basket"; `vaka ro'o` — `vaka r-o'o` — cow possm-flesh — "cow's meat."

### Noun incorporation and compounding

Two roots can be compounded directly. A frequent pattern incorporates a body-part noun into the verb to derive a lexicalized predicate (often glossed in the corpus with `+`). The whole compound takes a single set of prefixes, and the incorporated noun is no longer a free direct object.

- `ojurumboty` — `o-juru+mboty` — 3.act-mouth+close — "s/he closes his/her mouth"
- `ojepohéi` — `o-je-po+héi` — 3.act-agd-hand+wash — "s/he washes his/her hands"
- `ohovapete chupe` — `o-h-ova+pete chupe` — 3.act-possm3-face+slap to.him — "they slapped him in the face"
- `ipy'aguapy` — `i-py'a+guapy` — 3.inact-chest+sit — "s/he is at peace"
- `kuãirũ` — `kuã+irũ` — finger+friend — "ring"
- `pirapire` — `pira+pire` — fish+leather — "money"
- `mitãrusu` — `mitã+rusu` — child+grown — "adolescent"
- `mitãporã` — `mitã+porã` — child+beautiful — "pretty child"

A non-incorporated equivalent uses the body-part noun as a separate possessed object: `omboty ijuru` — `o-mboty i-juru` — 3.act-close 3.inact-mouth — "s/he closes his/her mouth." The incorporated form (`ojurumboty`) is more idiomatic; the periphrastic form is less common.

### Copular, existential, equative

Guaraní typically has no overt copula. A predicative property is expressed by giving the property word an inactive person prefix.

- `Che tuicha.` — `che tuicha` — I big — "I am big."
- `Nde ndetuja.` — `nde nde-tuja` — you 2sg.inact-old — "You are old."
- `Kuña imbarete.` — `kuña i-mbarete` — woman 3.inact-strong — "The woman is strong."
- `Pe karia'y hekomirĩ.` — `pe karia'y h-eko+mirĩ` — that young.man 3.inact-essence+small — "This young man is modest."

Equative clauses (X is Y) are a simple juxtaposition of two noun phrases:

- `Ndesy mbo'ehára.` — `nde-sy mbo'e-hára` — 2sg.inact-mother teach-nmlz.ag — "Your mother is a teacher."

Existential "there is / are" uses the verb `oĩ` (and its negative `ndaipóri`):

- `Oĩ heta mba'asy.` — `oĩ h-eta mba'+asy` — there.is possm3-numerous thing+pain — "There are many illnesses."
- `Ndaipóri va'ekue ñu.` — `ndaipóri va'ekue ñu` — there.is.not past field — "There were no fields."

Possession ("have") is expressed either with the verb `-guereko` "have" or with an inactive-prefixed body-part / kinship noun:

- `Itúva ha isy oguereko peteĩ jagua'i.` — `i-túva ha i-sy o-guereko peteĩ jagua-'i` — 3.inact-father and 3.inact-mother 3.act-have one dog-dim — "His father and his mother have a little dog."
- `Panambi ipepo.` — `panambi i-pepo` — butterfly 3.inact-wing — "Butterflies have wings."

### Word order

Verb-final and verb-medial orders are both attested, and word order is fairly free, but an unmarked declarative tends to put the subject before the verb when the subject is a full lexical NP, and to drop pronominal subjects altogether when they are recoverable from the prefix. Topical nouns and demonstratives commonly come first. Possessor precedes possessed, modifier (adjective, demonstrative) usually follows the noun. Examples:

- `Cheru ohayhu chesýpe.` — S V O.
- `Kuarahy overa ko'ãga.` — S V Adv.
- `Pe karai ome'ẽ so'o itajýrape.` — S V O IO.

---

## Artifact 2 — Exemplar bank

Selected entries from the corpus that look like plausible image captions: declarative sentences with a clear subject and a concrete predicate, describing actions, states, or locations. Grouped loosely by scene type.

### People acting on objects / on others

```
GUARANÍ: Cheru ohayhu chesýpe.
GLOSS:   che-r-u o-h-ayhu che-sy=pe | 1SG.INACT-POSSM-father 3.ACT-POSSM3-love 1SG.INACT-mother=in
ENGLISH: My father loves my mother.
```

```
GUARANÍ: Pe karai ome'ẽ so'o itajýrape.
GLOSS:   pe karai o-me'ẽ so'o i-tajýra=pe | MED.SG gentleman 3.ACT-give meat 3.INACT-daughter.of.man=in
ENGLISH: That gentleman gives meat to his daughter.
```

```
GUARANÍ: Itúva ha isy oguereko peteĩ jagua'i.
GLOSS:   i-túva ha i-sy o-guereko peteĩ jagua-'i | 3.INACT-father and 3.INACT-mother 3.ACT-have one dog-DIM
ENGLISH: His father and his mother have a little dog.
```

```
GUARANÍ: Cheru oguereko mbohapy kavaju.
GLOSS:   che-r-u o-guereko mbohapy kavaju | 1SG.INACT-POSSM-father 3.ACT-have three horse
ENGLISH: My father has three horses.
```

```
GUARANÍ: Kola akói oinupã imbarakaja.
GLOSS:   Kola akói oi-nupã i-mbarakaja | Kola always 3.ACT-beat 3.INACT-cat
ENGLISH: Kola always punishes his cat.
```

```
GUARANÍ: Oresy orenupã.
GLOSS:   ore-sy ore-nupã | 1PL.EXCL.INACT-mother 1PL.EXCL.INACT-beat
ENGLISH: Our mother beats us.
```

```
GUARANÍ: Ainupã ichupe.
GLOSS:   ai-nupã ichupe | 1SG.ACT-beat to.him/her
ENGLISH: I beat him/her.
```

```
GUARANÍ: Aipytyvõ ichupe.
GLOSS:   ai-pytyvõ ichupe | 1SG.ACT-help to.him/her
ENGLISH: I help him/her.
```

```
GUARANÍ: Agueru pakova.
GLOSS:   a-gueru pakova | 1SG.ACT-bring banana
ENGLISH: I bring bananas.
```

```
GUARANÍ: Agueru ndéve yva.
GLOSS:   a-gueru ndéve yva | 1SG.ACT-bring to.you.SG fruit
ENGLISH: I bring you fruit.
```

```
GUARANÍ: Ame'ẽ ko ryguasu ndéve.
GLOSS:   a-me'ẽ ko ryguasu ndéve | 1SG.ACT-give PROX.SG hen to.you.SG
ENGLISH: I gave you this hen.
```

```
GUARANÍ: Ahai ko kuatia ndéve.
GLOSS:   a-h-ai ko kuatia ndéve | 1SG.ACT-POSSM3-write PROX.SG text to.you.SG
ENGLISH: I wrote you this letter.
```

```
GUARANÍ: Ojapo la chupekuéra ogustávante.
GLOSS:   o-japo la chupe=kuéra o-gusta-va-nte | 3.ACT-make DET.SG to.him/her=PL 3.ACT-please-ADJZ-only
ENGLISH: They do only what pleases them.
```

```
GUARANÍ: Guaranikuéra omba'ejuka ha oipirakutu.
GLOSS:   guarani=kuéra o-mba'e-juka ha oi-pira+kutu | Guarani=PL 3.ACT-THING-kill and 3.ACT-fish-pierce
ENGLISH: The Guarani hunted (animals) and fished.
```

```
GUARANÍ: Avakuéra opirakutu opaichagua pira.
GLOSS:   ava=kuéra o-pira+kutu opa-icha=gua pira | person=PL 3.ACT-fish+pierce all-as=from fish
ENGLISH: People fish all sorts of fish.
```

```
GUARANÍ: Cheru ojukapáta tahyikuéra.
GLOSS:   che-r-u o-juka-pa-ta tahýi=kuéra | 1SG.INACT-POSSM-father 3.ACT-kill-all-FUT ant=PL
ENGLISH: My father will kill all the ants.
```

```
GUARANÍ: Ko'ãga remongarúta nerymba guéi.
GLOSS:   ko'ãga re-mo-ngaru-ta ne-r-ymba guéi | now 2SG.ACT-MAKE1-eat-FUT 2SG.INACT-POSSM-animal ox
ENGLISH: Now you will feed your ox.
```

```
GUARANÍ: Namboguata ñandejagua.
GLOSS:   ña-mbo-guata ñande-jagua | 1PL.INCL.ACT-MAKE1-walk 1PL.INCL.INACT-dog
ENGLISH: We make our dog walk.
```

### Motion and location

```
GUARANÍ: Aha Luquegui Paraguaýpe.
GLOSS:   a-ha Luque=gui Paraguay=pe | 1SG.ACT-go Luque=from Asunción=in
ENGLISH: I go from Luque to Asunción.
```

```
GUARANÍ: Aháma kuehe pe mbo'ehaópe.
GLOSS:   a-ha-ma kuehe pe mbo'ehao=pe | 1SG.ACT-go-already yesterday MED.SG school=in
ENGLISH: I already went to school yesterday.
```

```
GUARANÍ: Jaháta ñandetávagotyo kavaju'ári.
GLOSS:   ja-ha-ta ñande-táva=gotyo kavaju='ári | 1PL.INCL.ACT-go-FUT 1PL.INCL.INACT-town=towards horse=upon
ENGLISH: We will go towards our town on horses.
```

```
GUARANÍ: Luisa térã José ohóta ñemuhame.
GLOSS:   Luisa térã José o-ho-ta ñemu-ha=me | Luisa or Jose 3.ACT-go-FUT trade-NMLZ.LOC=in
ENGLISH: Luisa or José will go to the store.
```

```
GUARANÍ: Upe ára, ou peteĩ kuimba'e.
GLOSS:   upe ára o-u peteĩ kuimba'e | MED.SG day 3.ACT-come one man
ENGLISH: That day, a man came.
```

```
GUARANÍ: Chavuku ou jey yvýpe.
GLOSS:   Chavuku o-u jevy yvy=pe | Chavuku 3.ACT-come again earth=in
ENGLISH: Chavuku returned to Earth.
```

```
GUARANÍ: Ha'a yvýpe.
GLOSS:   ha-'a yvy=pe | 1SG.ACT-fall earth=in
ENGLISH: I fell to the earth.
```

```
GUARANÍ: Ko che irũ oike ka'aguy marã'ỹme.
GLOSS:   ko che-irũ o-ike ka'aguy marã-'ỹ=me | PROX.SG 1SG.INACT-friend 3.ACT-enter forest spotless=in
ENGLISH: This friend of mine is entering into the virgin forest.
```

```
GUARANÍ: Mokõi mokõi tapicha oikekuri pýpe.
GLOSS:   mokõi mokõi t-apicha o-ike-kuri pýpe | two two NPOSSM-fellow.man 3.ACT-enter-DIR.PAST inside
ENGLISH: People entered inside in twos.
```

```
GUARANÍ: Peiko kokuépe.
GLOSS:   pe-iko kokue=pe | 2PL.ACT-be countryside=in
ENGLISH: You live in the countryside.
```

```
GUARANÍ: Che ndaikói gueteri Paraguáipe.
GLOSS:   che nd-a-iko-i gueteri Paraguái=pe | I NEG-1SG.ACT-be-NEG still Paraguay=in
ENGLISH: I don't live in Paraguay yet.
```

### States and descriptions

```
GUARANÍ: Kuarahy overa ko'ãga.
GLOSS:   kuarahy o-vera ko'ãga | sun 3.ACT-shine now
ENGLISH: The sun is shining now.
```

```
GUARANÍ: Kuarahy overa asy.
GLOSS:   kuarahy o-vera asy | sun 3.ACT-shine pain
ENGLISH: The sun shines intensely.
```

```
GUARANÍ: Kuña imbarete.
GLOSS:   kuña i-mbarete | woman 3.INACT-strong
ENGLISH: The woman is strong.
```

```
GUARANÍ: Kuña ikatupyry.
GLOSS:   kuña i-katupyry | woman 3.INACT-skilful
ENGLISH: Women are skilful.
```

```
GUARANÍ: Nde sy iporã yvotyicha.
GLOSS:   nde-sy i-porã yvoty-icha | 2SG.INACT-mother 3.INACT-beautiful flower-as
ENGLISH: Your mother is beautiful like a flower.
```

```
GUARANÍ: Ndetía iporã.
GLOSS:   nde-tía i-porã | 2SG.INACT-aunt 3.INACT-beautiful
ENGLISH: Your aunt is pretty.
```

```
GUARANÍ: Pe karia'y hekomirĩ.
GLOSS:   pe karia'y h-eko+mirĩ | MED.SG young.man POSSM3-essence+small
ENGLISH: This young man is modest.
```

```
GUARANÍ: Susana membykuéra ikyra meme.
GLOSS:   Susana memby=kuéra i-kyra meme | Susana child=PL 3.INACT-fat continuously
ENGLISH: Susana's children are all fat.
```

```
GUARANÍ: Ivevúi asy pe kambuchi.
GLOSS:   i-vevúi asy pe kambuchi | 3.INACT-lightweight pain MED.SG clay.jug
ENGLISH: This jug is delicate.
```

```
GUARANÍ: Yvágaicha iporã yvy marae'ỹ.
GLOSS:   yvága-icha i-porã yvy marae'ỹ | sky-as 3.INACT-beautiful earth spotless
ENGLISH: The land without evil was beautiful like the sky.
```

```
GUARANÍ: Amo yvyra yvate cherógaicha.
GLOSS:   amo yvyra yvate che-r-óga-icha | DIST.SG tree tall 1SG.INACT-POSSM-house-as
ENGLISH: That tree over there is as tall as my house.
```

```
GUARANÍ: Tahyikuéra omanomba.
GLOSS:   tahýi=kuéra o-mano-mba | ant=PL 3.ACT-die-all
ENGLISH: The ants all died.
```

```
GUARANÍ: Ipu jeýma.
GLOSS:   i-pu jevy-ma | 3.INACT-sound again-already
ENGLISH: It sounds again already.
```

```
GUARANÍ: Edelio oikove gueteri.
GLOSS:   Edelio o-iko-ve gueteri | Edelio 3.ACT-be-more still
ENGLISH: Edelio is still alive.
```

```
GUARANÍ: Cheirũ omanombota hína.
GLOSS:   che-irũ o-mano-mbota hína | 1SG.INACT-friend 3.ACT-die-about.to PROG
ENGLISH: My friend is about to die.
```

### Possession and existence

```
GUARANÍ: Panambi ipepo.
GLOSS:   panambi i-pepo | butterfly 3.INACT-wing
ENGLISH: Butterflies have wings.
```

```
GUARANÍ: Aguereko irundy ary.
GLOSS:   a-guereko irundy ary | 1SG.ACT-have four year
ENGLISH: I am four years old.
```

```
GUARANÍ: Aguereko 28 ary ha mokõi che memby.
GLOSS:   a-guereko 28 ary ha mokõi che-memby | 1SG.ACT-have 28 year and two 1SG.INACT-child
ENGLISH: I am 28 years old and I have two children.
```

```
GUARANÍ: Hetave mba'asy oĩ añete.
GLOSS:   h-eta-ve mba'+asy oĩ añete | POSSM3-numerous-more thing+pain there.is true
ENGLISH: There are in truth many more illnesses.
```

```
GUARANÍ: Añorairõ tymba ñarõndive.
GLOSS:   a-ño-rairõ t-ymba ñarõ=ndive | 1SG.ACT-RECP-attack NPOSSM-animal wild=with
ENGLISH: I fight with wild animals.
```

```
GUARANÍ: Mokõi kuña ikatu oñohetũ.
GLOSS:   mokõi kuña ikatu o-ño-h-etũ | two woman be.able 3.ACT-RECP-POSSM3-kiss
ENGLISH: Two women can kiss one another.
```

```
GUARANÍ: Roikotevẽ pirapire.
GLOSS:   roi-kotevẽ pira+pire | 1PL.EXCL.ACT-need fish+leather
ENGLISH: We need money.
```

```
GUARANÍ: Pe mbarakaja oikotevẽ tembi'u.
GLOSS:   pe mbarakaja oi-kotevẽ t-embi-'u | MED.SG cat 3.ACT-need NPOSSM-NMLZ.REL-ingest
ENGLISH: That cat needs food.
```

### Plural participants and groups

```
GUARANÍ: Ofarrea hikuái.
GLOSS:   o-farrea hikuái | 3.ACT-party they
ENGLISH: They party.
```

```
GUARANÍ: Oikuaa hikuái.
GLOSS:   oi-kuaa hikuái | 3.ACT-know they
ENGLISH: They know.
```

```
GUARANÍ: Ojuhu hikuái juky iñasãiva hóga jerére.
GLOSS:   o-juhu hikuái juky iñ-asãi-va h-óga jerére | 3.ACT-find they salt 3.INACT-extended-ADJZ POSSM3-house around
ENGLISH: They found salt that spread all around their houses.
```

```
GUARANÍ: Oñangareko hikuái nderógare.
GLOSS:   o-ñangareko hikuái nde-r-óga=re | 3.ACT-take.care.of they 2SG.INACT-POSSM-house=at
ENGLISH: They take care of your house.
```

```
GUARANÍ: Oñorairõ hikuái oimeraẽ mba'erehe.
GLOSS:   o-ño-rairõ hikuái oimeraẽ mba'e=rehe | 3.ACT-RECP-attack they any thing=because
ENGLISH: They fought for any reason.
```

```
GUARANÍ: Ou la arriéro ha ovy'apa lo kuña.
GLOSS:   o-u la arriéro ha o-vy'a-pa lo kuña | 3.ACT-come DET.SG peasant and 3.ACT-joy-all DET.PL woman
ENGLISH: The man came and the women were all happy.
```

```
GUARANÍ: Ohopa hikuái.
GLOSS:   o-ho-pa hikuái | 3.ACT-go-all they
ENGLISH: They all went.
```

```
GUARANÍ: Okarujoa hikuái.
GLOSS:   o-karu-joa hikuái | 3.ACT-eat-all they
ENGLISH: They are all eating.
```

```
GUARANÍ: Ha'ekuéra hoy'u mbohapy kagua peteĩteĩ.
GLOSS:   ha'e=kuéra ho-y+'u mbohapy kagua peteĩ~teĩ | s/he=PL 3.ACT-water+ingest three glass one~one
ENGLISH: They drank three glasses each.
```

```
GUARANÍ: Oñe'ẽ voi isýicha.
GLOSS:   o-ñe'ẽ voi i-sy-icha | 3.ACT-speak EMPH 3.INACT-mother-as
ENGLISH: S/he talks like his/her mother.
```

```
GUARANÍ: Mitãkuéra okakuaapa vove, ovevepa.
GLOSS:   mitã=kuéra o-kakuaa-pa vove o-veve-pa | child=PL 3.ACT-grow.up-all during 3.ACT-fly-all
ENGLISH: As soon as they are all grown up, children all fly.
```

### Body actions and routines

```
GUARANÍ: Ojurumboty.
GLOSS:   o-juru+mboty | 3.ACT-mouth+close
ENGLISH: S/he closes his/her mouth.
```

```
GUARANÍ: Omboty ijuru.
GLOSS:   o-mboty i-juru | 3.ACT-close 3.INACT-mouth
ENGLISH: S/he closes his/her mouth.
```

```
GUARANÍ: Ajepohéita.
GLOSS:   a-je-po+héi-ta | 1SG.ACT-AGD-hand+wash-FUT
ENGLISH: I will wash my hands.
```

```
GUARANÍ: Ahechangy.
GLOSS:   a-h-echa-ngy | 1SG.ACT-POSSM3-see-ATT
ENGLISH: I glimpse it.
```

```
GUARANÍ: Apu'ã jepi voiete.
GLOSS:   a-pu'ã jepi voi-ete | 1SG.ACT-get.up usually early-very
ENGLISH: I usually get up very early.
```

```
GUARANÍ: Che apuka.
GLOSS:   che a-puka | I 1SG.ACT-laugh
ENGLISH: I laugh.
```

```
GUARANÍ: Jasy opurahéi chéve ha che apurahéi ndéve.
GLOSS:   jasy o-purahéi chéve ha che a-purahéi ndéve | moon 3.ACT-sing to.me and I 1SG.ACT-sing to.you.SG
ENGLISH: The moon sings to me and I sing to you.
```

```
GUARANÍ: Reñe'ẽ heta.
GLOSS:   re-ñe'ẽ h-eta | 2SG.ACT-talk POSSM3-numerous
ENGLISH: You talk a lot.
```

```
GUARANÍ: Oha'arõ tapiaite imembykuérape.
GLOSS:   o-h-a'arõ tapia-ite i-memby=kuéra=pe | 3.ACT-POSSM3-wait always-very 3.INACT-child=PL=in
ENGLISH: She always waited for her children.
```

```
GUARANÍ: Ahecháma ichupe.
GLOSS:   a-h-echa-ma ichupe | 1SG.ACT-POSSM3-see-already to.him/her
ENGLISH: I already saw him/her.
```

```
GUARANÍ: Opuka ha oñembohorýnte ha'e.
GLOSS:   o-puka ha o-ñe-mbo-h-ory-nte ha'e | 3.ACT-laugh and 3.ACT-AGD-MAKE1-POSSM3-joy-only s/he
ENGLISH: S/he laughed and just enjoyed himself/herself.
```

```
GUARANÍ: Panambi oñeha'ã oñemomombyry.
GLOSS:   panambi o-ñe-h-a'ã o-ñe-mo-mombyry | butterfly 3.ACT-AGD-POSSM3-attempt 3.ACT-AGD-MAKE1-far
ENGLISH: The butterfly tried to move away.
```

```
GUARANÍ: Ovevejoa hembi'u rekávo.
GLOSS:   o-veve-joa h-embi-'u r-eka-vo | 3.ACT-fly-all POSSM3-NMLZ.REL-ingest POSSM-seek-while
ENGLISH: They all flew together looking for their food.
```

"""
Code-format grammar rules for Paraguayan Guaraní.
Auto-generated from grammar_guarani_proc_filt.md.
"""

# === ### 3.1 Nouns ===
def nouns_identify_by_morphosyntactic_behavior():
    """
    Identifies Guarani nouns based on morphosyntactic criteria: they can appear with plural/enclitics, nominal tense markers, possessive markers, postpositional complements, or the verb-forming suffix -'o.
    """
    def is_noun(root):
        # 1. Can take plural enclitic =kuéra or multitudinal =ita
        if root + "=kuéra" or root + "=ita":
            return True
        # 2. Can take nominal tense/aspect markers -kue or -rã
        if root + "kue" or root + "rã":
            return True
        # 3. Can take inactive personal markers for possession (e.g., che-, je-, etc.)
        if "che" + root or "je" + root or "ha" + root:
            return True
        # 4. Can function as head in postpositional complement (e.g., root + postposition)
        if root + "guasúpe" or root + "mbo'ehá" or root + "porã":
            return True
        # 5. Can take derivational suffix -'o to form verbs
        if root + "'o":
            return True
        return False

    # Example noun usage:
    # koty = 'room' → kotykuéra = 'rooms', kotykue = 'former room'
    # mena = 'husband' → menarã = 'future husband, boyfriend'
    # pire = 'skin' → pire'o = 'to skin'
    return is_noun

# === ### 3.1.1 Plural marking ===
def mark_plural_enclitic(noun, has_nasal_vowel=False, is_countable=True, has_numeral=False):
    """
    Applies plural enclitics =kuéra/=nguéra or =eta/=ita to countable nouns based on noun type and context.
    Plural marking is optional and favored for animate nouns or when plurality is salient.
    """
    # Skip plural marking if numeral or determiner already indicates plurality (though optional usage may override)
    if has_numeral:
        return noun  # numeral already marks quantity

    # Determine appropriate plural enclitic
    if noun[-1] in 'ãẽĩõũ':  # nasal vowel ending
        plural_suffix = '=nguéra' if has_nasal_vowel else '=kuéra'
    else:
        plural_suffix = '=kuéra'

    # For substantial/multitudinal plurality (esp. for countable nouns)
    if not is_countable or (is_countable and not has_nasal_vowel and noun[-1] in 'aeiouAEIOU'):
        # Use multitudinal suffixes =eta or =ita (simplified rule)
        if noun[-1] in 'ĩõū':  # closed vowel
            plural_suffix = '=eta'
        else:  # mid/open vowel
            plural_suffix = '=ita'

    # Animate nouns (people, animals) more likely to be plural-marked
    if noun in ['arai', 'mbyja', 'kuña', 'oremenarã']:
        return noun + plural_suffix
    elif not is_countable:
        # Inanimate/uncountable may still take =eta for 'many' sense
        return noun + '=eta'
    else:
        # Optional plural marking — often omitted unless salient
        return noun  # or optionally return noun + plural_suffix

# Examples:
# arai + =kuéra → arai=kuéra ('clouds')
# panambi + =eta → panambi=eta ('many butterflies')

# === ### 5.1 Postpositions marking a predicate's complements ===
def mark_direct_object_with_pe_me():
    """Marks human or personified animate direct objects with postposition =pe/=me; inanimate direct objects remain unmarked."""
    def apply_rule(obj_noun_phrase, verb_lemma):
        # Check if object is human or personified animate
        if obj_noun_phrase.is_human or obj_noun_phrase.is_personified_animate:
            # Add =pe (after voice-less) or =me (after nasal) allomorph
            if verb_lemma.endswith(('a', 'e', 'i', 'o', 'u')):
                obj_noun_phrase += "=pe"
            else:  # after consonants, often nasal allomorph =me
                obj_noun_phrase += "=me"
        # Else: inanimate objects stay unmarked
        return obj_noun_phrase

    # Example: human direct object → marked
    # oha'arõ tapiaite imembykuérape → 'She always waited for her children.'
    # Example: inanimate direct object → unmarked
    # cheru ojukapáta tahyikuéra → 'My father will kill all the ants.'
    return apply_rule

# === ### 5.2 Postpositions of place ===
def postposition_of_place(base, pronoun=False, nasal=False):
    """
    Selects the correct spatial postposition (and allomorph) based on base type,
    personal pronoun inclusion, and nasal phonological environment.
    """
    # Normalize base: check if it ends in a non-high vowel
    non_high_vowels = {'a', 'e', 'o', 'i', 'u'}
    ends_non_high = base[-1] in non_high_vowels if base else False

    # Core selection logic
    if nasal:
        return 'ngotyo' if base == 'gotyo' else 'me' if base == 'pe' else 'meve' if base == 'peve' else base  # placeholder

    if pronoun:
        if base == 'gua': return 'ygua'
        if base == 'gui': return 'hegui'
        if base == 'pe': return 've'
        if base == 'rehe': return 'hese'  # third-person pronoun allomorph
        return base

    if base == 'gotyo': return 'ngotyo' if nasal else 'gotyo'
    if base == 'gua': return 'ygua'
    if base == 'gui': return 'gui'  # no nasal variant listed
    if base == 'guive': return 'guive'  # note: =ve variant applies to =pe-like use
    if base == 'jerére': return 'jerére'
    if base == 'pe': return 'me' if nasal else 'pe'
    if base == 'peve': return 'meve' if nasal else 'peve'
    if base == 'rehe': return 're'  # free variation, default to 're'
    if base == 'rovake': return 'rovake'
    if base == 'rupi': return 'rupi'
    if base == 'ári': return 'ári'

    return base  # fallback

# Examples:
# "ja-ha-ta ñande-táva=gotyo kavaju='ári" -> "We will go towards our town on horses."
# "o-juhu hikuái juky iñ-asãi-va h-óga jerére" -> "They found salt that spread all around their houses."

# === ### 5.3 Postpositions of time ===
def postpositions_of_time():
    """
    Postpositions of time in Guaraní follow the noun phrase they modify and indicate temporal relations (e.g., 'since', 'until', 'during', 'before', 'after').
    """
    def apply_time_postposition(np, postposition):
        # Postposition attaches after the NP (no agreement or mutation required)
        return f"{np} {postposition}"

    # Valid postpositions and their meanings
    time_postpositions = {
        "aja": "during", 
        "guive": "since", 
        "jave": "during", 
        "mboyve": "before", 
        "peve": "until", 
        "ramo": "when", 
        "rire": "after", 
        "vove": "during"
    }

    # Example usage (not executed in function):
    # apply_time_postposition("15 ary", "guive") → "15 ary guive"
    # apply_time_postposition("ka'aguy=re", "jave") → "ka'aguy=re jave"

    return time_postpositions, apply_time_postposition

# === ### 5.4 Other postpositions ===
def postposition_with_manner_or_cause(gui, icha, káusa, ndive, pe, pópe, ramo, rehe, rupi, rupive, without):
    """
    Selects and applies Guaraní postpositions to indicate manner, cause, accompaniment, or instrument,
    with allomorph variation and semantic restrictions where applicable.
    """
    # Allomorphs: ndive → n/di, ndie (free variation)
    # káusa is semantically restricted to negative causality; ramo can mean 'instead of' or 'if'
    # pe is used with nasal-initial bases (e.g., p=pe for 'with' instrument); rehe for instrumental 'with'
    # pópe for 'with' manner; rupi/rep for 'because'; rupive for 'by means of'
    
    # Example 1: comitative with ndive
    # Ejumína chendie → 'Please come with me.'
    # Example 2: manner with icha
    # Ndesy iporã yvotýicha → 'Your mother is beautiful like a flower.'
    
    if context == 'comitative':
        return ndive
    elif context == 'manner':
        return pópe
    elif context == 'cause_negative':
        return káusa
    elif context == 'instrument_nasal':
        return pe
    elif context == 'instrument_non_nasal':
        return rehe
    elif context == 'means':
        return rupive
    elif context == 'simile':
        return icha
    elif context == 'if':
        return ramo
    elif context == 'without':
        return without
    else:
        return None

# === ### 6.1 Active voice ===
def mark_active_voice_agent_or_subject(prefix_type, predicate_type, arguments):
    """
    Marks the active voice by attaching an active-set person prefix to the verb,
    for the S argument of intransitive predicates or the A argument of transitive predicates.
    Active voice is only used if the predicate is intransitive & active, or if the transitive patient is 3rd person.
    """
    if predicate_type == "intransitive":
        # Attach active prefix to verb for S argument
        verb_form = prefix_type + "_" + arguments["root"]
        return verb_form
    elif predicate_type == "transitive" and arguments.get("patient", "").startswith("3"):
        # Transitive predicate with 3rd person patient: prefix marks A (agent)
        verb_form = prefix_type + "_" + arguments["root"]
        return verb_form
    else:
        raise ValueError("Active voice not allowed for this predicate/argument configuration")

# Examples:
# a-guata → 'I walk(ed)'  (intransitive, 1SG.ACT → S)
# re-ñani → 'you (sg.) run/ran'  (intransitive, 2SG.ACT → S)
# pei-nupã ichupe → 'you (pl.) hit him/her'  (transitive, 2PL.ACT → A, P=3)
# ja-h-echa ichupe=kuéra → 'we see them'  (transitive, 1PL.INCL.ACT → A, P=3.PL)

# === ### 6.3 Passive/reflexive/impersonal voice ===
def agent_demoting_voice_je_ne():
    """
    Assigns je-/ñe- prefix to verbs to demote the agent, producing passive, reflexive, or impersonal readings.
    Prefix is added to verb stem; with intransitives it yields impersonal/generic meanings, with transitives it yields passive or reflexive depending on context.
    """
    def apply_voice_prefix(verb_stem, is_transitive):
        if verb_stem.startswith(('a', 'e', 'i', 'o', 'u')):
            prefix = 'je'
        else:
            prefix = 'ñe'
        
        if is_transitive:
            # passive (non-specified agent) or reflexive (agent = subject)
            return prefix + verb_stem
        else:
            # impersonal/generic (subject eliminated)
            return prefix + verb_stem
    
    # Example usage:
    # je- + mba’e → jemba’e ("Something is done", lit. "it is done")
    # ñe- + ha’á → ñeha’á ("He/She washes himself/herself" or "It washes itself")
    return apply_voice_prefix

# Note: Context (e.g., subject properties) resolves passive vs. reflexive for transitives.

# === ### 6.3.1 With intransitive verbs: generic and impersonal interpretations ===
def je_ne_impersonal_generic_intransitive(verb_root, verb_type="active"):
    """
    Forms impersonal/generic readings with intransitive verbs using je-/ñe- + o- prefix.
    The je-/ñe- prefix (AGD) combines with 3sg active prefix o-, yielding oje-/oñe-.
    Used with active intransitive verbs for generic/impersonal interpretations.
    """
    # Select je- or ñe- based on phonological context (simplified: use je- as default)
    prefix = "je" if verb_root[0] not in ["a", "e", "i", "o", "u"] else "ñe"
    
    # Add o- (3.ACT-SG) prefix before je-/ñe-
    stem = "o" + prefix + "-" + verb_root
    
    # Return morpheme segmentation and reading type
    return {
        "segmentation": f"o-{prefix}-{verb_root}",
        "meaning_type": "impersonal" if verb_type == "active" and "generic" not in verb_root else "generic",
        "example": f"{stem}-ne" if verb_type == "active" else stem
    }

# Examples:
# ojejeroky = o-je-jeroky → 'there is dancing'
# ojejapo = o-je-japo → 'one makes / it is made'

# === ### 6.3.2 With transitive verbs: passive and reflexive interpretations ===
def je_active_derives_passive_reflexive(verb_root, person_prefix):
    """
    Applies the je-/ñe- prefix to a transitive verb to derive passive or reflexive interpretations.
    The prefix demotes the agent (A), making the subject (S) either the patient (passive) or reflexive.
    Context resolves ambiguity; overt agents are not allowed in this construction.
    """
    # Determine je/ñe variant based on person prefix onset (simplified rule)
    if person_prefix.startswith('o') or person_prefix.startswith('a'):
        prefix = 'je'
    else:
        prefix = 'ñe'
    
    # Person prefix may lose final -i before je- (modern variation: i may attach to root)
    base_form = person_prefix.rstrip('i') + prefix + verb_root
    variant_with_i = person_prefix.rstrip('i') + prefix + 'i' + verb_root  # e.g., ojeipuru
    
    return [base_form, variant_with_i]


# Examples:
# je-japi → 'rejejapi' = 'you were shot' / 'you shot yourself'
# je-kytĩ → 'oñekytĩ' = 's/he was cut' / 's/he cut him/herself'

# === ### 6.4 Reciprocal voice ===
def reciprocal_voice(subject_plural: bool, verb_root: str) -> str:
    """
    Forms reciprocal verbs in Paraguayan Guaraní by adding the prefix jo-/ño- 
    to the verb root, requiring a plural subject; indicates mutual action.
    """
    if not subject_plural:
        raise ValueError("Reciprocal voice requires a plural subject.")
    
    # Palatalization: jo- → ño- after nasal-initial roots or certain phonotactic contexts
    reciprocal_prefix = "ño-" if verb_root.startswith(("n", "ñ", "m")) else "jo-"
    
    # Construct verb: subject prefix + reciprocal prefix + verb root + (optional) inflectional suffixes
    verb_form = f"{reciprocal_prefix}{verb_root}"
    return verb_form

# Examples (in morpheme gloss format):
# jajohayhu = ja-jo-h-ayhu ('we love each other')
# oñohetũ = o-ño-h-etũ ('they can kiss each other')

# === ### 6.5 Antipassive voice ===
def antipassive_voice_transitive():
    """
    Forms antipassive from transitive verbs by prefixing poro-/po- (for human object) or mba'e- (for non-human object), omitting the direct object while leaving the agent as subject; only applies to direct-object transitive verbs (not postpositional objects).
    """
    # Input: transitive verb stem (must not take postpositional object)
    # Output: antipassive verb form
    def apply_antipassive(verb_stem, obj_humanness):
        if obj_humanness == 'human':
            prefix = 'poro'
            # Alternate form: 'po-' allowed for some speakers
            if obj_humanness == 'human' and random.random() < 0.2:
                prefix = 'po'
            return f"{prefix}-{verb_stem}"
        elif obj_humanness == 'nonhuman':
            return f"mba'e-{verb_stem}"
        else:
            raise ValueError("obj_humanness must be 'human' or 'nonhuman'")
    
    # Example uses (as comments):
    # ro-poro-mbo'e  # 'we teach (people)'
    # pe-mba'e-jogua  # 'you buy (things)'
    
    return apply_antipassive

# === ### 6.6 Causative voice ===
def causative_verb_construction(verb_stem, voice_type, base_arity):
    """
    Constructs causative forms in Guaraní by adding a causer argument; voice_type determines argument structure.
    Intransitive causative/verbal sociative: base intransitive (1 arg) → transitive (2 args: causer + causee).
    Transitive causative: base transitive (2 args) → ditransitive (3 args: causer + causee + affectee).
    """
    # Determine suffix and new argument count based on voice type and base verb arity
    if base_arity == 1 and voice_type in ["intransitive_causative", "sociative_causative"]:
        causative_suffix = "-e"
        new_arity = 2  # causer + causee
    elif base_arity == 2 and voice_type == "transitive_causative":
        causative_suffix = "-a"
        new_arity = 3  # causer + causee + affectee
    else:
        raise ValueError("Invalid causative construction")

    # Form causative verb stem
    causative_verb = verb_stem + causative_suffix

    # Example: 'ha'e' (he/she runs) → 'ha'ere' (I make him/her run)
    # Example: 'mboy' (he/she hits it) → 'mboya' (I make him/her hit it [on me/for me])
    return causative_verb, new_arity

# === ### 6.6.1 Causative voice for intransitive verbs ===
def causative_intransitive_to_transitive(verb_root, causer_person, causee_person):
    """
    Converts an intransitive verb to a transitive causative by adding mbo-/mo- prefix.
    The causer is marked with an active person prefix; the causee becomes the direct object.
    """
    # Select causative prefix: 'mbo-' after active 1st/2nd person prefixes, 'mo-' otherwise
    if causer_person in ['1', '2']:
        causative_prefix = 'mbo'
    else:
        causative_prefix = 'mo'
    
    # Build causative verb: active causer prefix + causative morpheme + verb root
    verb_stem = f"{causative_prefix}-{verb_root}"
    
    # Return verb form with causer marked actively and causee marked as direct object
    return verb_stem

    # Example: 
    # a-mbo-puka ('I make him/her laugh') from a-puka ('I laugh')
    # a-mo-kane'õ maymáva=pe ('I make everybody tired') from che-kane'õ ('I am tired')

# === ### 6.6.2 Sociative causative ===
def sociative_causative_ro_guero():
    """
    Forms a sociative causative by prefixing ro- or guero- when the causer 
    participates in the action with the causee; often lexicalized with 
    psychological verbs, yielding non-compositional meanings.
    """
    # Choose prefix based on phonological context (ro- vs guero-; see §4.7)
    # Apply prefix to verb/nominal root
    # Gloss as MAKE.SOC; subject is causer, object is causee (optional)
    # Meaning is often idiomatic, especially for psych-verbs

    # ñamboguata ñandejagua → 'we make our dog walk' (non-sociative)
    # jagueroguata ñandejagua → 'we walk our dog' (sociative)
    # che roguerokyhyje chememby → 'I am afraid for you, my child.'
    # ha'e o(gue)rotũ isýpe → 'S/he is ashamed of his/her mother.'
    # oguerosapukái aty ñomongeta → 'They repudiate the meeting.'
    
    pass  # Rule is morphological + semantic; implementation requires lexicon

# === ### 6.6.3 Causative voice for transitive verbs ===
def apply_stressed_causative_suffix_uka(verb_root, active_prefix, direct_object_marking):
    """
    Applies the stressed causative suffix -uka (MAKE2) to transitive verbs to form ditransitive verbs.
    The causer (initiator) takes an active prefix, the affectee is marked as direct object, and the causee is an indirect object (often omitted).
    Suffix variants: -uka (after non-u verbs), -uka/-uka → -yka after other vowels; -uka → -ka after -u.
    """
    # Determine suffix variant based on verb root final vowel
    if verb_root.endswith('u'):
        suffix = 'ka'
    elif verb_root[-1] in 'aeiou':
        suffix = 'yka'
    else:
        suffix = 'uka'
    
    # Construct derived verb form
    derived_verb = verb_root + suffix
    
    # Return full verbal construction with arguments
    # Active prefix → verb → direct object marking (indirect object optional)
    return f"{active_prefix} {derived_verb} {direct_object_marking}"


# Example 1: pehechauka = pe- (2PL.ACT) + hecha (see) + -uka → 'you show'
# Example 2: ajapouka = a- (1SG.ACT) + japo + -uka → 'I have (something) made'

# === ### 7.1 Emphatic and veridical markers ===
def emphasize_with_voi_or_niko():
    """
    Adds emphatic/veridical emphasis via second-position clitics voi or variants of =niko (k o, ngo, ningo)
    to assert certainty, contrast hearer expectations, or affirm truth of statement.
    """
    # Select clitic: voi (emphatic) or =niko/k o/ngo/ningo (veridical emphatic)
    # Attach to first constituent (word or phrase) in the sentence as a clitic (affixed or enclitic)
    # voi: pure emphasis; niko/k o/ngo/ningo: emphasis + veridicality (speaker's affirmed knowledge)
    
    # Procedure:
    # 1. Identify first phrase (subject, verb, or verb phrase depending on clause type)
    # 2. Attach chosen clitic to its end (voi unbound; =niko variants often written =niko/k o/ngo/ningo)
    # 3. Gloss as EMPH or VERD accordingly
    
    # Examples:
    # i-porã voi → 'It is (certainly) beautiful.'
    # re-poko che=rehe ha'e niko ndéve → 'I did tell you not to touch me.'
    
    # Implementation logic (pseudocode):
    # if emphasis_type == 'voi': clitic = 'voi'
    # elif emphasis_type == 'veridical': clitic = choice(['niko', 'k o', 'ngo', 'ningo'])
    # sentence_first_constituent = extract_first_constituent(sentence)
    # new_sentence = attach_clitic(sentence_first_constituent, clitic)
    # return new_sentence with updated gloss (EMPH or VERD)
    pass

# === ### 7.2 Markers of hearsay ===
def mark_hearsay_clitic_or_suffix():
    """
    Attaches hearsay markers ndaje, ñandeko, jeko (second-position clitics) or -je (unstressed verb suffix)
    to indicate that the event is reported by a third party, not firsthand.
    Clitics attach as second-position enclitics; -je attaches to the verb stem as a suffix.
    """
    # Identify verb or clause root
    verb_root = get_verb_root()
    clause_position = get_clausal_position(verb_root)

    # If -je is selected (verb suffix), attach to verb
    if marker == "-je":
        verb_root += "-je"
    # Otherwise, use clitics: prefer second position (after first word or aux)
    elif marker in {"ndaje", "ñandeko", "jeko"}:
        if clause_position == "second":
            insert_after_first_word_or_aux(marker)
        else:
            # Allow marginal non-second position (e.g., clause-initial in narrative)
            insert_at_clause_position(marker, preferred_position="second", allowed_positions=["first", "second"])

    # Example: umi céntimo ha níkel 1 guarani = ndaje → 'We will use again cents and nickel (they say)'
    # Example: o-h-enói-uka-je → 'They say that one night...'

    return form_clause()

# === ### 7.3 Markers of direct evidence ===
def mark_direct_evidence_kuri():
    """Uses unstressed particle 'kuri' to mark direct evidence: speaker witnessed the event firsthand; 
    often interpreted as recent past tense but only when evidential basis is direct observation."""
    def apply(sentence_tokens):
        # kuri appears freely but commonly after predicate
        # mandatory condition: speaker has direct (visual/firsthand) evidence of event
        if has_direct_evidence_speaker() and "kuri" in sentence_tokens:
            # kuri functions as evidential marker, not tense marker per se
            # often corresponds to recent past interpretation when direct evidence is present
            return annotate_evidential(sentence_tokens, "direct", "kuri")
        return sentence_tokens

    # Examples:
    # upe ka'aru n-o-mýi-ri t-e'ongue-ty-icha kuri → 'The afternoon was still like a cemetery.'
    # che ha'é-ma kuri mokoĩ ore-hermano o-u-hague do año ante → 'I already said that two of our brothers came two years before.'
    return apply

# === ### 7.4 Markers of reasoned evidence ===
def mark_reasoned_evidence():
    """Assigns the recent inference marker 'ra'e' (or extended forms like 'mbora'e', 'nipo ra'e') to express conclusions drawn through internal reasoning, often with surprise or counterexpectation; can co-occur with uncertainty markers; 'raka'e' signals longer reasoning chains."""
    # Conditions: speaker draws conclusion via internal inference (not direct perception or hearsay)
    # Placement: relatively free in clause (not clause-finally required)
    # Morphological operations:
    # - Base marker: 'ra'e' (recent inference, often mirative)
    # - Extended: 'mbora'e' (mbo + ra'e) or 'nipo ra'e' for stronger counterexpectation
    # - Alternative marker 'raka'e' for extended/distant past inference
    # Word order: flexible; typically post-verbal but may appear clause-initially or medially
    # Examples:
    # EBY oipytyvõ radio maúpe ra'e → '(It turned out that) EBY helped illegal radio stations.'
    # ndevaléngo ra'e → 'It turned out that you were good (worth it), in the end.'
    return "ra'e (recent inference) | mbora'e (uncertainty + recent inference) | nipo ra'e (counterexpectation + recent inference) | raka'e (distant inference)"

# === ### 8.1 Word order in simple clauses ===
def simple_clause_word_order():
    """
    Guarani simple clauses allow flexible subject placement (SV or VS), but object 
    noun phrases (especially human) typically follow the verb (VO order); subject 
    and object NPs may be omitted (drop) when coreferenced by verbal agreement prefixes.
    """
    # Base clause: predicate + optional arguments + optional adverbials
    # 1. Subject NP: can appear before (SV) or after (VS) the verb
    # 2. Object NP: if present and human, usually follows verb (VO)
    # 3. Both subject and object can be unexpressed via agreement prefixes

    # Subject drop example: a-h-echa-ma 'I saw (him/her/it) already.'
    # Object drop example: che-r-echa-ma 'They/You saw me already.' / 'I have already been seen.'

    # Procedural rule:
    clause = {
        "predicate": None,  # verb or noun/adjective/adverb with inactive prefix
        "subject_np": None,  # optional; SV or VS order
        "object_np": None,   # optional; if present & human, usually postverbal (VO)
        "adverbials": []     # optional; freely placed
    }

    # If subject NP present → may precede (SV) or follow (VS) predicate
    # If object NP present (human) → typically follows predicate (VO)
    # Verbal prefixes encode subject/object when NPs are omitted
    return clause

# === ### 8.2 Predicative and equative clauses ===
def guaraní_equative_predicative_clause():
    """
    Equative and predicative clauses in Guaraní use noun phrase juxtaposition without a copula verb.
    Subject and predicate are separated prosodically (e.g., pause/intonation break) to avoid ambiguity with possessives.
    """
    def parse_clause(subject, predicate, evidence_marker=None):
        # Equative: subject = predicate (identical referent)
        # Predicative: subject has property described by predicate
        # Structure: [Subject] [Predicate] [optional evidence/emphatic marker]
        if evidence_marker:
            # Emphatic (e.g., -ngo) or evidential (e.g., -tía + iporã) marker clarifies clause type
            return f"{subject} {evidence_marker} {predicate}"
        else:
            # Juxtaposition with prosodic boundary (notated in writing as a pause)
            return f"{subject} {predicate}"

    # Examples:
    # ore-r-etã mburuvicha Mario Abdo Benítez → 'The president of our country is Mario Abdo Benítez' (equative)
    # nde-sy ngo mbo'e-hára → 'But your mother is a teacher!' (predicative with emphatic -ngo)

# === ### 8.3 Location and existence clauses ===
def be_location_clause():
    """
    Expresses location/existence using copular verb -ime 'to be located' (3sg: -oĩ/-oime) or -iko 'to exist/live'.
    Third person uses -oĩ/-oime for 'there is/are'; first/second use person-marking + -ime/-iko.
    Word order: Subject + CLB + Verb + Location (if any).
    """
    # Example: 'I am here.' -> a-ime ko'ápe
    # Example: 'Where are you?' -> moõpa reime

    def form_location_verb(person, number, is_location=True):
        if person == 3 and number == "sg":
            return "oĩ" if is_location else "oikove"  # oĩ for location, oikove for existence/aliveness
        elif person == 1 and number == "sg":
            return "a-ime" if is_location else "a-iko"
        elif person == 2 and number == "sg":
            return "re-ime" if is_location else "re-iko"
        elif person == 1 and number == "pl_incl":
            return "ña-ime" if is_location else "ña-iko"
        else:
            raise ValueError("Unsupported person/number")

    # Check if location clause (uses -ime, optionally + õ̃pa for Q-particle)
    # Third-person impersonal existence uses oĩ/oime + -pa (question marker)
    # First/second person uses person-marking + -ime + location

    # Rule: If location is specified, use -ime; if general existence/state, use -iko
    # Example: 'You live in the countryside.' -> pe-iko kokue=pe
    # Example: 'I don't live in Paraguay yet.' -> che nd-a-iko-i gueteri Paraguái=pe

    return "Copula: person-mark + [-ime (location) | -iko (existence/state/living)] + optional -pa (Q) + location phrase"

# === ### 8.4 Sentences expressing possession ===
def possessive_clause_structure():
    """
    In Guaraní, possession is expressed via a copular clause with the possessor in subject position,
    the possessed noun as predicate, and the copula 'to' in the appropriate tense/aspect/mood form.
    The possessed noun typically takes the genitive prefix 'a-' if it is animate or high-in-rank.
    """
    def build_possession_clause(possessor, possessed_noun, tense="present"):
        # Determine if genitive prefix 'a-' is required (animate/high-in-rank nouns)
        needs_genitive_prefix = possessed_noun in ANIMATE_OR_HIGH_RANK_NOUNS
        
        # Apply genitive prefix if needed
        possessed_form = f"a{possessed_noun}" if needs_genitive_prefix else possessed_noun
        
        # Select copula form based on tense
        copula_form = {
            "present": "to",
            "past": "ro",
            "future": "ho",
        }.get(tense, "to")
        
        # Word order: possessor (subject) + copula + possessed noun (predicate)
        clause = f"{possessor} {copula_form} {possessed_form}"
        return clause

    # Example: 'Maria has a dog' → Maria to akãi
    # Example: 'He has a house' → Ō to oka (inanimate noun, no prefix)

# === ### 8.4.1 Non-verbal possessive sentences ===
def inalienable_possessive_sentence():
    """
    Forms verbless possessive sentences for inalienable nouns (body parts, kinship) using inactive person prefixes on the possessum, which functions as the predicate.
    """
    # Conditions: possessum is inalienable (e.g., body part, kinship term)
    # Rule: Possessor → inactive prefix attached to possessum; no verb required
    # Word order: [Topic] + [Possessive predicate (prefix + possessum)]
    # The predicate may be modified by clitics/affixes (e.g., -se, -rõ, negative clitics)

    # Example 1: 'It has wings.'
    # i-pepo  (3.INACT-wing)

    # Example 2: 'I want to have a child.' (by a woman)
    # che che-memby-se  (1.INACT-child.of.woman-want)

    # Numerals appear outside the predicate:
    # -Chejyva mokõi. ('I have two arms.')
    # mbovýpa ndejyva. ('How many arms do you have?')

    pass  # Core morphosyntactic rule: inactive prefix + inalienable noun = predicate

# === ### 8.4.2 Verbal possessive sentences ===
def verbal_possessive_sentences(subject, possessum, age_or_transitive_context=False):
    """
    Expresses alienable possession using the verb *reko* ('to have') with subject-marking prefixes
    and object-marking suffixes. The subject (animate possessor) is the grammatical subject,
    and the possessum is the direct object. Used for transient possession and age expressions.
    """
    # Subject is animate and clausal subject; mark with subject prefix on *reko*
    verb_root = "reko"
    if subject == "1sg.inact":
        subject_prefix = "o-"  # e.g., oguereko (father is subject, 3sg.ACT object)
    elif subject == "2sg.act":
        subject_prefix = "nde-re-"
    elif subject == "1sg.act":
        subject_prefix = "che-rereko"  # literal 'I-have' → transitive sense
    else:
        subject_prefix = f"{subject}-re-"  # generic for animate 3rd person subjects

    # For age: subject = possessor, possessum = number + *áño* (year)
    if age_or_transitive_context:
        return f"{subject_prefix} {possessum}"  # e.g., 'a-reko 28 áño'

    # For standard possession: subject (animate) + verb + object (possessum)
    # e.g., 'oguereko mbohapy kavaju' → 'has three horses'
    return f"{subject_prefix} {possessum}"  # possessum may be noun phrase

# Examples:
# 'My father has three horses.' → 'oguereko mbohapy kavaju'
# 'I am 28 years old and have two children.' → 'a-reko 28 áño ha che-memby'

# === ### 8.5 Questions ===
def forming_yes_no_questions(guaraní_sentence):
    """
    Forms yes/no questions by attaching the interrogative clitics =pa or =piko 
    to the first phrase in the sentence; no change in word order or intonation.
    """
    # Identify first phrase (typically the focus)
    first_phrase = guaraní_sentence.phrases[0]
    
    # Select appropriate clitic: =pa (common) or =piko (also common)
    # Clitic choice not semantically determined per extant literature
    clitic = "=pa"  # default; =piko also acceptable
    # Attach clitic to first phrase (orthographically: hyphen or equals sign)
    questioned_phrase = f"{first_phrase}{clitic}"
    
    # Reconstruct sentence: [questioned phrase] + [rest of sentence]
    rest_of_sentence = " ".join(guaraní_sentence.phrases[1:])
    question = f"{questioned_phrase} {rest_of_sentence}".strip()
    
    return question

    # Examples:
    # ndépa Pablo → 'Are you Pablo?'
    # chepy'apiko oporohayhu → 'Does my heart love (others)?'

# === ### 10.1 Comparatives ===
def mark_comparison_with_icha():
    """
    Marks the standard of comparison in equality comparisons with the unstressed enclitic =icha (or =cha after i-ending stems), 
    with no special marking on the compared entity or the property.
    """
    def apply_rule():
        # Standard of comparison must be a noun phrase
        if isinstance(standard_of_comparison, NP):
            # Attach =icha (or =cha if stem ends in i)
            if standard_of_comparison[-1] == 'i':
                marker = '-cha'
            else:
                marker = '-icha'
            return standard_of_comparison + marker
        
        # For adverbial or clause-like standards, use =guáicha (present), =guaréicha (past), or =guarãicha (future)
        elif isinstance(standard_of_comparison, (Adverb, ClauseFunctioningAsAdverb)):
            if time_reference == 'past':
                return standard_of_comparison + '-guaréicha'
            elif time_reference == 'future':
                return standard_of_comparison + '-guarãicha'
            else:  # present / general
                return standard_of_comparison + '-guáicha'
        
        # Dedicated comparative words (e.g., ñemo'ã, ha'ete, ojoja) precede the standard NP
        elif comparative_word in ['ñemo'ã', 'ha'ete', 'ojoja']:
            if comparative_word == 'ojoja':
                return comparative_word + ' ' + standard_of_comparison + ' =ndive'
            else:
                return comparative_word + ' ' + standard_of_comparison
        
        return standard_of_comparison  # no change if not matched

    # Examples:
    # 'That tree over there is as tall as my house.' → yvyra yvate che-r-óga-icha
    # 'She talks like her mother.' → oñe'ẽ voi i-sy-icha
    return apply_rule()

# === ### 10.2 Superlatives ===
def mark_absolute_superlative_with_ite(root):
    """
    Forms absolute superlatives (very X) by attaching the stressed suffix -ite/-te/-ete
    to adjectives or verbs, with allomorph selection based on the final vowel of the root.
    """
    # Allomorph selection: -ete after high vowels (i, u), -te after mid front vowels (e, ë, a, ñ),
    # -ite otherwise (especially after back vowels like a, o, or consonants)
    if root.endswith(('i', 'u')):
        suffix = 'ete'
    elif root.endswith(('e', 'ë', 'a', 'ñ')):
        suffix = 'te'
    else:
        suffix = 'ite'
    
    superlative_form = root + suffix
    return superlative_form

# ivaiete = i-vai-ete → 's/he/it is very ugly'
# che kuimba'ete = che kuimba'e-te → 'I am a real man'

# === ### 12.1 Coordinated clauses ===
def coordinated_clauses_asymmetric_order():
    """
    Coordinates clauses of equal syntactic hierarchy using conjunctions (ha 'and', tẽra 'or', yrõ 'or else/otherwise') 
    or by juxtaposition (asyndetic coordination), with no required fixed word order; morphemes and clauses remain independent.
    """
    def coordinate_clauses(clause1, clause2, conjunction=None):
        # Asyndetic: juxtapose clauses directly
        if conjunction is None:
            return [clause1, clause2]
        # Syndetic: insert conjunction between clauses
        elif conjunction in ["ha", "tẽra", "yrõ"]:
            return [clause1, conjunction, clause2]
        else:
            raise ValueError("Invalid coordinating conjunction")
    # Example: ehóna eñeno mba'e → go lie down something
    # Example: ojapova'erã ha ndouetevoi → make must and (they) came not at all
    return coordinate_clauses


# Coordination with 'ha' (copulative): clause1 ha clause2
# Coordination with 'tẽra' (disjunctive): clause1 tẽra clause2  
# Coordination with 'yrõ' (conditional alternative): clause1 yrõ clause2

# === ### 12.2 Subordinate clauses ===
def mark_subordinate_clause():
    """
    Marks a clause as subordinate in Guarani by adding a specific suffix or postposed particle to its predicate; 
    no other syntactic changes (e.g., word order, verb form) occur.
    """
    def check_main_clause_dependency(clause):
        return clause.is_subordinate and clause.main_clause is not None

    def apply_subordination_marker(predicate):
        # Select appropriate marker based on clause type and context
        if predicate.has_nominal_function:
            return predicate + "-i"  # e.g., for relative/complement clauses
        elif predicate.in_adverbial_context:
            return predicate + "-pe"  # e.g., temporal or causal adverbial clauses
        else:
            # In some cases, subordination is unmarked
            return predicate

    # Example: [Che ramo] [ha’ẽrõ] → [Che ramo-i] [ha’ẽrõ] 
    # 'The dog [that bit me]' 
    # Example: [Omajae] [ha’ẽrõ] → [Omajae-pe] [ha’ẽrõ] 
    # 'After he left, he came' 

    return apply_subordination_marker if check_main_clause_dependency else None

# === ### 12.2.1 Relative clauses ===
def mark_relative_clause_adjectival(verb_root, tense="present", person_prefix="3"):
    """
    Marks a subordinate predicate as a relative clause using the suffix -va (or -va'e for historical form),
    with optional tense markers -kue (past) or -rã (future). Word order: relative clause precedes noun.
    Person prefixes on the subordinate verb help disambiguate subject vs object relative interpretations.
    """
    # Base relative suffix
    suffix = "-va"
    if tense == "past":
        suffix = "-va'ekue"  # or phonetically reduced "-vaekue" or "-akue"
    elif tense == "future":
        suffix = "-va'erã"  # or phonetically reduced "-vaerã" or "-arã"
    
    # Construct relative verb form (person prefix + verb root + suffix)
    relative_verb = f"{person_prefix}.{suffix.lstrip('-')}"  # simplified gloss format
    
    # Example: subject relative (subject marked by inactive prefix)
    # aheka peteĩ kuña nderechava'ekue → 'a woman who saw you' (2SG.INACT-POSSM-see-ADJZ-POST)
    # Example: object relative (object marked by active prefix)
    # aheka peteĩ aranduka ome'ẽva'ekue → 'a book that my dad gave me' (3.ACT-give-ADJZ-POST)
    
    return {
        "base_suffix": suffix,
        "requires_noun_antecedent": True,
        "relative_clause_order": "pre-nominal",
        "tense_variants": {"past": "va'ekue", "future": "va'erã"},
        "person_prefix_clues": {"inactive": "likely subject relative", "active": "likely object relative"}
    }

# === ### 12.2.2 Complement clauses ===
def complement_clause_with_ha_hague():
    """
    Forms complement clauses (noun-like subordinate clauses) using -ha (general nominalizer) or -hague (past interpretation).
    The subordinate predicate is suffixed with -ha unless it has a past interpretation, in which case -hague is used.
    The clause functions as subject, object, or other complement of the main verb.
    """
    def build_complement_clause(predicate_morphemes):
        # predicate_morphemes: list of (morpheme, tense/aspect/mood) tuples for the subordinate clause
        # Check tense: future uses -ha; past uses -hague
        if predicate_morphemes[-1][1] == 'past':
            suffix = '-hague'
        elif predicate_morphemes[-1][1] == 'future' or predicate_morphemes[-1][1] is None:
            suffix = '-ha'
        else:
            # default to -ha for non-past
            suffix = '-ha'
        return predicate_morphemes + [('SUF', suffix)]
    
    # Example 1: future interpretation → -ha
    # 'ai-kuaa che-andu-ta-ha' → 'I know that you will visit me.'
    
    # Example 2: past interpretation → -hague  
    # 'ore-visita-hague' → 'your visit (in the past), i.e., that you visited'
    
    return build_complement_clause


# Usage: complement_clause_with_ha_hague()(predicate_morphemes)

# === ### 12.2.3 Adverbial clauses ===
def adverbial_clause_modifies_main_predicate():
    """
    Adverbial clauses subordinate to the main clause and modify the predicate
    by expressing time, cause, condition, or manner; they precede the main clause.
    """
    def classify_adverbial_type(clause):
        if "ha'e" in clause:  # 'because' / reason
            return "causal"
        elif "mbye" in clause:  # 'when' / time
            return "temporal"
        elif "pe" in clause and "rerek" in clause:  # 'if' / condition
            return "conditional"
        elif "ha" in clause and "pytã" in clause:  # 'how' / manner
            return "manner"
        return "unknown"

    # Word order: Adverbial clause always precedes main clause
    # Main clause uses same verb as in independent use; no auxiliaries for clause linkage
    # Examples:
    # Ha'e umi oĩ, jasy pyahúra. 'Because I came, he left.' (causal)
    # Mbye oĩ, jasy pyahúra. 'When I came, he left.' (temporal)
    pass  # Implementation details abstracted for linguistic rule only

# === ### 12.2.3.1 Purposive ===
def mark_purposive_clause(subordinate_verb_stem, is_negative=False, neg_marker="ani"):
    """
    Marks a subordinate clause expressing purpose (or avoidance of an outcome) in Guaraní.
    The purposive is introduced by haguã 'for' (after the verb) or ani haguã 'so as not to' (before the verb);
    alternative negative marking uses the privative suffix -'ỹ on the predicate.
    """
    if is_negative:
        # Option 1: use 'ani haguã' around the verb (ani precedes verb, haguã follows)
        return f"{neg_marker} {subordinate_verb_stem} haguã"
    else:
        # Positive purposive: haguã follows the verb
        return f"{subordinate_verb_stem} haguã"
    # Note: Alternative negative marking via privative suffix -'ỹ (not shown in core logic here)
    # Examples:
    # o-ñe-h-a'ã haguã → 's/he tries so that (I) see' (positive)
    # ani hag̃ua a-h-echa → 'so that I do not see' (negative via ani+haguã)
    # o-ñe-h-a'ã-ỹ → 's/he tries not to let me see' (negative via -ỹ)

# === ### 12.2.3.2 Concessive ===
def concessive_clause_subordinator_jepe():
    """Expresses a concession where the subordinate clause presents an impediment or potential condition that does not prevent the main clause's proposition; uses 'ramo jepe' for real/actual concessions and optative mood for non-real/potential ones."""
    def process_clause(subordinate_clause, main_clause, reality_status="real"):
        # Reality status determines verb mood in subordinate clause
        if reality_status == "real":
            # Real concession: subordinate clause uses indicative (past/present)
            # Subordinator 'ramo jepe' is placed after the subordinate clause
            return [subordinate_clause + ["ramo", "jepe"], main_clause]
        elif reality_status == "potential":
            # Potential concession: subordinate clause predicate in optative mood
            # Optative marker: -vo (for 3rd act) or equivalent morpheme
            subordinate_clause_with_optative = mark_optative(subordinate_clause)
            return [subordinate_clause_with_optative + ["jepe"], main_clause]
        else:
            raise ValueError("Reality status must be 'real' or 'potential'")
    
    # Example 1: real concession (actual state)
    # ndachekatupyrýi ramo jepe cheñe'ẽme, ndaupéichai hína chemba'ekuaápe.
    # 'Even though I am not skilled in my speech, it is not so for my knowledge.'
    
    # Example 2: potential concession (optative)
    # taha'e jepe hetãtee → 'even if it be his/her own country'
    
    return process_clause

# === ### 12.2.3.3 Cousol ===
def express_causal_clause_with_postpositions():
    """Use locative postpositions =gui, =rehe, =rupi attached to a predicate to mark causal relation with the main clause."""
    # Check if postposition =gui, =rehe, or =rupi is attached to a predicate
    # These postpositions derive from locative use but express cause here
    # The predicate with postposition functions as a clausal adjunct preceding or following the main clause
    # Word order is flexible; causal adjunct may precede (as in written) or follow (common in speech) main clause
    
    # Example 1: Adjunct precedes main clause
    # oĩgui Ysyry Guasu Paraguay ... → 'Because it is on the banks of the Paraguay River, people fish...'

    # Example 2: Adjunct follows main clause with ha 'and' linking causal elements
    # ... ha ijapurehe declaración jave → '... and for having lied in a statement'

    # Example 3: rupi with adjective+noun compound
    # imarangatu ha imba'ekuaaiterei rupi → 'because he was divine and wise'
    pass  # Rule is structural/positional: postposed causal phrase using =gui/=rehe/=rupi + predicate

# === ### 12.2.3.4 Conditional ===
def conditional_clause():
    """
    Marks hypothetical and counterfactual conditions using unstressed postpositions =ramo/=r rõo (hypothetical) or =rire (counterfactual), 
    with counterfactuals requiring =va'erãmo'ã in the main clause.
    """
    def mark_condition(main_clause, sub_clause, type_):
        if type_ == "hypothetical":
            sub_clause.marker = "=ramo"  # or "=r rõo" (free variation)
            return sub_clause + " " + main_clause
        elif type_ == "counterfactual":
            sub_clause.marker = "=rire"
            main_clause.modifiers = ["=va'erãmo'ã"]
            return sub_clause + " " + main_clause
        else:
            raise ValueError("Conditional type must be 'hypothetical' or 'counterfactual'")
    
    # Examples:
    # mark_condition("ejúke", "cherendúramo", "hypothetical") → 'cherendúramo ejúke' ('If you heard me, come!')
    # mark_condition("ahava'erãmo'ã", "ai-kuaa=rire", "counterfactual") → 'ai-kuaa=rire a-ha-va'erã-mo'ã' ('If I had known it, I would have gone.')

# === ### 12.2.3.5 Moпneг ===
def manner_clause_with_nmlz_icha():
    """Forms manner clauses using nominalized subordinate predicates ending in -ha/-hague + -icha 'as'"""
    def construct_manner_clause(main_verb, sub_verb_root, tense="nonpast"):
        # Subordinate clause: nominalize verb root with -ha (present) or -hague (past)
        if tense == "past":
            sub_verb = sub_verb_root + "-hague"
        else:
            sub_verb = sub_verb_root + "-ha"
        
        # Combine with -icha to form manner clause
        manner_clause = f"{sub_verb}-icha"
        
        # Main clause comes first, manner clause follows
        result = f"{main_verb} {manner_clause}"
        return result

    # Example: IMP-make + want-NMLZ-as → 'do (it) as you want'
    # Example: OPT-3.ACT-make + 2SG.ACT.say-NMLZ.PAST-as → 'Let him/her do it as you said.'
    return construct_manner_clause(main_verb="e-japo", sub_verb_root="rei-pota", tense="nonpast")  # e-japo rei-pota-ha-icha

# === ### 12.2.3.6 Temporal ===
def temporal_subordination_simultaneity():
    """
    Forms simultaneous temporal clauses in Guaraní by using the particle 'vo' (while/when) or the suffix '-vo' on verbs, 
    where both main and subordinate events occur at the same time.
    """
    # Select verb stem for main clause (3rd person active typically)
    # Append '-vo' to subordinate verb to mark simultaneity
    # Alternatively, use standalone particle 'vo' or 'ha' before clause
    # Word order: Main clause + [ subordinate clause with -vo or vo/ha-prefixed clause ]
    # Subordinate clause can precede or follow main clause; no fixed order
    
    # Example: o-iko-vo peteĩ yvyrarehe → 'While it was pacing around a tree...'
    # Example: ro-karu aja o-g̃uahẽ ore-r-u → 'While we ate, our father arrived.'
    pass  # rule description only; no implementation needed

# === ### 12.2.3.7 Locotive ===
def locative_clause_maker(subordinate_predicate, main_predicate, postposition):
    """
    Creates a locative clause using the nominalizer -ha followed by a place postposition.
    The -ha nominalizer converts the subordinate predicate into a location noun phrase,
    which then functions as a temporal/spatial location for the main predicate.
    """
    # Step 1: Nominalize the subordinate predicate with -ha
    nominalized_subordinate = subordinate_predicate + "-ha"
    
    # Step 2: Attach the location postposition (=pe for general location, =gui for source, etc.)
    if postposition == "in":
        location_marker = "=pe"
    elif postposition == "from":
        location_marker = "=gui"
    else:
        location_marker = "=" + postposition
    
    # Step 3: Combine nominalized subordinate with location marker (no space)
    locative_phrase = nominalized_subordinate + location_marker
    
    # Step 4: Construct clause: locative phrase + main predicate
    clause = f"{locative_phrase} {main_predicate}"
    
    return clause

# Example 1: kuña guápa oũhápe → "Where there is an industrious woman..."
# Example 2: ojuhágui → "from where his/her mother comes"

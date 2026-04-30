"""
Code-format grammar rules for Paraguayan Guaraní.
Auto-generated from grammar_guarani_proc_filt.md.
"""

# === ### 3.1 Nouns ===
def is_guarani_noun(root, affixes, position_in_phrase):
    """
    Determines if a root functions as a noun based on its capacity to 
    combine with specific nominal markers and its position in a phrase.
    """
    nominal_enclitics = {"kuéra", "eta", "ita"}
    nominal_markers = {"kue", "rã"}
    nominal_derivatives = {"'o"}

    # Check for nominal morpheme combinations
    if any(affix in affixes for affix in nominal_enclitics): return True
    if any(affix in affixes for affix in nominal_markers): return True
    if any(affix in affixes for affix in nominal_derivatives): return True
    
    # Check for inactive personal markers (possession)
    if "inactive_person_marker" in affixes: return True
    
    # Check if it is the head of a postpositional complement
    if position_in_phrase == "head_of_postposition": return True

    return False

# Examples:
# koty + "kuéra" -> True (kotykuéra: 'rooms')
# che + "koty" -> True (chekoty: 'my room')

# === ### 3.1.1 Plural marking ===
def apply_plural_marking(noun, category="countable", count_type="standard", is_nasal=False):
    """
    Applies plural markers to Guaraní nouns based on animacy, quantity, and phonology.
    Returns the pluralized string or the original noun.
    """
    if count_type == "standard":
        # =kuéra / =nguéra for countable/animate nouns
        suffix = "nguéra" if is_nasal else "kuéra"
        return f"{noun}={suffix}" # e.g., mbyja=kuéra (stars)

    if count_type == "multitudinal":
        # =eta for closed vowels, =ita for mid/open vowels
        suffix = "ita" if noun[-1] in "a e o" else "eta"
        return f"{noun}={suffix}" # e.g., panambi=eta (many butterflies)

    if count_type == "collective":
        # -ty/-ndy for plants/objects, -kua for people/animals
        if category == "animate":
            return f"{noun}-kua"
        suffix = "ndy" if is_nasal else "ty"
        return f"{noun}-{suffix}" # e.g., avati-ty (cornfield)

    return noun # Plural omitted if numeral/determiner present (e.g., mokõi jyva)

# === ### 5.1 Postpositions marking a predicate's complements ===
def mark_predicate_complement(noun_phrase, verb_type, is_human=False, is_animal=False, is_personified=False):
    """
    Determines the postposition marking for a predicate's complement.
    Direct objects are marked if human/personified; indirect objects are always marked.
    """
    # Resolve nasal allomorph for =pe
    postposition = "=me" if noun_phrase.ends_with_nasal() else "=pe"
    
    if verb_type == "ditransitive" and noun_phrase.role == "indirect_object":
        return noun_phrase + postposition  # Ame'ẽta chesýpe (I will give it to my mother)
        
    if verb_type == "transitive" and noun_phrase.role == "direct_object":
        if is_human or is_animal or is_personified:
            return noun_phrase + postposition # Oha'arõ imembykuérape (She waited for her children)
        else:
            return noun_phrase # Cheru ojukapáta tahyikuéra (My father will kill ants)
            
    return noun_phrase + noun_phrase.required_postposition # e.g., =rehe or =gui

# === ### 5.2 Postpositions of place ===
def apply_spatial_postposition(base, postposition):
    """
    Appends a spatial postposition to a base, applying allomorphic 
    changes based on the base's nasality or grammatical category.
    """
    # Handle nasal allomorphs
    if base.is_nasal:
        mapping = {
            "gotyo": "ngotyo",
            "pe": "me",
            "peve": "meve"
        }
        postposition = mapping.get(postposition, postposition)

    # Handle specific base categories
    if base.is_personal_pronoun:
        mapping = {
            "gui": "hegui",
            "pe": "ve"
        }
        postposition = mapping.get(postposition, postposition)
    
    if base.ends_with_non_high_vowel and postposition == "gua":
        postposition = "ygua"

    return f"{base}{postposition}"

# Examples:
# merkádogui -> "from the market"
# orerógape -> "in/at their house"

# === ### 5.3 Postpositions of time ===
def apply_time_postposition(noun_or_verb, postposition):
    """
    Appends a time-related postposition to a noun or verb to express temporal relations.
    Handles allomorphy for 'until' based on nasalization of the base.
    """
    # Allomorphy rule for 'until'
    if postposition == "peve":
        if is_nasal_base(noun_or_verb):
            postposition = "meve"

    # Postpositions follow the base (noun or verb)
    # Examples: 15 ary guive (since 15 years), michĩ vove (while little)
    return f"{noun_or_verb}={postposition}"

def is_nasal_base(word):
    # Helper to check for nasal consonant ending
    nasals = ('m', 'n', 'ñ', 'ng')
    return word.endswith(nasals)

# === ### 5.4 Other postpositions ===
def apply_postposition(noun_phrase, postposition, is_negative_cause=False):
    """
    Appends a postposition to a noun phrase to express spatial, causal, or comitative relations.
    """
    # Handle specific lexical constraints
    if postposition == "káusa" and not is_negative_cause:
        raise ValueError("káusa can only be used for negative causal relations")

    # Handle allomorphic variation for comitative 'with'
    if postposition == "ndive":
        # Variation: ndive, ndi, ndie
        postposition = "ndive" 

    # Handle nasal harmony for instrumental 'pe'
    if postposition == "pe" and noun_phrase.ends_with_nasal():
        postposition = "me"

    # Construct the final word order (Noun + Postposition)
    return f"{noun_phrase}{postposition}"

# Examples:
# yvoty-icha ('like a flower')
# che-ndive ('with me')

# === ### 6.1 Active voice ===
def apply_guarani_voice(root, argument, voice="active"):
    """
    Assigns active or inactive person prefixes based on the predicate type 
    and the role of the argument (Agent/Subject vs Patient).
    """
    active_prefixes = {"1SG": "a-", "1PL_INCL": "ja-", "2SG": "re-", "2PL": "pei-"}
    inactive_prefixes = {"1SG": "che-", "1PL_EXCL": "ore-", "2SG": "ne-", "3": "i-"}

    if voice == "active":
        # Active voice: marks S (intransitive) or A (transitive if P is 3rd person)
        prefix = active_prefixes.get(argument)
        return f"{prefix}{root}" # e.g., a-guata ('I walk')

    elif voice == "inactive":
        # Inactive voice: marks S (intransitive state) or P (patient of transitive)
        prefix = inactive_prefixes.get(argument)
        return f"{prefix}{root}" # e.g., che-atĩa ('I sneeze') or ore-nupã ('we are hit')

# === ### 6.3 Passive/reflexive/impersonal voice ===
def apply_agent_demoting_voice(verb_stem, is_transitive, is_reflexive_or_passive=False):
    """
    Applies the AGD prefix (je-/ñe-) to demote the agent, creating a 
    passive, reflexive, or impersonal construction.
    """
    # Rule: Prefix je- or ñe- is applied based on phonetic harmony
    agd_prefix = "ñe-" # Simplified selection logic
    
    if not is_transitive:
        # Impersonal/Generic: Subject is eliminated
        return f"{agd_prefix}{verb_stem}" # Example: ñembo'e (one learns / it is taught)
    
    if is_transitive and is_reflexive_or_passive:
        # Passive (unspecified agent) or Reflexive (subject acts on self)
        return f"{agd_prefix}{verb_stem}" # Example: ñemonda (he/she dresses himself/herself)
    
    return verb_stem

# === ### 6.3.1 With intransitive verbs: generic and impersonal interpretations ===
def apply_impersonal_generic_construction(verb_root, is_intransitive=True):
    """
    Constructs an impersonal or generic form using the prefix je-/ñe- 
    and the 3rd person singular active prefix 'o-'.
    """
    if is_intransitive:
        # Rule: 3.ACT + AGD_prefix + verb_root
        agd_prefix = "je-"  # (or ñe- depending on phonology)
        verb_form = f"o{agd_prefix}{verb_root}"
        return verb_form
    
    return None

# ojejeroky: 'there is dancing' (impersonal)
# ojejapo: 'one makes / it is made' (generic)

# === ### 6.3.2 With transitive verbs: passive and reflexive interpretations ===
def apply_agent_demoting_voice(active_prefix, verb_root, is_aireal=False):
    """
    Applies the je-/ñe- prefix to a transitive verb to create a 
    passive or reflexive meaning, demoting the agent.
    """
    # Determine the appropriate agent-demoting prefix
    # Typically je- or ñe- depending on phonological context
    agd_prefix = "ñe-" if active_prefix.startswith(("o", "pe")) else "je-"
    
    # Handle aireal verb variation: final 'i' of prefix may shift to root
    if is_aireal:
        processed_root = f"i{verb_root}" # optional variation: ojeipuru vs ojepuru
    else:
        processed_root = verb_root

    # Construction: Active Person Prefix + AGD Prefix + Root
    # Note: Agent (A) cannot be overtly expressed in this voice
    return f"{active_prefix}-{agd_prefix}-{processed_root}"

# Example: "rejejapi" (re-je-japi) -> 'you were shot' / 'you shot yourself'
# Example: "oñekytĩ" (o-ñe-kytĩ) -> 's/he was cut' / 's/he cut him/herself'

# === ### 6.4 Reciprocal voice ===
def apply_reciprocal_voice(subject, verb_root):
    """
    Adds reciprocal meaning to a verb using the jo-/ño- prefix.
    Requires a plural subject acting as both agent and patient.
    """
    if not subject.is_plural:
        raise ValueError("Reciprocal voice requires a plural subject")

    # Selection of reciprocal prefix based on phonetic environment
    # (Typically jo- for most, ño- before certain consonants/vowels)
    prefix = "ño-" if verb_root.starts_with_nasal_or_specific() else "jo-"
    
    # Word order: [Subject Prefix] + [Reciprocal Prefix] + [Verb Root]
    reciprocal_verb = f"{subject.prefix}{prefix}{verb_root}"
    
    return reciprocal_verb

# Examples:
# jajohayhu (ja-jo-hayhu) -> 'we love each other'
# oñohetũ (o-ño-hetũ) -> 'they kiss each other'

# === ### 6.5 Antipassive voice ===
def apply_antipassive_voice(verb, object_type, person_prefix=None):
    """
    Converts a transitive verb to antipassive voice by removing the direct object
    and adding a prefix based on the object's animacy (human vs non-human).
    """
    if not verb.is_transitive or verb.has_postpositional_object:
        return verb

    # Determine antipassive prefix based on implied object
    prefix = "poro-" if object_type == "human" else "mba'e-"
    # Note: some speakers use "po-" for human
    
    # Rule: [Person Prefix] + [Antipassive Prefix] + [Verb Root]
    result = f"{person_prefix if person_prefix else ''}{prefix}{verb.root}"
    
    return result

# Examples:
# apply_antipassive_voice(Verb("mbo'e"), "human", "ro-") -> "roporombo'e" (we teach people)
# apply_antipassive_voice(Verb("jogua"), "non-human", "pe-") -> "pemba'ejogua" (you buy things)

# === ### 6.6 Causative voice ===
def apply_causative_voice(verb, causer, causee, affectee=None):
    """
    Converts a base event into a causative event by adding a causer.
    Increases the number of participants: Intransitive becomes Transitive; Transitive becomes Ditransitive.
    """
    if verb.is_intransitive:
        # Intransitive Causative/Sociative: S -> A, Causer -> S
        # Result: [Causer] makes [Causee] [Verb]
        word_order = [causer, causee, verb]
    elif verb.is_transitive:
        # Transitive Causative: A -> S, Causer -> A, P remains
        # Result: [Causer] makes [Causee] [Verb] [Affectee]
        if affectee is None:
            raise ValueError("Transitive causatives require an affectee")
        word_order = [causer, causee, verb, affectee]
    
    return " ".join(word_order)

# Example: "che jaguare" (she runs) -> "che amombáy" (I make her run)
# Example: "che amomba'é" (I make him/her do it)

# === ### 6.6.1 Causative voice for intransitive verbs ===
def apply_intransitive_causative(verb_root, causer_prefix, causee_object):
    """
    Converts an intransitive verb into a transitive causative verb using mbo-/mo- prefixes.
    The original subject becomes the direct object (causee), and a new causer is introduced.
    """
    # Determine prefix based on root initial sound (phonological rule)
    causative_prefix = "mbo-" if verb_root[0] not in "aeio u" else "mo-"
    
    # Construct the causative verb: [Causer Prefix] + [Causative Marker] + [Root]
    causative_verb = f"{causer_prefix}{causative_prefix}{verb_root}"
    
    # The causee is marked as a direct object (e.g., using -pe or possessive markers)
    return f"{causative_verb} {causee_object}"

# Example 1: ambopuka ichupe ('I make him/her laugh') from a-puka
# Example 2: amokane'õ maymávape ('I make everybody tired') from che-kane'õ

# === ### 6.6.2 Sociative causative ===
def apply_sociative_causative(verb_root, subject_prefix, causee):
    """
    Applies the sociative causative prefix (ro- or guero-) to a verb 
    indicating the causer performs the action together with the causee.
    """
    # Prefix selection based on phonological/grammatical rules (ref 4.7)
    prefix = "guero" if subject_prefix.endswith('o') else "ro"
    
    # Construct verb: [Subject Prefix] + [Sociative Causative] + [Verb Root]
    sociative_verb = f"{subject_prefix}-{prefix}-{verb_root}"
    
    # Word order: Subject + Sociative Verb + Causee
    return f"{subject_verb} {causee}"

# jagueroguata ñandejagua ('we walk our dog' - both are walking)
# roguerokyhyje chememby ('I am afraid for my child' - conventionalized psych-verb)

# === ### 6.6.3 Causative voice for transitive verbs ===
def apply_transitive_causative(verb_stem, active_prefix, direct_object, causee=None):
    """
    Converts a transitive verb into a ditransitive causative verb using the -uka suffix.
    The causer is the active subject, the affectee is the direct object, and the causee is the indirect object.
    """
    # Determine suffix variant based on stem ending
    if verb_stem.endswith('u'):
        suffix = "ka"
    elif verb_stem[-1].isalpha() and verb_stem[-1] not in 'aeiou':
        suffix = "uka"
    else:
        suffix = "yka"

    # Morphological construction: [Active Prefix] + [Verb Stem] + [Causative Suffix]
    causative_verb = f"{active_prefix}{verb_stem}{suffix}"
    
    # Word order: Subject(Causer) -> Verb -> IndirectObject(Causee) -> DirectObject(Affectee)
    sentence_structure = {
        "causer": active_prefix,
        "verb": causative_verb,
        "causee": causee,
        "affectee": direct_object
    }
    
    return sentence_structure

# Examples:
# pehechauka ("you show") -> pe- + echa + uka (you make someone see something)
# ojukauka ("he had killed") -> o- + juka + uka (he had someone kill someone)

# === ### 7.1 Emphatic and veridical markers ===
def apply_emphatic_veridical_marker(sentence_structure, marker_type="emphatic"):
    """
    Adds emphatic (voi) or veridical (niko/ko/ngo/ningo) markers to a sentence.
    Markers are placed as second-position enclitics at the end of the first phrase.
    """
    first_phrase = sentence_structure[0]
    
    if marker_type == "emphatic":
        # 'voi' serves as a stressed verbal particle/enclitic
        marker = "voi"
    elif marker_type == "veridical":
        # Variants: niko, ko, ngo, ningo (free variation)
        marker = random.choice(["niko", "ko", "ngo", "ningo"])
    else:
        return sentence_structure

    # Attach marker to the end of the first phrase/word
    sentence_structure[0] = f"{first_phrase}={marker}"
    
    return sentence_structure

# Examples:
# Iporã voi ('It is certainly beautiful')
# Auto tujango kóa ('But this is an old car!')

# === ### 7.2 Markers of hearsay ===
def apply_hearsay_marker(clause, marker):
    """
    Adds a hearsay evidential marker to a clause to indicate third-party reportage.
    Supports clitics (ndaje, jeko, ñandeko) or a verb suffix (-je).
    """
    clitics = ["ndaje", "jeko", "ñandeko"]
    
    if marker == "-je":
        # Append as unstressed verb suffix
        clause['verb'] = clause['verb'] + "-je"
        # Example: o-h-enói-uka-je (They say he had [someone] called)
    elif marker in clitics:
        # Place as a second-position clitic (generally following the first word)
        words = clause['words']
        words.insert(1, marker)
        # Example: jai-puru-jevy-ta ndaje (It is said we will use again)
    
    return clause

# === ### 7.3 Markers of direct evidence ===
def apply_direct_evidence_marker(sentence, has_direct_witness):
    """
    Adds the particle 'kuri' to a clause when the speaker has direct evidence 
    of the event, often functioning as a recent past marker.
    """
    if not has_direct_witness:
        return sentence

    # 'kuri' has free distribution, typically appearing after the predicate
    marker = " kuri"
    
    # Logic: Append to the end of the clause/predicate phrase
    result = f"{sentence}{marker}"
    
    return result

# Example: "te'onguetýicha kuri" -> "like a cemetery (direct evidence/past)"
# Example: "he'i voi kuri" -> "did say (direct evidence/past)"

# === ### 7.4 Markers of reasoned evidence ===
def apply_reasoned_evidence_marker(clause, evidence_type="recent"):
    """
    Adds markers of reasoned evidence (mirative/inference) to a clause.
    Distinguishes between recent realization (ra'e) and long-term reasoning (raka'e).
    """
    if evidence_type == "recent":
        # 'ra'e' is often clause-final; can combine with uncertainty markers
        marker = "ra'e"
        # Example: Ndevaléngo ra'e (It turned out you were good)
        # Example: Omano nipo ra'e (It turned out s/he died)
    elif evidence_type == "long_term":
        # 'raka'e' indicates distant past or extended reasoning
        marker = "raka'e"
        # Example: Oiko raka'e (Lived [at some point in the past])
    else:
        return clause

    return f"{clause} {marker}"

# === ### 8.1 Word order in simple clauses ===
def construct_simple_clause(predicate, subject=None, object_np=None):
    """
    Constructs a simple clause allowing for subject/object drop.
    Default word order is typically VO, with variable subject position (SV or VS).
    """
    clause_elements = []

    # Subject is variable: can be omitted, placed before, or placed after verb
    # For this logic, we'll implement a common SV pattern if subject is provided
    if subject:
        clause_elements.append(subject)

    # The predicate is mandatory (contains internal person prefixes)
    clause_elements.append(predicate)

    # Human object noun phrases most frequently appear after the verb (VO)
    if object_np:
        clause_elements.append(object_np)

    # Handle VS order case: if subject is placed at the end
    # (Simplified: the caller determines the order of arguments)
    
    return " ".join(clause_elements)

# Examples:
# construct_simple_clause("ahecháma", object_np="ichupe") -> "ahecháma ichupe" (I already saw him/her)
# construct_simple_clause("opuka", subject="ha'e") -> "opuka ha'e" (S/he laughed)

# === ### 8.2 Predicative and equative clauses ===
def form_equative_predicative_clause(subject_np, predicate_np, marker=None):
    """
    Forms an equative or predicative clause via juxtaposition of two noun phrases.
    Guaraní lacks a copula ('to be'), relying on juxtaposition and prosody.
    """
    # Structure: [Subject NP] + [Optional Marker] + [Predicate NP]
    clause_elements = []
    
    clause_elements.append(subject_np)
    
    if marker:
        # Markers like 'ndaje' (evidential) or 'ngo' (emphatic) help disambiguate
        clause_elements.append(marker)
        
    clause_elements.append(predicate_np)
    
    # Result is a juxtaposition of NPs without an explicit verb
    return " ".join(clause_elements)

# Example: "Ndesy mbo'ehára" -> "Your mother is a teacher"
# Example: "Ndetía ndaje iporã" -> "Your aunt is pretty (they say)"

# === ### 8.3 Location and existence clauses ===
def construct_existence_location_clause(subject, state_type, location=None, negation=False):
    """
    Determines the correct copula for existence, location, or state.
    Uses -ime for location, -iko for state/life, and ha'e as a general invariant copula.
    """
    # Handle general identity/classification (invariant copula)
    if state_type == "identity":
        copula = "ha'e"
    # Handle physical/psychological state or living in a place
    elif state_type == "state_or_life":
        copula = "iko"
    # Handle physical location or existence (there is/are)
    elif state_type == "location_existence":
        copula = "ime" if subject != "3rd_person_impersonal" else "oĩ"
    
    # Apply person markers (Simplified: 1sg 'a-', 2sg 're-', 3rd 'o-')
    # Example: a-ime (I am located), re-iko (you live)
    prefix = get_person_prefix(subject)
    word = f"{prefix}{copula}"
    
    # Apply negation: nd- [verb] -i
    if negation:
        word = f"nd{word}i"
        
    return f"{word} {location if location else ''}".strip()

# Examples:
# construct_existence_location_clause("1sg", "location_existence", "ko'ápe") -> "aime ko'ápe" (I am here)
# construct_existence_location_clause("2sg", "state_or_life", "porã") -> "reiko porã" (You are well)

# === ### 8.4 Sentences expressing possession ===
def apply_possessive_structure(possessor, possessed_noun, possessive_prefix):
    """
    Constructs a possessive phrase by attaching the appropriate 
    person-marker prefix to the possessed noun.
    """
    # The possessor typically precedes the possessed noun in the sentence
    # The possessed noun takes a prefix matching the person of the possessor
    
    possessed_word = possessive_prefix + possessed_noun
    
    return f"{possessor} {possessed_word}"

# Example: "che ryrý" (my house) -> che + ryrý
# Example: "nde ryrý" (your house) -> nde + ryrý

# === ### 8.4.1 Non-verbal possessive sentences ===
def apply_non_verbal_possession(possessor, possessum, numeral=None):
    """
    Expresses possession without a verb using an inactive person prefix.
    Commonly used for inalienable possession (body parts, kinship).
    """
    # Construct the predicate: [Inactive Person Prefix] + [Possessed Object]
    predicate = f"{possessor.prefix_inactive}-{possessum}"

    # Handle numerals: placed outside the predicate (before or after)
    if numeral:
        return f"{numeral} {predicate}" if numeral.position == "before" else f"{predicate} {numeral}"
    
    return predicate

# Example: "i-pepo" (3.INACT-wing) -> "It has wings."
# Example: "che-jyva mokõi" (1SG.INACT-arm two) -> "I have two arms."

# === ### 8.4.2 Verbal possessive sentences ===
def apply_verbal_possessive_reko(possessor, possessum):
    """
    Expresses alienable/transient possession or age using the verb 'reko'.
    The possessor acts as the clausal subject and the possessum as the object.
    """
    # The root is 'reko' (to have), often with increments -gue- or -re-
    verb_root = "reko"
    
    # Structure: [Possessor (Subject)] + [Person Marker + Root] + [Possessum (Object)]
    # Note: Possessor must be animate
    if possessor.is_animate:
        sentence = f"{possessor} {possessor.person_marker}{verb_root} {possessum}"
        return sentence

# Example: "Cheru oguereko mbohapy kavaju" (My father has three horses)
# Example: "Areko 28 áño" (I am 28 years old)

# === ### 8.5 Questions ===
def form_yes_no_question(sentence_elements):
    """
    Converts a declarative sentence into a yes/no question by attaching 
    an interrogative clitic (=pa or =piko) to the first phrase.
    """
    # Interrogative clitics available in modern Guaraní
    clitics = ["pa", "piko"]
    chosen_clitic = clitics[0] # Logic for selection is not clearly defined in text
    
    # Focus element is the first phrase/word of the sentence
    focus_element = sentence_elements[0]
    
    # Attach clitic to the focus element (second position in sentence)
    sentence_elements[0] = f"{focus_element}={chosen_clitic}"
    
    return " ".join(sentence_elements)

# Example: Ndépa Pablo (Are you Pablo?) -> focus: 'nde' + '=pa'
# Example: Chepy'apiko oporohayhu (Does my heart love others?) -> focus: 'chepy'a' + '=piko'

# === ### 10.1 Comparatives ===
def apply_comparative_equality(standard, tense="PRESENT"):
    """
    Marks the standard of comparison using enclitics. 
    Uses =icha for nouns and =guáicha (with tense markers) for adverbs/clauses.
    """
    # Handle morphophonemic change for i-ending stems
    suffix = "cha" if standard.endswith('i') else "icha"
    
    if is_noun_phrase(standard):
        # Example: cherógaicha (like my house)
        return f"{standard}={suffix}"
    
    elif is_adverb_or_clause(standard):
        # Select tense marker for non-noun standards
        tense_marker = {
            "PAST": "guare",
            "FUTURE": "guaran",
            "PRESENT": "gua"
        }.get(tense, "gua")
        
        # Example: tapiaguáicha (as always)
        return f"{standard}={tense_marker}={suffix}"

# Amo yvyra yvate cherógaicha. (That tree is as tall as my house.)
# Kueheguaréicha. (Like yesterday.)

# === ### 10.2 Superlatives ===
def apply_absolute_superlative(root):
    """
    Adds the stressed suffix -ite/-te/-ete to a root to indicate 'very' or 'real'.
    The variant is determined by the final vowel of the root.
    """
    # Determine suffix based on root's final vowel
    if root.endswith(('i', 'u')):
        suffix = "ete"
    elif root.endswith(('e', 'o')):
        suffix = "te"
    else:
        suffix = "ite"
    
    return root + suffix

# Examples:
# apply_absolute_superlative("ivai") -> "ivaiete" (very ugly)
# apply_absolute_superlative("guarani") -> "guaraniete" (true Guarani)

# === ### 12.1 Coordinated clauses ===
def coordinate_clauses(clause_a, clause_b, coordinator=None):
    """
    Coordinates two clauses of equal hierarchy using asyndetic juxtaposition, 
    copulative/disjunctive conjunctions, or adversative conjunctions.
    """
    # Asyndetic coordination (common with verbs of movement)
    if coordinator is None:
        return f"{clause_a} {clause_b}" # eho na eñeno mba'e (Please go and lie down)

    # Copulative/Disjunctive: ha (and), tẽra (or), yrõ (otherwise)
    if coordinator in ['ha', 'tẽra', 'yrõ']:
        return f"{clause_a} {coordinator} {clause_b}" # Luisa tẽra José ohóta (Luisa or Jose will go)

    # Adversative: ha katu (but/and yet)
    if coordinator == 'ha katu':
        return f"{clause_a} ha katu {clause_b}"

    return f"{clause_a} {coordinator} {clause_b}"

# === ### 12.2 Subordinate clauses ===
def create_subordinate_clause(main_clause, sub_clause, sub_type):
    """
    Converts a clause into a subordinate clause by adding a 
    specific nominalizing suffix or postposed particle to the predicate.
    """
    predicate = sub_clause.get_predicate()
    
    # Subordination is marked specifically on the predicate
    if sub_type in ['relative', 'complement']:
        # Sentential nominalization via suffix
        predicate.apply_suffix(sub_type_nominalizer)
    elif sub_type == 'adverbial':
        # Subordination via specific suffix or postposed particle
        predicate.apply_marker(adverbial_marker)
    
    # Word order remains unchanged from main clause structure
    return main_clause + sub_clause

# Example: "Che ikatu amombarete pe oñemoĩ va'erã" 
# (I can strengthen the one that must be placed)
# Example: "Aikuaa ndojehesa'i" 
# (I know that it is not lacking)

# === ### 12.2.1 Relative clauses ===
def form_relative_clause(predicate, tense='present'):
    """
    Marks a subordinate predicate as a relative clause using the adjectivizer suffix.
    Adds tense markers to the historical form -va'e for past or future.
    """
    if tense == 'present':
        suffix = "-va"
    elif tense == 'past':
        suffix = "-va'ekue"
    elif tense == 'future':
        suffix = "-va'erã"
    else:
        suffix = "-va"

    # The relative clause follows the noun it modifies
    return f"{predicate}{suffix}"

# Example: "iporãva" (who is beautiful) -> Pe kuimba'e iporãva (That man who is beautiful)
# Example: "ome'ẽva'ekue" (that gave) -> peteĩ aranduka ome'ẽva'ekue (a book that gave/was given)

# === ### 12.2.2 Complement clauses ===
def apply_complement_clause_nominalization(subordinate_predicate, tense="present"):
    """
    Marks a subordinate clause as a noun phrase using nominalizing suffixes.
    The suffix -ha is used for present/future, and -hague for past interpretations.
    """
    if tense == "past":
        nominalizer = "-hague"
    else:
        # Future interpretation is marked on the predicate before the nominalizer
        nominalizer = "-ha"

    return f"{subordinate_predicate}{nominalizer}"

# Examples:
# Aikuaa cherayhuha (I know that you love me) -> present/general
# Peimo'äpiko che ajuhague (Do you think that I came) -> past

# === ### 12.2.3 Adverbial clauses ===
def apply_adverbial_clause_modification(main_clause_predicate, subordinate_clause):
    """
    Modifies a main clause predicate by attaching a subordinate clause 
    that functions as an adverbial modifier.
    """
    # Identify the adverbial meaning (e.g., time, cause, purpose, condition)
    adverbial_type = subordinate_clause.semantic_role
    
    # Adverbial clauses generally follow the predicate they modify
    word_order = [main_clause_predicate, subordinate_clause]
    
    # Resulting structure: [Main Verb] + [Subordinate Clause]
    return " ".join(word_order)

# Example: "Ajapo ndaje oĩvo" (I do it, perhaps, while being)
# Example: "Oho haguã" (He goes in order to/so that)

# === ### 12.2.3.1 Purposive ===
def apply_purposive_clause(verb, is_negative=False, is_simultaneous=False):
    """
    Marks a clause as purposive. 
    Uses 'haguã' after the verb for general purpose, 'ani haguã' before for negative, 
    or '-vo' suffix for simultaneous movement.
    """
    if is_simultaneous:
        # Example: a-ju a-poro-mbo'e-vo (I came to teach)
        return f"{verb}-vo"
    
    if is_negative:
        # Example: ani haguã a-h-echa (so that I will not see)
        return f"ani haguã {verb}"
    
    # Example: a-ru haguã (in order to bring)
    return f"{verb} haguã"

# === ### 12.2.3.2 Concessive ===
def apply_concessive_clause(subordinate_clause, is_potential=False):
    """
    Constructs a concessive clause using 'ramo jepe' (even though) 
    or an optative predicate for potential scenarios.
    """
    if is_potential:
        # Predicate must be in optative mood
        predicate = set_mood(subordinate_clause.predicate, "optative")
        return f"{predicate} jepe"
    else:
        # Standard concessive: clause + ramo jepe
        return f"{subordinate_clause} ramo jepe"

# Examples:
# "Ñandereta ramo jepe" -> "Even though we are many"
# "taha'e jepe" -> "even if it be"

# === ### 12.2.3.3 Cousol ===
def apply_causal_clause(predicate, causal_marker):
    """
    Converts a predicate into a causal clause by appending a locative 
    postposition (=gui, =rehe, or =rupi) to express cause.
    """
    causal_postpositions = ["gui", "rehe", "rupi"]
    
    if causal_marker in causal_postpositions:
        # The locative postposition is attached directly to the predicate
        causal_clause = f"{predicate}={causal_marker}"
        return causal_clause
    
    return predicate

# Example: oĩ + gui -> oĩgui (Because there is/it is)
# Example: imarangatu ha imba'ekuaaiterei + rupi -> ... rupi (Because s/he is wise)

# === ### 12.2.3.4 Conditional ===
def apply_conditional_marker(predicate, is_counterfactual=False, is_negative=False):
    """
    Applies the appropriate conditional postposition to a predicate.
    Hypotheticals use =rõo/=ramo; counterfactuals use =rire and require main clause marking.
    """
    # Handle negation for hypothetical conditionals
    if is_negative and not is_counterfactual:
        predicate = f"na{predicate}i" # Apply negation circumfix na...i

    if is_counterfactual:
        # Counterfactual: use =rire (Note: main clause must have -va'erã-mo'ã)
        return f"{predicate}=rire"
    else:
        # Hypothetical: use =rõo or =ramo (free variation)
        marker = "ramo" # or "rõo"
        return f"{predicate}={marker}"

# Example 1: "Cherendúramo" (If you heard me) -> apply_conditional_marker("cherendu")
# Example 2: "Aikuaárire" (If I had known) -> apply_conditional_marker("aikuaa", is_counterfactual=True)

# === ### 12.2.3.5 Moпneг ===
def apply_manner_clause(predicate, tense="present", negative=False):
    """
    Converts a predicate into a manner clause using nominalizing suffixes 
    followed by -icha (as) or -'yrye (without).
    """
    if negative:
        suffix = "-'yrye"
    else:
        # Use -hague for past, -ha for present/future
        nominalizer = "-hague" if tense == "past" else "-ha"
        suffix = f"{nominalizer}-icha"
    
    return f"{predicate}{suffix}"

# Example: reipotaháicha (as you want) -> apply_manner_clause("reipota")
# Example: erehaguéicha (as you said) -> apply_manner_clause("ere", tense="past")
# Example: añeñanduvai'ỹre (without feeling bad) -> apply_manner_clause("añeñanduvai", negative=True)

# === ### 12.2.3.6 Temporal ===
def apply_temporal_marker(verb_phrase, temporal_relation):
    """
    Appends or attaches temporal particles to a verb phrase to indicate the 
    sequential timing between a subordinate and a main clause.
    """
    # Examples:
    # "Aháramo agueraháta" (When I go, I will bring)
    # "re-kakuaa rire" (after you grow up)
    
    markers = {
        "simultaneity": ["-ramo", "-vo", "aja"],
        "precedence": ["mboyve"],
        "subsequence": ["vove", "rire", "guive"]
    }
    
    particle = markers.get(temporal_relation)
    
    if temporal_relation == "simultaneity" and "-ramo" in particle:
        return f"{verb_phrase}=ramo"  # Suffix for 'when/if'
    elif temporal_relation == "simultaneity" and "-vo" in particle:
        return f"{verb_phrase}-vo"    # Suffix for 'while'
    else:
        return f"{verb_phrase} {particle[0]}" # Post-positional particle

# === ### 12.2.3.7 Locotive ===
def form_locative_clause(predicate, postposition):
    """
    Converts a predicate into a locative clause by adding the 
    nominalizer -ha and a specifying postposition of place.
    """
    # Core grammatical rule: Predicate + Nominalizer + Postposition
    nominalizer = "-ha"
    locative_phrase = f"{predicate}{nominalizer}={postposition}"
    
    return locative_phrase

# Example: "oĩ-ha=pe" (where there is) -> 'Where there is an industrious woman...'
# Example: "o-ju-ha=gui" (from where [she] comes) -> 'That child comes from where...'

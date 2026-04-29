# extract_parallel_gua.py

parallel = []
non_para = []

# with open('grammar_guarani.md', 'r') as f:
#     lines = f.readlines()
# import re

import json
import re
from word2number import w2n
import tqdm
import csv

# add language ID to avoid English lines
import fasttext
model = fasttext.load_model('../lid.176.bin')

def readbook(file: str):
    with open(file, 'r') as f:
        lines = f.read().splitlines()
    return lines

def langid(line: str):
    predictions = model.predict(line)
    lang_id = predictions[0][0].split("__label__")[1]  # Get lang id
    confidence = predictions[1][0]  # Get confidence
    return [lang_id, confidence]

def check_trans(line: str):
    if line.startswith("'"):
        return True
    elif line.startswith("'") and line.endswith("'"):
        return True
    else:
        return False

# def process_eng(line:  str):
#     english = line.rsplit("'", 1)[0]
#     english = str(english).strip().replace("[", "").replace("]", "")[1:].capitalize()
#     return english

# def process_kal(line: str):
#     substrings = ["=", "~", "-", "(", ")", "[", "]", "NP", "Obj", "Subj", "V1", "V2", "Pred", "A1", "A2", "A3", "A2+3"]
#     regex = "|".join(map(re.escape, substrings))
#     kalamang = re.sub(regex, "", line).capitalize()
#     return kalamang


def extract_parallel_and_explanations(file_path):
    parallel = []
    explanations = []
    remove_indices = set()

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines if line.strip()]


    for c, line in enumerate(lines):
        english, guarani = None, None

        stripped = line.strip()

        # Check for English translation (lines enclosed in single quotes)
        if stripped.startswith("'"):
            english = line

        if english:
            remove_indices.update({c})

            for i in [3, 2, 1]:
                no_match = False

                try:
                    if check_trans(lines[c-1]):
                        no_match = True

                    if langid(lines[c-i])[0] == "en" and langid(lines[c-i])[1] > 0.8:
                        if stripped.count(".") >= 2:
                            pass

                        # count number of uppercase letters
                        elif sum(1 for c in stripped if c.isupper()) >= 3:
                            pass

                        else:
                            # print(line)
                            no_match = True
                    
                    if langid(lines[c-i])[0] == "gn":
                        guarani = lines[c-i]
                        print(guarani)
                    
                    if len(lines[c-i]) > 3 * len(english):
                        no_match = True

                    if guarani:
                        indices = [c-i, c-i+1]
                        remove_indices.update(set(indices))


                    if no_match:
                        continue

                    indices = range(c, c-i-1, -1)
                    remove_indices.update(set(indices))

                except IndexError:
                    pass

        # pair handling
        if stripped.count("'") >= 2 and stripped.endswith("'"):
            remove_indices.update({c})
        
        if stripped.count("'") >= 2 and stripped.endswith("\\"):
            remove_indices.update({c})

        if stripped.count("'") >= 2 and stripped.count("|") >= 2:
            remove_indices.update({c})

        if stripped.count("'") >= 2 and stripped.count(">") >= 1:
            remove_indices.update({c})
        
        if stripped.count("'") >= 2 and stripped.count(")") >= 1:
            remove_indices.update({c})

    non_para = [line for line in lines if lines.index(line) not in remove_indices]
    para = [line for line in lines if lines.index(line) in remove_indices]

    # print(explanations)

    return para, non_para, lines


# Reporomoñombo'e.
# re-poro-mo-ño-mbo'e
# 2SG.ACT-PEOPLE-MAKE1-RECP-teach
# 'You (sg.) make people teach one another.'

# Example usage:
parallel, explanations, lines = extract_parallel_and_explanations('grammar_guarani_proc_filt.md')

# print(parallel)

with open('gua_parallel.txt', 'w', encoding='utf-8') as f:
    parallel = [p.strip() for p in parallel]
    f.write("\n".join(parallel))

with open('gua_non_parallel.txt', 'w', encoding='utf-8') as f:
    explanations = [l for l in lines if l not in parallel and l.strip()]
    f.write("\n".join(explanations))




# # Write results to separate files if needed
# with open('gua_parallel.txt', 'w', encoding='utf-8') as f:
#     parallel = [p.strip() for p in parallel]
#     f.write("\n".join(parallel))

# with open('gua_parallel.txt', 'r', encoding='utf-8') as f:
#     para = f.readlines()
#     para = [l.strip() for l in para]

# # print(para[0])

# expl_lines = [l.strip() for l in lines if l.strip()]
# with open('gua_non_parallel.txt', 'w', encoding='utf-8') as f:
#     f.write("\n".join(expl_lines))

# with open('gua_non_parallel.txt', 'r', encoding='utf-8') as f:
#     expl = f.readlines()
#     expl = [l.strip() for l in expl]

# unique_lines = [line for line in expl if line.strip() not in para]
# print(unique_lines[:500])

# with open('gua_non_parallel.txt', 'w', encoding='utf-8') as output_file:
#     # output_file.writelines(unique_lines)
#     output_file.write("\n".join(unique_lines))




# for l in lines:
#     # print(l)
#     # if l == "Reporomoñombo'e.":
#     #     print(l)
#     if l.strip():
#         if l.strip() in para:
#             lines.remove(l)
#     if not l.strip():
#         lines.remove(l)


# # explanations = [l for l in lines if l not in para and l.strip()]
# explanations = lines

# with open('gua_non_parallel.txt', 'w', encoding='utf-8') as f:
#     f.write("\n".join(explanations))


# print(lines)
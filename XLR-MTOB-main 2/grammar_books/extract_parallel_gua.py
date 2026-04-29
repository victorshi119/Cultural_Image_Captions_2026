# extract_parallel_gua.py

parallel = []
non_para = []

with open('grammar_guarani.md', 'r') as f:
    lines = f.readlines()

import re

def extract_parallel_and_explanations(file_path):
    parallel = []
    explanations = []

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # lines = [l.strip() for l in lines]

    temp_block = []  # Temporary storage for potential parallel examples
    collecting_parallel = False  # Flag to track if we are collecting a parallel example
    buffer = []  # Buffer to hold lines preceding the English translation

    for line in lines:
        stripped = line.strip()

        # Check for English translation (lines enclosed in single quotes)
        if stripped.startswith("'"):
            # English translation found: Start or continue a parallel block
            collecting_parallel = True
            temp_block = buffer + [line]  # Include buffered lines + current line
            buffer = []  # Clear the buffer after using it

        elif collecting_parallel:
            # Collect additional lines until a blank line signals the end
            if stripped:
                temp_block.append(line)
            else:
                # Blank line: Finalize the block
                parallel.append("".join(temp_block))
                temp_block = []
                collecting_parallel = False

        elif stripped:
            # Buffer lines to check if they belong to a parallel example
            if stripped:
                buffer.append(line)
                if len(buffer) > 3:  # Keep only the last 2 lines in the buffer
                    buffer.pop(0)
            elif line.strip():
                    explanations.append(line)
                
            # else:
            #     # Blank line: Non-parallel explanatory content
            #     if line.strip() and not collecting_parallel:
            #         explanations.append(line)

    # Final block check
    if collecting_parallel and temp_block:
        parallel.append("".join(temp_block))
    elif buffer:  # Include buffered lines as explanation if no parallel follows
        explanations.extend(buffer)

    return parallel, explanations, lines


# Example usage:
parallel, _, lines = extract_parallel_and_explanations('grammar_guarani_filtered.md')

# print(parallel[0])



# Write results to separate files if needed
with open('gua_parallel.txt', 'w', encoding='utf-8') as f:
    parallel = [p.strip() for p in parallel]
    f.write("\n".join(parallel))

with open('gua_parallel.txt', 'r', encoding='utf-8') as f:
    para = f.readlines()
    para = [l.strip() for l in para]

# print(para[0])

expl_lines = [l.strip() for l in lines if l.strip()]
with open('gua_non_parallel.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(expl_lines))

with open('gua_non_parallel.txt', 'r', encoding='utf-8') as f:
    expl = f.readlines()
    expl = [l.strip() for l in expl]

unique_lines = [line for line in expl if line.strip() not in para]
print(unique_lines[:500])

with open('gua_non_parallel.txt', 'w', encoding='utf-8') as output_file:
    # output_file.writelines(unique_lines)
    output_file.write("\n".join(unique_lines))




for l in lines:
    # print(l)
    # if l == "Reporomoñombo'e.":
    #     print(l)
    if l.strip():
        if l.strip() in para:
            lines.remove(l)
    if not l.strip():
        lines.remove(l)


# explanations = [l for l in lines if l not in para and l.strip()]
explanations = lines

# with open('gua_non_parallel.txt', 'w', encoding='utf-8') as f:
#     f.write("\n".join(explanations))


# print(lines)
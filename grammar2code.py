#grammar to code
import os 
import re
import time
from openai import OpenAI
import argparse
reallms_base_url = "https://reallms.rescloud.iu.edu/direct/v1"

convo_prompt = """\
You are a computational linguist converting a grammar book section into a code-format rule.

Given a section of a Paraguayan Guaraní grammar book, write a Python pseudocode function that:
1. Has a descriptive function name (snake_case) capturing the rule
2. Has a docstring summarizing the rule in 1-2 sentences
3. Shows the rule as procedural logic (conditions, morpheme operations, word order)
4. Includes 1-2 brief Guaraní examples as comments with English translation
5. Is concise — max 30 lines

Focus only on the CORE grammatical rule. Skip historical notes, lengthy explanations, and irrelevant examples.
Output ONLY the Python function, no markdown fences, no extra text.

Grammar section:
{section}
"""

def parse_section(path: str):
    #takes in grammar books return gammar section by section
    with open(path,encoding="utf-8") as f:
        lines = f.readlines()

    sections = []
    current_header = None
    current_lines = []

    for line in lines:
        if line.startswith("### "):
            if current_header is not None:
                sections.append((current_header,"".join(current_lines)))
            current_header = line.strip()
            current_lines = []

        elif (current_header is not None):
            current_lines.append(line)

    if current_header is not None:
        sections.append((current_header,"".join(current_lines)))
    #grammar rules start from chapter 3 onwards
    relevant = []
    for header, content in sections:
        match = re.search(r"### (\d+)",header)
        if match and int(match.group(1)) >= 3:
            relevant.append((header,content))


    return relevant

def section_to_code(client: OpenAI, header: str, content: str, model: str):
    section_text = f"{header}\n{content}"
    prompt = convo_prompt.format(section=section_text)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role":"user","content":prompt}],
        max_tokens=600,
    ) 
    return response.choices[0].message.content.strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model",default="gemma-4-31B-it")
    parser.add_argument("--output",default=None)

    args = parser.parse_args()

    #get the api key that is saved in the env
    api_key = os.environ.get("REALLMS_API_KEY")
    client = OpenAI(api_key=api_key,base_url=reallms_base_url)

    grammar_path = "resources/grammar_guarani_proc_filt.md" # already filter grammar book by Estigarribia/ Aycock et al.
    model_slug = args.model.replace("/","_").replace("-")
    output_path = args.output or f"resources/grammar_code_rules_{model_slug}.py"

    sections = parse_section(grammar_path)

    results = []
    for i, (header,content) in enumerate(sections, 1):
        code = section_to_code(client,header,content,model=args.model)
        results.append(f"# === {header} ===\n{code}\n")
        time.sleep(0.5)

    with open(output_path,"w",encoding="utf-8") as f:
        f.write('"""\nCode-format grammar rules for Paraguayan Guaraní.\nAuto-generated from grammar_guarani_proc_filt.md.\n"""\n\n')
        f.write("\n".join(results))

if __name__ == "__main__":
    main()


import re
import markdown
from bs4 import BeautifulSoup
import pydetex.pipelines as pip



def latex_to_plaintext(latex_md):
    # Convert Markdown to HTML
    # html = markdown.markdown(latex_md)
    
    # # Parse HTML and extract text
    # soup = BeautifulSoup(html, 'html.parser')
    
    # # Get text from HTML
    # text = soup.get_text()
    
    text = latex_md

    # Remove LaTeX math expressions (inline and block)
    # text = re.sub(r'\$\$.*?\$\$', '', text, flags=re.DOTALL)  # Block math
    # text = re.sub(r'\$.*?\$', '', text)  # Inline math
    
    # # Remove LaTeX commands starting with backslashes, including the backslash
    # text = re.sub(r'\\[a-zA-Z]+\{.*?\}', '', text)  # Remove commands with braces
    # text = re.sub(r'\\[a-zA-Z]+', '', text)  # Remove commands without braces
    # text = text.replace("{", "").replace("}", "")
    text = text.replace("\\", "")
    text = text.replace("{", "(").replace("}", ")")

    # text = text.replace("\n", " ")

    # text = text.replace("\\", " ")
    # text = text.replace('/', '').replace('\\', '\\\\')

    return text


# def latex_to_plaintext(input_file):
#     # Open the input file and read its contents
#     with open(input_file, 'r', encoding='utf-8') as infile:
#         text = infile.read()

#     # latex_command_pattern = r'\\[a-zA-Z]+\*?\{[^}]*\}|\[.*?\]|\\[a-zA-Z]+\s*\{.*?\}|\%.*?$|\\begin\{.*?\}.*?\\end\{.*?\}'



#     # Remove LaTeX commands and environments
#     cleaned_text = re.sub(latex_command_pattern, '', text, flags=re.DOTALL | re.MULTILINE)


#     return cleaned_text 


with open("../grammar_books/gua_parallel.txt", "r", encoding='utf-8') as f:
    lines = f.readlines()
lines = "".join(lines)
out=latex_to_plaintext(lines)
# out = pip.simple(lines)
with open('../grammar_books/gua_parallel_proc.txt', 'w') as f:
    f.write(out)

with open("../grammar_books/gua_non_parallel.txt", "r") as f:
    lines = f.readlines()
lines = "".join(lines)
out=latex_to_plaintext(lines)
# out = pip.simple(lines)
with open('../grammar_books/gua_non_parallel_proc.txt', 'w', encoding='utf-8') as f:
    f.write(out)
# print(out)

with open("/home/saycock/personal/mtob/grammar_books/grammar_guarani_proc_filt.md", "r") as f:
    lines = f.readlines()
lines = "".join(lines)
out=latex_to_plaintext(lines)
# out = pip.simple(lines)
with open('../grammar_books/gua_full_proc.txt', 'w', encoding='utf-8') as f:
    f.write(out)
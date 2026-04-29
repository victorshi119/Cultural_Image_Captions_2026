from string import punctuation
import re

def replace_textsc_with_uppercase(latex_content):
    pattern = r'\\textsc\{(.*?)\}'
    def to_uppercase(match):
        return f"\\textsc{{{match.group(1).upper()}}}"
    updated_content = re.sub(pattern, to_uppercase, latex_content)
    return updated_content

replacement={
    "\glkin": "VOL",
    "\glme": "TOP",
    "\glhe": "IAM",
    "\glteba": "PROG",
    "\glte": "NFIN",
    "\glta": "NFIN",
    "\glra": "RA",
    "\glse": "IAM",
    "\glet": "IRR",
    "\glkinp": "POSS",
    "\gli": "PLNL",
    "\glnn": "N",
    "\glp": "DISTR",
    "\glmambon": "EXIST",
    "\glopa": "ANA",
    "\gltt": "T",
    "\glba": "FOC",
    "\glcond": "COND",
    "\glten": "TEN"
}

with open("/home/saycock/personal/mtob/resources/grammar_book_corrected.tex", "r") as f, open("/home/saycock/personal/mtob/resources/grammar_book.txt", "r") as g, open("/home/saycock/personal/mtob/resources/grammar_book_corrected.txt", "w") as h:
    corrected_latex = f.read().splitlines()
    book_txt = g.read().splitlines()
    corrected_txt = []

    corrected_lines = []
    search_lines = []

    punctuation = punctuation.replace("-","").replace("=","").replace("∼", "").replace(".","").replace("&", "")

    for c, line in enumerate(corrected_latex):
        # check if any of replacement keys are in the line
        if any(word in line for word in replacement.keys()):
            line1 = line
            line2 = line
            # replace any instance of key with value in line without splitting
            for key, value in replacement.items():
                line2 = line2.replace(key, value)
            line_replaced = line2
            # print(line_replaced)
            
            for key in replacement.keys():
                line1 = line1.replace(key, "")
            line_del = line1
            # print(line_del)

            # make anything inside textsc{x} uppercase
            line_replaced = replace_textsc_with_uppercase(line_replaced)
            # remove any punctuation in line not in "-=∼"
            line_replaced = line_replaced.replace("textsc", "").replace("textbf", "").replace("textit", "").replace("textcolor\{red\}", "").replace("textcolor\{blue\}", "").replace("textcolor\{lsLightWine\}", "").replace("textcolor\{lsLightWine\}", "")
            line_replaced = "".join([char for char in line_replaced if char not in punctuation])

            corrected_lines.append(line_replaced)


            line_del = line_del.replace("textsc", "").replace("textbf", "")
            line_del = "".join([char for char in line_del if char not in punctuation])
            search_lines.append(line_del)

        elif "textsc" in line and "\\\\" in line and "&" not in line:
            # print(line)
            line_replaced = replace_textsc_with_uppercase(line)
            line_replaced = line_replaced.replace("textsc", "").replace("textbf", "").replace("textit", "")
            line_replaced = "".join([char for char in line_replaced if char not in punctuation])
            corrected_lines.append(line_replaced)
            line_del = line.replace("textsc", "").replace("textbf", "").replace("textit", "")
            line_del = "".join([char for char in line_del if char not in punctuation])
            search_lines.append(line_del)
            # print(line_replaced)
        
        elif "textcolor" in line and "\\\\" in line and "&" not in line:
            print(line)
            line1 = line.replace("\ex", "").replace("\gll", "").replace("\glt", "")
            line_replaced = line1.replace("textcolor{red}", "").replace("textcolor{blue}", "").replace("textcolor{lsLightWine}", "").replace("textcolor{lsLightWine}", "")
            line_replaced = "".join([char for char in line_replaced if char not in punctuation])
            corrected_lines.append(line_replaced)
            line_del = line.replace("textcolor{red}", "").replace("textcolor{blue}", "").replace("textcolor{lsLightWine}", "").replace("textcolor{lsLightWine}", "")
            line_del = "".join([char for char in line_del if char not in punctuation])
            line_del = line_replaced.replace("-t=", "-=").replace("-n-", "--").replace("-t-", "--").strip()
            search_lines.append(line_del)
            print(line_del)
            print(line_replaced)
            
    matches = 0
    
    print(len(search_lines))

    updated_book_lines = {}
    
    for c, line in enumerate(search_lines):

        line_split = line.lower().split()
        # print(line_split)

        for book_count, book_line in enumerate(book_txt):
            book_split = book_line.lower().split()
            if line_split == book_split:
                # print(line_split)
                matches += 1
                updated_book_lines[book_count] = corrected_lines[c].strip()
            # if line_split in book_line.lower():
            #     print(line)
            #     print(book_line)
            #     print("\n")
            #     corrected_txt.append(book_line)
            #     break
            
                
    # print(matches)
    # print(updated_book_lines)

    # also address non-changed lines that need uppercasing

    for c, line in enumerate(book_txt):
        if c in list(updated_book_lines.keys()):
            h.write(updated_book_lines[c] + "\n")
        else:
            h.write(line + "\n")

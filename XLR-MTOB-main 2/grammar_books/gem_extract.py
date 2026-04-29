# gem_extract.py

def extract_parallel_examples(text):
  """
  Extracts parallel Guarani examples, gloss, English translation, and explanations.

  Args:
      text: A string containing Guarani text.

  Returns:
      A tuple of four lists:
          - examples: List of Guarani sentences.
          - glosses: List of glosses corresponding to the examples.
          - english: List of English translations corresponding to the examples.
          - explanations: List of explanations for each example.
  """
  examples = []
  glosses = []
  english = []
  explanations = []
  current_example = ""
  current_gloss = ""
  current_english = ""
  current_explanation = ""
  in_explanation = False
  in_english = False  # Flag to track English lines
  for line in text.splitlines():
    line = line.strip()
    if not line:
      # Empty line, save the current example, gloss, english and explanation
      if current_example:
        examples.append(current_example.strip())
        glosses.append(current_gloss.strip())
        if current_english:
          english.append(current_english.strip())
        explanations.append(current_explanation.strip())
        current_example = ""
        current_gloss = ""
        current_english = ""
        current_explanation = ""
    elif line.startswith("##"):
      # Explanation section, switch flag
      in_explanation = True
      in_english = False
    elif line.startswith("'"):
      # English line, potentially following Guarani and gloss
      in_english = True
      if current_example and current_gloss:
        # Capture the previous 2-3 lines (assuming max 3 lines for Guarani/gloss)
        previous_lines = text.splitlines()[-4:]  # Get the last 4 lines
        guarani_part = "\n".join([line for line in previous_lines if not line.startswith("'")])
        examples.append(guarani_part.strip())
        glosses.append(current_gloss.strip())
        current_gloss = ""
        english.append(line.strip())
      else:
        current_english = line.strip()
    else:
      if in_explanation:
        current_explanation += line + "\n"
      else:
        # Guarani or gloss line
        if in_english:
          current_gloss += line + "\n"
        else:
          current_example += line + "\n"
  # Check for the last example, gloss and english
  if current_example:
    examples.append(current_example.strip())
    glosses.append(current_gloss.strip())
    if current_english:
      english.append(current_english.strip())
  return examples, glosses, english, explanations

# Example usage
with open('grammar_guarani.md', 'r') as f:
    lines = f.read()
text = lines

examples, glosses, english, explanations = extract_parallel_examples(text)

print("Examples:")
for example in examples:
  print(example)

print("\nGlosses:")
for gloss in glosses:
  print(gloss)

print("\nEnglish:")
for e in english:
  print(e)

print("\nExplanations:")
for explanation in explanations:
  print(explanation)
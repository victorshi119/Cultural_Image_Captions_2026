#main
#takes in image then generate caption in target langauge (Guarani)
#use reallms api as backbone
import argparse
import base64
import json
import os
from pathlib import Path
from typing import Optional
from io import BytesIO
from PIL import Image
from openai import OpenAI
import re

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

GUARANI_SYSTEM_PROMPT = """You are an expert image captioning system for Paraguayan Guaraní culture.

Your task: Generate a single, factual caption in Paraguayan Guaraní (Avañe'ẽ) that describes only what is visually present in the image.

CAPTION RULES:
1. Describe ONLY what you can directly see — objects, people, settings, actions, colors, materials.
2. Do NOT include cultural interpretation, historical background, spiritual meaning, or symbolic significance.
3. Do NOT add context that is not visible in the image (e.g., where a drink is consumed, what a monument commemorates, why an object matters).
4. Name specific objects using their correct Guaraní or Spanish loanword terms if you can identify them with confidence.
5. If you cannot confidently identify a cultural object, describe its physical appearance instead.
6. Write entirely in Guaraní. Spanish loanwords are acceptable where natural in Guaraní speech.
7. Do NOT add explanations in English or Spanish.

CULTURAL OBJECT RECOGNITION REFERENCE:
Use this list only to correctly name objects you can visually identify — do not use it to add meaning or context.

Drink and Food:
- Tereré – cold herbal drink; served in a guampa (cow-horn or wooden cup) with a bombilla (metal straw)
  Distinguish from mate (hot version, served in a round gourd)
- Chipa – round cheese bread made from mandioca starch
- Sopa paraguaya – cornbread with cheese and onion (not a liquid soup)
- Mbejú – flat cassava bread
- Vori vori – soup with yellow cornmeal and cheese balls

Medicine and Markets:
- Pohã ñana / pohã ro'ysã – dried herbs and roots sold as traditional medicine; commonly found at Mercado 4, Asunción
  Distinguish from produce (yuca, plantain, vegetables)

Crafts:
- Ñandutí – circular spider-web lace, typically white or colorful
- Ao po'i – fine hand-embroidered fabric

Monuments and People:
- Las Residentas – monument depicting Paraguayan women from the War of the Triple Alliance
- San Blas – patron saint of Paraguay; statues typically hold a book and a candle

Festivals:
- Pelota tata – fireball football played during San Juan festivities
- Tata ári jehasa – fire-walking ritual

CAPTION FORMAT:
Write one to three sentences. Describe the main subject first, then notable details (materials, colors, location if a sign or landmark is visible).

EXAMPLE (correct style):
Image: A tereré set on a wooden fence
CORRECT: "Tereré ekípo oĩva poyvi ári peteĩ korapy yvýrayty mbytépe: peteĩ térmo vakapíregui mbojegua pyre, guámpa yvyragui ojejapopyréva ha vombílla kuarepotigui."
WRONG: "Un mate y su bombilla, bebida sagrada y social de los pueblos guaraníes, simbolizando conexión y hospitalidad ancestral."
"""

GUARANI_SYSTEM_PROMPT_V3 = """Eres un sistema de subtitulado de imágenes diseñado para describir imágenes con relevancia cultural para el pueblo Guaraní.

Tu tarea: Generar subtítulos concisos, respetuosos y culturalmente precisos (2-4 oraciones máximo).

CONTEXTO CULTURAL A RECONOCER:
Los guaraníes son un grupo de varios pueblos nativos sudamericanos que se ubican geográficamente en parte de Paraguay, noreste de Argentina (en las provincias de Corrientes, Entre Ríos, Formosa, Misiones y zonas del noreste de la actual Salta, donde se los ha conocido más como "chiriguanos"), sur y suroeste de Brasil (en los estados de Río Grande del Sur, Santa Catarina, Paraná y Mato Grosso del Sur) y sureste de Bolivia (en los departamentos de Tarija, Santa Cruz y Chuquisaca).

DIRECTRICES PARA SUBTÍTULOS CONCISOS:

1. Sé breve y directo:
   - Máximo 2-4 oraciones
   - Identifica primero lo visible
   - Añade solo el contexto cultural esencial
   - Omite detalles secundarios

2. Estructura simple:
   "[Qué se ve]. [Significado/uso cultural]. [Contexto breve si es necesario]."

3. Mantén respeto cultural:
   - No trivialices elementos sagrados
   - Reconoce la cultura como viva y contemporánea

Genera subtítulos concisos siguiendo este formato."""



# v4: Victor's minimal edit of the AmericasNLP committee prompt (v3)
GUARANI_SYSTEM_PROMPT_V4 = """Eres un sistema de subtitulado de imágenes diseñado para describir imágenes con relevancia cultural para el pueblo Guaraní.

Tu tarea: Generar subtítulos concisos, respetuosos y culturalmente precisos (2-4 oraciones máximo).

CONTEXTO CULTURAL A RECONOCER:
Los guaraníes son un grupo de varios pueblos nativos sudamericanos que se ubican geográficamente en parte de Paraguay, noreste de Argentina (en las provincias de Corrientes, Entre Ríos, Formosa, Misiones y zonas del noreste de la actual Salta, donde se los ha conocido más como "chiriguanos"), sur y suroeste de Brasil (en los estados de Río Grande del Sur, Santa Catarina, Paraná y Mato Grosso del Sur) y sureste de Bolivia (en los departamentos de Tarija, Santa Cruz y Chuquisaca).

DIRECTRICES PARA SUBTÍTULOS CONCISOS:

1. Sé breve y directo:
   - Máximo 2-4 oraciones
   - Identifica primero lo visible
   - Añade solo el contexto cultural esencial
   - Omite detalles secundarios

2. Mantén el contenido basado en lo observable:
   - No infieras usos, significados o funciones que no sean claramente visibles
   - Evita sobre-interpretaciones culturales o históricas
   - El contexto cultural debe estar directamente conectado con lo que se ve en la imagen

3. Estructura simple:
   "[Qué se ve], [con una breve mención de su uso o significado si es evidente en la imagen]."
   - El significado cultural debe integrarse como parte de la descripción, no como una explicación separada

4. Mantén respeto cultural:
   - No trivialices elementos sagrados
   - Reconoce la cultura como viva y contemporánea

Genera subtítulos concisos siguiendo este formato."""

reallms_base_url = "https://reallms.rescloud.iu.edu/direct/v1"

prompt_version = {
    "v2":GUARANI_SYSTEM_PROMPT, 
    "v3":GUARANI_SYSTEM_PROMPT_V3,
    "v4":GUARANI_SYSTEM_PROMPT_V4,
}

CAPTION_INSTRUCTION = "Embojera ko ta'ãnga guaraníme, iñemíva teko paraguaigua rehe. (Caption this image in Guaraní, grounded in Paraguayan culture.)"

def _pil_to_data_url(img: Image.Image, fmt: str = "JPEG"):
    #helper to pass img to api
    buf = BytesIO()
    if fmt.upper() == "JPEG":
        img.save(buf, format="JPEG", quality=92)
        mime = "image/jpeg"
    else:
        img.save(buf, format="PNG")
        mime = "image/png"
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:{mime};base64,{b64}"

def _describe_image(image_path: str, client: OpenAI, model: str, lang: str = "English"):
    img = Image.open(image_path).convert("RGB")
    messages = [{"role": "user", "content": [
        {"type": "image_url", "image_url": {"url": _pil_to_data_url(img)}},
        {"type": "text", "text": f"Briefly describe what you see in this image in 1-2 {lang} sentences. Focus on objects, people, actions, and setting."},
    ]}]
    return client.chat.completions.create(
        model=model, messages=messages, max_tokens=80
    ).choices[0].message.content.strip()

def parse_grammar_sections(path: str) -> list[tuple[str, str]]:
    section_pat = re.compile(r"^#{1,3} \d")
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    chunks = []
    current_header = None
    current_lines = []
    for line in lines:
        if section_pat.match(line):
            if current_header and current_lines:
                chunks.append((current_header.strip(), "".join(current_lines).strip()))
            current_header = line.strip("# \n")
            current_lines = []
        elif current_header is not None:
            current_lines.append(line)
    if current_header and current_lines:
        chunks.append((current_header.strip(), "".join(current_lines).strip()))
    return chunks

def build_grammar_bm25(chunks: list[tuple[str, str]]):
    from rank_bm25 import BM25Okapi
    corpus = []
    for header, content in chunks:
        text = header + " " + content
        tokens = re.findall(r"[a-zA-Záéíóúñãẽĩõũ]+", text.lower())
        corpus.append(tokens)
    return BM25Okapi(corpus)

def retrieve_grammar_sections(image_path: str, chunks: list[tuple[str, str]], bm25, client: OpenAI, model: str, top_k: int = 5, desc: Optional[str] = None):
    if desc is None:
        desc = _describe_image(image_path, client, model, lang="English")
    query_tokens = re.findall(r"[a-zA-Záéíóúñãẽĩõũ]+", desc.lower())
    scores = bm25.get_scores(query_tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    top_indices = sorted(top_indices)
    lines = ["SECCIONES DE GRAMÁTICA GUARANÍ RELEVANTES:"]
    for i in top_indices:
        header, content = chunks[i]
        # cap each section at 300 chars to avoid overflow
        lines.append(f"### {header}\n{content[:300]}")
    return "\n\n".join(lines)

def build_flores_bm25(pairs: list[dict]):
    from rank_bm25 import BM25Okapi
    corpus = []
    for p in pairs:
        text = p["en"] + " " + p.get("es", "")
        tokens = re.findall(r"[a-zA-Záéíóúñãẽĩõũ]+", text.lower())
        corpus.append(tokens)
    return BM25Okapi(corpus)

def retrieve_flores_by_image(image_path: str, pairs: list[dict], bm25, client: OpenAI, model: str, top_k: int = 100, desc: Optional[str] = None):
    if desc is None:
        desc = _describe_image(image_path, client, model, lang="English")
    query_tokens = re.findall(r"[a-zA-Záéíóúñãẽĩõũ]+", desc.lower())
    scores = bm25.get_scores(query_tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    top_indices = sorted(top_indices)
    lines = ["EJEMPLOS DE ORACIONES DE GUARANÍ (pares naturales EN→GN para referencia):"]
    for i in top_indices:
        p = pairs[i]
        lines.append(f"English: {p['en']}")
        lines.append(f"Guaraní: {p['gn']}")
        lines.append("")
    return "\n".join(lines)

def load_dampy_spanish_entries(spanish_captions_dir: str, guarani_captions_path: str) -> list[dict]:
    # load guarani captions
    id_to_guarani = {}
    for line in Path(guarani_captions_path).read_text().splitlines():
        if "\t" in line:
            stem, caption = line.split("\t", 1)
            id_to_guarani[stem] = caption

    # load all _es.tsv files from the dir
    entries = []
    for tsv in sorted(Path(spanish_captions_dir).glob("*_es.tsv")):
        category = tsv.stem.replace("guarani_", "").replace("_captions_es", "").capitalize()
        for line in tsv.read_text().splitlines():
            if "\t" not in line:
                continue
            stem, spanish = line.split("\t", 1)
            guarani = id_to_guarani.get(stem)
            if guarani:
                entries.append({"stem": stem, "spanish": spanish, "guarani": guarani, "category": category})
    return entries

def build_dampy_bm25(entries: list[dict]):
    from rank_bm25 import BM25Okapi
    corpus = [re.findall(r"[a-zA-Záéíóúñãẽĩõũ]+", e["spanish"].lower()) for e in entries]
    return BM25Okapi(corpus)

def retrieve_dampy_bm25(spanish_desc: str, entries: list[dict], bm25, top_k: int = 5) -> str:
    query_tokens = re.findall(r"[a-zA-Záéíóúñãẽĩõũ]+", spanish_desc.lower())
    scores = bm25.get_scores(query_tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    lines = ["EJEMPLOS DE REFERENCIA (descripción → subtítulo guaraní):"]
    for i in top_indices:
        e = entries[i]
        lines.append(f"\n• Descripción: {e['spanish']}")
        lines.append(f"  Subtítulo: {e['guarani']}")
    lines.append("\n---")
    lines.append("Para la imagen actual, genera ÚNICAMENTE el subtítulo en guaraní.")
    return "\n".join(lines)

def load_trilingual_entries(jsonl_path: str, images_dir: str) -> list[dict]:
    entries = []
    images_dir = Path(images_dir)
    for line in Path(jsonl_path).read_text().splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        img_path = images_dir / Path(obj["filename"]).name
        if img_path.exists():
            entries.append({
                "stem": obj["id"],
                "spanish": obj["spanish_caption"],
                "guarani": obj["target_caption"],
                "img_path": str(img_path),
            })
    return entries

def retrieve_dev_visual_bm25(spanish_desc: str, entries: list[dict], bm25, top_k: int = 5) -> list[tuple]:
    query_tokens = re.findall(r"[a-zA-Záéíóúñãẽĩõũ]+", spanish_desc.lower())
    scores = bm25.get_scores(query_tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    return [(Image.open(entries[i]["img_path"]).convert("RGB"), entries[i]["guarani"]) for i in top_indices]

#-- end code generation rag function helper --#
def load_culture_knowledge(path: str):
    with open(path,"r",encoding="utf-8") as f:
        return f.read().strip()


def load_interlinear(path: str, n:int):
    header = "EJEMPLOS INTERLINEALES DE GUARANÍ (desglose de morfemas + glosa + inglés):"
    with open(path,"r",encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return header + "\n" + "\n".join(lines[:n])

def load_grammar_parallel(path: str, n:int):
    header = "EJEMPLOS DE ORACIONES DE GUARANÍ (de libro de gramática):"
    with open(path,"r",encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return header + "\n" + "\n".join(lines[:n])

def load_parallel_examples(path: str, n:int):
    with open(path,"r",encoding="utf-8") as f:
        pairs = json.load(f)

    sampled = pairs[:n]
    lines = ["EJEMPLOS DE ORACIONES DE GUARANÍ (pares naturales EN→GN para referencia):"]
    for p in sampled:
        lines.append(f"English: {p['en']}")
        lines.append(f"Guaraní: {p['gn']}")
        lines.append("")

    return "\n".join(lines)

def load_grammar_book(path: str, n: int):
    header = "REFERENCIA DE GRAMÁTICA GUARANÍ (libro de gramática):"
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return header + "\n" + "\n".join(lines[:n])

# fixed syntax after manual edit broke filter placement
def load_dampy_visual_pairs(images_dir, captions_path, n=0, n_per_category=0):
    # images_dir:      root with subfolders Comida/, Fauna/, Flora/
    #                  each subfolder has item dirs, each item dir has one image
    # captions_path:   TSV with lines  "item_id\tGuarani caption"
    # n:               total pairs to return (flat mode, used when n_per_category=0)
    # n_per_category:  if >0, take this many pairs from each category subfolder

    # build id -> caption lookup from the TSV (skip section headers with no tab)
    id_to_caption = {}
    for line in Path(captions_path).read_text().splitlines():
        if "\t" in line:
            img_id, caption = line.split("\t", 1)
            id_to_caption[img_id] = caption

    # load image + caption for a given path; stem (filename without ext) is the shared key
    def load(p):
        return Image.open(p).convert("RGB"), id_to_caption[p.stem]

    if n_per_category > 0:
        if n > 0:
            print(f"Warning: --num_dampy_shots ({n}) is ignored when --num_dampy_shots_per_category ({n_per_category}) is set")
        pairs = []
        for cat in sorted(p for p in Path(images_dir).iterdir() if p.is_dir()):
            imgs = sorted(p for p in cat.rglob("*") if p.suffix.lower() in IMAGE_EXTENSIONS and p.stem in id_to_caption)
            pairs += [load(p) for p in imgs[:n_per_category]]
        return pairs

    # flat mode: collect all matched images across categories, return first n
    imgs = [p for p in Path(images_dir).rglob("*") if p.suffix.lower() in IMAGE_EXTENSIONS and p.stem in id_to_caption]
    return [load(p) for p in imgs[:n]]

def load_dampy_text_captions(images_dir, captions_path, n_per_category):
    # same per-category selection as load_dampy_visual_pairs but returns caption text only
    # images_dir used only to determine which IDs exist and their category order
    # returns a formatted string ready to append to the system prompt
    id_to_caption = {}
    for line in Path(captions_path).read_text().splitlines():
        if "\t" in line:
            img_id, caption = line.split("\t", 1)
            id_to_caption[img_id] = caption

    lines = ["EJEMPLOS DE SUBTÍTULOS EN GUARANÍ (pares de referencia):"]
    for cat in sorted(p for p in Path(images_dir).iterdir() if p.is_dir()):
        imgs = sorted(p for p in cat.rglob("*") if p.suffix.lower() in IMAGE_EXTENSIONS and p.stem in id_to_caption)
        for p in imgs[:n_per_category]:
            lines.append(f"{p.stem}: {id_to_caption[p.stem]}")
    return "\n".join(lines)

def load_apertium_summary(path: str, chars:int):
    with open(path,"r",encoding="utf-8") as f:
        text = f.read(chars)
    if len(text) == chars:
        idx = text.rfind("\n")
        if idx != -1:
            text = text[:idx]

    return text
def build_system_prompt(
    base_prompt: str,
    parallel_path: Optional[str] = None,
    num_parallel: Optional[int] = None,
    interlinear_path: Optional[str] = None,
    num_interlinear: Optional[int] = None,
    grammar_parallel_path: Optional[str] = None,
    num_grammar_parallel: Optional[int] = None,
    apertium_path: Optional[str] = None,
    apertium_chars: Optional[int] = 15000,
    culture_knowledge_path: Optional[str] = None,
    grammar_book_path: Optional[str] = None,
    num_grammar_book: Optional[int] = None,
):
    prompt = base_prompt

    # 1. Cultural context
    if culture_knowledge_path:
        prompt += "\n" + load_culture_knowledge(culture_knowledge_path)

    # 2. Linguistic reference (morphology / rules)
    if apertium_path:
        prompt += "\n" + load_apertium_summary(apertium_path, apertium_chars)

    # 3. Grammar and structure examples
    if grammar_book_path:
        prompt += "\n" + load_grammar_book(grammar_book_path, num_grammar_book)

    if grammar_parallel_path:
        prompt += "\n" + load_grammar_parallel(grammar_parallel_path, num_grammar_parallel)

    if interlinear_path:
        prompt += "\n" + load_interlinear(interlinear_path, num_interlinear)

    # 4. Parallel examples — closest to the task, we placed last
    if parallel_path:
        prompt += "\n" + load_parallel_examples(parallel_path, num_parallel)

    return prompt
    
# def generate_caption(image_path: str, system_prompt: str,caption_prompt: str,client: OpenAI, model: str):
#     test_image = Image.open(image_path).convert("RGB")
#     messages = [{"role":"system","content":system_prompt}]
#     messages.append(
#         {
#             "role":"user",
#             "content": [
#                 {"type":"image_url","image_url": {"url": _pil_to_data_url(test_image)}},
#                 {"type":"text","text":caption_prompt}
#             ]
#         }
#     )
#     response = client.chat.completions.create(model=model,messages=messages,max_tokens=512)
#     return response.choices[0].message.content.strip()

def generate_caption(image_path: str, system_prompt: str, caption_prompt: str, client: OpenAI, model: str,
                     few_shot_pairs: Optional[list] = None):
    test_image = Image.open(image_path).convert("RGB")
    messages = [{"role": "system", "content": system_prompt}]
    for ex_img, ex_caption in (few_shot_pairs or []):
        messages.append({"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": _pil_to_data_url(ex_img)}},
            {"type": "text", "text": caption_prompt},
        ]})
        messages.append({"role": "assistant", "content": ex_caption})
    messages.append({"role": "user", "content": [
        {"type": "image_url", "image_url": {"url": _pil_to_data_url(test_image)}},
        {"type": "text", "text": caption_prompt},
    ]})
    response = client.chat.completions.create(model=model, messages=messages, max_tokens=512)
    return response.choices[0].message.content.strip()


def run_captioning(
    image_paths: list[Path],
    output_file: str,
    system_prompt: str,
    client: OpenAI,
    model_name: str,
    grammar_chunks: Optional[list] = None,
    grammar_bm25=None,
    grammar_bm25_top_k: Optional[int] = 5,
    flores_pairs: Optional[list] = None,
    flores_bm25=None,
    flores_bm25_top_k: Optional[int] = 100,
    dampy_bm25_entries: Optional[list] = None,
    dampy_bm25=None,
    dampy_bm25_top_k: Optional[int] = 5,
    culture_chunks: Optional[list] = None,
    culture_bm25=None,
    culture_bm25_top_k: Optional[int] = 5,
    dev_entries: Optional[list] = None,
    dev_bm25=None,
    dev_bm25_text_top_k: Optional[int] = 0,
    dev_bm25_visual_top_k: Optional[int] = 0,
    few_shot_pairs: Optional[list] = None,
):
    results = []
    for img_path in image_paths:
        img_name = img_path.name
        per_img_prompt = system_prompt

        # compute image descriptions once and reuse across BM25 retrievers
        needs_desc = grammar_bm25 is not None or flores_bm25 is not None
        img_desc = _describe_image(str(img_path), client, model_name) if needs_desc else None
        needs_desc_es = dampy_bm25 is not None or dev_bm25 is not None or culture_bm25 is not None
        img_desc_es = _describe_image(str(img_path), client, model_name, lang="Spanish") if needs_desc_es else None

        if grammar_bm25 is not None:
            grammar_retrieved = retrieve_grammar_sections(image_path=str(img_path),chunks=grammar_chunks,bm25=grammar_bm25,client=client,model=model_name,top_k=grammar_bm25_top_k,desc=img_desc)
            per_img_prompt+="\n"+grammar_retrieved
        if flores_bm25 is not None:
            flores_retrieved = retrieve_flores_by_image(image_path=str(img_path),pairs=flores_pairs,bm25=flores_bm25,client=client,model=model_name,top_k=flores_bm25_top_k,desc=img_desc)
            per_img_prompt+="\n"+flores_retrieved
        if culture_bm25 is not None:
            culture_retrieved = retrieve_grammar_sections(image_path=str(img_path),chunks=culture_chunks,bm25=culture_bm25,client=client,model=model_name,top_k=culture_bm25_top_k,desc=img_desc_es)
            per_img_prompt+="\n"+culture_retrieved
        if dampy_bm25 is not None:
            dampy_retrieved = retrieve_dampy_bm25(img_desc_es, dampy_bm25_entries, dampy_bm25, dampy_bm25_top_k)
            per_img_prompt+="\n"+dampy_retrieved
        if dev_bm25 is not None and dev_bm25_text_top_k > 0:
            dev_retrieved = retrieve_dampy_bm25(img_desc_es, dev_entries, dev_bm25, dev_bm25_text_top_k)
            per_img_prompt+="\n"+dev_retrieved

        dev_few_shot = None
        if dev_bm25 is not None and dev_bm25_visual_top_k > 0:
            dev_few_shot = retrieve_dev_visual_bm25(img_desc_es, dev_entries, dev_bm25, dev_bm25_visual_top_k)
        combined_few_shot = (few_shot_pairs or []) + (dev_few_shot or [])

        caption = generate_caption(str(img_path), system_prompt=per_img_prompt, client=client, model=model_name,
                                   caption_prompt=CAPTION_INSTRUCTION, few_shot_pairs=combined_few_shot or None)
        results.append((img_name, caption))

    if output_file:
        out = Path(output_file)
        out.parent.mkdir(parents=True,exist_ok=True)
        with open(out, "w",encoding="utf-8") as f:
            for img_id, caption in results:
                f.write(f"{img_id}\t{caption.replace(chr(10), ' ').replace(chr(13), ' ')}\n")
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image_dir",type=str,help="Folder of test images to caption")
    parser.add_argument("--model",type=str,default="gemma-4-31B-it",help="model for inference")
    parser.add_argument("--output",type=str,default="generated_captions.tsv")
    parser.add_argument("--prompt_version",type=str,choices=list(prompt_version.keys()),default="v4",help="base prompt version (v4 performs best)")
    parser.add_argument("--parallel_examples",type=str,default=None,help="path to en-gn parallel json (flores) flores_dev_examples_en-gn.json")
    parser.add_argument("--num_parallel",type=int,default=10,help="Number of FLORES EN-GN pairs to inject into the system prompt")
    parser.add_argument("--interlinear",type=str,default=None,help="path to interlinear file (gua_para.txt)")
    parser.add_argument("--num_interlinear",type=int,default=8,help="number of interlinear blocks to inject")
    parser.add_argument("--grammar_parallel",type=str,default=None,help="path to grammar book parallel examples ie. gua_parallel.txt")
    parser.add_argument("--num_grammar_parallel",type=int,default=5,help="number of grammar book parallel pairs to inject")
    parser.add_argument("--culture_knowledge",type=str,default=None,help="path to guarani culture knowledge (static injection)")
    parser.add_argument("--culture_bm25",type=str,default=None,help="path to culture knowledge file for per-image BM25 retrieval (queries in Spanish)")
    parser.add_argument("--culture_bm25_top_k",type=int,default=5,help="number of culture knowledge sections to retrieve per image")
    parser.add_argument("--apertium",type=str,default=None,help="path to summary of apertium morphology apertium_grn_summary.txt")
    parser.add_argument("--apertium_chars",type=int,default=15000,help="number of characters to take from apertium summary")
    parser.add_argument("--grammar_book",type=str,default=None,help="path to grammar book file")
    parser.add_argument("--num_grammar_book",type=int,default=50,help="number of lines to take from grammar book")
    parser.add_argument("--grammar_book_bm25",type=str,default=None,help="path to grammar book for per-image BM25 retrieval")
    parser.add_argument("--grammar_book_bm25_top_k",type=int,default=5,help="number of grammar sections to retrieve per image")
    parser.add_argument("--flores_bm25",type=str,default=None,help="path to flores JSON for per-image BM25 retrieval")
    parser.add_argument("--flores_bm25_top_k",type=int,default=100,help="number of flores pairs to retrieve per image")
    parser.add_argument("--dev_jsonl",type=str,default=None,help="path to dev trilingual JSONL for BM25 retrieval (e.g. data/dev/guarani/guarani_trilingual.jsonl)")
    parser.add_argument("--dev_images_dir",type=str,default=None,help="path to dev images dir (required with --dev_jsonl for visual few-shot)")
    parser.add_argument("--dev_bm25_text_top_k",type=int,default=0,help="if >0, inject this many dev Spanish-Guaraní text pairs per image via BM25")
    parser.add_argument("--dev_bm25_visual_top_k",type=int,default=0,help="if >0, use this many BM25-retrieved dev images as visual few-shot")
    parser.add_argument("--dampy_spanish_captions_dir",type=str,default=None,help="path to dir containing guarani_*_captions_es.tsv files for BM25 retrieval")
    parser.add_argument("--dampy_bm25_top_k",type=int,default=5,help="number of DAMPY Spanish-Guaraní pairs to retrieve per image")
    parser.add_argument("--dampy_images",type=str,default=None,help="path to dampy images root dir (subfolders: Comida/Fauna/Flora)")
    parser.add_argument("--dampy_captions",type=str,default=None,help="path to dampy caption tsv (id<tab>caption); required with --dampy_images")
    parser.add_argument("--num_dampy_shots",type=int,default=0,help="number of dampy image-caption few-shot examples to prepend (flat)")
    parser.add_argument("--num_dampy_shots_per_category",type=int,default=0,help="if >0, sample this many examples from each category subfolder instead of flat --num_dampy_shots")
    parser.add_argument("--num_dampy_text_shots_per_category",type=int,default=0,help="if >0, inject this many caption-only examples per category into the system prompt (no images)")
    args = parser.parse_args()
    
    api_key = os.environ.get("REALLMS_API_KEY")
    client = OpenAI(api_key=api_key,base_url=reallms_base_url)
    
    image_dir = Path(args.image_dir)
    image_paths = sorted(p for p in image_dir.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS)

    def to_path(a): return str(Path(a).expanduser()) if a else None # helper function to help deal with path 
    parallel_path = to_path(args.parallel_examples)
    interlinear_path = to_path(args.interlinear)
    grammar_parallel_path = to_path(args.grammar_parallel)
    apertium_path = to_path(args.apertium)
    culture_knowledge_path = to_path(args.culture_knowledge)
    grammar_book_path = to_path(args.grammar_book)

    base_prompt = prompt_version[args.prompt_version]

    system_prompt = build_system_prompt(
        parallel_path=parallel_path,
        num_parallel=args.num_parallel,
        interlinear_path=interlinear_path,
        num_interlinear=args.num_interlinear,
        grammar_parallel_path=grammar_parallel_path,
        num_grammar_parallel=args.num_grammar_parallel,
        apertium_path=apertium_path,
        apertium_chars=args.apertium_chars,
        base_prompt=base_prompt,
        culture_knowledge_path=culture_knowledge_path,
        grammar_book_path=grammar_book_path,
        num_grammar_book=args.num_grammar_book,
    )

    if args.grammar_book and args.grammar_book_bm25 and to_path(args.grammar_book) == to_path(args.grammar_book_bm25):
        print("Warning: --grammar_book and --grammar_book_bm25 point to the same file; grammar content will appear twice in the prompt")

    grammar_chunks, grammar_bm25_index = None, None
    if args.grammar_book_bm25:
        grammar_chunks = parse_grammar_sections(to_path(args.grammar_book_bm25))
        grammar_bm25_index = build_grammar_bm25(grammar_chunks)

    flores_all_pairs, flores_bm25_index = None, None
    if args.flores_bm25:
        with open(to_path(args.flores_bm25), "r", encoding="utf-8") as f:
            flores_all_pairs = json.load(f)
        flores_bm25_index = build_flores_bm25(flores_all_pairs)

    few_shot_pairs = None
    if args.dampy_images and args.dampy_captions and (args.num_dampy_shots > 0 or args.num_dampy_shots_per_category > 0):
        few_shot_pairs = load_dampy_visual_pairs(
            images_dir=to_path(args.dampy_images),
            captions_path=to_path(args.dampy_captions),
            n=args.num_dampy_shots,
            n_per_category=args.num_dampy_shots_per_category,
        )
        print(f"Loaded {len(few_shot_pairs)} dampy visual few-shot pairs")

    culture_chunks, culture_bm25_index = None, None
    if args.culture_bm25:
        culture_chunks = parse_grammar_sections(to_path(args.culture_bm25))
        culture_bm25_index = build_grammar_bm25(culture_chunks)
        print(f"Loaded {len(culture_chunks)} culture knowledge sections for BM25")

    dev_entries, dev_bm25_index = None, None
    if args.dev_jsonl and args.dev_images_dir and (args.dev_bm25_text_top_k > 0 or args.dev_bm25_visual_top_k > 0):
        dev_entries = load_trilingual_entries(
            jsonl_path=to_path(args.dev_jsonl),
            images_dir=to_path(args.dev_images_dir),
        )
        dev_bm25_index = build_dampy_bm25(dev_entries)
        print(f"Loaded {len(dev_entries)} dev entries for BM25")

    dampy_bm25_entries, dampy_bm25_index = None, None
    if args.dampy_spanish_captions_dir and args.dampy_captions:
        dampy_bm25_entries = load_dampy_spanish_entries(
            spanish_captions_dir=to_path(args.dampy_spanish_captions_dir),
            guarani_captions_path=to_path(args.dampy_captions),
        )
        dampy_bm25_index = build_dampy_bm25(dampy_bm25_entries)
        print(f"Loaded {len(dampy_bm25_entries)} DAMPY Spanish-Guaraní entries for BM25")

    if args.dampy_images and args.dampy_captions and args.num_dampy_text_shots_per_category > 0:
        dampy_text = load_dampy_text_captions(
            images_dir=to_path(args.dampy_images),
            captions_path=to_path(args.dampy_captions),
            n_per_category=args.num_dampy_text_shots_per_category,
        )
        system_prompt += "\n" + dampy_text
        print(f"Injected dampy text captions ({args.num_dampy_text_shots_per_category} per category) into system prompt")

    run_captioning(
        image_paths=image_paths,
        output_file=args.output,
        system_prompt=system_prompt,
        client=client,
        model_name=args.model,
        grammar_chunks=grammar_chunks,
        grammar_bm25=grammar_bm25_index,
        grammar_bm25_top_k=args.grammar_book_bm25_top_k,
        flores_pairs=flores_all_pairs,
        flores_bm25=flores_bm25_index,
        flores_bm25_top_k=args.flores_bm25_top_k,
        dampy_bm25_entries=dampy_bm25_entries,
        dampy_bm25=dampy_bm25_index,
        dampy_bm25_top_k=args.dampy_bm25_top_k,
        culture_chunks=culture_chunks,
        culture_bm25=culture_bm25_index,
        culture_bm25_top_k=args.culture_bm25_top_k,
        dev_entries=dev_entries,
        dev_bm25=dev_bm25_index,
        dev_bm25_text_top_k=args.dev_bm25_text_top_k,
        dev_bm25_visual_top_k=args.dev_bm25_visual_top_k,
        few_shot_pairs=few_shot_pairs,
    )
if __name__ == "__main__":
    main()

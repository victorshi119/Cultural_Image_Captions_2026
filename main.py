#main
#takes in image then generate caption in target langauge (Guarani)
#use reallms api as backbone
import argparse
import base64
from contextlib import contextmanager
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

#-- start code generate rag part --#
def parse_code_rules(path: str) -> list[tuple[str, str]]:
    #Parse code rules file into (section_header, code_block) pairs.
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    chunks = []
    for block in content.split("# === "):
        block = block.strip()
        if not block or block.startswith('"""'):
            continue
        lines = block.splitlines()
        header = lines[0].strip().strip("=").strip()
        code = "\n".join(lines[1:]).strip()
        if code:
            chunks.append((header, code))
    return chunks

def _describe_image(image_path: str, client: OpenAI, model: str):
    #Get a brief English description of an image via the VLM.
    img = Image.open(image_path).convert("RGB")
    messages = [{"role": "user", "content": [
        {"type": "image_url", "image_url": {"url": _pil_to_data_url(img)}},
        {"type": "text", "text": "Briefly describe what you see in this image in 1-2 English sentences. Focus on objects, people, actions, and setting."},
    ]}]
    return client.chat.completions.create(
        model=model, messages=messages, max_tokens=80
    ).choices[0].message.content.strip()

def build_bm25_index(chunks: list[tuple[str, str]]):
    from rank_bm25 import BM25Okapi
    corpus = []
    for header, code in chunks:
        text = header + " " + code
        tokens = re.findall(r"[a-zA-Z'ãẽĩõũáéíóúñ]+", text.lower())
        corpus.append(tokens)
    return BM25Okapi(corpus)

def retrieve_relevant_rules_bm25(
    image_path: str,
    chunks: list[tuple[str,str]],
    bm25,
    client: OpenAI,
    model: str,
    top_k: int = 10,
):
    desc = _describe_image(image_path, client, model)
    query_tokens = re.findall(r"[a-zA-Z'ãẽĩõũáéíóúñ]+", desc.lower())
    scores = bm25.get_scores(query_tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    top_indices = sorted(top_indices)

    rules_text = "Reglas de formato de código guaraní (recuperadas para esta imagen):\n"
    rules_text += f"# Descripción de la imagen: {desc}\n"
    for i in top_indices:
        header, code = chunks[i]
        rules_text += f"# === {header} ===\n{code}\n"
    return rules_text


#-- end code generation rag function helper --#
def load_culture_knowledge(path: str):
    with open(path,"r",encoding="utf-8") as f:
        return f.read().strip()


def load_interlinear(path: str, n:int):
    #take the first n lines of interlinear file
    header = "EJEMPLOS INTERLINEALES DE GUARANÍ (desglose de morfemas + glosa + inglés):"
    lines = []
    with open(path,"r",encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    return header + "\n" + "\n".join(lines[:n])

def load_grammar_parallel(path: str, n:int):
    header = "EJEMPLOS DE ORACIONES DE GUARANÍ (de libro de gramática):"
    lines = []
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

def load_apertium_summary(path: str, chars:int):
    with open(path,"r",encoding="utf-8") as f:
        text = f.read(chars)
    if len(text)==chars:
        text = text[:text.rfind("\n")]

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
):
    prompt = base_prompt

    if culture_knowledge_path:
        prompt += "\n" + load_culture_knowledge(culture_knowledge_path)

    if interlinear_path:
        prompt += "\n" + load_interlinear(interlinear_path,num_interlinear)

    if grammar_parallel_path:
        prompt += "\n" + load_grammar_parallel(grammar_parallel_path,num_grammar_parallel)

    if parallel_path:
        prompt += "\n" + load_parallel_examples(parallel_path, num_parallel)

    if apertium_path:
        prompt += "\n" + load_apertium_summary(apertium_path,apertium_chars)

    return prompt
    
def generate_caption(image_path: str, system_prompt: str,caption_prompt: str,client: OpenAI, model: str):
    test_image = Image.open(image_path).convert("RGB")
    messages = [{"role":"system","content":system_prompt}]
    messages.append(
        {
            "role":"user",
            "content": [
                {"type":"image_url","image_url": {"url": _pil_to_data_url(test_image)}},
                {"type":"text","text":caption_prompt}
            ]
        }
    )
    response = client.chat.completions.create(model=model,messages=messages,max_tokens=512)
    return response.choices[0].message.content.strip()


def run_captioning(
    image_paths: list[Path],
    output_file: str,
    system_prompt: str,
    client: OpenAI,
    model_name: str,
    bm25_chunks: Optional[list] = None,
    bm25_index=None,
    bm25_top_k: Optional[int] =10,
):
    results = []
    for img_path in image_paths:
        img_name = img_path.name
        per_img_prompt = system_prompt
        if bm25_index is not None:
            retrieved = retrieve_relevant_rules_bm25(image_path=str(img_path),chunks=bm25_chunks,bm25=bm25_index,client=client,model=model_name,top_k=bm25_top_k)
            per_img_prompt+="\n"+retrieved
        
        caption = generate_caption(str(img_path),system_prompt=per_img_prompt,client=client,model=model_name,caption_prompt=CAPTION_INSTRUCTION)
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
    parser.add_argument("--prompt_version",type=str,choices=list(prompt_version.keys()),default="v2",help="default base prompt the best one is v4")
    parser.add_argument("--parallel_examples",type=str,default=None,help="path to en-gn parallel json (flores) flores_dev_examples_en-gn.json")
    parser.add_argument("--num_parallel",type=int,default=10,help="Number of FLORES EN-GN pairs to inject into the system prompt")
    parser.add_argument("--interlinear",type=str,default=None,help="path to interlinear file (gua_para.txt)")
    parser.add_argument("--num_interlinear",type=int,default=8,help="number of interlinear blocks to inject")
    parser.add_argument("--grammar_parallel",type=str,default=None,help="path to grammar book parallel examples ie. gua_parallel.txt")
    parser.add_argument("--num_grammar_parallel",type=int,default=5,help="number of grammar book parallel pairs to inject")
    parser.add_argument("--culture_knowledge",type=str,default=None,help="path to guarani culture knowledge")
    parser.add_argument("--code_rules",type=str,default=None,help="path to code-format grammar rule file grammar_code_rules_Qwen3_Coder_Next.py")
    parser.add_argument("--retrieval_top_k",type=int,default=10,help="number of code rules to retrieve per image")
    parser.add_argument("--apertium",type=str,default=None,help="path to summary of apertium morphology apertium_grn_summary.txt")
    parser.add_argument("--apertium_chars",type=int,default=15000,help="number of characters to take from apertium summary")
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
    code_rules_path = to_path(args.code_rules)

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
        culture_knowledge_path=culture_knowledge_path
    )

    bm25_chunks, bm25_index = None, None
    if code_rules_path:
        bm25_chunks = parse_code_rules(code_rules_path)
        bm25_index = build_bm25_index(bm25_chunks)

    run_captioning(
        image_paths=image_paths,
        output_file=args.output,
        system_prompt=system_prompt,
        client=client,
        model_name=args.model,
        bm25_chunks=bm25_chunks,
        bm25_index=bm25_index,
        bm25_top_k=args.retrieval_top_k,
    )
if __name__ == "__main__":
    main()

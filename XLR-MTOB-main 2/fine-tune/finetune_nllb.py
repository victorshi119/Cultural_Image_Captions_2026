# %%

import pandas as pd
from transformers import NllbTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments, Seq2SeqTrainer, DataCollatorForSeq2Seq
from transformers import Seq2SeqTrainingArguments as TrainingArguments
from datasets import load_dataset, load_metric
import numpy as np
import torch
from datasets import Dataset, DatasetDict
import evaluate
import json
import random

metric = evaluate.load("chrf")

def postprocess_text(preds, labels):
    preds = [pred.strip() for pred in preds]
    labels = [[label.strip()] for label in labels]

    return preds, labels

def compute_metrics(eval_preds):
    preds, labels = eval_preds
    if isinstance(preds, tuple):
        preds = preds[0]
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

    # Replace -100 in the labels as we can't decode them.
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # Some simple post-processing
    decoded_preds, decoded_labels = postprocess_text(decoded_preds, decoded_labels)

    result = metric.compute(predictions=decoded_preds, references=decoded_labels, word_order=2)
    result = {"chrf": result["score"]}

    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
    result["gen_len"] = np.mean(prediction_lens)
    result = {k: round(v, 4) for k, v in result.items()}
    return result

def preprocess_logits_for_metrics(logits, labels):
    if isinstance(logits, tuple):
        logits = logits[0]
    return logits.argmax(dim=-1)

# %% 

model_name = "facebook/nllb-200-distilled-600M"

trans_df = pd.read_csv('../splits/kgv-en.csv', sep=",")

def _file2list(file_path):
    with open(file_path, 'r') as f:
        return f.read().splitlines()

train_eng = _file2list("../splits/extra.en")
train_kgv = _file2list("../splits/extra.kal")

pairs_eng = _file2list("../splits/pairs.en")
pairs_kgv = _file2list("../splits/pairs.kal")

dev_eng = _file2list("../splits/train_dictionaria_filtered.en")
dev_kgv = _file2list("../splits/train_dictionaria_filtered.kal")

test_eng = _file2list("../splits/test.en")
test_kgv = _file2list("../splits/test.kal")


train_full_eng = _file2list("../splits/train_full_parallel.en")
train_full_kgv = _file2list("../splits/train_full_parallel.kal")

dev_eng = train_full_eng[-500:]
dev_kgv = train_full_kgv[-500:]


train_full_pairs_eng = train_full_eng + pairs_eng
train_full_pairs_kgv = train_full_kgv + pairs_kgv

with open("../splits/en-kg-train-full-pairs.json", "w") as f:
    for i in range(len(train_full_pairs_eng)):
        json_object = {"translation": {"en": train_full_pairs_eng[i], "kg": train_full_pairs_kgv[i], "eng": train_full_pairs_eng[i], "kgv": train_full_pairs_kgv[i]}}
        f.write(json.dumps(json_object) + "\n")

with open("../splits/en-kg-train-full.json", "w") as f:
    for i in range(len(train_full_eng[:-500])):
        json_object = {"translation": {"en": train_full_eng[i], "kg": train_full_kgv[i], "eng": train_full_eng[i], "kgv": train_full_kgv[i]}}
        f.write(json.dumps(json_object) + "\n")

with open("../splits/en-kg-dev-full.json", "w") as f:
    for i in range(len(dev_eng)):
        json_object = {"translation": {"en": dev_eng[i], "kg": dev_kgv[i], "eng": dev_eng[i], "kgv": dev_kgv[i]}}
        f.write(json.dumps(json_object) + "\n")

with open("../splits/en-kg-test.json", "w") as f:
    for i in range(len(test_eng)):
        json_object = {"translation": {"en": test_eng[i], "kg": test_kgv[i], "eng": test_eng[i], "kgv": test_kgv[i]}}
        f.write(json.dumps(json_object) + "\n")

# exit()

# for mafand mt
with open("../splits/en-kg-train.json", "w") as f:
    for i in range(len(train_eng)):
        json_object = {"translation": {"en": train_eng[i], "kg": train_kgv[i], "ms": train_kgv[i]}}
        f.write(json.dumps(json_object) + "\n")

with open("../splits/en-kg-dev-500.json", "w") as f:
    dev_joint = list(zip(dev_eng, dev_kgv))
    dev_joint = random.sample(dev_joint, 500)
    dev_eng, dev_kgv = zip(*dev_joint)
    
    for i in range(len(dev_eng)):
        json_object = {"translation": {"en": dev_eng[i], "kg": dev_kgv[i], "ms": dev_kgv[i]}}
        f.write(json.dumps(json_object) + "\n")

with open("../splits/en-kg-test.json", "w") as f:
    for i in range(len(test_eng)):
        json_object = {"translation": {"en": test_eng[i], "kg": test_kgv[i], "ms": test_kgv[i]}}
        f.write(json.dumps(json_object) + "\n")


# for mafand mt
with open("../splits/eng-kgv-train.json", "w") as f:
    for i in range(len(train_eng)):
        json_object = {"translation": {"en": train_eng[i], "kg": train_kgv[i], "eng": train_eng[i], "kgv": train_kgv[i]}}
        f.write(json.dumps(json_object) + "\n")

with open("../splits/eng-kgv-dev-500.json", "w") as f:
    dev_joint = list(zip(dev_eng, dev_kgv))
    dev_joint = random.sample(dev_joint, 500)
    dev_eng, dev_kgv = zip(*dev_joint)
    
    for i in range(len(dev_eng)):
        json_object = {"translation": {"en": dev_eng[i], "kg": dev_kgv[i], "eng": dev_eng[i], "kgv": dev_kgv[i]}}
        f.write(json.dumps(json_object) + "\n")

with open("../splits/eng-kgv-test.json", "w") as f:
    for i in range(len(test_eng)):
        json_object = {"translation": {"en": test_eng[i], "kg": test_kgv[i], "eng": test_eng[i], "kgv": test_kgv[i]}}
        f.write(json.dumps(json_object) + "\n")


# all_kgv = train_kgv + dev_kgv


# from collections import Counter
# import re
# import sys
# import unicodedata
# from sacremoses import MosesPunctNormalizer

# mpn = MosesPunctNormalizer(lang="en")
# mpn.substitutions = [
#     (re.compile(r), sub) for r, sub in mpn.substitutions
# ]

# def get_non_printing_char_replacer(replace_by: str = " "):
#     non_printable_map = {
#         ord(c): replace_by
#         for c in (chr(i) for i in range(sys.maxunicode + 1))
#         # same as \p{C} in perl
#         # see https://www.unicode.org/reports/tr44/#General_Category_Values
#         if unicodedata.category(c) in {"C", "Cc", "Cf", "Cs", "Co", "Cn"}
#     }

#     def replace_non_printing_char(line) -> str:
#         return line.translate(non_printable_map)

#     return replace_non_printing_char

# replace_nonprint = get_non_printing_char_replacer(" ")
# def preproc(text):
#     clean = mpn.normalize(text)
#     clean = replace_nonprint(clean)
#     clean = unicodedata.normalize("NFKC", clean)
#     return clean

# all_texts_norm = [preproc(text) for text in all_kgv]
# chars_cnt = Counter(c for t in all_texts_norm for c in t)
# required_chars = ''.join([
#     k for k, v in chars_cnt.most_common() 
#     if v >= 3 and k not in ' '
# ])

# import sentencepiece as spm
# all_texts_file = 'kgv_texts_plain.txt'
# SPM_PREFIX = 'spm_kgv_1k'
# with open(all_texts_file, 'w') as f:
#     for i, text in enumerate(all_kgv):
#         print(text, file=f)

# spm.SentencePieceTrainer.train(
#     input=all_texts_file,
#     model_prefix=SPM_PREFIX,
#     vocab_size=2**10,  # 1024
#     character_coverage = 1,
#     num_threads=16,
#     train_extremely_large_corpus=False,
#     add_dummy_prefix=False,
#     max_sentencepiece_length=128,
#     max_sentence_length=4192*4,
#     pad_id=0,
#     eos_id=1,
#     unk_id=2,
#     bos_id=-1,
#     required_chars=required_chars,
# )

exit()

df_train = pd.DataFrame({'eng': train_eng, 'kgv': train_kgv})
df_dev = pd.DataFrame({'eng': dev_eng, 'kgv': dev_kgv})
df_test = pd.DataFrame({'eng': test_eng, 'kgv': test_kgv})

train_dataset = Dataset.from_pandas(df_train)
dev_dataset = Dataset.from_pandas(df_dev)
test_dataset = Dataset.from_pandas(df_test)

dataset = DatasetDict({
    'train': train_dataset,
    'dev': dev_dataset,
    'test': test_dataset
})

# dataset.push_to_hub("sethjsa/kgv-eng-mt", private=True)

tokenizer = NllbTokenizer.from_pretrained(model_name)

# Adding a new language tag to the tokenizer and model
def fix_tokenizer(tokenizer, new_lang='kgv_Latn'):
    """
    Add a new language token to the tokenizer vocabulary
    """
    old_len = len(tokenizer) - int(new_lang in tokenizer.added_tokens_encoder)
    tokenizer.lang_code_to_id[new_lang] = old_len-1
    tokenizer.id_to_lang_code[old_len-1] = new_lang
    # move "mask" to the last position
    tokenizer.fairseq_tokens_to_ids["<mask>"] = len(tokenizer.sp_model) + len(tokenizer.lang_code_to_id) + tokenizer.fairseq_offset

    tokenizer.fairseq_tokens_to_ids.update(tokenizer.lang_code_to_id)
    tokenizer.fairseq_ids_to_tokens = {v: k for k, v in tokenizer.fairseq_tokens_to_ids.items()}
    if new_lang not in tokenizer._additional_special_tokens:
        tokenizer._additional_special_tokens.append(new_lang)
    # clear the added token encoder; otherwise a new token may end up there by mistake
    tokenizer.added_tokens_encoder = {}
    tokenizer.added_tokens_decoder = {}

fix_tokenizer(tokenizer)

added_token_id = tokenizer.convert_tokens_to_ids('kgv_Latn')
# standard malay is similar to kalamang
similar_lang_id = tokenizer.convert_tokens_to_ids('zsm_Latn')

# load model
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
model.resize_token_embeddings(len(tokenizer))

# moving the embedding for "mask" to its new position
model.model.shared.weight.data[added_token_id+1] = model.model.shared.weight.data[added_token_id]
# initializing new language token with a token of a similar language
model.model.shared.weight.data[added_token_id] = model.model.shared.weight.data[similar_lang_id]

# %%

dir = "ek"

max_length=128

dir_dict = {
    "ek": {
        "src_lang": "eng_Latn",
        "tgt_lang": "kgv_Latn",
        "lang1": "eng",
        "lang2": "kgv"},
    "ke": {
        "src_lang": "kgv_Latn",
        "tgt_lang": "eng_Latn",
        "lang1": "kgv",
        "lang2": "eng"}
}

tokenizer.src_lang = dir_dict[dir]["src_lang"]
tokenizer.tgt_lang = dir_dict[dir]["tgt_lang"]

def preprocess_function(examples):
    inputs = examples[dir_dict[dir]["lang1"]]
    targets = examples[dir_dict[dir]["lang2"]]
    model_inputs = tokenizer(inputs, max_length=max_length, truncation=True)
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=max_length, truncation=True)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_datasets = dataset.map(preprocess_function, batched=True)
tokenized_datasets = tokenized_datasets.remove_columns(["eng", "kgv"])


# # %%
batch_size = 16


torch.cuda.empty_cache()

training_args = TrainingArguments(
    output_dir="../models/kgv-eng-v1",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    optim="adamw_torch",
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    eval_accumulation_steps=16,
    gradient_accumulation_steps=2,
    num_train_epochs=6,
    weight_decay=0.01,
    save_steps=200,
    save_total_limit=2,
    predict_with_generate=True,
    logging_dir="./logs",
    logging_steps=500,
    fp16=True,
)

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    tokenizer=tokenizer,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["dev"],
    compute_metrics=compute_metrics,
    # preprocess_logits_for_metrics=preprocess_logits_for_metrics
)

trainer.train()

# Save the model and tokenizer
model.save_pretrained("./results")
tokenizer.save_pretrained("./results")

trainer.push_to_hub()
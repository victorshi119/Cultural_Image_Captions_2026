#!/bin/bash
#SBATCH --account=r01360
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=16G
#SBATCH --time=2:00:00
#SBATCH --partition=general
#SBATCH --job-name=finale_dampy_bm25_visual_dev
#SBATCH --output=/N/project/CoRSAL/Cultural_Image_Captions_2026/logs/finale_dampy_bm25_visual_dev_%j.output
#SBATCH --mail-type=ALL
#SBATCH --mail-user=wencshi@iu.edu

module purge
module add conda git
ulimit -n 100000

source /N/slate/wencshi/miniforge3/etc/profile.d/conda.sh
conda activate /N/project/CoRSAL/.conda/envs/L605_americasnlp

cd /N/project/CoRSAL/Cultural_Image_Captions_2026

mkdir -p logs outputs

# --------------------------------------------------
# FIXED
# --------------------------------------------------
GRAMMAR_LINES=157
INTERLINEAR_LINES=144

python main.py \
  data/dev/guarani/images \
  --model gemma-4-31B-it \
  --prompt_version v3 \
  --output outputs/finale_dampy_bm25_visual5_dev.tsv \
  \
  --culture_knowledge resources/Claude_2step_guarani_cultural_knowledge.txt \
  \
  --grammar_book resources/guarani_ref.md \
  --num_grammar_book $GRAMMAR_LINES \
  \
  --interlinear resources/guarani_grammar_primer_claude.md \
  --num_interlinear $INTERLINEAR_LINES \
  \
  --parallel_examples resources/flores_dev_examples_en-gn.json \
  --num_parallel 50 \
  \
  --dampy_images new_data/dampy_output/images \
  --dampy_captions resources/dampy_gemma_claude_caption.txt \
  --dampy_spanish_captions_dir new_data/damp_data_caption \
  --dampy_bm25_visual_top_k 5

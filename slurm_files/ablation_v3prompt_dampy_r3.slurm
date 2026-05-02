#!/bin/bash
#SBATCH --account=r01360
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=8G
#SBATCH --time=2:00:00
#SBATCH --partition=general
#SBATCH --job-name=ablation_captions
#SBATCH --array=0,3,7
#SBATCH --output=/N/project/CoRSAL/Cultural_Image_Captions_2026/logs/ablation_v3prompt_dampy_r3-%A_%a.output
#SBATCH --mail-type=ALL
#SBATCH --mail-user=wencshi@iu.edu

module purge
module add conda git
ulimit -n 100000

# Activate conda env
source /N/slate/wencshi/miniforge3/etc/profile.d/conda.sh
conda activate /N/project/CoRSAL/.conda/envs/L605_americasnlp

cd /N/project/CoRSAL/Cultural_Image_Captions_2026

mkdir -p logs outputs

# Add-one-forward ablation (8 runs)
# 0 = none
# 1 = +pe
# 2 = +ck
# 3 = +ap
# 4 = +il
# 5 = +gp
# 6 = +dampy
# 7 = all

ID=$SLURM_ARRAY_TASK_ID

ARGS=(
    data/dev/guarani/images
    --model gemma-4-31B-it
    --prompt_version v3
)

case $ID in
  0) LABEL="none" ;;
  1) LABEL="pe"
     ARGS+=(--parallel_examples resources/flores_dev_examples_en-gn.json --num_parallel 99999) ;;
  2) LABEL="ck"
     ARGS+=(--culture_knowledge resources/Claude_2step_guarani_cultural_knowledge.txt) ;;
  3) LABEL="ap"
     ARGS+=(--apertium resources/apertium-grn-caption-cheatsheet.txt) ;;
  4) LABEL="il"
     ARGS+=(--interlinear resources/guarani_grammar_primer_claude.md --num_interlinear 99999) ;;
  5) LABEL="gp"
     ARGS+=(--grammar_parallel resources/guarani_exemplar_bank_claude.md --num_grammar_parallel 99999) ;;
  6) LABEL="dampy"
     ARGS+=(--grammar_book resources/dampy_gemma_claude_caption.txt --num_grammar_book 99999) ;;
  7) LABEL="all"
     ARGS+=(--culture_knowledge resources/Claude_2step_guarani_cultural_knowledge.txt)
     ARGS+=(--interlinear resources/guarani_grammar_primer_claude.md --num_interlinear 99999)
     ARGS+=(--grammar_parallel resources/guarani_exemplar_bank_claude.md --num_grammar_parallel 99999)
     ARGS+=(--apertium resources/apertium-grn-caption-cheatsheet.txt)
     ARGS+=(--parallel_examples resources/flores_dev_examples_en-gn.json --num_parallel 99999)
     ARGS+=(--grammar_book resources/dampy_gemma_claude_caption.txt --num_grammar_book 99999) ;;
esac

OUTFILE="outputs/ablation_v3prompt_dampy_05-01_${LABEL}_r3.tsv"

echo "Task $ID  config: $LABEL"
echo "Output: $OUTFILE"

ARGS+=(--output "$OUTFILE")

python main.py "${ARGS[@]}"

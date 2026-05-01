#!/bin/bash
#SBATCH --account=r01360
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=8G
#SBATCH --time=2:00:00
#SBATCH --partition=general
#SBATCH --job-name=ablation_captions
#SBATCH --array=0-6
#SBATCH --output=/N/project/CoRSAL/Cultural_Image_Captions_2026/logs/ablation_v2-%A_%a.output
#SBATCH --mail-type=ALL
#SBATCH --mail-user=wencshi@iu.edu

module purge
module add conda git
ulimit -n 100000

# Activate conda env
source /N/slate/wencshi/miniforge3/etc/profile.d/conda.sh
conda activate /N/project/CoRSAL/.conda/envs/L605_americasnlp

cd /geode2/home/u070/partkaew/BigRed200/Cultural_Image_Captions_2026

mkdir -p logs outputs

# Add-one-forward ablation (7 runs)
# 0 = none
# 1 = +ck
# 2 = +il
# 3 = +gp
# 4 = +ap
# 5 = +pe
# 6 = all

ID=$SLURM_ARRAY_TASK_ID

ARGS=(
    data/dev/guarani/images
    --model gemma-4-31B-it
    --prompt_version v4
)

case $ID in
  0) LABEL="none" ;;
  1) LABEL="pe"
     ARGS+=(--parallel_examples resources/flores_dev_examples_en-gn.json --num_parallel 200) ;;
  2) LABEL="ck"
     ARGS+=(--culture_knowledge resources/Claude_2step_guarani_cultural_knowledge.txt) ;;
  3) LABEL="ap"
     ARGS+=(--apertium resources/apertium-grn-caption-cheatsheet.md) ;;
  4) LABEL="il"
     ARGS+=(--interlinear resources/guarani_grammar_primer_claude.md --num_interlinear 60) ;;
  5) LABEL="gp"
     ARGS+=(--grammar_parallel resources/guarani_exemplar_bank_claude.md --num_grammar_parallel 30) ;;
  6) LABEL="all"
     ARGS+=(--culture_knowledge resources/guarani_culture_knowledge.txt)
     ARGS+=(--interlinear resources/guarani_grammar_primer_claude.md --num_interlinear 60)
     ARGS+=(--grammar_parallel resources/guarani_exemplar_bank_claude.md --num_grammar_parallel 30)
     ARGS+=(--apertium resources/apertium-grn-caption-cheatsheet.md)
     ARGS+=(--parallel_examples resources/flores_dev_examples_en-gn.json --num_parallel 200) ;;
esac

OUTFILE="outputs/ablation_v3_05-01_${LABEL}.tsv"

echo "Task $ID  config: $LABEL"
echo "Output: $OUTFILE"

ARGS+=(--output "$OUTFILE")

python main.py "${ARGS[@]}"

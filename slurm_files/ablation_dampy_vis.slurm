#!/bin/bash
#SBATCH --account=r01360
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=16G
#SBATCH --time=2:00:00
#SBATCH --partition=general
#SBATCH --job-name=ablation_dampy_vis
#SBATCH --array=0-2
#SBATCH --output=/N/project/CoRSAL/Cultural_Image_Captions_2026/logs/ablation_dampy_vis-%A_%a.output
#SBATCH --mail-type=ALL
#SBATCH --mail-user=wencshi@iu.edu

module purge
module add conda git
ulimit -n 100000

source /N/slate/wencshi/miniforge3/etc/profile.d/conda.sh
conda activate /N/project/CoRSAL/.conda/envs/L605_americasnlp

cd /N/project/CoRSAL/Cultural_Image_Captions_2026

mkdir -p logs outputs

# 3 conditions:
# 0 = none
# 1 = +dampy_vis  (2 image-caption shots from each of Comida, Fauna, Flora = 6 total)
# 2 = all         (ck + il + gp + ap + pe + dampy_vis 6-shot)

ID=$SLURM_ARRAY_TASK_ID

DAMPY_IMGS="new_data/dampy_output/images"
DAMPY_CAPS="resources/dampy_gemma_claude_caption.txt"

ARGS=(
    data/dev/guarani/images
    --model gemma-4-31B-it
    --prompt_version v3
)

case $ID in
  0) LABEL="none" ;;
  1) LABEL="dampy_vis"
     ARGS+=(--dampy_images "$DAMPY_IMGS"
            --dampy_captions "$DAMPY_CAPS"
            --num_dampy_shots_per_category 2) ;;
  2) LABEL="all"
     ARGS+=(--culture_knowledge resources/Claude_2step_guarani_cultural_knowledge.txt)
     ARGS+=(--interlinear resources/guarani_grammar_primer_claude.md --num_interlinear 99999)
     ARGS+=(--grammar_parallel resources/guarani_exemplar_bank_claude.md --num_grammar_parallel 99999)
     ARGS+=(--apertium resources/apertium-grn-caption-cheatsheet.txt)
     ARGS+=(--parallel_examples resources/flores_dev_examples_en-gn.json --num_parallel 99999)
     ARGS+=(--dampy_images "$DAMPY_IMGS"
            --dampy_captions "$DAMPY_CAPS"
            --num_dampy_shots_per_category 2) ;;
esac

OUTFILE="outputs/ablation_dampy_vis_05-01_${LABEL}.tsv"

echo "Task $ID  config: $LABEL"
echo "Output: $OUTFILE"

ARGS+=(--output "$OUTFILE")

python main.py "${ARGS[@]}"

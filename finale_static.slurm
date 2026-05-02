#!/bin/bash
#SBATCH --account=r01116
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=16G
#SBATCH --time=2:00:00
#SBATCH --partition=general
#SBATCH --job-name=finale_static
#SBATCH --array=0-8
#SBATCH --output=/geode2/home/u070/partkaew/BigRed200/Cultural_Image_Captions_2026/logs/finale_static_%A_%a.out
#SBATCH --error=/geode2/home/u070/partkaew/BigRed200/Cultural_Image_Captions_2026/logs/finale_static_%A_%a.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=partkaew@iu.edu

module purge
module load conda git
ulimit -n 100000

conda activate americasnlp

cd /geode2/home/u070/partkaew/BigRed200/Cultural_Image_Captions_2026

mkdir -p logs outputs

ID=$SLURM_ARRAY_TASK_ID

# --------------------------------------------------
# FIXED
# --------------------------------------------------
GRAMMAR_LINES=157
INTERLINEAR_LINES=144

# --------------------------------------------------
# SPLIT
# --------------------------------------------------

if [ $ID -le 5 ]; then
    MODE="text"

    # vary static flores pairs and dampy text shots per category
    case $ID in
      0) NUM_PARALLEL=20;  DAMPY_TEXT_CAT=2 ;;
      1) NUM_PARALLEL=30;  DAMPY_TEXT_CAT=3 ;;
      2) NUM_PARALLEL=50;  DAMPY_TEXT_CAT=3 ;;
      3) NUM_PARALLEL=50;  DAMPY_TEXT_CAT=5 ;;
      4) NUM_PARALLEL=80;  DAMPY_TEXT_CAT=3 ;;
      5) NUM_PARALLEL=100; DAMPY_TEXT_CAT=5 ;;
    esac

    OUTFILE="outputs/finale_static_text_${ID}.tsv"

    echo "TEXT MODE | ID=$ID"
    echo "FLORES=$NUM_PARALLEL DAMPY_TEXT_CAT=$DAMPY_TEXT_CAT"

    python main.py \
      data/test/guarani/images \
      --model gemma-4-31B-it \
      --prompt_version v3 \
      --output "$OUTFILE" \
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
      --num_parallel $NUM_PARALLEL \
      \
      --dampy_images new_data/dampy_output/images \
      --dampy_captions resources/dampy_gemma_claude_caption.txt \
      --num_dampy_text_shots_per_category $DAMPY_TEXT_CAT

else
    MODE="visual"

    # vary visual few-shot shots; flores and grammar fixed
    case $ID in
      6) SHOTS=5;  NUM_PARALLEL=30 ;;
      7) SHOTS=10; NUM_PARALLEL=30 ;;
      8) SHOTS=15; NUM_PARALLEL=50 ;;
    esac

    OUTFILE="outputs/finale_static_visual_${SHOTS}shot.tsv"

    echo "VISUAL MODE | ID=$ID"
    echo "SHOTS=$SHOTS FLORES=$NUM_PARALLEL"

    python main.py \
      data/test/guarani/images \
      --model gemma-4-31B-it \
      --prompt_version v3 \
      --output "$OUTFILE" \
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
      --num_parallel $NUM_PARALLEL \
      \
      --dampy_images new_data/dampy_output/images \
      --dampy_captions resources/dampy_gemma_claude_caption.txt \
      --num_dampy_shots $SHOTS
fi

#!/bin/bash
#SBATCH --account=r01116
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=16G
#SBATCH --time=24:00:00
#SBATCH --partition=general
#SBATCH --job-name=finale
#SBATCH --array=0-8
#SBATCH --output=/geode2/home/u070/partkaew/BigRed200/Cultural_Image_Captions_2026/logs/finale_%A_%a.out
#SBATCH --error=/geode2/home/u070/partkaew/BigRed200/Cultural_Image_Captions_2026/logs/finale_%A_%a.err
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
# FIXED (full context)
# --------------------------------------------------
GRAMMAR_LINES=157
INTERLINEAR_LINES=144

# --------------------------------------------------
# SPLIT
# --------------------------------------------------

if [ $ID -le 5 ]; then
    MODE="text"

    case $ID in
      0) DAMPY_K=5;  FLORES_K=100;  DEV_K=5;  CULTURE_K=5 ;;
      1) DAMPY_K=10;  FLORES_K=100;  DEV_K=10;  CULTURE_K=5 ;;
      2) DAMPY_K=15;  FLORES_K=100; DEV_K=10;  CULTURE_K=5 ;;
      3) DAMPY_K=20;  FLORES_K=100; DEV_K=10;  CULTURE_K=6 ;;
      4) DAMPY_K=15; FLORES_K=120; DEV_K=10;  CULTURE_K=8 ;;
      5) DAMPY_K=15; FLORES_K=150; DEV_K=10; CULTURE_K=10 ;;
    esac

    OUTFILE="outputs/finale_text_${ID}.tsv"

    echo "TEXT MODE | ID=$ID"
    echo "DAMPY=$DAMPY_K FLORES=$FLORES_K DEV=$DEV_K CULTURE=$CULTURE_K"

    python main.py \
      data/test/guarani/images \
      --model gemma-4-31B-it \
      --prompt_version v3 \
      --output "$OUTFILE" \
      \
      --culture_bm25 resources/Claude_2step_guarani_cultural_knowledge.txt \
      --culture_bm25_top_k $CULTURE_K \
      \
      --dampy_spanish_captions_dir new_data/damp_data_caption \
      --dampy_captions new_data/damp_data_caption/guarani_all_caption \
      --dampy_bm25_top_k $DAMPY_K \
      \
      --grammar_book resources/guarani_ref.md \
      --num_grammar_book $GRAMMAR_LINES \
      \
      --interlinear resources/guarani_grammar_primer_claude.md \
      --num_interlinear $INTERLINEAR_LINES \
      \
      --flores_bm25 resources/flores_dev_examples_en-gn.json \
      --flores_bm25_top_k $FLORES_K \
      \
      --dev_jsonl data/dev/guarani/guarani_trilingual.jsonl \
      --dev_images_dir data/dev/guarani/images \
      --dev_bm25_text_top_k $DEV_K

else
    MODE="visual"

    case $ID in
      6) SHOTS=15; FLORES_K=100;  DEV_K=10 ;;
      7) SHOTS=25; FLORES_K=100;  DEV_K=15 ;;
      8) SHOTS=50; FLORES_K=100; DEV_K=20 ;;
    esac

    OUTFILE="outputs/finale_visual_${SHOTS}shot.tsv"

    echo "VISUAL MODE | ID=$ID"
    echo "SHOTS=$SHOTS FLORES=$FLORES_K DEV=$DEV_K"

    python main.py \
      data/test/guarani/images \
      --model gemma-4-31B-it \
      --prompt_version v3 \
      --output "$OUTFILE" \
      \
      --culture_bm25 resources/Claude_2step_guarani_cultural_knowledge.txt \
      --culture_bm25_top_k 5 \
      \
      --grammar_book resources/guarani_ref.md \
      --num_grammar_book $GRAMMAR_LINES \
      \
      --interlinear resources/guarani_grammar_primer_claude.md \
      --num_interlinear $INTERLINEAR_LINES \
      \
      --flores_bm25 resources/flores_dev_examples_en-gn.json \
      --flores_bm25_top_k $FLORES_K \
      \
      --dev_jsonl data/dev/guarani/guarani_trilingual.jsonl \
      --dev_images_dir data/dev/guarani/images \
      --dev_bm25_text_top_k $DEV_K \
      \
      --dampy_images new_data/dampy/images \
      --dampy_captions new_data/dampy/guarani_captions.tsv \
      --num_dampy_shots $SHOTS
fi
#!/usr/bin/env bash
#SBATCH -A r01360
#SBATCH -J grn_to_es
#SBATCH -p gpu-debug
#SBATCH --gres=gpu:1
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -t 01:00:00
#SBATCH -o grn2es-%j.out
#SBATCH -e grn2es-%j.err
export HF_HOME=/N/project/CoRSAL/hf_cache
export TRANSFORMERS_CACHE=$HF_HOME
mkdir -p "$HF_HOME"
set -eo pipefail

cd /N/project/CoRSAL/Cultural_Image_Captions_2026

# Activate conda env
source /N/slate/wencshi/miniforge3/etc/profile.d/conda.sh
conda activate /N/project/CoRSAL/.conda/envs/nllb_gpu

python -c "import torch"

python grn_to_es_nllm.py
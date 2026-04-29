#!/bin/bash

#SBATCH --job-name=search
#SBATCH --ntasks=1
#SBATCH --partition=gpu
#SBATCH --gres=gpu:nvidia_rtx_a6000:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=96GB
#SBATCH --time=96:00:00
#SBATCH --array=0-216  # Replace <N> with the number of hyperparameter combinations minus 1
#SBATCH --output=./slurm/slurm-%A_%a.out  # Save output logs to ./slurm directory
#SBATCH --error=./slurm/slurm-%A_%a.err 

# Load necessary modules or activate your environment
source activate cuda11

# iterate through configs in the config/array folder
CONFIG_FILE="/home/saycock/personal/mtob/scripts/configs/array/config_$SLURM_ARRAY_TASK_ID.json"
echo "Running config file: $CONFIG_FILE"

# Run your Python script with the new config file
python ft.py $CONFIG_FILE

# clean up checkpoint directory
python rm_checkpoints.py $CONFIG_FILE
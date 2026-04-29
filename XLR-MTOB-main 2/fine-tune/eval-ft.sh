#!/usr/bin/bash


python convert_ft_to_json.py $1
python ../baselines/eval.py --input_file "$1/results.json"


#takes in generated captions compare against the baseline
#provided by the competition
"""
Usage:
    python evaluate_chrf.py --dataframe data.csv --translations wixarika_generated_captions.txt
"""

import argparse
import pandas as pd
from sacrebleu.metrics import CHRF


def chrf_score(ground_truth: str, generated_text: str) -> float:
    chrf = CHRF(word_order=2)
    return chrf.sentence_score(generated_text, [ground_truth]).score


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataframe", required=True)
    parser.add_argument("--generated", required=True)
    args = parser.parse_args()

    df = pd.read_json(args.dataframe, lines=True)

    with open(args.generated, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    # Support TSV with filename\tcaption or plain text (one caption per line)
    if lines and "\t" in lines[0]:
        generated_captions = [line.split("\t", 1)[1] for line in lines]
    else:
        generated_captions = lines

    print(f"Number of generated captions: {len(generated_captions)}")
    print(f"Number of rows in dataframe: {len(df)}")
    assert len(generated_captions) == len(df), "Mismatch between generated captions and dataframe rows!"

    df["generated_caption"] = generated_captions

    df["chrf_score"] = df.apply(
        lambda row: chrf_score(row["target_caption"], row["generated_caption"]),
        axis=1,
    )

    print(f"Mean chrF++ score: {df['chrf_score'].mean():.2f}")


if __name__ == "__main__":
    main()
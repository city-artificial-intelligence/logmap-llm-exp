from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.constants import GT_COL_DIVIDER, PRED_COL_DIVIDER


def calculate_logpropgs_confidence(log_probs: dict) -> float:
    for pred_tocken_info in log_probs:
        if pred_tocken_info["token"].strip() not in ["true", "false"]:
            continue
        top_logprobs = pred_tocken_info["top_logprobs"]
        positive_logprob = max([e["logprob"] for e in top_logprobs if e["token"].strip() == "true"], default=np.nan)
        negative_logprob = max([e["logprob"] for e in top_logprobs if e["token"].strip() == "false"], default=np.nan)
        break
    else:
        positive_logprob = np.nan
        negative_logprob = np.nan
    return np.nanmax([np.exp(positive_logprob), np.exp(negative_logprob)])


def save_oracle_results(results: list[str], path: Path) -> None:
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    with path.open("w") as file:
        for line in results:
            file.write(line + "\n")
    return


def read_candidate_pairs_file(pairs_file: Path) -> list[str]:
    with pairs_file.open() as file:
        return file.readlines()


def get_gt_pairs(gt_positive_pairs_path: Path | str) -> pd.DataFrame:
    gt_positive_pairs = pd.read_csv(gt_positive_pairs_path, sep=GT_COL_DIVIDER, header=None)
    if len(gt_positive_pairs.columns) == 3:
        gt_positive_pairs.columns = ["Source", "Target", "Label"]
    else:
        gt_positive_pairs.columns = ["Source", "Target", "=", "Label", "notes"]
    return gt_positive_pairs


def get_pred_pairs(pred_results_path: Path | str) -> pd.DataFrame:
    pred_pairs = pd.read_csv(pred_results_path, sep=PRED_COL_DIVIDER, header=None)
    if len(pred_pairs.columns) == 4:
        pred_pairs.columns = ["Source", "Target", "Prediction", "Confidence"]
    else:
        pred_pairs.columns = ["Source", "Target", "Prediction"]
    return pred_pairs


def extend_preds_with_labels_info(df: pd.DataFrame, gt_df: pd.DataFrame) -> pd.DataFrame:
    df["Label"] = False
    for _, row in gt_df.iterrows():
        source = row["Source"]
        target = row["Target"]
        mask = (df["Source"] == source) & (df["Target"] == target) | (df["Source"] == target) & (df["Target"] == source)
        df.loc[mask, "Label"] = True

    df["Type"] = df.apply(
        lambda x: "TP"
        if x["Label"] and x["Prediction"]
        else "TN"
        if not x["Label"] and not x["Prediction"]
        else "FP"
        if not x["Label"] and x["Prediction"]
        else "FN",
        axis=1,
    )
    return df

# ruff: noqa: T201, T201, T203, ERA001, BLE001
from __future__ import annotations

from pathlib import Path
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

from config.config import OUTPUTS_DIR, RUN_DIR
from config.runs_vars import DATASET_SUBSETS_MAP, SUBSET_TO_DATASET_MAP
from src.analysis import discover_all_experiments
from src.constants import GT_COL_DIVIDER, RESULTS_SEPARATOR, USAGE_COLUMNS
from src.error_taxonomy import ERROR_COLUMNS, RETRY_COUNT_COLUMNS, ErrorCategory, ErrorType
from src.formatting import (
    format_gt_pairs_filepath,
    format_predictions_run_path,
    format_run_metrics_path,
    format_storing_pathes_from_run_path,
)
from src.onto_access import OntologyAccess
from src.onto_object import OntologyEntryAttr
from src.utils import save_run_results


def plot_usage_histograms(
    tokens_usage: np.array, confidences: np.array, do_plot: bool = True, do_print: bool = True, suptitle: str = ""
) -> None:
    tokens_usage = np.array(tokens_usage, dtype=float)
    if do_print:
        print(f"Mean input tokens: {np.nanmean(tokens_usage[:,0]):.1f}")
        print(f"Mean output tokens: {np.nanmean(tokens_usage[:,1]):.1f}")
        print(f"Total input tokens: {np.nansum(tokens_usage[:,0]):.0f}")
        print(f"Total output tokens: {np.nansum(tokens_usage[:,1]):.0f}")
        if tokens_usage.shape[1] > 2:
            print(f"Mean cached input tokens: {np.nanmean(tokens_usage[:,2]):.1f}")
            print(f"Mean reasoning output tokens: {np.nanmean(tokens_usage[:,3]):.1f}")
            print(f"Mean proc time: {np.nanmean(tokens_usage[:,4]):.3f}s")

    if do_plot:
        n_cols = min(3, 2 + (tokens_usage.shape[1] > 2))
        fig, axes = plt.subplots(1, n_cols, figsize=(4 * n_cols, 4))
        fig.suptitle(suptitle)
        axes[0].hist(tokens_usage[:, 0], bins=20)
        axes[0].set_title("Input tokens usage")
        axes[1].hist(tokens_usage[:, 1], bins=20)
        axes[1].set_title("Output tokens usage")
        if n_cols > 2:
            axes[2].hist(confidences, bins=50)
            axes[2].set_title("Confidence distribution")
        plt.show()
    return


def compute_run_metrics(df: pd.DataFrame) -> dict:
    """Compute binary-matching metrics plus error/retry/token aggregates for one run.

    ``df`` must hold a boolean ``Label`` column and a ``Prediction`` column; optional
    ``is_error``, ``error_type``, ``error_category``, ``num_retries``, retry-count and
    token-usage columns enrich the result. The returned dict mirrors what is persisted in
    the ``*_stats.txt`` files, so it can be reused both at run time and by the leaderboard.
    """
    total_count = len(df)
    if "is_error" in df.columns:
        error_mask = df["is_error"]
    else:
        pred_str = df["Prediction"].astype(str).str.strip().str.lower()
        error_mask = ~pred_str.isin({"true", "false"})

    num_errors = int(error_mask.sum())
    valid_df = df[~error_mask].copy()
    pred_mapped = valid_df["Prediction"].astype(str).str.strip().str.lower().map({"true": True, "false": False})
    valid_df["Prediction"] = pred_mapped

    if valid_df.empty:
        # Every call errored: report a fully-failed run instead of crashing on an empty matrix.
        nan = float("nan")
        metrics = {
            "Accuracy": nan, "Precision": nan, "Recall": nan, "F1 Score": nan,
            "Specificity": nan, "Sensitivity": nan, "TP": 0, "TN": 0, "FP": 0, "FN": 0,
        }
    else:
        # labels=[False, True] forces a 2x2 matrix even when predictions are single-class.
        conf_matrix = confusion_matrix(valid_df["Label"], valid_df["Prediction"], labels=[False, True])
        tn, fp, fn, tp = conf_matrix.ravel()
        metrics = {
            "Accuracy": accuracy_score(valid_df["Label"], valid_df["Prediction"]),
            "Precision": precision_score(valid_df["Label"], valid_df["Prediction"], zero_division=0),
            "Recall": recall_score(valid_df["Label"], valid_df["Prediction"], zero_division=0),
            "F1 Score": f1_score(valid_df["Label"], valid_df["Prediction"], zero_division=0),
            "Specificity": tn / (tn + fp) if (tn + fp) else float("nan"),
            "Sensitivity": tp / (tp + fn) if (tp + fn) else float("nan"),
            "TP": int(tp), "TN": int(tn), "FP": int(fp), "FN": int(fn),
        }

    metrics["Youden's index"] = metrics["Sensitivity"] + metrics["Specificity"] - 1
    metrics["num_errors"] = num_errors
    metrics["error_rate"] = num_errors / total_count if total_count > 0 else 0.0

    # Detailed error breakdown by type and category
    if "error_type" in df.columns:
        error_rows = df[error_mask]
        error_types = error_rows["error_type"].dropna().astype(str)
        error_types = error_types[error_types != ""]
        for et in ErrorType:
            count = int((error_types == et.value).sum())
            if count > 0:
                metrics[f"errors_{et.value}"] = count
        # Category-level aggregates
        if "error_category" in df.columns:
            error_cats = error_rows["error_category"].dropna().astype(str)
            error_cats = error_cats[error_cats != ""]
            for ec in ErrorCategory:
                count = int((error_cats == ec.value).sum())
                if count > 0:
                    metrics[f"errors_cat_{ec.value}"] = count

    if "num_retries" in df.columns:
        retries = pd.to_numeric(df["num_retries"], errors="coerce").dropna()
        if not retries.empty:
            metrics["mean_num_retries"] = retries.mean()
            metrics["total_num_retries"] = int(retries.sum())

    # Per-error-type retry counts
    for col in RETRY_COUNT_COLUMNS:
        if col in df.columns:
            values = pd.to_numeric(df[col], errors="coerce").dropna()
            if not values.empty:
                total = int(values.sum())
                if total > 0:
                    metrics[f"total_{col}"] = total

    for col in USAGE_COLUMNS:
        if col in df.columns:
            valid = pd.to_numeric(df[col], errors="coerce").dropna()
            if not valid.empty:
                metrics[f"mean_{col}"] = valid.mean()
                if col == "proc_time":
                    metrics[f"total_{col}"] = valid.sum()
                else:
                    metrics[f"total_{col}"] = int(valid.sum())

    return metrics


def save_analysis_results(
    df: pd.DataFrame,
    print_results: bool = True,
    plot_confusion_matrix: bool = True,
    subtitle: str = "",
    cm_save_path: Path | None = None,
    stats_path: Path | None = None,
) -> dict:
    metrics = compute_run_metrics(df)
    conf_matrix = np.array([[metrics["TN"], metrics["FP"]], [metrics["FN"], metrics["TP"]]])

    if print_results:
        for metric, value in metrics.items():
            print(f"{metric}: {value:.3f}")

    if stats_path:
        save_run_results(list(metrics.items()), stats_path, RESULTS_SEPARATOR, columns=["Metric", "Value"])

    if plot_confusion_matrix or cm_save_path:
        plt.figure(figsize=(4, 4))
        sns.heatmap(
            conf_matrix,
            annot=True,
            fmt="d",
            cmap="Blues",
            cbar=False,
            xticklabels=["Negative", "Positive"],
            yticklabels=["Negative", "Positive"],
        )
        plt.xlabel("Predicted Label")
        plt.ylabel("True Label")
        plt.title(f"{subtitle}")

        if cm_save_path:
            if not cm_save_path.parent.exists():
                cm_save_path.parent.mkdir(parents=True)
            plt.savefig(cm_save_path)

        if plot_confusion_matrix:
            plt.show()
        plt.close()

    return {**metrics, "confusion matrix": conf_matrix}


def get_gt_pairs(gt_positive_pairs_path: Path | str, sep: str = GT_COL_DIVIDER) -> pd.DataFrame:
    gt_positive_pairs = pd.read_csv(gt_positive_pairs_path, sep=sep, header=None)
    if len(gt_positive_pairs.columns) == 3:
        gt_positive_pairs.columns = ["Source", "Target", "Label"]
    else:
        gt_positive_pairs.columns = ["Source", "Target", "=", "Label", "notes"]
    return gt_positive_pairs


def get_pred_pairs(pred_results_path: Path | str, sep: str = RESULTS_SEPARATOR) -> pd.DataFrame:
    pred_df = pd.read_csv(pred_results_path, sep=sep)
    for col in [*USAGE_COLUMNS, "num_retries", *ERROR_COLUMNS, *RETRY_COUNT_COLUMNS]:
        if col not in pred_df.columns:
            pred_df[col] = np.nan

    pred_str = pred_df["Prediction"].astype(str).str.strip().str.lower()
    is_error = ~pred_str.isin({"true", "false"})
    pred_df["is_error"] = is_error
    return pred_df


def extend_preds_with_labels_info(df: pd.DataFrame, gt_df: pd.DataFrame) -> pd.DataFrame:
    gt_pairs = {frozenset((row["Source"], row["Target"])) for _, row in gt_df.iterrows()}
    df["Label"] = df.apply(lambda row: frozenset((row["Source"], row["Target"])) in gt_pairs, axis=1)

    pred_str = df["Prediction"].astype(str).str.strip().str.lower()
    if "is_error" not in df.columns:
        df["is_error"] = ~pred_str.isin({"true", "false"})
    pred_bool = pred_str.map({"true": True, "false": False})

    def classify_type(row: pd.Series) -> str:
        if row["is_error"]:
            return "Error"
        pred = pred_bool[row.name]
        if row["Label"] and pred:
            return "TP"
        if not row["Label"] and not pred:
            return "TN"
        if not row["Label"] and pred:
            return "FP"
        return "FN"

    df["Type"] = df.apply(classify_type, axis=1)
    return df


def get_predictions_with_gt(
    run_path: str, dataset_name: str, set_name: str, model: str, prompt_name: str, suffix: str = ""
) -> tuple[pd.DataFrame, pd.DataFrame]:
    gt_positive_pairs_path = format_gt_pairs_filepath(dataset_name, set_name)
    pred_results_path, _, _ = format_storing_pathes_from_run_path(run_path, set_name, model, prompt_name, suffix)
    gt_df = get_gt_pairs(gt_positive_pairs_path)
    pred_df = get_pred_pairs(pred_results_path)

    return extend_preds_with_labels_info(pred_df, gt_df)


def store_run_metrics_df(
    prompt_functions: list,
    run_path: Path,
    dataset_name: str,
    set_name: str,
    model: str,
    suffix: str = "",
    log_all_errors: bool = True,
) -> pd.DataFrame | None:
    results_data = []
    for prompt_function in prompt_functions:
        try:
            _, stats_path, _ = format_storing_pathes_from_run_path(run_path, set_name, model, prompt_function, suffix)
            stats = pd.read_csv(stats_path, index_col=0).T
            results_data.append(
                {
                    "Prompt": prompt_function,
                    **{key: stats[key].to_numpy()[0] for key in stats.columns},
                    "Dataset": dataset_name,
                    "SubSet": set_name,
                    "Model": model,
                }
            )
        except FileNotFoundError:
            if log_all_errors:
                print(f"File not found for {prompt_function} in {run_path}")
            continue

    if not results_data:
        if log_all_errors:
            print(f"No results data found for run: {run_path}")
        return None

    results_df = pd.DataFrame(results_data).round(4)

    results_df.to_csv(format_run_metrics_path(run_path, suffix), index=False)
    return results_df


def read_run_metrics_df(run_subdir: str, suffix: str = "") -> pd.DataFrame:
    run_metrics_path = format_run_metrics_path(RUN_DIR / run_subdir, suffix)
    return pd.read_csv(run_metrics_path)


def print_results_entry(
    res_df: pd.DataFrame, onto_tgt: OntologyAccess, onto_src: OntologyAccess, pair_type: str = "FP", idx: int = 0
) -> None:
    source_uri = res_df[res_df["Type"] == pair_type].iloc[idx]["Source"]
    target_uri = res_df[res_df["Type"] == pair_type].iloc[idx]["Target"]

    source_entry = OntologyEntryAttr(source_uri, onto_src)
    target_entry = OntologyEntryAttr(target_uri, onto_tgt)

    print(f"Processing pair {idx} of type {pair_type}")
    pprint("Source Entry:\n")
    pprint(source_entry.annotation)
    pprint("Target Entry:\n")
    pprint(target_entry.annotation)

    print(f"Parent of Source Concept: {source_entry.get_parents_preferred_names()}")
    print(f"Parent of Target Concept: {target_entry.get_parents_preferred_names()}")


def reevaluate_setup(setup: dict, save_diagrams: bool = False) -> dict:
    subset = setup["subset"]
    dataset = SUBSET_TO_DATASET_MAP[subset]
    model = setup["model"]
    exp_name = setup["experiment_name"]
    suffix = setup["suffix"]
    experiment_type = setup["experiment_type"]
    prompt_functions = setup["prompt_functions"]

    run_path = format_predictions_run_path(dataset, subset, model, experiment_type, exp_spec=exp_name)
    results = {"subset": subset, "model": model, "exp_name": exp_name, "success": True, "errors": []}

    for prompt_name in prompt_functions:
        try:
            prediction_path, stats_path, diagram_path = format_storing_pathes_from_run_path(
                run_path, subset, model, prompt_name, suffix=suffix
            )
            predictions = get_predictions_with_gt(run_path, dataset, subset, model, prompt_name, suffix=suffix)
            save_analysis_results(
                predictions,
                print_results=False,
                plot_confusion_matrix=False,
                subtitle=f"{subset}: {model} {prompt_name} | ",
                cm_save_path=diagram_path if save_diagrams else None,
                stats_path=stats_path,
            )
        except Exception as e:
            results["errors"].append(f"Prompt {prompt_name}: {e}")

    try:
        store_run_metrics_df(prompt_functions, run_path, dataset, subset, model, suffix=suffix, log_all_errors=False)
    except Exception as e:
        results["success"] = False
        results["errors"].append(str(e))

    return results


def reevaluate_all_experiments(
    outputs_dir: Path | None = None,
    datasets_map: dict[str, list[str]] | None = None,
    suffix: str = "_reduced",
    save_diagrams: bool = False,
    log_progress: bool = True,
) -> list[dict]:
    if outputs_dir is None:
        outputs_dir = Path(OUTPUTS_DIR)
    if datasets_map is None:
        datasets_map = DATASET_SUBSETS_MAP

    experiments = discover_all_experiments(outputs_dir, datasets_map, suffix)
    all_results = []
    for i, exp in enumerate(experiments):
        setup = {
            "subset": exp["subset"],
            "model": exp["model"],
            "experiment_name": exp["experiment_name"],
            "suffix": suffix,
            "experiment_type": exp["experiment_type"],
            "prompt_functions": exp["prompts"],
        }
        result = reevaluate_setup(setup, save_diagrams=save_diagrams)
        all_results.append(result)
        if log_progress and (i + 1) % 50 == 0:
            print(f"Re-evaluated {i + 1}/{len(experiments)} experiments")

    if log_progress:
        n_ok = sum(1 for r in all_results if r["success"])
        n_err = sum(1 for r in all_results if not r["success"])
        print(f"Done: {n_ok} succeeded, {n_err} failed out of {len(all_results)} experiments")

    return all_results

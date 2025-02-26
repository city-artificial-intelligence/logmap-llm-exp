import os
import time
from config.config import *

def format_oracle_predictions_filepath(set_name: str, model: str, exp_name: str) -> Path:
    return OUTPUTS_DIR / "llm_oracle_results" / f"{set_name}_{model}_{exp_name}.txt"


def format_confusion_matrix_filepath(set_name: str, model: str, exp_name: str, suffix: str = "") -> Path:
    if suffix:
        return METRICS_DIR / "confusion_matrices" / f"{set_name}_{model}_{exp_name}_{suffix}.png"
    return METRICS_DIR / "confusion_matrices" / f"{set_name}_{model}_{exp_name}.png"


def format_gt_pairs_filepath(dataset_path: str, set_name: str) -> Path:
    return DATA_DIR / dataset_path / set_name / "refs_equiv/full.tsv"


def format_oracle_pairs_filepath(dataset_name: str, set_name: str) -> Path:
    return DATA_DIR / dataset_name / set_name / f"{dataset_name}-{set_name}-logmap_mappings_to_ask_oracle_user_llm.txt"

def format_run_path() -> Path:
    date = time.strftime("%Y-%m-%d")
    time_now = time.strftime("%H-%M-%S")
    os.makedirs(RUN_DIR, exist_ok=True)
    os.makedirs(RUN_DIR / f"{date}_{time_now}")

    return RUN_DIR / f"{date}_{time_now}"

def format_from_run_path(run_path: str, set_name: str, model: str, exp_name: str) -> Path:
    path_to_results = run_path / f"{set_name}_{model}_{exp_name}_results.csv"
    path_to_stats = run_path /f"{set_name}_{model}_{exp_name}_stats.txt"
    path_to_diagrams = run_path /f"{set_name}_{model}_{exp_name}.png"
    return path_to_results, path_to_stats, path_to_diagrams
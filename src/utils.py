from __future__ import annotations

import functools
from itertools import product
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd

from src.constants import PAIRS_SEPARATOR, RESULTS_SEPARATOR, USAGE_COLUMNS
from src.error_taxonomy import ERROR_COLUMNS, RETRY_COUNT_COLUMNS


def retry(max_retries: int = 1) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Retry the function up to `max_retries` times if an exception occurs."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:  # noqa: ANN401
            attempts = 0
            while attempts <= max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts > max_retries:
                        raise e
            return None

        return wrapper

    return decorator


def calculate_logpropgs_confidence(log_probs: list) -> float:
    for pred_tocken_info in log_probs:
        if pred_tocken_info["token"].strip() not in ["true", "false"]:
            continue
        top_logprobs = pred_tocken_info["top_logprobs"]
        positive_logprob = max([e["logprob"] for e in top_logprobs if e["token"].strip() == "true"], default=np.nan)
        negative_logprob = max([e["logprob"] for e in top_logprobs if e["token"].strip() == "false"], default=np.nan)
        break
    else:
        positive_logprob = 0.0
        negative_logprob = 0.0
    return np.nanmax([np.exp(positive_logprob), np.exp(negative_logprob)])


def write_lines(results: list[str], path: Path) -> None:
    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    with path.open("w") as file:
        for line in results:
            file.write(line + "\n")
    return


def read_file(pairs_file: Path) -> list[str]:
    with pairs_file.open() as file:
        return file.readlines()


def read_oracle_pairs(file_path: Path, sep: str = PAIRS_SEPARATOR) -> list[tuple[str]]:
    with file_path.open() as file:
        return [tuple(line.strip().split(sep)[:2]) for line in file.readlines()]


def save_run_results(
    results: list[tuple], path: Path, sep: str = RESULTS_SEPARATOR, columns: list[str] | None = None
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    if not columns:
        columns = ["Source", "Target", "Prediction", "Confidence", *USAGE_COLUMNS, "num_retries", *ERROR_COLUMNS, *RETRY_COUNT_COLUMNS]

    # Pad rows that are shorter than expected columns (backward compat with old results)
    expected_len = len(columns)
    padded_results = []
    for row in results:
        row_list = list(row) if not isinstance(row, list) else row
        if len(row_list) < expected_len:
            row_list.extend([""] * (expected_len - len(row_list)))
        padded_results.append(row_list)

    results_df = pd.DataFrame(padded_results, columns=columns)
    results_df.to_csv(path, sep=sep, index=False)
    return


def expand_setups(setups: list[dict], base_setup: dict | None, exclude_keys: list[str] | None = None) -> list[dict]:
    base_setup = base_setup or {}
    exclude_keys = exclude_keys or []

    expanded = []
    for setup in setups:
        constant_part = {}
        keys, values = [], []
        setup = {**base_setup, **setup}

        for k, v in setup.items():
            if isinstance(v, list) and k not in exclude_keys:
                keys.append(k)
                values.append(v)
            else:
                constant_part[k] = v

        for combo in product(*values):
            new_setup = constant_part.copy()
            new_setup.update(dict(zip(keys, combo)))
            expanded.append(new_setup)
    return expanded


def calculate_mean_token_usage(tokens_usage: list[tuple]) -> dict[str, float]:
    if not tokens_usage:
        return {f"mean_{col}": 0.0 for col in USAGE_COLUMNS} | {f"total_{col}": 0 for col in USAGE_COLUMNS}

    full_len = len(USAGE_COLUMNS)
    normalized = []
    for t in tokens_usage:
        if t is None:
            continue
        t = tuple(t) if not isinstance(t, tuple) else t
        padded = t + (None,) * (full_len - len(t)) if len(t) < full_len else t[:full_len]
        normalized.append(padded)

    result = {}
    for i, col in enumerate(USAGE_COLUMNS):
        values = [t[i] for t in normalized if t[i] is not None and not (isinstance(t[i], float) and np.isnan(t[i]))]
        result[f"mean_{col}"] = float(np.mean(values)) if values else 0.0
        if col == "proc_time":
            result[f"total_{col}"] = float(np.sum(values)) if values else 0.0
        else:
            result[f"total_{col}"] = int(np.sum(values)) if values else 0

    return result


def save_token_usage_stats(
    tokens_usage: list[tuple],
    path: Path,
    sep: str = RESULTS_SEPARATOR,
    predictions_path: Path | None = None,
) -> dict[str, float]:
    stats = calculate_mean_token_usage(tokens_usage)

    has_data = any(v != 0 and v != 0.0 for v in stats.values())
    if not has_data and predictions_path is not None:
        derived = derive_token_usage_from_predictions(predictions_path, path, sep)
        if derived is not None:
            return derived

    path.parent.mkdir(parents=True, exist_ok=True)
    stats_df = pd.DataFrame(list(stats.items()), columns=["Metric", "Value"])
    stats_df.to_csv(path, sep=sep, index=False)

    return stats


def derive_token_usage_from_predictions(
    predictions_path: Path, usage_path: Path, sep: str = RESULTS_SEPARATOR
) -> dict[str, float] | None:
    if not predictions_path.exists():
        return None

    pred_df = pd.read_csv(predictions_path, sep=sep)

    present_cols = [c for c in USAGE_COLUMNS if c in pred_df.columns]
    if not present_cols:
        return None

    numeric_df = pred_df[present_cols].apply(pd.to_numeric, errors="coerce")
    if numeric_df.dropna(how="all").empty:
        return None

    result: dict[str, float] = {}
    for col in USAGE_COLUMNS:
        if col in numeric_df.columns:
            valid = numeric_df[col].dropna()
            result[f"mean_{col}"] = float(valid.mean()) if len(valid) > 0 else 0.0
            if col == "proc_time":
                result[f"total_{col}"] = float(valid.sum()) if len(valid) > 0 else 0.0
            else:
                result[f"total_{col}"] = int(valid.sum()) if len(valid) > 0 else 0
        else:
            result[f"mean_{col}"] = 0.0
            result[f"total_{col}"] = 0

    usage_path.parent.mkdir(parents=True, exist_ok=True)
    stats_df = pd.DataFrame(list(result.items()), columns=["Metric", "Value"])
    stats_df.to_csv(usage_path, sep=sep, index=False)

    return result

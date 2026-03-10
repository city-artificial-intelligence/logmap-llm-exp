from __future__ import annotations

import functools
from itertools import product
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd

from src.constants import PAIRS_SEPARATOR, RESULTS_SEPARATOR


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
    """Save the results of the run to a file.

    Args:
        results: list of tuples with the results.
        path: path to the file to save the results.
        sep: separator to use in the file.
        columns: columns names for entries in the results.

    """
    path.parent.mkdir(parents=True, exist_ok=True)

    if not columns:
        columns = ["Source", "Target", "Answer", "Confidence"]

    results_df = pd.DataFrame(results, columns=columns)
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


def calculate_mean_token_usage(tokens_usage: list[tuple[int, int]]) -> dict[str, float]:
    """Calculate mean token usage from a list of (input_tokens, output_tokens) tuples.

    Args:
        tokens_usage: list of tuples, each with (input_tokens, output_tokens).

    Returns:
        dict with mean_input_tokens, mean_output_tokens, total_input_tokens, total_output_tokens.

    """
    if not tokens_usage:
        return {
            "mean_input_tokens": 0.0,
            "mean_output_tokens": 0.0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
        }

    input_tokens = [t[0] for t in tokens_usage if t and len(t) >= 2]
    output_tokens = [t[1] for t in tokens_usage if t and len(t) >= 2]

    return {
        "mean_input_tokens": np.mean(input_tokens) if input_tokens else 0.0,
        "mean_output_tokens": np.mean(output_tokens) if output_tokens else 0.0,
        "total_input_tokens": sum(input_tokens),
        "total_output_tokens": sum(output_tokens),
    }


def save_token_usage_stats(
    tokens_usage: list[tuple[int, int]], path: Path, sep: str = RESULTS_SEPARATOR
) -> dict[str, float]:
    """Calculate and save mean token usage stats to a file.

    Args:
        tokens_usage: list of tuples, each with (input_tokens, output_tokens).
        path: path to save the token usage stats.
        sep: separator to use in the file.

    Returns:
        dict with token usage statistics.

    """
    stats = calculate_mean_token_usage(tokens_usage)
    path.parent.mkdir(parents=True, exist_ok=True)

    stats_df = pd.DataFrame(list(stats.items()), columns=["Metric", "Value"])
    stats_df.to_csv(path, sep=sep, index=False)

    return stats
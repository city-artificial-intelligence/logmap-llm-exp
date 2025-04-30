from __future__ import annotations

import functools
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd

from src.constants import PAIRS_SEPARATOR, RESULTS_SEPARATOR
from src.formatting import format_oracle_pairs_precomputed_dir, format_oracle_pairs_with_prompts_path


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
    if not columns:
        columns = ["Source", "Target", "Answer", "Confidence"]
    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    results_df = pd.DataFrame(results, columns=columns)
    results_df.to_csv(path, sep=sep, index=False)
    return


def load_precomputed_oracle_pairs(
    dataset_name: str, set_name: str, prompt_function: callable | None, sep: str = PAIRS_SEPARATOR
) -> list[tuple[str]]:
    oracle_pairs_dir = format_oracle_pairs_precomputed_dir(dataset_name, set_name)
    pairs_path = format_oracle_pairs_with_prompts_path(prompt_function, oracle_pairs_dir)

    if not pairs_path.exists():
        msg = f"Oracle pairs file not found: {pairs_path}"
        raise FileNotFoundError(msg)

    pairs_df = pd.read_csv(pairs_path, sep=sep, header=None)
    return list(zip(pairs_df[0], pairs_df[1], pairs_df[2]))

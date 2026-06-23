"""Parse LLM-response debug logs and aggregate token / timing statistics.

The inference loop can emit a per-call debug line such as::

    prompt=direct_entity, model='openai|gpt-4o-mini' source='...', target='...',
    input_tokens=123, output_tokens=4, proc_time=1.23

These helpers turn such a log into a tidy DataFrame and compute simple
per-group aggregates (mean tokens, throughput, ...).
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

LINE_PATTERN = re.compile(
    r"prompt=(?P<prompt>[^,]+),\s*"
    r"model='(?P<model>[^']+)'\s*"
    r"source='(?P<source>[^']+)',\s*"
    r"target='(?P<target>[^']+)',\s*"
    r"input_tokens=(?P<input_tokens>\d+),\s*"
    r"output_tokens=(?P<output_tokens>\d+),\s*"
    r"proc_time=(?P<proc_time>[0-9.]+)"
)


def read_log_to_df(path: str | Path) -> pd.DataFrame:
    """Parse a debug log into a DataFrame of one row per LLM call."""
    rows = []

    with Path(path).open() as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            match = LINE_PATTERN.match(line)
            if not match:
                msg = f"Failed to parse line {line_no}:\n{line}"
                raise ValueError(msg)

            row = match.groupdict()
            row["input_tokens"] = int(row["input_tokens"])
            row["output_tokens"] = int(row["output_tokens"])
            row["proc_time"] = float(row["proc_time"])
            rows.append(row)

    return pd.DataFrame(rows)


def add_derived_metrics(data: pd.DataFrame) -> pd.DataFrame:
    """Add total tokens, throughput and output/input ratio columns."""
    data = data.copy()
    data["total_tokens"] = data["input_tokens"] + data["output_tokens"]
    data["tokens_per_sec"] = data["total_tokens"] / data["proc_time"]
    data["output_input_ratio"] = data["output_tokens"] / data["input_tokens"]
    return data


def aggregate(
    data: pd.DataFrame,
    groupby: list[str],
    metrics: list[str],
    agg: str | list[str] = "mean",
    round_to: int = 4,
) -> pd.DataFrame:
    """Group ``data`` by ``groupby`` and aggregate ``metrics`` with rounding."""
    result = data.groupby(groupby)[metrics].agg(agg).reset_index()

    numeric_cols = result.select_dtypes("number").columns
    result[numeric_cols] = result[numeric_cols].round(round_to)

    return result

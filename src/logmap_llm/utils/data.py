"""
logmap_llm.utils.data

shared data utilities for the LogMap-LLM pipeline

Public API:

    normalise_prediction_column(df_or_series)
        Return a new DataFrame/Series with the Oracle_prediction column
        coerced from CSV-string form back to bools where possible; error
        values=("error", "skipped") and NaN pass through untouched

    prediction_is_true_mask(df_or_series)
        Return a boolean Series suitable for df[mask] filtering, where
        true means "the oracle accepted this mapping"; error values 
        and NaN evaluate to False

    filter_accepted_predictions(df)
        convenience wrapper: return the subset of rows where the oracle
        accepted the mapping (equivalent to df[prediction_is_true_mask(df)])

    dedupe_m_ask_by_uri_pair(m_ask_df)
        collapse duplicate (source, target) M_ask rows to one (keep first),
        preserving order; reverse pairs are preserved (directional dedup)

Note: callers should use 'df = normalise_prediction_column(df)'
"""
from __future__ import annotations

import pandas as pd
from logmap_llm.constants import (
    POSITIVE_TOKENS,
    NEGATIVE_TOKENS,
    ORACLE_PREDICTION_COLUMN,
)

def _normalise_value(val):
    """
    coerce a single prediction value to a Python bool where possible
    """
    if isinstance(val, bool):
        return val
    
    if isinstance(val, str):
        low = val.strip().lower()
        if low in POSITIVE_TOKENS:
            return True
        if low in NEGATIVE_TOKENS:
            return False
        return val  # "error", "skipped", or any other unparseable string
    return val  # NaN, None, or any non-string non-bool


def normalise_prediction_column(df_or_series):
    """
    return a new df/series with the 'Oracle_prediction' column norm'd to bools (where possible)
    callers should write:: df = normalise_prediction_column(df)
    """
    if isinstance(df_or_series, pd.DataFrame):
        out = df_or_series.copy()
        out[ORACLE_PREDICTION_COLUMN] = out[ORACLE_PREDICTION_COLUMN].map(
            _normalise_value
        )
        return out
    return df_or_series.map(_normalise_value)


def prediction_is_true_mask(df_or_series) -> pd.Series:
    """
    return a boolean series where true means "the oracle accepted this mapping"
    Usgae:
        mask = prediction_is_true_mask(predictions_df)
        accepted = predictions_df[mask]
    """
    if isinstance(df_or_series, pd.DataFrame):
        col = df_or_series[ORACLE_PREDICTION_COLUMN]
    else:
        col = df_or_series
    return col.map(lambda v: _normalise_value(v) is True)


def filter_accepted_predictions(df: pd.DataFrame) -> pd.DataFrame:
    """
    return the subset of rows where the oracle accepted the mapping
    """
    return df[prediction_is_true_mask(df)]

def dedupe_m_ask_by_uri_pair(m_ask_df: "pd.DataFrame") -> "pd.DataFrame":
    """
    Collapse duplicate (source, target) M_ask rows to a single row (keep first), preserving order.

    The KG-ABOX 'both' lane policy can make LogMap emit a mixed-use undeclared predicate as BOTH a
    data-property AND an object-property mapping for the SAME URI pair. Left unmerged, that candidate
    would be asked to the oracle twice and double-counted in every oracle metric. Dedup is DIRECTIONAL
    on (source, target): reverse pairs (legitimate bidirectional queries) are preserved. Positional-safe
    (uses the first two columns). Logs how many duplicate rows were dropped.
    """
    if m_ask_df is None or len(m_ask_df) == 0:
        return m_ask_df
    key_cols = [m_ask_df.columns[0], m_ask_df.columns[1]]  # (source_uri, target_uri), positional-safe
    before = len(m_ask_df)
    deduped = m_ask_df.drop_duplicates(subset=key_cols, keep="first").reset_index(drop=True)
    dropped = before - len(deduped)
    if dropped > 0:
        try:
            from logmap_llm.utils.logging import warning
            warning(f"M_ask: dropped {dropped} duplicate (source,target) row(s) — e.g. a mixed-use "
                    f"predicate emitted in both property lanes — to avoid double-asking the oracle.")
        except Exception:
            pass
    return deduped

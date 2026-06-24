"""Generate a fresh leaderboard for a matching subset directly from the outputs tree.

The leaderboard is recomputed from the raw per-prediction CSVs every time it is built, so it
stays in sync whenever ``outputs/`` changes (new models, re-runs, extra experiments). For each
experiment found under ``outputs/{dataset}/{subset}/{model}/{exp_type}/{exp_name}/`` and each
prompt, it reports:

* quality metrics (accuracy, precision, recall, F1, specificity, Youden's index, TP/TN/FP/FN);
* reliability: failure rate and error counts;
* retry behaviour: mean/total retries and a per-error-type retry breakdown;
* cost: total USD plus a breakdown into input / cached / output / reasoning spend.

Typical use in a notebook::

    from src.leaderboard import build_leaderboard, rank_leaderboard
    board = build_leaderboard(subset="human-mouse")          # scan + recompute
    rank_leaderboard(board, metric="F1 Score", best_per_model=True, max_fail_rate=0.05)
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from config.config import OUTPUTS_DIR
from config.runs_vars import SUBSET_TO_DATASET_MAP
from src.constants import RESULTS_SEPARATOR
from src.error_taxonomy import RETRY_COUNT_COLUMNS, ErrorCategory, ErrorType
from src.estimations import ModelMetadata, build_openrouter_pricing_map, resolve_openrouter_id
from src.evaluate import compute_run_metrics, extend_preds_with_labels_info, get_gt_pairs, get_pred_pairs
from src.formatting import format_gt_pairs_filepath

LOGGER = logging.getLogger(__name__)

DEFAULT_PROMPTS = ["direct_entity", "direct_entity_with_synonyms"]

# Column groups used to give the wide metrics frame a readable, stable order.
ID_COLUMNS = ["subset", "model", "experiment_type", "experiment_name", "prompt", "num_samples"]
METRIC_COLUMNS = [
    "F1 Score", "Youden's index", "Accuracy", "Precision", "Recall", "Specificity", "Sensitivity",
    "TP", "TN", "FP", "FN",
]
RELIABILITY_COLUMNS = ["num_errors", "fail_rate", "mean_num_retries", "total_num_retries"]
COST_COLUMNS = ["cost_total_$", "cost_input_$", "cost_cached_$", "cost_output_$", "cost_reasoning_$"]
TOKEN_COLUMNS = [
    "total_input_tokens", "total_output_tokens", "total_input_cached_tokens",
    "total_output_reasoning_tokens", "total_proc_time", "mean_proc_time",
]


def cost_breakdown(meta: ModelMetadata | None, metrics: dict) -> dict[str, float]:
    """Split spend into input / cached / output / reasoning USD from token totals and rates."""
    if meta is None:
        return dict.fromkeys(COST_COLUMNS, float("nan"))

    inp = float(metrics.get("total_input_tokens", 0) or 0)
    out = float(metrics.get("total_output_tokens", 0) or 0)
    cached = float(metrics.get("total_input_cached_tokens", 0) or 0)
    reasoning = float(metrics.get("total_output_reasoning_tokens", 0) or 0)

    non_cached_input = max(inp - cached, 0)
    cost_input = non_cached_input * meta.prompt_rate
    cost_cached = cached * (meta.cache_read_rate or meta.prompt_rate)
    cost_reasoning = reasoning * (meta.reasoning_rate or meta.completion_rate)
    cost_output = max(out - reasoning, 0) * meta.completion_rate
    return {
        "cost_total_$": cost_input + cost_cached + cost_output + cost_reasoning,
        "cost_input_$": cost_input,
        "cost_cached_$": cost_cached,
        "cost_output_$": cost_output,
        "cost_reasoning_$": cost_reasoning,
    }


def _build_pricing(models: list[str]) -> dict[str, ModelMetadata]:
    """Resolve per-model OpenRouter pricing once; empty dict if the API is unreachable."""
    try:
        pricing_map = build_openrouter_pricing_map()
    except Exception as exc:  # noqa: BLE001 - offline / API failure must not break the leaderboard
        LOGGER.warning("Could not fetch OpenRouter pricing (%s); cost columns will be empty.", exc)
        return {}

    metas: dict[str, ModelMetadata] = {}
    for model in models:
        or_id = resolve_openrouter_id(model)
        pricing = pricing_map.get(or_id) if or_id else None
        if pricing is not None:
            metas[model] = ModelMetadata.from_openrouter_pricing(model, pricing)
    return metas


def _prompt_from_filename(stem: str, model: str, suffix: str) -> str:
    prompt = stem.replace(f"_results{suffix}", "")
    marker = f"{model}_"
    return prompt.split(marker, 1)[-1] if marker in prompt else prompt


def build_leaderboard(
    subset: str = "human-mouse",
    outputs_dir: Path | None = None,
    prompts: list[str] | None = None,
    suffix: str = "_reduced",
    with_cost: bool = True,
) -> pd.DataFrame:
    """Scan every experiment for ``subset`` and return one row per (experiment, prompt).

    Metrics are recomputed from predictions + ground truth, so the table reflects the current
    state of ``outputs/``. Set ``with_cost=False`` to skip the (network) pricing lookup.
    """
    outputs_dir = outputs_dir or OUTPUTS_DIR
    prompts = prompts or DEFAULT_PROMPTS
    dataset = SUBSET_TO_DATASET_MAP.get(subset, "")
    subset_dir = outputs_dir / dataset / subset
    if not subset_dir.exists():
        msg = f"No outputs found for subset '{subset}' at {subset_dir}"
        raise FileNotFoundError(msg)

    gt_df = get_gt_pairs(format_gt_pairs_filepath(dataset, subset))

    rows: list[dict] = []
    models_seen: set[str] = set()
    for model_dir in sorted(subset_dir.iterdir()):
        if not model_dir.is_dir() or model_dir.name.startswith("."):
            continue
        model = model_dir.name
        for exp_type_dir in sorted(model_dir.iterdir()):
            if not exp_type_dir.is_dir():
                continue
            for exp_dir in sorted(exp_type_dir.iterdir()):
                if not exp_dir.is_dir():
                    continue
                for csv_file in sorted(exp_dir.glob(f"*_results{suffix}.csv")):
                    if csv_file.name == f"results{suffix}.csv":
                        continue
                    prompt = _prompt_from_filename(csv_file.stem, model, suffix)
                    if prompts and prompt not in prompts:
                        continue
                    try:
                        pred_df = get_pred_pairs(csv_file, sep=RESULTS_SEPARATOR)
                    except (pd.errors.ParserError, pd.errors.EmptyDataError, OSError) as exc:
                        LOGGER.debug("Unreadable results file %s (%s)", csv_file, exc)
                        continue
                    if pred_df.empty:
                        LOGGER.debug("Empty results file %s", csv_file)
                        continue
                    try:
                        labelled = extend_preds_with_labels_info(pred_df, gt_df)
                        metrics = compute_run_metrics(labelled)
                    except Exception as exc:  # noqa: BLE001 - keep scanning despite one bad run
                        LOGGER.warning("Skipping %s (%s)", csv_file, exc)
                        continue

                    models_seen.add(model)
                    rows.append(
                        {
                            "subset": subset,
                            "model": model,
                            "experiment_type": exp_type_dir.name,
                            "experiment_name": exp_dir.name,
                            "prompt": prompt,
                            "num_samples": len(labelled),
                            "fail_rate": metrics.get("error_rate", 0.0),
                            **metrics,
                        }
                    )

    board = pd.DataFrame(rows)
    if board.empty:
        return board

    if with_cost:
        metas = _build_pricing(sorted(models_seen))
        cost_rows = [cost_breakdown(metas.get(r["model"]), r) for r in rows]
        board = pd.concat([board, pd.DataFrame(cost_rows)], axis=1)

    return _order_columns(board)


def _order_columns(board: pd.DataFrame) -> pd.DataFrame:
    retry_cols = [f"total_{c}" for c in RETRY_COUNT_COLUMNS if f"total_{c}" in board.columns]
    error_cols = [c for c in board.columns if c.startswith(("errors_", "errors_cat_"))]
    lead = ID_COLUMNS + [c for c in METRIC_COLUMNS if c in board.columns] + RELIABILITY_COLUMNS
    lead += [c for c in COST_COLUMNS if c in board.columns]
    lead += retry_cols + error_cols + [c for c in TOKEN_COLUMNS if c in board.columns]
    ordered = [c for c in lead if c in board.columns]
    rest = [c for c in board.columns if c not in ordered]
    return board[ordered + rest]


def rank_leaderboard(
    board: pd.DataFrame,
    metric: str = "F1 Score",
    best_per_model: bool = False,
    max_fail_rate: float | None = None,
    ascending: bool = False,
) -> pd.DataFrame:
    """Sort the leaderboard by ``metric``, optionally filtering unreliable runs / collapsing per model.

    ``max_fail_rate`` drops runs whose ``fail_rate`` exceeds the threshold (e.g. 0.05); these
    runs report metrics on a fraction of the pairs and are not comparable. ``best_per_model``
    keeps only each model's best row.
    """
    ranked = board.copy()
    if max_fail_rate is not None:
        ranked = ranked[ranked["fail_rate"] <= max_fail_rate]
    ranked = ranked.sort_values(metric, ascending=ascending)
    if best_per_model:
        ranked = ranked.drop_duplicates(subset="model", keep="first")
    return ranked.reset_index(drop=True)


def retry_error_summary(board: pd.DataFrame) -> pd.DataFrame:
    """Aggregate per-error-type retry counts across the leaderboard (for the retry-errors report)."""
    retry_cols = [f"total_{c}" for c in RETRY_COUNT_COLUMNS if f"total_{c}" in board.columns]
    error_cols = [
        c for c in board.columns
        if c.startswith("errors_") and not c.startswith("errors_cat_")
        and c[len("errors_"):] in {e.value for e in ErrorType}
    ]
    category_values = {e.value for e in ErrorCategory}
    cat_cols = [
        c for c in board.columns
        if c.startswith("errors_cat_") and c[len("errors_cat_"):] in category_values
    ]
    keep = ["model", "experiment_type", "experiment_name", "prompt", *retry_cols, *error_cols, *cat_cols]
    summary = board[[c for c in keep if c in board.columns]].copy()
    value_cols = [c for c in summary.columns if c not in {"model", "experiment_type", "experiment_name", "prompt"}]
    return summary[summary[value_cols].fillna(0).sum(axis=1) > 0].reset_index(drop=True)

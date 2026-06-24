# ruff: noqa: T201
from __future__ import annotations

import json
import logging
import urllib.request
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field

from config.config import OUTPUTS_DIR
from config.runs_vars import DATASET_SUBSETS_MAP, SUBSET_TO_DATASET_MAP
from src.constants import USAGE_COLUMNS

LOGGER = logging.getLogger(__name__)

MILLION = 1_000_000

_LOCAL_TO_OPENROUTER: dict[str, str | None] = {
    "gemini-1.5-flash": "google/gemini-1.5-flash",
    "gemini-1.5-flash-lite": "google/gemini-1.5-flash",
    "gemini-2.0-flash": "google/gemini-2.0-flash-001",
    "gemini-2.0-flash-lite": "google/gemini-2.0-flash-lite-001",
    "gemini-2.5-flash": "google/gemini-2.5-flash",
    "gemini-2.5-flash-lite": "google/gemini-2.5-flash-lite",
    "gemini-2.5-pro": "google/gemini-2.5-pro",
    "gemini-2.5-flash-preview-04-17": "google/gemini-2.5-flash",
    "gemini-3-pro-preview": "google/gemini-3-pro-image-preview",
    "gpt-4o-mini": "openai/gpt-4o-mini",
    "gpt-4.1-nano": "openai/gpt-4.1-nano",
    "gpt-5-nano": "openai/gpt-5-nano",
    "gpt-5-mini": "openai/gpt-5-mini",
    "mistral.mistral-large-2402-v1:0": "mistralai/mistral-large-2512",
    "mistral.mistral-small-2402-v1:0": "mistralai/mistral-small-3.2-24b-instruct",
    # New models (added 2026-05)
    "x-ai|grok-4.3": "x-ai/grok-4.3",
    "x-ai|grok-4.20": "x-ai/grok-4.20",
    "anthropic|claude-opus-4.7": "anthropic/claude-opus-4.7",
    "openai|gpt-5.5": "openai/gpt-5.5",
    "openai|gpt-5.4-mini": "openai/gpt-5.4-mini",
    "deepseek|deepseek-v4-pro": "deepseek/deepseek-v4-pro",
    "deepseek|deepseek-v4-flash": "deepseek/deepseek-v4-flash",
    "mistralai|mistral-medium-3-5": "mistralai/mistral-medium-3-5",
    "mistralai|mistral-small-2603": "mistralai/mistral-small-2603",
    "ibm-granite|granite-4.1-8b": "ibm-granite/granite-4.1-8b",
    "google|gemma-4-31b-it": "google/gemma-4-31b-it",
    "google|gemma-4-26b-a4b-it": "google/gemma-4-26b-a4b-it",
    "nvidia|nemotron-3-nano-omni-30b-a3b-reasoning": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
    "nvidia|nemotron-3-super-120b-a12b": "nvidia/nemotron-3-super-120b-a12b",
    "z-ai|glm-5.1": "z-ai/glm-5.1",
    "qwen|qwen3.6-flash": "qwen/qwen3.6-flash",
    "qwen|qwen3.6-35b-a3b": "qwen/qwen3.6-35b-a3b",
    "qwen|qwen3.6-max-preview": "qwen/qwen3.6-max-preview",
    "qwen|qwen3.5-397b-a17b": "qwen/qwen3.5-397b-a17b",
    "qwen|qwen3.5-9b": "qwen/qwen3.5-9b",
    "minimax|minimax-m2.7": "minimax/minimax-m2.7",
    "bytedance-seed|seed-2.0-lite": "bytedance-seed/seed-2.0-lite",
    "moonshotai|kimi-k2.6": "moonshotai/kimi-k2.6",
    "meta.llama3-70b-instruct-v1:0": "meta-llama/llama-3-70b-instruct",
    "us.meta.llama3-2-3b-instruct-v1:0": "meta-llama/llama-3.2-3b-instruct",
    "anthropic.claude-3-sonnet-20240229-v1:0": "anthropic/claude-3-sonnet",
    "anthropic.claude-instant-v1": "anthropic/claude-instant-1.2",
    "us.anthropic.claude-3-7-sonnet-20250219-v1:0": "anthropic/claude-3.7-sonnet",
    # New candidates surfaced from OpenRouter (2026-06)
    "anthropic|claude-fable-5": "anthropic/claude-fable-5",
    "google|gemini-3.5-flash": "google/gemini-3.5-flash",
    "qwen|qwen3.7-plus": "qwen/qwen3.7-plus",
    "xiaomi|mimo-v2.5": "xiaomi/mimo-v2.5",
    "openai|gpt-5.5-pro": "openai/gpt-5.5-pro",
    "qwen3-8B": None,
    "qwen3-1.7B": None,
}


class ModelMetadata(BaseModel):
    name: str
    prompt_rate: float = Field(description="USD per input token")
    completion_rate: float = Field(description="USD per output token")
    cache_read_rate: float | None = Field(default=None, description="USD per cached-input token")
    reasoning_rate: float | None = Field(default=None, description="USD per reasoning output token")

    @classmethod
    def from_per_million(
        cls,
        name: str,
        prompt: float,
        completion: float,
        cache_read: float | None = None,
        reasoning: float | None = None,
    ) -> ModelMetadata:
        return cls(
            name=name,
            prompt_rate=prompt / MILLION,
            completion_rate=completion / MILLION,
            cache_read_rate=cache_read / MILLION if cache_read is not None else None,
            reasoning_rate=reasoning / MILLION if reasoning is not None else None,
        )

    @classmethod
    def from_openrouter_pricing(cls, name: str, pricing: dict[str, str | None]) -> ModelMetadata:
        def _f(v: str | None) -> float | None:
            return float(v) if v is not None and v != "0" else None

        return cls(
            name=name,
            prompt_rate=_f(pricing.get("prompt")) or 0.0,
            completion_rate=_f(pricing.get("completion")) or 0.0,
            cache_read_rate=_f(pricing.get("input_cache_read")),
        )

    def cost_for_tokens(
        self,
        input_tokens: float,
        output_tokens: float,
        cached_tokens: float = 0,
        reasoning_tokens: float = 0,
    ) -> float:
        non_cached_input = max(input_tokens - cached_tokens, 0)
        cached_cost = cached_tokens * (self.cache_read_rate or self.prompt_rate)
        input_cost = non_cached_input * self.prompt_rate
        reasoning_cost = reasoning_tokens * (self.reasoning_rate or self.completion_rate)
        normal_output = max(output_tokens - reasoning_tokens, 0)
        output_cost = normal_output * self.completion_rate + reasoning_cost
        return input_cost + cached_cost + output_cost

    def cost_for_usage_row(self, row: pd.Series) -> float:
        return self.cost_for_tokens(
            input_tokens=float(row.get("input_tokens", 0) or 0),
            output_tokens=float(row.get("output_tokens", 0) or 0),
            cached_tokens=float(row.get("input_cached_tokens", 0) or 0),
            reasoning_tokens=float(row.get("output_reasoning_tokens", 0) or 0),
        )


_OPENROUTER_API = "https://openrouter.ai/api/v1/models"


def fetch_openrouter_models(timeout: int = 30) -> list[dict[str, Any]]:
    req = urllib.request.Request(_OPENROUTER_API)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())
    return data["data"]


def build_openrouter_pricing_map(models: list[dict] | None = None) -> dict[str, dict]:
    if models is None:
        models = fetch_openrouter_models()
    return {m["id"]: m.get("pricing", {}) for m in models}


def resolve_openrouter_id(local_name: str) -> str | None:
    if local_name in _LOCAL_TO_OPENROUTER:
        return _LOCAL_TO_OPENROUTER[local_name]
    if "|" in local_name:
        return local_name.replace("|", "/")
    return None


def fetch_model_metadata(
    model_names: list[str] | None = None,
    pricing_map: dict[str, dict] | None = None,
) -> dict[str, ModelMetadata]:
    if pricing_map is None:
        pricing_map = build_openrouter_pricing_map()

    if model_names is None:
        exp_path = Path("model_to_experiments.json")
        if exp_path.exists():
            with exp_path.open() as f:
                model_names = list(json.load(f).keys())
        else:
            model_names = []

    result: dict[str, ModelMetadata] = {}
    for name in model_names:
        or_id = resolve_openrouter_id(name)
        if or_id is None:
            LOGGER.warning("No OpenRouter mapping for '%s' (local model?), skipping.", name)
            continue
        pricing = pricing_map.get(or_id)
        if pricing is None:
            LOGGER.warning("Model '%s' (→ %s) not found on OpenRouter.", name, or_id)
            continue
        result[name] = ModelMetadata.from_openrouter_pricing(name, pricing)
    return result


SUBTASK_NUM_PAIRS: dict[str, dict[str, int]] = {
    "ncit-doid": {"reduced": 3281, "full": 4687},
    "omim-ordo": {"reduced": 2606, "full": 3722},
    "snomed-fma.body": {"reduced": 5080, "full": 7257},
    "snomed-ncit.neoplas": {"reduced": 2664, "full": 3805},
    "snomed-ncit.pharm": {"reduced": 4063, "full": 5804},
    "fma-nci": {"reduced": 1770, "full": 3024},
    "fma-snomed": {"reduced": 2904, "full": 9008},
    "snomed-nci": {"reduced": 5144, "full": 18844},
    "human-mouse": {"reduced": 508, "full": 1516},
}


def get_num_pairs(subset: str, size: str = "reduced") -> int:
    return SUBTASK_NUM_PAIRS.get(subset, {}).get(size, 0)


def get_all_tasks() -> list[str]:
    return [s for subsets in DATASET_SUBSETS_MAP.values() for s in subsets]


def load_real_usage(
    subset: str,
    model: str,
    experiment_type: str,
    exp_name: str,
    prompt: str = "direct_entity_with_synonyms",
) -> pd.DataFrame | None:
    dataset = SUBSET_TO_DATASET_MAP.get(subset, "")
    base = OUTPUTS_DIR / dataset / subset / model / experiment_type / exp_name
    pattern = f"{subset}_{model}_{prompt}_results_reduced.csv"
    candidates = list(base.glob(f"**/{pattern}"))
    if not candidates:
        pattern2 = f"{subset}_{model}_{prompt}_results.csv"
        candidates = list(base.glob(f"**/{pattern2}"))
    if not candidates:
        return None

    pred_data = pd.read_csv(candidates[0])
    usage_present = [c for c in USAGE_COLUMNS if c in pred_data.columns]
    if not usage_present:
        return None
    return pred_data[usage_present]


def load_token_usage_stats(
    subset: str,
    model: str,
    experiment_type: str,
    exp_name: str,
    prompt: str = "direct_entity_with_synonyms",
) -> dict[str, float] | None:
    dataset = SUBSET_TO_DATASET_MAP.get(subset, "")
    base = OUTPUTS_DIR / dataset / subset / model / experiment_type / exp_name
    pattern = f"{subset}_{model}_{prompt}_token_usage_reduced.csv"
    candidates = list(base.glob(f"**/{pattern}"))

    stats: dict[str, float] = {}
    if candidates:
        stats_data = pd.read_csv(candidates[0])
        if not stats_data.empty and "Value" in stats_data.columns:
            raw = zip(stats_data["Metric"], stats_data["Value"])
            stats = {k: float(v) for k, v in raw if pd.notna(v) and str(v).strip()}

    if not stats:
        usage_df = load_real_usage(subset, model, experiment_type, exp_name, prompt)
        if usage_df is not None and not usage_df.empty:
            numeric_df = usage_df.apply(pd.to_numeric, errors="coerce")
            for col in USAGE_COLUMNS:
                if col in numeric_df.columns:
                    valid = numeric_df[col].dropna()
                    if len(valid) > 0:
                        stats[f"mean_{col}"] = float(valid.mean())
                        stats[f"total_{col}"] = float(valid.sum()) if col == "proc_time" else int(valid.sum())

    return stats or None


def collect_all_usage_stats(
    models: list[str] | None = None,
    subsets: list[str] | None = None,
    experiment_types: list[str] | None = None,
    prompts: list[str] | None = None,
) -> pd.DataFrame:
    if subsets is None:
        subsets = get_all_tasks()
    if prompts is None:
        prompts = ["direct_entity", "direct_entity_with_synonyms"]

    rows = []
    for subset in subsets:
        dataset = SUBSET_TO_DATASET_MAP.get(subset, "")
        base_dir = OUTPUTS_DIR / dataset / subset
        if not base_dir.exists():
            continue

        model_dirs = [d for d in base_dir.iterdir() if d.is_dir()] if models is None else [base_dir / m for m in models]
        for model_dir in model_dirs:
            if not model_dir.exists() or not model_dir.is_dir():
                continue
            model_name = model_dir.name
            for exp_type_dir in model_dir.iterdir():
                if not exp_type_dir.is_dir():
                    continue
                exp_type = exp_type_dir.name
                if experiment_types and exp_type not in experiment_types:
                    continue
                for exp_dir in exp_type_dir.iterdir():
                    if not exp_dir.is_dir():
                        continue
                    for prompt in prompts:
                        stats = load_token_usage_stats(subset, model_name, exp_type, exp_dir.name, prompt)
                        if stats:
                            rows.append(
                                {
                                    "subset": subset,
                                    "dataset": dataset,
                                    "model": model_name,
                                    "experiment_type": exp_type,
                                    "exp_name": exp_dir.name,
                                    "prompt": prompt,
                                    **stats,
                                }
                            )
    return pd.DataFrame(rows)


def load_performance_stats(
    subset: str,
    model: str,
    experiment_type: str,
    exp_name: str,
    prompt: str = "direct_entity_with_synonyms",
    suffix: str = "_reduced",
) -> dict[str, float] | None:
    dataset = SUBSET_TO_DATASET_MAP.get(subset, "")
    base = OUTPUTS_DIR / dataset / subset / model / experiment_type / exp_name
    pattern = f"{subset}_{model}_{prompt}_stats{suffix}.txt"
    candidates = list(base.glob(f"**/{pattern}"))
    if not candidates:
        return None
    try:
        stats_data = pd.read_csv(candidates[0])
        if stats_data.empty or "Value" not in stats_data.columns:
            return None
        return {row["Metric"]: float(row["Value"]) for _, row in stats_data.iterrows() if pd.notna(row["Value"])}
    except (pd.errors.ParserError, pd.errors.EmptyDataError, OSError, ValueError):
        return None


def collect_all_experiment_stats(
    models: list[str] | None = None,
    subsets: list[str] | None = None,
    prompts: list[str] | None = None,
) -> pd.DataFrame:
    if subsets is None:
        subsets = get_all_tasks()
    if prompts is None:
        prompts = ["direct_entity", "direct_entity_with_synonyms"]

    rows = []
    for subset in subsets:
        dataset = SUBSET_TO_DATASET_MAP.get(subset, "")
        base_dir = OUTPUTS_DIR / dataset / subset
        if not base_dir.exists():
            continue

        model_dirs = [d for d in base_dir.iterdir() if d.is_dir()] if models is None else [base_dir / m for m in models]
        for model_dir in model_dirs:
            if not model_dir.exists() or not model_dir.is_dir():
                continue
            model_name = model_dir.name
            for exp_type_dir in model_dir.iterdir():
                if not exp_type_dir.is_dir():
                    continue
                exp_type = exp_type_dir.name
                for exp_dir in exp_type_dir.iterdir():
                    if not exp_dir.is_dir():
                        continue
                    for prompt in prompts:
                        usage = load_token_usage_stats(subset, model_name, exp_type, exp_dir.name, prompt)
                        perf = load_performance_stats(subset, model_name, exp_type, exp_dir.name, prompt)
                        if not usage and not perf:
                            continue
                        row: dict[str, Any] = {
                            "subset": subset,
                            "dataset": dataset,
                            "model": model_name,
                            "experiment_type": exp_type,
                            "exp_name": exp_dir.name,
                            "prompt": prompt,
                        }
                        if usage:
                            row.update(usage)
                        if perf:
                            row.update({f"perf_{k}": v for k, v in perf.items()})
                        rows.append(row)
    return pd.DataFrame(rows)


class UsageProfile(BaseModel):
    mean_input_tokens: float
    mean_output_tokens: float
    mean_cached_tokens: float = 0.0
    mean_reasoning_tokens: float = 0.0
    mean_proc_time: float = 0.0

    @classmethod
    def from_usage_stats(cls, stats: dict[str, float]) -> UsageProfile:
        return cls(
            mean_input_tokens=stats.get("mean_input_tokens", 0),
            mean_output_tokens=stats.get("mean_output_tokens", 0),
            mean_cached_tokens=stats.get("mean_input_cached_tokens", 0),
            mean_reasoning_tokens=stats.get("mean_output_reasoning_tokens", 0),
            mean_proc_time=stats.get("mean_proc_time", 0),
        )

    @classmethod
    def from_dataframe(cls, usage_df: pd.DataFrame) -> UsageProfile:
        def _col_mean(col: str) -> float:
            if col not in usage_df.columns:
                return 0.0
            return float(pd.to_numeric(usage_df[col], errors="coerce").mean())

        return cls(
            mean_input_tokens=_col_mean("input_tokens"),
            mean_output_tokens=_col_mean("output_tokens"),
            mean_cached_tokens=_col_mean("input_cached_tokens"),
            mean_reasoning_tokens=_col_mean("output_reasoning_tokens"),
            mean_proc_time=_col_mean("proc_time"),
        )

    def with_reasoning_budget(self, reasoning_tokens: float) -> UsageProfile:
        return self.model_copy(update={"mean_reasoning_tokens": reasoning_tokens})

    def with_few_shots(self, n_shots: int, tokens_per_shot: float = 150) -> UsageProfile:
        extra = n_shots * tokens_per_shot
        return self.model_copy(update={"mean_input_tokens": self.mean_input_tokens + extra})


def estimate_task_cost(
    model: ModelMetadata,
    subset: str,
    usage: UsageProfile,
    size: str = "reduced",
    n_versions: int = 1,
) -> float:
    n_pairs = get_num_pairs(subset, size)
    per_pair = model.cost_for_tokens(
        input_tokens=usage.mean_input_tokens,
        output_tokens=usage.mean_output_tokens,
        cached_tokens=usage.mean_cached_tokens,
        reasoning_tokens=usage.mean_reasoning_tokens,
    )
    return per_pair * n_pairs * n_versions


def estimate_dataset_cost(
    model: ModelMetadata,
    dataset: str,
    usage: UsageProfile,
    size: str = "reduced",
    n_versions: int = 1,
) -> dict[str, float]:
    subsets = DATASET_SUBSETS_MAP.get(dataset, [])
    return {s: estimate_task_cost(model, s, usage, size=size, n_versions=n_versions) for s in subsets}


def estimate_full_eval_cost(
    model: ModelMetadata,
    usage: UsageProfile,
    size: str = "reduced",
    n_versions: int = 1,
    n_prompts: int = 2,
) -> dict[str, float]:
    costs = {}
    for subset in get_all_tasks():
        costs[subset] = estimate_task_cost(model, subset, usage, size=size, n_versions=n_versions) * n_prompts
    return costs


def build_cost_comparison_table(
    models: dict[str, ModelMetadata],
    usage: UsageProfile,
    size: str = "reduced",
    n_versions: int = 1,
    n_prompts: int = 2,
    reasoning_budgets: list[float] | None = None,
    few_shot_configs: list[int] | None = None,
    tokens_per_shot: float = 150,
) -> pd.DataFrame:
    configs: list[tuple[str, UsageProfile]] = []

    if reasoning_budgets is None and few_shot_configs is None:
        configs.append(("base", usage))
    else:
        for rb in reasoning_budgets or [0]:
            u = usage.with_reasoning_budget(rb)
            for ns in few_shot_configs or [0]:
                u2 = u.with_few_shots(ns, tokens_per_shot) if ns > 0 else u
                label = f"reason={int(rb)},shots={ns}"
                configs.append((label, u2))

    rows = []
    all_subsets = get_all_tasks()
    for model_name, model_meta in models.items():
        for config_label, profile in configs:
            row: dict[str, Any] = {
                "Model": model_name,
                "Config": config_label,
                "Experiment": f"{model_name}&{config_label}",
            }
            total = 0.0
            for subset in all_subsets:
                cost = estimate_task_cost(model_meta, subset, profile, size=size, n_versions=n_versions) * n_prompts
                row[subset] = cost
                total += cost
            row["Total"] = total
            rows.append(row)

    return pd.DataFrame(rows)


def build_cost_table_from_real_usage(
    models: dict[str, ModelMetadata],
    reference_usage: dict[str, UsageProfile],
    target_subsets: list[str] | None = None,
    size: str = "reduced",
    n_versions: int = 1,
    n_prompts: int = 2,
) -> pd.DataFrame:
    if target_subsets is None:
        target_subsets = get_all_tasks()

    if reference_usage:
        fallback = UsageProfile(
            mean_input_tokens=float(np.mean([u.mean_input_tokens for u in reference_usage.values()])),
            mean_output_tokens=float(np.mean([u.mean_output_tokens for u in reference_usage.values()])),
            mean_cached_tokens=float(np.mean([u.mean_cached_tokens for u in reference_usage.values()])),
            mean_reasoning_tokens=float(np.mean([u.mean_reasoning_tokens for u in reference_usage.values()])),
            mean_proc_time=float(np.mean([u.mean_proc_time for u in reference_usage.values()])),
        )
    else:
        fallback = UsageProfile(mean_input_tokens=300, mean_output_tokens=20)

    rows = []
    for model_name, model_meta in models.items():
        row: dict[str, Any] = {"Model": model_name}
        total = 0.0
        for subset in target_subsets:
            profile = reference_usage.get(subset, fallback)
            cost = estimate_task_cost(model_meta, subset, profile, size=size, n_versions=n_versions) * n_prompts
            row[subset] = cost
            total += cost
        row["Total"] = total
        rows.append(row)

    return pd.DataFrame(rows)


def format_cost(value: float) -> str:
    if value < 0.01:
        return f"${value:.4f}"
    if value < 1:
        return f"${value:.3f}"
    return f"${value:.2f}"


def summarize_model_pricing(models: dict[str, ModelMetadata]) -> pd.DataFrame:
    rows = []
    for name, m in models.items():
        rows.append(
            {
                "Model": name,
                "Input ($/1M)": m.prompt_rate * MILLION,
                "Output ($/1M)": m.completion_rate * MILLION,
                "Cache ($/1M)": m.cache_read_rate * MILLION if m.cache_read_rate else None,
                "Reasoning ($/1M)": m.reasoning_rate * MILLION if m.reasoning_rate else None,
            }
        )
    return pd.DataFrame(rows).set_index("Model")


def build_real_usage_cost_table(
    usage_stats_df: pd.DataFrame,
    model_metadata: dict[str, ModelMetadata],
    tasks: list[str] | None = None,
    size: str = "reduced",
    n_prompts: int = 2,
) -> pd.DataFrame:
    """Estimate per-task cost for each (model, experiment) from collected usage stats.

    Real per-subset usage is used where available; subsets without data fall back to the
    experiment's average profile. Returns one row per (model, experiment) with a column per task,
    a ``{task}_source`` marker (``real``/``scaled``), ``Total`` and real/scaled task counts.
    """
    tasks = tasks or get_all_tasks()
    experiment_usage: dict[tuple[str, str, str], UsageProfile] = {}
    experiment_fallback: dict[tuple[str, str], UsageProfile] = {}

    for (model, exp_name), group in usage_stats_df.groupby(["model", "exp_name"]):
        subset_profiles: dict[str, UsageProfile] = {}
        for subset, sub_group in group.groupby("subset"):
            cached = sub_group.get("mean_input_cached_tokens", pd.Series([0])).mean()
            reasoning = sub_group.get("mean_output_reasoning_tokens", pd.Series([0])).mean()
            profile = UsageProfile.from_usage_stats(
                {
                    "mean_input_tokens": sub_group["mean_input_tokens"].mean(),
                    "mean_output_tokens": sub_group["mean_output_tokens"].mean(),
                    "mean_input_cached_tokens": cached,
                    "mean_output_reasoning_tokens": reasoning,
                    "mean_proc_time": sub_group.get("mean_proc_time", pd.Series([0])).mean(),
                }
            )
            experiment_usage[(model, exp_name, str(subset))] = profile
            subset_profiles[str(subset)] = profile

        if subset_profiles:
            experiment_fallback[(model, exp_name)] = UsageProfile(
                mean_input_tokens=float(np.mean([p.mean_input_tokens for p in subset_profiles.values()])),
                mean_output_tokens=float(np.mean([p.mean_output_tokens for p in subset_profiles.values()])),
                mean_cached_tokens=float(np.mean([p.mean_cached_tokens for p in subset_profiles.values()])),
                mean_reasoning_tokens=float(np.mean([p.mean_reasoning_tokens for p in subset_profiles.values()])),
                mean_proc_time=float(np.mean([p.mean_proc_time for p in subset_profiles.values()])),
            )

    rows: list[dict[str, Any]] = []
    for (model, exp_name), fallback in experiment_fallback.items():
        model_meta = model_metadata.get(model)
        if model_meta is None:
            continue
        row: dict[str, Any] = {"Model": model, "Experiment": exp_name}
        total, real_count, scaled_count = 0.0, 0, 0
        for subset in tasks:
            profile = experiment_usage.get((model, exp_name, subset), fallback)
            is_real = (model, exp_name, subset) in experiment_usage
            cost = estimate_task_cost(model_meta, subset, profile, size=size, n_versions=1) * n_prompts
            row[subset] = cost
            row[f"{subset}_source"] = "real" if is_real else "scaled"
            total += cost
            real_count += int(is_real)
            scaled_count += int(not is_real)
        row["Total"] = total
        row["real_tasks"] = real_count
        row["scaled_tasks"] = scaled_count
        rows.append(row)

    return pd.DataFrame(rows)


def add_experiment_costs(
    stats_df: pd.DataFrame,
    model_metadata: dict[str, ModelMetadata],
    subset: str = "human-mouse",
    size: str = "reduced",
) -> pd.DataFrame:
    """Add ``cost_per_pair`` and ``total_cost`` columns from per-row mean token usage."""
    result = stats_df.copy()
    n_pairs = get_num_pairs(subset, size)

    def _per_pair(row: pd.Series) -> float:
        model_meta = model_metadata.get(row["model"])
        if model_meta is None:
            return float("nan")
        return model_meta.cost_for_tokens(
            input_tokens=float(row.get("mean_input_tokens") or 0),
            output_tokens=float(row.get("mean_output_tokens") or 0),
            cached_tokens=float(row.get("mean_input_cached_tokens") or 0),
            reasoning_tokens=float(row.get("mean_output_reasoning_tokens") or 0),
        )

    result["cost_per_pair"] = result.apply(_per_pair, axis=1)
    result["total_cost"] = result["cost_per_pair"] * n_pairs
    return result


def compute_cost_components(
    token_agg_df: pd.DataFrame,
    model_metadata: dict[str, ModelMetadata],
    label_col: str = "exp_name",
) -> pd.DataFrame:
    """Split per-pair cost into Input / Cached Input / Output / Reasoning components per experiment."""
    rows: list[dict[str, Any]] = []
    for _, row in token_agg_df.iterrows():
        model_meta = model_metadata.get(row["model"])
        if model_meta is None:
            continue
        input_tokens = float(row.get("mean_input_tokens") or 0)
        output_tokens = float(row.get("mean_output_tokens") or 0)
        cached_tokens = float(row.get("mean_input_cached_tokens") or 0)
        reasoning_tokens = float(row.get("mean_output_reasoning_tokens") or 0)
        rows.append(
            {
                "label": row.get(label_col, row.get("exp_name")),
                "model": row["model"],
                "exp_name": row["exp_name"],
                "Input Cost": max(input_tokens - cached_tokens, 0) * model_meta.prompt_rate,
                "Cached Input Cost": cached_tokens * (model_meta.cache_read_rate or model_meta.prompt_rate),
                "Output Cost": max(output_tokens - reasoning_tokens, 0) * model_meta.completion_rate,
                "Reasoning Cost": reasoning_tokens * (model_meta.reasoning_rate or model_meta.completion_rate),
            }
        )
    components = pd.DataFrame(rows)
    if not components.empty:
        components["Total Cost"] = components[
            ["Input Cost", "Cached Input Cost", "Output Cost", "Reasoning Cost"]
        ].sum(axis=1)
    return components


def add_token_breakdown_pct(token_agg_df: pd.DataFrame) -> pd.DataFrame:
    """Add total tokens plus input/output/cache-hit/reasoning percentage columns."""
    bd = token_agg_df.copy()
    bd["total_tokens"] = bd["mean_input_tokens"] + bd["mean_output_tokens"]
    bd["input_pct"] = (bd["mean_input_tokens"] / bd["total_tokens"] * 100).round(1)
    bd["output_pct"] = (bd["mean_output_tokens"] / bd["total_tokens"] * 100).round(1)
    cached = bd.get("mean_input_cached_tokens", pd.Series(0, index=bd.index))
    reasoning = bd.get("mean_output_reasoning_tokens", pd.Series(0, index=bd.index))
    bd["cache_hit_pct"] = (cached / bd["mean_input_tokens"].replace(0, np.nan) * 100).round(1).fillna(0)
    bd["reasoning_pct"] = (reasoning / bd["mean_output_tokens"].replace(0, np.nan) * 100).round(1).fillna(0)
    return bd

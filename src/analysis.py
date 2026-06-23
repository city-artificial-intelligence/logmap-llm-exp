# ruff: noqa: T201
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from itertools import product
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from config.config import METRICS_DIR, OUTPUTS_DIR, RUN_DIR
from config.runs_vars import DATASET_SUBSETS_MAP, SUBSET_TO_DATASET_MAP
from src.error_taxonomy import ERROR_COLUMNS, ErrorCategory, ErrorType

DEFAULT_PROMPT_NAMES_MAP: dict[str, str] = {
    "direct_entity_ontological": "P",
    "sequential_hierarchy_ontological": "P_{EC}",
    "direct_entity": "P^{NLF}",
    "sequential_hierarchy": "P_{EC}^{NLF}",
    "direct_entity_with_synonyms": "P_{S}^{NLF}",
    "sequential_hierarchy_with_synonyms": "P_{EC+S}^{NLF}",
}

DEFAULT_MODEL_NAMES_MAP: dict[str, str] = {
    "gemini-1.5-flash": "Flash.1.5",
    "gemini-2.0-flash": "Flash.2.0",
    "gemini-2.0-flash-lite": "Flash.2.0.lite",
    "gemini-2.5-flash-preview-04-17": "Flash.2.5",
    "gpt-4o-mini": "gpt.4o.mini",
}

DEFAULT_TASK_NAMES_MAP: dict[str, str] = {
    x: x
    for x in [
        "human-mouse",
        "ncit-doid",
        "omim-ordo",
        "snomed-fma.body",
        "snomed-ncit.neoplas",
        "snomed-ncit.pharm",
        "fma-nci",
        "fma-snomed",
        "snomed-nci",
    ]
}

ALL_TASKS: list[str] = list(DEFAULT_TASK_NAMES_MAP.keys())



def save_plot(fig: plt.Figure, save_dir: Path, filename: str) -> None:
    save_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(save_dir / f"{filename}.png", bbox_inches="tight")
    plt.close(fig)


def wrap_to_latex(text: str) -> str:
    if not (text.startswith("$") and text.endswith("$")):
        text = f"${text}$"
    return text




def plot_box(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    palette: str = "Set2",
    ax: plt.Axes | None = None,
    rotation: int = 34,
    consistent_prefix_color: bool = False,
) -> None:
    if ax is None:
        _, ax = plt.subplots()

    if consistent_prefix_color:
        data = data.copy()
        unique_prefixes = data[x_col].str.split("-").str[0].unique()
        palette_colors = sns.color_palette(palette, n_colors=len(unique_prefixes))
        color_dict = dict(zip(unique_prefixes, palette_colors))

        box_plot = sns.boxplot(ax=ax, data=data, x=x_col, y=y_col, color="white", fliersize=0, linewidth=1.5)
        for patch, label in zip(box_plot.patches, data[x_col].unique()):
            patch.set_facecolor(color_dict[label.split("-")[0]])
    else:
        sns.boxplot(ax=ax, data=data, x=x_col, y=y_col, palette=palette, hue=x_col, legend=False)

    sns.stripplot(ax=ax, data=data, x=x_col, y=y_col, color="black", alpha=0.5, jitter=True, size=4)
    ax.set_xlabel(wrap_to_latex(x_col))
    ax.set_ylabel(y_col)
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels([wrap_to_latex(t.get_text()) for t in ax.get_xticklabels()], rotation=rotation)


def plot_heatmap(
    data: pd.DataFrame,
    row_col: str,
    col_col: str,
    val_col: str,
    precision: int = 2,
    ax: plt.Axes | None = None,
    fontsize: int = 12,
) -> None:
    if ax is None:
        _, ax = plt.subplots()

    pivot = data.pivot_table(index=row_col, columns=col_col, values=val_col, sort=True)
    pivot = pivot.reindex(index=data[row_col].unique(), columns=data[col_col].unique())
    sns.heatmap(
        ax=ax,
        data=pivot,
        cmap="coolwarm",
        annot=True,
        fmt=f".{precision}f",
        linewidths=0.5,
        annot_kws={"fontsize": fontsize},
    )
    ax.set_xlabel(wrap_to_latex(col_col), fontsize=fontsize)
    ax.set_ylabel(wrap_to_latex(row_col), fontsize=fontsize)
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(
        [wrap_to_latex(t.get_text()) for t in ax.get_xticklabels()], rotation=34, fontdict={"fontsize": fontsize}
    )
    ax.set_yticklabels([wrap_to_latex(t.get_text()) for t in ax.get_yticklabels()], fontdict={"fontsize": fontsize})


def plot_combined_heatmap(
    data: pd.DataFrame,
    row_col: str,
    col1: str,
    col2: str,
    val_col: str,
    precision: int = 2,
    ax: plt.Axes | None = None,
) -> None:
    if ax is None:
        _, ax = plt.subplots()

    p1 = data.pivot_table(index=row_col, columns=col1, values=val_col)
    p2 = data.pivot_table(index=row_col, columns=col2, values=val_col)
    combined = pd.concat([p1, p2], axis=1)
    sns.heatmap(ax=ax, data=combined, cmap="coolwarm", annot=True, fmt=f".{precision}f", linewidths=0.5)
    ax.set_xlabel(f"{col1} and {col2}")
    ax.set_ylabel(wrap_to_latex(row_col))
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels([wrap_to_latex(t.get_text()) for t in ax.get_xticklabels()], rotation=34)
    ax.set_yticklabels([wrap_to_latex(t.get_text()) for t in ax.get_yticklabels()])


def plot_histogram(data: pd.DataFrame, metric: str, ax: plt.Axes | None = None) -> None:
    if ax is None:
        _, ax = plt.subplots()
    sns.histplot(ax=ax, data=data[metric], bins=20, kde=True, color="purple")
    ax.set_xlabel(metric)
    ax.set_ylabel("Frequency")




def plot_detailed_analysis(
    metrics_df: pd.DataFrame,
    metric: str,
    run_col_name: str,
    experiment_col: str,
    left_col: str,
    right_col: str,
    left_col_name: str,
    right_col_name: str,
    run_separator: str = "__",
    precision: int = 2,
    subfolder_name: str | None = None,
    filename_suffix: str = "",
    save_plots: bool = False,
    figsize: tuple[int, int] = (13, 8),
    save_dir_base: Path | None = None,
) -> None:
    metrics_df[run_col_name] = metrics_df[left_col].str.cat(metrics_df[right_col], sep=run_separator)
    metrics_df[left_col_name] = metrics_df[run_col_name].str.split(run_separator).str[0]
    metrics_df[right_col_name] = metrics_df[run_col_name].str.split(run_separator).str[1]

    if subfolder_name is None:
        subfolder_name = "plots"
    if save_dir_base is None:
        save_dir_base = METRICS_DIR
    date_str = datetime.today().strftime("%Y-%m-%d")
    save_dir = save_dir_base / date_str / subfolder_name

    plot_defs = [
        (
            f"boxplot-by-{run_col_name.lower()}",
            lambda ax: plot_box(
                metrics_df, run_col_name, metric, palette="Set2",
                ax=ax, rotation=90, consistent_prefix_color=True,
            ),
        ),
        (
            f"boxplot-by-{experiment_col.lower()}",
            lambda ax: plot_box(metrics_df, experiment_col, metric, palette="Set3", ax=ax),
        ),
        (
            f"{metric}--heatmap-{experiment_col.lower()}",
            lambda ax: plot_heatmap(metrics_df, run_col_name, experiment_col, metric, precision, ax=ax),
        ),
        ("histogram-metric-distribution", lambda ax: plot_histogram(metrics_df, metric, ax=ax)),
        (
            f"{metric}--heatmap-{left_col_name.lower()}-vs-{right_col_name.lower()}",
            lambda ax: plot_heatmap(metrics_df, left_col_name, right_col_name, metric, precision, ax=ax),
        ),
        (
            f"{metric}--heatmap-{run_col_name.lower()}-by-{left_col_name.lower()}-and-{right_col_name.lower()}",
            lambda ax: plot_combined_heatmap(
                metrics_df, run_col_name, left_col_name, right_col_name,
                metric, precision, ax=ax,
            ),
        ),
        (
            f"boxplot-by-{left_col_name.lower()}",
            lambda ax: plot_box(metrics_df, left_col_name, metric, palette="viridis", ax=ax, rotation=0),
        ),
        (
            f"boxplot-by-{right_col_name.lower()}",
            lambda ax: plot_box(metrics_df, right_col_name, metric, palette="coolwarm", ax=ax, rotation=0),
        ),
    ]

    if save_plots:
        for idx, (name, plot_fn) in enumerate(plot_defs):
            fig, ax = plt.subplots(figsize=figsize)
            plot_fn(ax)
            ax.set_title(name.replace("-", " ").title())
            plt.tight_layout()
            save_plot(fig, save_dir, f"{idx}_{name}{filename_suffix}")
        return

    fig, axes = plt.subplots(4, 2, figsize=(28, 34))
    fig.suptitle(f"{metric} Metric Analysis Across Models, Experiments, and Experiment Splits", fontsize=16)
    axes = axes.flatten()
    for ax, (_, plot_fn) in zip(axes, plot_defs):
        plot_fn(ax)
    plt.tight_layout(rect=[0, 0, 1, 0.96])




def preprocess_metrics_df(
    metrics_df: pd.DataFrame,
    prompt_names_map: dict[str, str] | None = None,
    model_names_map: dict[str, str] | None = None,
    task_names_map: dict[str, str] | None = None,
) -> pd.DataFrame:
    if prompt_names_map is None:
        prompt_names_map = DEFAULT_PROMPT_NAMES_MAP
    if model_names_map is None:
        model_names_map = DEFAULT_MODEL_NAMES_MAP
    if task_names_map is None:
        task_names_map = DEFAULT_TASK_NAMES_MAP

    metrics_df["Youden's index"] = metrics_df["Specificity"] + metrics_df["Sensitivity"] - 1
    metrics_df = metrics_df.rename(columns={"SubSet": "Matching Task"})

    if "Prompt" not in metrics_df.columns:
        metrics_df["Prompt"] = None

    if "Experiment" in metrics_df.columns:
        metrics_df.loc[metrics_df["Prompt"].isna(), "Prompt"] = metrics_df.loc[
            metrics_df["Prompt"].isna(), "Experiment"
        ]

    for col, mapping in [
        ("Matching Task", task_names_map),
        ("Prompt", prompt_names_map),
        ("Model", model_names_map),
    ]:
        metrics_df[col] = metrics_df[col].map(mapping)
        metrics_df[col] = pd.Categorical(metrics_df[col], categories=list(mapping.values()), ordered=True)

    metrics_df = metrics_df.dropna()
    metrics_df["ExperimentType"] = "old-run"
    metrics_df["ExpName"] = "0"
    metrics_df["SubSet"] = metrics_df["Matching Task"]
    return metrics_df.sort_values(["Model", "Matching Task", "Prompt"])


def get_experiments_metrics(
    task_names: list[str],
    models: list[str],
    experiments_subtypes: dict[str, list[str]],
    log_warnings: bool = True,
    suffix: str = "_reduced",
    outputs_dir: Path | None = None,
) -> pd.DataFrame:
    dfs = []
    if outputs_dir is None:
        outputs_dir = OUTPUTS_DIR

    for set_name in task_names:
        dataset = SUBSET_TO_DATASET_MAP[set_name]
        for model in models:
            for experiment_type in experiments_subtypes:
                for experiment in experiments_subtypes[experiment_type]:
                    run_subdir = f"{dataset}/{set_name}/{model}/{experiment_type}/{experiment}"
                    path = outputs_dir / run_subdir / f"results{suffix}.csv"
                    if not path.exists():
                        if log_warnings:
                            print(f"Skipping missing {path}")
                        continue

                    if path.stat().st_size == 0:
                        if log_warnings:
                            print(f"Skipping empty {path}")
                        continue

                    try:
                        exp_metrics_df = pd.read_csv(path)
                    except (pd.errors.ParserError, pd.errors.EmptyDataError) as e:
                        if log_warnings:
                            print(f"Error reading {path}: {e}")
                        continue

                    for col, value in zip(
                        ["Dataset", "SubSet", "Model", "ExperimentType", "ExpName"],
                        [dataset, set_name, model, experiment_type, experiment],
                    ):
                        if col not in exp_metrics_df.columns:
                            exp_metrics_df[col] = value

                    exp_metrics_df["Run"] = run_subdir
                    dfs.append(exp_metrics_df)

    return pd.concat(dfs, ignore_index=True)


def load_runs_metrics(suffix: str = "", runs_dir: Path | None = None) -> pd.DataFrame:
    if runs_dir is None:
        runs_dir = RUN_DIR
    return pd.read_csv(runs_dir / f"all_runs_metrics{suffix}.csv")




def discover_model_experiments(
    base_dir: Path,
) -> dict[str, dict[str, list[str]]]:
    model_to_experiments: dict[str, dict[str, list[str]]] = defaultdict(dict)
    if not base_dir.exists():
        return dict(model_to_experiments)

    for model_dir in base_dir.iterdir():
        if not model_dir.is_dir():
            continue
        for exp_type_dir in model_dir.iterdir():
            if not exp_type_dir.is_dir():
                continue
            experiment_names = [d.name for d in exp_type_dir.iterdir() if d.is_dir()]
            model_to_experiments[model_dir.name][exp_type_dir.name] = experiment_names

    return dict(model_to_experiments)


def get_models_by_experiment_type(
    model_to_experiments: dict[str, dict[str, list[str]]],
    experiment_type: str,
) -> list[str]:
    return [
        model
        for model, experiments in model_to_experiments.items()
        if experiment_type in experiments
    ]


def discover_all_experiments(
    outputs_dir: Path | None = None,
    datasets_map: dict[str, list[str]] | None = None,
    suffix: str = "_reduced",
) -> list[dict]:
    if outputs_dir is None:
        outputs_dir = OUTPUTS_DIR
    if datasets_map is None:
        datasets_map = DATASET_SUBSETS_MAP

    experiments = []
    for dataset, subsets in datasets_map.items():
        for subset in subsets:
            subset_dir = outputs_dir / dataset / subset
            if not subset_dir.exists():
                continue
            for model_dir in sorted(subset_dir.iterdir()):
                if not model_dir.is_dir() or model_dir.name.startswith("."):
                    continue
                for exp_type_dir in sorted(model_dir.iterdir()):
                    if not exp_type_dir.is_dir():
                        continue
                    for exp_name_dir in sorted(exp_type_dir.iterdir()):
                        if not exp_name_dir.is_dir():
                            continue
                        prompts = []
                        total_errors = 0
                        total_samples = 0
                        error_type_counts: dict[str, int] = {}
                        error_category_counts: dict[str, int] = {}
                        for csv_file in sorted(exp_name_dir.glob(f"*_results{suffix}.csv")):
                            if csv_file.name == f"results{suffix}.csv":
                                continue
                            stem = csv_file.stem.replace(f"_results{suffix}", "")
                            model_prefix = f"{model_dir.name}_"
                            prompt = stem.split(model_prefix, 1)[-1] if model_prefix in stem else stem
                            prompts.append(prompt)
                            try:
                                csv_df = pd.read_csv(csv_file)
                                if "Prediction" in csv_df.columns:
                                    n = len(csv_df)
                                    errs = (csv_df["Prediction"].astype(str).str.lower() == "error").sum()
                                    total_samples += n
                                    total_errors += errs
                                    # Aggregate error types if column exists
                                    if "error_type" in csv_df.columns:
                                        err_rows = csv_df[csv_df["Prediction"].astype(str).str.lower() == "error"]
                                        for et_val in err_rows["error_type"].dropna().astype(str):
                                            if et_val:
                                                error_type_counts[et_val] = error_type_counts.get(et_val, 0) + 1
                                    if "error_category" in csv_df.columns:
                                        err_rows = csv_df[csv_df["Prediction"].astype(str).str.lower() == "error"]
                                        for ec_val in err_rows["error_category"].dropna().astype(str):
                                            if ec_val:
                                                error_category_counts[ec_val] = error_category_counts.get(ec_val, 0) + 1
                            except (pd.errors.ParserError, pd.errors.EmptyDataError, OSError):
                                pass

                        if not prompts:
                            continue

                        entry = {
                            "dataset": dataset,
                            "subset": subset,
                            "model": model_dir.name,
                            "experiment_type": exp_type_dir.name,
                            "experiment_name": exp_name_dir.name,
                            "prompts": prompts,
                            "num_prompts": len(prompts),
                            "num_samples": int(total_samples),
                            "num_errors": int(total_errors),
                            "error_rate": round(total_errors / total_samples, 4) if total_samples > 0 else 0.0,
                            "error_type_counts": error_type_counts,
                            "error_category_counts": error_category_counts,
                        }
                        experiments.append(entry)

    return experiments


def save_experiments_json(
    output_path: Path | str = "model_to_experiments.json",
    outputs_dir: Path | None = None,
    datasets_map: dict[str, list[str]] | None = None,
    suffix: str = "_reduced",
) -> list[dict]:
    experiments = discover_all_experiments(outputs_dir, datasets_map, suffix)

    model_index: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for exp in experiments:
        key = f"{exp['experiment_type']}/{exp['experiment_name']}"
        if key not in model_index[exp["model"]].get(exp["experiment_type"], []):
            model_index[exp["model"]][exp["experiment_type"]].append(exp["experiment_name"])

    output_path = Path(output_path)
    output_path.write_text(json.dumps(
        {m: dict(v) for m, v in sorted(model_index.items())},
        indent=4,
    ))

    full_path = output_path.with_stem(output_path.stem + "_full")
    full_path.write_text(json.dumps(experiments, indent=2))

    print(f"Saved {len(experiments)} experiments to {full_path}")
    print(f"Saved model index ({len(model_index)} models) to {output_path}")
    return experiments


def plot_nfew_shots_analysis(
    sub_results: pd.DataFrame,
    save_dir: Path | None = None,
) -> None:
    sub_results = sub_results.copy()
    sub_results["version"] = sub_results["ExpName"].str.split("/").str[0]
    sub_results["n_few_shots"] = sub_results["ExpName"].str.split("/").str[1].astype(int)

    for subset in sub_results["SubSet"].unique():
        prompts = sub_results["Prompt"].unique()
        n_prompts = len(prompts)
        ncols = 2
        nrows = int(np.ceil(n_prompts / ncols))

        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6 * ncols, 5 * nrows), squeeze=False)
        fig.suptitle(f"Subset: {subset}", fontsize=16)

        for i, prompt in enumerate(prompts):
            ax = axes[i // ncols, i % ncols]
            subset_df = sub_results[(sub_results["SubSet"] == subset) & (sub_results["Prompt"] == prompt)]
            if subset_df.empty:
                ax.set_visible(False)
                continue
            for version in subset_df["version"].unique():
                version_df = subset_df[subset_df["version"] == version]
                ax.plot(version_df["n_few_shots"], version_df["Youden's index"], marker="o", label=version)
            ax.set_title(f"Prompt: {prompt}")
            ax.set_xlabel("Number of few shots")
            ax.set_ylabel("Youden's index")
            ax.legend(title="Version")
            ax.grid(True)
            ax.set_ylim(0, 1)

        plt.tight_layout(rect=[0, 0, 1, 0.97])
        if save_dir:
            save_path = save_dir / f"few_shots_{subset}.png"
            save_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path)
        plt.show()


def plot_nfew_shots_analysis_mean(
    sub_results: pd.DataFrame,
    model: str | None = None,
    save_dir: Path | None = None,
) -> None:
    if model is not None:
        sub_results = sub_results[sub_results["Model"] == model]

    sub_results = sub_results.copy()
    sub_results["version"] = sub_results["ExpName"].str.split("/").str[0]
    sub_results["n_few_shots"] = sub_results["ExpName"].str.split("/").str[1].astype(int)

    for subset in sub_results["SubSet"].unique():
        prompts = sub_results["Prompt"].unique()
        n_prompts = len(prompts)
        ncols = n_prompts
        nrows = 1

        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6 * ncols, 4 * nrows), squeeze=False)
        if model is not None:
            fig.suptitle(f"Subset: {subset} | Model: {model}", fontsize=16)
        else:
            fig.suptitle(f"Subset: {subset}", fontsize=16)

        for i, prompt in enumerate(prompts):
            ax = axes[i // ncols, i % ncols]
            subset_df = sub_results[(sub_results["SubSet"] == subset) & (sub_results["Prompt"] == prompt)]
            if subset_df.empty:
                ax.set_visible(False)
                continue

            grouped = subset_df.groupby("n_few_shots")["Youden's index"].agg(["mean", "std"]).reset_index()
            ax.errorbar(
                grouped["n_few_shots"],
                grouped["mean"],
                yerr=grouped["std"],
                marker="o",
                capsize=4,
                label="Mean across versions",
            )
            ax.set_title(f"Prompt: {prompt}")
            ax.set_xlabel("Number of few shots")
            ax.set_ylabel("Youden's index (mean +/- std)")
            ax.legend()
            ax.grid(True)
            ax.set_ylim(0, 1)

        plt.tight_layout(rect=[0, 0, 1, 0.97])
        if save_dir and model:
            save_path = save_dir / f"subset_{subset}_{model}.png"
            save_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path)
        plt.show()




def make_radar_chart(
    ax: plt.Axes,
    categories: list[str],
    values_list: list[list[float]],
    labels: list[str],
    colors: list[str],
    linestyles: list[str | tuple],
    r_range: tuple[float, float],
    title: str = "",
    scale: float = 1.01,
) -> None:
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)

    ax.set_rlabel_position(0)
    ax.set_ylim(*r_range)
    yticks = np.linspace(r_range[0], r_range[1], 4)
    ax.set_yticks(yticks)
    ax.set_yticklabels([f"{y:.3f}" for y in yticks], fontsize=9)

    for values, label, color, linestyle in zip(values_list, labels, colors, linestyles):
        values = values + values[:1]
        ax.set_ylim(ax.get_ylim()[0], np.max(values) * scale)
        ax.plot(angles, values, label=label, color=color, linestyle=linestyle, linewidth=1)
        ax.fill(angles, values, color=color, alpha=0.05)
        ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.5)

    ax.set_title(title, size=12, y=1.1)




def select_best_configs(
    df: pd.DataFrame,
    metric: str = "Youden's index",
    config_cols: list[str] | None = None,
) -> pd.DataFrame:
    if config_cols is None:
        config_cols = ["Prompt", "ExperimentType", "ExpName"]

    config_task_counts = df.groupby(["Model", *config_cols])["Task"].nunique().reset_index(name="TaskCount")
    max_task_count = config_task_counts.groupby("Model")["TaskCount"].transform("max")
    best_coverage_configs = config_task_counts[config_task_counts["TaskCount"] == max_task_count]

    model_config_mean = (
        df.merge(best_coverage_configs, on=["Model", *config_cols])
        .groupby(["Model", *config_cols], as_index=False)[metric]
        .mean()
    )

    return model_config_mean.loc[model_config_mean.groupby("Model")[metric].idxmax()].reset_index(drop=True)




def compute_error_rates(
    datasets_map: dict[str, list[str]],
    models: list[str],
    experiment_type: str,
    experiments: list[str],
    outputs_dir: Path | None = None,
    suffix: str = "_reduced",
) -> pd.DataFrame:
    if outputs_dir is None:
        outputs_dir = OUTPUTS_DIR

    records = []
    for dataset, subsets in datasets_map.items():
        for subset in subsets:
            for model in models:
                for exp in experiments:
                    run_dir = outputs_dir / dataset / subset / model / experiment_type / exp
                    if not run_dir.exists():
                        continue
                    for csv_file in run_dir.glob("*.csv"):
                        if csv_file.name == f"results{suffix}.csv":
                            continue
                        prompt_name = csv_file.stem.replace(f"_results{suffix}", "")
                        if f"{model}_" in prompt_name:
                            prompt_name = prompt_name.split(f"{model}_")[-1]
                        try:
                            csv_df = pd.read_csv(csv_file)
                        except (pd.errors.ParserError, pd.errors.EmptyDataError, OSError):
                            continue
                        if "Prediction" not in csv_df.columns:
                            continue
                        total = len(csv_df)
                        if total == 0:
                            continue
                        error_mask = csv_df["Prediction"].astype(str).str.lower() == "error"
                        error_count = int(error_mask.sum())
                        if error_count == 0:
                            continue

                        record = {
                            "Task": f"{dataset}/{subset}",
                            "Model": model,
                            "Prompt": prompt_name,
                            "FewShot": exp,
                            "ErrorRate": error_count / total,
                            "ErrorCount": error_count,
                            "TotalSamples": total,
                        }

                        # Add per-error-type counts
                        if "error_type" in csv_df.columns:
                            err_rows = csv_df[error_mask]
                            for et in ErrorType:
                                cnt = int((err_rows["error_type"].astype(str) == et.value).sum())
                                record[f"errors_{et.value}"] = cnt
                        if "error_category" in csv_df.columns:
                            err_rows = csv_df[error_mask]
                            for ec in ErrorCategory:
                                cnt = int((err_rows["error_category"].astype(str) == ec.value).sum())
                                record[f"errors_cat_{ec.value}"] = cnt

                        records.append(record)

    return pd.DataFrame(records)


def compute_prediction_distributions(
    datasets_map: dict[str, list[str]],
    models: list[str],
    experiment_type: str,
    few_shot_versions: list[str],
    few_shot_numbers: list[int],
    outputs_dir: Path | None = None,
) -> pd.DataFrame:
    if outputs_dir is None:
        outputs_dir = OUTPUTS_DIR

    records = []
    for dataset, subsets in datasets_map.items():
        for subset in subsets:
            for model in models:
                for n, v in product(few_shot_numbers, few_shot_versions):
                    run_dir = outputs_dir / dataset / subset / model / experiment_type / f"{v}/{n}"
                    if not run_dir.exists():
                        continue
                    for csv_file in run_dir.glob("*.csv"):
                        if csv_file.name == "results_reduced.csv":
                            continue
                        prompt_name = csv_file.stem.replace("_results_reduced", "")
                        prompt_name = prompt_name.split(f"{model}_")[-1]
                        try:
                            csv_df = pd.read_csv(csv_file)
                        except (pd.errors.ParserError, pd.errors.EmptyDataError, OSError):
                            continue
                        if "Prediction" not in csv_df.columns:
                            continue
                        counts = csv_df["Prediction"].value_counts().to_dict()
                        total = len(csv_df)
                        for pred_label, count in counts.items():
                            records.append({
                                "Dataset": dataset,
                                "Subset": subset,
                                "Task": f"{dataset}/{subset}",
                                "Model": model,
                                "FewShot": f"{v}/{n}",
                                "Prompt": prompt_name,
                                "Prediction": str(pred_label),
                                "Count": count,
                                "Total": total,
                            })

    results_df = pd.DataFrame(records)
    if not results_df.empty:
        results_df["Proportion"] = results_df["Count"] / results_df["Total"]
    return results_df




def plot_missing_experiments_heatmap(
    datasets_map: dict[str, list[str]],
    models: list[str],
    experiment_type: str,
    experiments: list[str],
    outputs_dir: Path | None = None,
    suffix: str = "_reduced",
) -> None:
    if outputs_dir is None:
        outputs_dir = OUTPUTS_DIR

    records = []
    for dataset, subsets in datasets_map.items():
        for subset in subsets:
            for model in models:
                for exp in experiments:
                    run_subdir = f"{dataset}/{subset}/{model}/{experiment_type}/{exp}"
                    path = outputs_dir / run_subdir / f"results{suffix}.csv"
                    if not path.exists() or path.stat().st_size == 0:
                        continue
                    try:
                        df_local = pd.read_csv(path)
                    except (pd.errors.ParserError, pd.errors.EmptyDataError, OSError):
                        continue
                    if "Prompt" not in df_local.columns:
                        continue
                    for prompt in df_local["Prompt"].unique():
                        records.append({
                            "Dataset": dataset,
                            "Subset": subset,
                            "Model": model,
                            "Experiment": exp,
                            "Prompt": prompt,
                            "Exists": True,
                        })

    records_df = pd.DataFrame(records)
    if records_df.empty:
        print("No data found for missing experiments analysis.")
        return

    records_df["TaskPrompt"] = records_df["Dataset"] + "/" + records_df["Subset"] + " | " + records_df["Prompt"]
    sns.set_theme(style="whitegrid")

    for model in records_df["Model"].unique():
        model_df = records_df[records_df["Model"] == model]
        pivot = model_df.pivot_table(
            index="TaskPrompt", columns="Experiment", values="Exists", aggfunc="first", fill_value=False
        )
        plt.figure(figsize=(16, max(6, 0.3 * len(pivot))))
        sns.heatmap(
            pivot,
            cmap=["#ffcccc", "#c6efce"],
            cbar=False,
            linewidths=0.4,
            linecolor="gray",
        )
        plt.title(f"Missing Experiments for {model}", fontsize=14)
        plt.xlabel("Few-shot version / number")
        plt.ylabel("Task / Prompt")
        plt.xticks(rotation=90, ha="right")
        plt.tight_layout()
        plt.show()


# ──────────────────────────────────────────────────────────────────────────────
# Error Analysis Plotting
# ──────────────────────────────────────────────────────────────────────────────


def plot_error_breakdown(
    error_rates_df: pd.DataFrame,
    group_col: str = "Model",
    title: str = "Error Breakdown",
    figsize: tuple[int, int] = (14, 6),
    save_path: Path | None = None,
) -> None:
    """Plot stacked bar chart showing error type distribution per group (e.g. Model).

    Args:
        error_rates_df: DataFrame from compute_error_rates() with per-error-type counts.
        group_col: Column to group by (e.g. "Model", "Task", "Prompt").
        title: Plot title.
        figsize: Figure size.
        save_path: If provided, save the figure.

    """
    error_type_cols = [f"errors_{et.value}" for et in ErrorType if f"errors_{et.value}" in error_rates_df.columns]
    if not error_type_cols:
        print("No error type columns found in DataFrame. Run inference with updated pipeline first.")
        return

    grouped = error_rates_df.groupby(group_col)[error_type_cols].sum()
    # Remove columns with all zeros
    grouped = grouped.loc[:, (grouped > 0).any()]

    if grouped.empty:
        print("No errors to plot.")
        return

    ax = grouped.plot(kind="bar", stacked=True, figsize=figsize, colormap="Set2")
    ax.set_title(title)
    ax.set_ylabel("Error Count")
    ax.set_xlabel(group_col)
    ax.legend(
        title="Error Type",
        labels=[c.replace("errors_", "") for c in grouped.columns],
        bbox_to_anchor=(1.05, 1),
        loc="upper left",
    )
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.show()


def plot_error_category_pie(
    error_rates_df: pd.DataFrame,
    title: str = "Error Categories Distribution",
    figsize: tuple[int, int] = (8, 8),
    save_path: Path | None = None,
) -> None:
    """Plot pie chart of error categories.

    Args:
        error_rates_df: DataFrame from compute_error_rates().
        title: Plot title.
        figsize: Figure size.
        save_path: If provided, save the figure.

    """
    cat_cols = [f"errors_cat_{ec.value}" for ec in ErrorCategory if f"errors_cat_{ec.value}" in error_rates_df.columns]
    if not cat_cols:
        print("No error category columns found. Run inference with updated pipeline first.")
        return

    totals = error_rates_df[cat_cols].sum()
    totals = totals[totals > 0]
    if totals.empty:
        print("No errors to plot.")
        return

    labels = [c.replace("errors_cat_", "").replace("_", " ").title() for c in totals.index]
    colors = sns.color_palette("Set3", len(labels))

    fig, ax = plt.subplots(figsize=figsize)
    ax.pie(totals.values, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax.set_title(title)
    plt.tight_layout()
    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.show()


def plot_error_rate_heatmap(
    error_rates_df: pd.DataFrame,
    row_col: str = "Model",
    col_col: str = "Task",
    figsize: tuple[int, int] = (14, 8),
    title: str = "Error Rate Heatmap",
    save_path: Path | None = None,
) -> None:
    """Plot heatmap of error rates across two dimensions.

    Args:
        error_rates_df: DataFrame from compute_error_rates().
        row_col: Row grouping column.
        col_col: Column grouping column.
        figsize: Figure size.
        title: Plot title.
        save_path: If provided, save the figure.

    """
    pivot = error_rates_df.pivot_table(index=row_col, columns=col_col, values="ErrorRate", aggfunc="mean")
    if pivot.empty:
        print("No data to plot.")
        return

    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(pivot, cmap="YlOrRd", annot=True, fmt=".3f", linewidths=0.5, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(col_col)
    ax.set_ylabel(row_col)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.show()


def summarize_errors(error_rates_df: pd.DataFrame) -> pd.DataFrame:
    """Return a summary DataFrame with error counts by type and category.

    Args:
        error_rates_df: DataFrame from compute_error_rates().

    Returns:
        Summary DataFrame with totals per error type and category.

    """
    from src.error_taxonomy import ERROR_TYPE_TO_CATEGORY

    summary_rows = []

    # Per error type
    for et in ErrorType:
        col = f"errors_{et.value}"
        if col in error_rates_df.columns:
            total = int(error_rates_df[col].sum())
            if total > 0:
                summary_rows.append({
                    "level": "type",
                    "name": et.value,
                    "category": ERROR_TYPE_TO_CATEGORY[et].value,
                    "count": total,
                })

    # Per error category
    for ec in ErrorCategory:
        col = f"errors_cat_{ec.value}"
        if col in error_rates_df.columns:
            total = int(error_rates_df[col].sum())
            if total > 0:
                summary_rows.append({
                    "level": "category",
                    "name": ec.value,
                    "category": ec.value,
                    "count": total,
                })

    return pd.DataFrame(summary_rows)

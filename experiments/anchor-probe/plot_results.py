"""Plots for the anchor-probe runs. Makes no calls; run after consult (and after `report` for figures 2 and 3).

    python experiments/anchor-probe/plot_results.py                     # reads runs/, writes runs/figures/
    python experiments/anchor-probe/plot_results.py --runs path/to/runs

1. probe_accuracy.png  per task: each model's accuracy on the probe pairs, by pair kind (anchors = TPR, every
                       negative kind = TNR) and probe J, per probe set, over the pairs answered so far (the
                       "answered" column shows coverage, so partial runs can be read). Needs only the consult CSVs.
2. probe_vs_real.png   per task x probe set: probe J against real J on M_ask, one point per model; the probe's
                       pick and the real best are marked. Needs report_table.csv / report_summary.json.
3. regret.png          per task: real J lost by picking with each probe set, next to the references (30 / 50
                       labelled M_ask pairs, Dawid-Skene, random pick). Needs report_summary.json.
Also writes summary.csv (one row per task x probe set) when report outputs exist.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
SET_ORDER = ["v4-100", "v4-200", "v5-g-150", "v5-mix-150"]
KIND_ORDER = ["anchor_masked", "hard_discarded", "granularity_parent", "granularity_child"]
KIND_SHORT = {"anchor_masked": "anchors", "hard_discarded": "hard-disc.", "granularity_parent": "parent",
              "granularity_child": "child"}
BLUE, ORANGE, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#0b0b0b", "#898781", "#e4e3df"

plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "figure.dpi": 150, "savefig.bbox": "tight"})


def short(model: str) -> str:
    return model.split("/")[-1]


def set_key(name: str) -> tuple:
    return (SET_ORDER.index(name) if name in SET_ORDER else len(SET_ORDER), name)


def probe_sets(runs: Path) -> dict[str, list[str]]:
    out = {}
    for task_dir in sorted(p for p in runs.iterdir() if p.is_dir() and p.name != "figures"):
        sets = sorted((d.name for d in task_dir.iterdir() if d.is_dir()), key=set_key)
        if sets:
            out[task_dir.name] = sets
    return out


def probe_accuracy(runs: Path, pairs: Path, task: str, ps: str) -> pd.DataFrame:
    """Per model: accuracy per pair kind and probe J over the answered pairs, plus the answered fraction.
    (`report` instead counts a failed answer as wrong; the two agree once a run is complete.)"""
    labels = pd.read_csv(pairs / task / f"{ps}.tsv", sep="\t")
    rows = []
    for f in sorted((runs / task / ps).glob("*.csv")):
        if f.name.startswith("report"):
            continue
        r = pd.read_csv(f)
        m = labels[["src", "tgt", "label", "kind"]].merge(r, left_on=["src", "tgt"], right_on=["Source", "Target"],
                                                          how="left")
        answered = m.Prediction.astype(str).isin(["True", "False"])
        correct = answered & (m.Prediction.astype(str).eq("True") == m.label.eq(1))
        row = {"model": json.loads(f.with_suffix(".json").read_text())["model_name"] if f.with_suffix(".json").exists()
               else f.stem.replace("__", "/"), "answered": answered.mean()}
        m, correct = m[answered], correct[answered]
        for kind in KIND_ORDER:
            if labels.kind.eq(kind).any():
                k = m.kind.eq(kind)
                row[kind] = correct[k].mean() if k.any() else np.nan
        pos = m.label.eq(1)
        row["J"] = correct[pos].mean() + correct[~pos].mean() - 1 if pos.any() and (~pos).any() else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def fig_probe_accuracy(runs: Path, pairs: Path, sets: dict[str, list[str]], out: Path) -> None:
    width = max(sum(len(KIND_SHORT) + 2 for _ in s) for s in sets.values())
    fig, axes = plt.subplots(len(sets), 1, figsize=(max(8, 0.75 * width), 3.6 * len(sets)), squeeze=False)
    for ax, (task, task_sets) in zip(axes[:, 0], sets.items()):
        cols, blocks, models = [], [], set()
        tables = {ps: probe_accuracy(runs, pairs, task, ps) for ps in task_sets}
        for t in tables.values():
            models |= set(t.model)
        models = sorted(models, key=lambda m: short(m).lower())
        for ps, t in tables.items():
            t = t.set_index("model").reindex(models)
            for c in [k for k in KIND_ORDER if k in t] + ["J", "answered"]:
                cols.append(f"{ps}\n{KIND_SHORT.get(c, c)}")
                blocks.append(t[c].to_numpy(float) if c in t else np.full(len(models), np.nan))
        M = np.column_stack(blocks)
        ax.imshow(np.clip(M, 0, 1), cmap="Blues", vmin=0, vmax=1, aspect="auto")
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                v = M[i, j]
                if not np.isnan(v):
                    ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7,
                            color="white" if v > 0.6 else INK)
        ax.set_xticks(range(len(cols)), cols, fontsize=7)
        ax.set_yticks(range(len(models)), [short(m) for m in models])
        ax.grid(False)
        edge = 0
        for ps, t in tables.items():
            edge += sum(k in t for k in KIND_ORDER) + 2
            ax.axvline(edge - 0.5, color="white", lw=3)
        ax.set_title(f"{task}: probe accuracy by pair kind (anchors = TPR, negatives = TNR) and probe J",
                     loc="left", color=INK)
    fig.tight_layout()
    fig.savefig(out / "probe_accuracy.png")
    plt.close(fig)


def load_reports(runs: Path, sets: dict[str, list[str]]) -> dict[tuple[str, str], tuple[pd.DataFrame, dict]]:
    found = {}
    for task, task_sets in sets.items():
        for ps in task_sets:
            d = runs / task / ps
            if (d / "report_table.csv").exists() and (d / "report_summary.json").exists():
                found[task, ps] = (pd.read_csv(d / "report_table.csv"), json.loads((d / "report_summary.json").read_text()))
    return found


def fig_probe_vs_real(reports, sets, out: Path) -> None:
    tasks = [t for t in sets if any((t, ps) in reports for ps in sets[t])]
    ncol = max(sum((t, ps) in reports for ps in sets[t]) for t in tasks)
    fig, axes = plt.subplots(len(tasks), ncol, figsize=(3.6 * ncol, 3.4 * len(tasks)), squeeze=False)
    for r, task in enumerate(tasks):
        keys = [ps for ps in sets[task] if (task, ps) in reports]
        for c in range(ncol):
            ax = axes[r, c]
            if c >= len(keys):
                ax.set_visible(False)
                continue
            table, summ = reports[task, keys[c]]
            x, y = table.probe_J.to_numpy(), table.real_J.to_numpy()
            pick, best = int(np.argmax(x)), int(np.argmax(y))
            ax.scatter(x, y, s=36, color=BLUE, edgecolor="white", linewidth=1.5, zorder=3)
            ax.scatter(x[pick], y[pick], s=110, facecolor="none", edgecolor=ORANGE, linewidth=2, zorder=4,
                       label="probe's pick")
            ax.scatter(x[best], y[best], s=36, marker="*", color=INK, zorder=5, label="real best")
            for xi, yi, m in zip(x, y, table.model):
                ax.annotate(short(m), (xi, yi), xytext=(4, 3), textcoords="offset points", fontsize=6.5, color=INK)
            ax.set_title(f"{task} / {keys[c]}\nSpearman {summ['spearman']:.2f}, regret {summ['regret']:.3f}",
                         loc="left", fontsize=8.5, color=INK)
            ax.set_xlabel("probe J")
            if c == 0:
                ax.set_ylabel("real J on M_ask")
    handles, names = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, names, loc="upper right", ncol=2, frameon=False, fontsize=8)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(out / "probe_vs_real.png")
    plt.close(fig)


def fig_regret(reports, sets, out: Path) -> None:
    tasks = [t for t in sets if any((t, ps) in reports for ps in sets[t])]
    fig, axes = plt.subplots(1, len(tasks), figsize=(5.2 * len(tasks), 3.4), squeeze=False)
    for ax, task in zip(axes[0], tasks):
        keys = [ps for ps in sets[task] if (task, ps) in reports]
        summ0 = reports[task, keys[0]][1]  # references depend on M_ask only, identical across probe sets
        rows = [(f"probe {ps}", reports[task, ps][1]["regret"], reports[task, ps][1]["boot_mean_regret"], BLUE)
                for ps in keys]
        rows += [("30 labelled M_ask pairs", summ0["labelled_regret_30"], None, MUTED),
                 ("50 labelled M_ask pairs", summ0["labelled_regret_50"], None, MUTED),
                 ("Dawid-Skene (no labels)", summ0["dawid_skene_regret"], None, MUTED),
                 ("random pick", summ0["random_regret"], None, MUTED)]
        ys = np.arange(len(rows))[::-1]
        for yv, (name, v, boot, col) in zip(ys, rows):
            ax.hlines(yv, 0, v, color=col, lw=2)
            ax.scatter(v, yv, s=36, color=col, zorder=3)
            if boot is not None:
                ax.scatter(boot, yv, s=36, facecolor="none", edgecolor=col, linewidth=1.5, zorder=3)
            ax.annotate(f"{v:.3f}", (v, yv), xytext=(6, -3), textcoords="offset points", fontsize=7, color=INK)
        ax.set_yticks(ys, [r[0] for r in rows])
        ax.set_xlim(0, max(r[1] for r in rows) * 1.25 + 1e-3)
        ax.set_xlabel("regret: real J of best model − real J of pick (lower is better)")
        ax.set_title(f"{task} ({summ0['n_models']} models; hollow = bootstrap mean)", loc="left", color=INK)
        ax.grid(axis="y", visible=False)
    fig.tight_layout()
    fig.savefig(out / "regret.png")
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", type=Path, default=HERE / "runs")
    ap.add_argument("--pairs", type=Path, default=HERE / "pairs")
    ap.add_argument("--out", type=Path, default=None, help="default: <runs>/figures")
    a = ap.parse_args()
    if not a.runs.is_dir():
        raise SystemExit(f"no runs folder at {a.runs}; run consult first")
    out = a.out or a.runs / "figures"
    out.mkdir(parents=True, exist_ok=True)
    sets = probe_sets(a.runs)

    fig_probe_accuracy(a.runs, a.pairs, sets, out)
    print(f"wrote {out / 'probe_accuracy.png'}")
    reports = load_reports(a.runs, sets)
    if not reports:
        print("no report outputs yet (run `python -m logmap_llm.anchor_probe report ...`): skipped probe_vs_real, regret")
        return
    fig_probe_vs_real(reports, sets, out)
    fig_regret(reports, sets, out)
    summary = pd.DataFrame([{k: v for k, v in s.items() if k != "boot_spearman_ci"}
                            | {"spearman_ci_lo": s["boot_spearman_ci"][0], "spearman_ci_hi": s["boot_spearman_ci"][1]}
                            for _, s in reports.values()])
    summary.to_csv(out / "summary.csv", index=False)
    print(f"wrote {out / 'probe_vs_real.png'}, {out / 'regret.png'}, {out / 'summary.csv'}")


if __name__ == "__main__":
    main()

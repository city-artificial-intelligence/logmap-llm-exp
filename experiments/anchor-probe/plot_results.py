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
From runs/<task>/budget.csv (`budget` command), at n pairs answered per model for probe subsets, Dawid-Skene and
labelled M_ask pairs:
4. budget.png          mean regret and mean Spearman against n.
5. hit_at_k.png        hit@k = P(real best model in the method's top k) against k, at n = 50, 100, 150.
6. hit_vs_budget.png   hit@1, hit@3, hit@5 against n.
"""
from __future__ import annotations

import argparse
import json
import re
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
SET_COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]  # probe sets, in SET_ORDER (categorical slots 1-4)

plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "figure.dpi": 150, "savefig.bbox": "tight"})


def short(model: str) -> str:
    """deepseek/deepseek-v4-flash -> deepseek-v4-flash, Qwen3-235B-A22B-Instruct-2507 -> Qwen3-235B."""
    return re.sub(r"-A\d+B|-[Ii]nstruct(-\d+)?$|-it$", "", model.split("/")[-1])


def label_column(ax, x, y, names, gap: float = 0.085) -> None:
    """Names in a column right of the axes, spread to `gap` (axes fraction) apart, with leader lines to the points."""
    lo, hi = ax.get_ylim()
    fy = (np.asarray(y) - lo) / (hi - lo)
    order = np.argsort(-fy)
    t = fy[order].clip(None, 0.98)
    for i in range(1, len(t)):
        t[i] = min(t[i], t[i - 1] - gap)
    if t[-1] < 0.02:
        t += 0.02 - t[-1]
    for k, ty in zip(order, t):
        ax.annotate(names[k], (x[k], y[k]), xytext=(1.04, ty), textcoords="axes fraction", va="center", fontsize=7,
                    color=INK, annotation_clip=False,
                    arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.5, shrinkA=0, shrinkB=4))


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
        # the coverage column only says something while a run is partial
        extra = {ps: ["J", "answered"] if (t.answered < 1).any() else ["J"] for ps, t in tables.items()}
        for ps, t in tables.items():
            t = t.set_index("model").reindex(models)
            for c in [k for k in KIND_ORDER if k in t] + extra[ps]:
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
            edge += sum(k in t for k in KIND_ORDER) + len(extra[ps])
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
    # real J is the same for every probe set of a task, so each row shares its y axis
    fig, axes = plt.subplots(len(tasks), ncol, figsize=(4.4 * ncol, 3.4 * len(tasks)), squeeze=False, sharey="row")
    for r, task in enumerate(tasks):
        keys = [ps for ps in sets[task] if (task, ps) in reports]
        for c in range(ncol):
            ax = axes[r, c]
            if c >= len(keys):
                ax.set_visible(False)
                continue
            table, summ = reports[task, keys[c]]
            x, y = table.probe_J.to_numpy(), table.real_J.to_numpy()
            picks, best = np.flatnonzero(np.isclose(x, x.max())), int(np.argmax(y))
            pad = 0.06 * (y.max() - y.min())
            ax.set_ylim(y.min() - pad, y.max() + pad)
            ax.scatter(x, y, s=36, color=BLUE, edgecolor="white", linewidth=1.5, zorder=3)
            ax.scatter(x[picks], y[picks], s=110, facecolor="none", edgecolor=ORANGE, linewidth=2, zorder=4,
                       label="probe's pick (all circled if tied)")
            ax.scatter(x[best], y[best], s=36, marker="*", color=INK, zorder=5, label="real best")
            label_column(ax, x, y, [short(m) for m in table.model])
            tie = " (tie, mean of picks)" if len(picks) > 1 else ""
            ax.set_title(f"{task} / {keys[c]}\nSpearman {summ['spearman']:.2f}, regret {summ['regret']:.3f}{tie}",
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
        rows = [(f"probe {ps}", reports[task, ps][1]["regret"], reports[task, ps][1].get("boot_mean_regret"), BLUE)
                for ps in keys]
        has_boot = any(r[2] is not None for r in rows)
        rows += [("30 labelled M_ask pairs", summ0.get("labelled_regret_30"), None, MUTED),
                 ("50 labelled M_ask pairs", summ0.get("labelled_regret_50"), None, MUTED),
                 ("Dawid-Skene (no labels)", summ0.get("dawid_skene_regret"), None, MUTED),
                 ("random pick", summ0.get("random_regret"), None, MUTED)]
        rows = [r for r in rows if r[1] is not None]  # references need the M_ask predictions; may be absent
        ys = np.arange(len(rows))[::-1]
        for yv, (name, v, boot, col) in zip(ys, rows):
            ax.hlines(yv, 0, v, color=col, lw=2)
            ax.scatter(v, yv, s=36, color=col, zorder=3)
            if boot is not None:
                ax.scatter(boot, yv, s=36, facecolor="none", edgecolor=col, linewidth=1.5, zorder=3)
            text = f"{v:.3f}" if boot is None else f"{v:.3f} (bootstrap {boot:.3f})"
            ax.annotate(text, (max(v, boot or 0), yv), xytext=(7, -3), textcoords="offset points", fontsize=7,
                        color=INK)
        ax.set_yticks(ys, [r[0] for r in rows])
        ax.set_xlim(0, max(r[1] for r in rows) * 1.25 + 1e-3)
        ax.set_xlabel("regret: real J of best model − real J of pick (lower is better)")
        ax.set_title(f"{task} ({summ0['n_models']} models{'; hollow = bootstrap mean' if has_boot else ''})",
                     loc="left", color=INK)
        if not has_boot:
            ax.annotate("bootstrap, labelled-pair and Dawid-Skene references need the M_ask predictions: not computed",
                        (0, -0.32), xycoords="axes fraction", fontsize=7, color=MUTED)
        ax.grid(axis="y", visible=False)
    fig.tight_layout()
    fig.savefig(out / "regret.png")
    plt.close(fig)


def budget_tables(runs: Path, sets: dict[str, list[str]]) -> dict[str, pd.DataFrame]:
    return {t: pd.read_csv(runs / t / "budget.csv") for t in sets if (runs / t / "budget.csv").exists()}


def budget_series(b: pd.DataFrame) -> list[tuple[str, str, str, str]]:
    """(method, legend label, colour, line style) for every method of a budget table, probe sets first."""
    probes = sorted((m for m in b.method.unique() if m.startswith("probe:")), key=lambda m: set_key(m[6:]))
    series = [(m, f"probe {m[6:]}", SET_COLORS[i % len(SET_COLORS)], "-") for i, m in enumerate(probes)]
    return series + [("dawid_skene", "Dawid-Skene, M_ask pairs (no labels)", INK, "-"),
                     ("labelled", "labelled M_ask pairs (reference)", MUTED, "--")]


def n_axis(ax, b: pd.DataFrame) -> int:
    """Ticks at every budget n, the full M_ask marked (max); returns the M_ask size."""
    m_ask = int(b.loc[b.method == "dawid_skene", "source_size"].max())
    ticks = [n for n in sorted(set(b.loc[b.n > 0, "n"])) if n == m_ask or m_ask - n > 0.06 * m_ask]
    ax.set_xticks(ticks, [f"{n}\n(max)" if n == m_ask else str(n) for n in ticks], fontsize=7)
    return m_ask


def shared_legend(fig, axes, top: float) -> None:
    handles = {}
    for ax in axes.flat:  # union of legend entries (not every method exists in every panel)
        for h, l in zip(*ax.get_legend_handles_labels()):
            handles.setdefault(l, h)
    fig.legend(list(handles.values()), list(handles), loc="upper center", ncol=4, frameon=False, fontsize=8)
    fig.tight_layout(rect=(0, 0, 1, top))


def fig_budget(runs: Path, sets: dict[str, list[str]], out: Path) -> bool:
    """Per task: mean regret and mean Spearman against n pairs per model, for probe subsets, Dawid-Skene, labelled."""
    tables = budget_tables(runs, sets)
    if not tables:
        return False
    fig, axes = plt.subplots(2, len(tables), figsize=(6.2 * len(tables), 7), squeeze=False)
    for c, (task, b) in enumerate(tables.items()):
        for r, (col, ylabel) in enumerate([("mean_regret", "mean regret (lower is better)"),
                                           ("mean_spearman", "mean Spearman with the real ranking")]):
            ax = axes[r, c]
            for method, label, color, ls in budget_series(b):
                s = b[b.method == method].sort_values("n")
                ax.plot(s.n, s[col], ls, color=color, lw=2, marker="o", ms=4, label=label)
            if col == "mean_regret":
                rnd = float(b.loc[b.method == "random", "mean_regret"].iloc[0])
                ax.axhline(rnd, color=MUTED, lw=1, ls=":", label="random pick")
                ax.annotate("random pick", (1, rnd), xycoords=("axes fraction", "data"), xytext=(-2, 3),
                            textcoords="offset points", ha="right", fontsize=7, color=MUTED)
                ax.set_ylim(bottom=0)
            else:
                ax.axhline(0, color=MUTED, lw=0.8)
            m_ask = n_axis(ax, b)
            ax.set_ylabel(ylabel)
            if r == 1:
                ax.set_xlabel("pairs answered per model (n)")
        axes[0, c].set_title(f"{task}: {int(b.n_models.iloc[0])} models, M_ask {m_ask} pairs", loc="left", color=INK)
    shared_legend(fig, axes, 0.93)
    fig.savefig(out / "budget.png")
    plt.close(fig)
    return True


def fig_hits(runs: Path, sets: dict[str, list[str]], out: Path, budgets=(50, 100, 150)) -> bool:
    """hit@k = P(real best model in the method's top k) against k, per task (rows) and budget n (columns)."""
    tables = {t: b for t, b in budget_tables(runs, sets).items() if "hit@1" in b}
    if not tables:
        return False
    fig, axes = plt.subplots(len(tables), len(budgets), figsize=(4.2 * len(budgets), 3.6 * len(tables)),
                             squeeze=False, sharey=True)
    for r, (task, b) in enumerate(tables.items()):
        K = int(b.n_models.iloc[0])
        ks = np.arange(1, K + 1)
        for c, n in enumerate(budgets):
            ax = axes[r, c]
            ax.plot(ks, ks / K, ":", color=MUTED, lw=1, label="random ranking")
            for method, label, color, ls in budget_series(b):
                row = b[(b.method == method) & (b.n == n)]
                if len(row):
                    ax.plot(ks, row[[f"hit@{k}" for k in ks]].iloc[0].to_numpy(float), ls, color=color, lw=2,
                            marker="o", ms=4, label=label)
            ax.set_xticks(ks)
            ax.set_ylim(0, 1.04)
            ax.set_title(f"{task}, n = {n} pairs per model", loc="left", fontsize=9, color=INK)
            if c == 0:
                ax.set_ylabel("hit@k: real best in top k")
            if r == len(tables) - 1:
                ax.set_xlabel("k (models shortlisted)")
    shared_legend(fig, axes, 0.92)
    fig.savefig(out / "hit_at_k.png")
    plt.close(fig)
    return True


def fig_hits_vs_budget(runs: Path, sets: dict[str, list[str]], out: Path, ks=(1, 3, 5)) -> bool:
    """P(real best model in the method's top k) against n pairs per model, per task (rows) and k (columns)."""
    tables = {t: b for t, b in budget_tables(runs, sets).items() if "hit@1" in b}
    if not tables:
        return False
    fig, axes = plt.subplots(len(tables), len(ks), figsize=(4.4 * len(ks), 3.6 * len(tables)),
                             squeeze=False, sharey=True)
    for r, (task, b) in enumerate(tables.items()):
        K = int(b.n_models.iloc[0])
        for c, k in enumerate(ks):
            ax = axes[r, c]
            if k > K:
                ax.set_visible(False)
                continue
            for method, label, color, ls in budget_series(b):
                s = b[b.method == method].sort_values("n")
                ax.plot(s.n, s[f"hit@{k}"], ls, color=color, lw=2, marker="o", ms=4, label=label)
            ax.axhline(k / K, color=MUTED, lw=1, ls=":", label="random ranking")
            n_axis(ax, b)
            ax.set_ylim(0, 1.04)
            ax.set_title(f"{task}: real best in top {k} of {K}", loc="left", fontsize=9, color=INK)
            if c == 0:
                ax.set_ylabel("P(real best in top k)")
            if r == len(tables) - 1:
                ax.set_xlabel("pairs answered per model (n)")
    shared_legend(fig, axes, 0.92)
    fig.savefig(out / "hit_vs_budget.png")
    plt.close(fig)
    return True


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
    if fig_budget(a.runs, sets, out):
        print(f"wrote {out / 'budget.png'}")
    if fig_hits(a.runs, sets, out):
        print(f"wrote {out / 'hit_at_k.png'}")
    if fig_hits_vs_budget(a.runs, sets, out):
        print(f"wrote {out / 'hit_vs_budget.png'}")
    reports = load_reports(a.runs, sets)
    if not reports:
        print("no report outputs yet (run `python -m logmap_llm.anchor_probe report ...`): skipped probe_vs_real, regret")
        return
    fig_probe_vs_real(reports, sets, out)
    fig_regret(reports, sets, out)
    summary = pd.DataFrame([{k: v for k, v in s.items() if k != "boot_spearman_ci"}
                            | dict(zip(["spearman_ci_lo", "spearman_ci_hi"], s.get("boot_spearman_ci") or [None, None]))
                            for _, s in reports.values()])
    summary.to_csv(out / "summary.csv", index=False)
    print(f"wrote {out / 'probe_vs_real.png'}, {out / 'regret.png'}, {out / 'summary.csv'}")


if __name__ == "__main__":
    main()

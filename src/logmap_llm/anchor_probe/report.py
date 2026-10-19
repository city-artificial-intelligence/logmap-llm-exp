"""Does the probe rank the oracles the way M_ask does?

Real side : each job's own M_ask predictions file, scored against the reference alignment. Failed consultations
            count as wrong. The J computed here is checked against the job's evaluation_results.json. Where the
            prediction files are not available, runs/<task>/m_ask_verdicts.csv (exported by report / budget) is used.
Probe side: the probe set's free labels; a failed or missing answer counts as wrong.

Reported per task and probe set:
  * per model: real J / TPR / TNR on M_ask, probe J / TPR / TNR, probe TNR per negative kind;
  * rank agreement: Spearman, Kendall, top-1, and REGRET = real J of the true best - real J of the probe's pick;
  * paired, class-stratified bootstrap over both pair sets: mean regret, P(regret <= 0.02), Spearman 95% CI;
  * references: random pick, n labelled M_ask pairs (n = 30, 50), Dawid-Skene on the jobs' M_ask verdicts,
    and the noise ceiling (how often the real top model stays top when M_ask is resampled).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from .inputs import Task, m_ask_predictions, m_ask_verdicts_path, reference

N_BOOT = 2000


def spearmanr(a, b) -> tuple[float, None]:
    """Spearman rho (average ranks for ties); NaN when either side is constant. Same value as scipy's."""
    ra, rb = pd.Series(a).rank().to_numpy(), pd.Series(b).rank().to_numpy()
    if ra.std() == 0 or rb.std() == 0:
        return float("nan"), None
    return float(np.corrcoef(ra, rb)[0, 1]), None


def kendalltau(a, b) -> tuple[float, None]:
    """Kendall tau-b (tie-corrected), O(n^2): fine for a handful of models."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    i, j = np.triu_indices(len(a), 1)
    da, db = np.sign(a[i] - a[j]), np.sign(b[i] - b[j])
    denom = np.sqrt((da != 0).sum() * (db != 0).sum())
    return (float((da * db).sum() / denom) if denom else float("nan")), None


def youden(gt: np.ndarray, pred: np.ndarray) -> float:
    return float(pred[gt].mean() + (~pred[~gt]).mean() - 1.0)


def jmat(gt: np.ndarray, P: np.ndarray) -> np.ndarray:
    return P[gt].mean(0) + (~P[~gt]).mean(0) - 1.0


def dawid_skene(P: np.ndarray, iters: int = 150, tol: float = 1e-7) -> np.ndarray:
    """Two-parameter EM (Dawid & Skene 1979); returns estimated sensitivity + specificity - 1 per column."""
    q = np.clip(P.mean(1).astype(float), 1e-3, 1 - 1e-3)
    se = sp = None
    for _ in range(iters):
        pi = np.clip(q.mean(), 1e-6, 1 - 1e-6)
        se = np.clip((q[:, None] * P).sum(0) / q.sum(), 1e-3, 1 - 1e-3)
        sp = np.clip(((1 - q)[:, None] * ~P).sum(0) / (1 - q).sum(), 1e-3, 1 - 1e-3)
        l1 = np.log(pi) + (P * np.log(se) + ~P * np.log(1 - se)).sum(1)
        l0 = np.log(1 - pi) + (~P * np.log(sp) + P * np.log(1 - sp)).sum(1)
        m = np.maximum(l1, l0)
        new = np.exp(l1 - m) / (np.exp(l1 - m) + np.exp(l0 - m))
        done = np.max(np.abs(new - q)) < tol
        q = np.clip(new, 1e-6, 1 - 1e-6)
        if done:
            break
    return se + sp - 1.0


def regret(score: np.ndarray, real: np.ndarray) -> float:
    """Real J lost by picking argmax(score); ties are averaged."""
    tied = np.flatnonzero(score == score.max())
    return float(real.max() - real[tied].mean())


def _strat(gt: np.ndarray, rng) -> np.ndarray:
    pos, neg = np.flatnonzero(gt), np.flatnonzero(~gt)
    return np.concatenate([rng.choice(pos, len(pos)), rng.choice(neg, len(neg))])


def real_side_from_export(task: Task, jobs) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """The real side read from runs/<task>/m_ask_verdicts.csv (written by report / budget where the prediction
    files are)."""
    f = m_ask_verdicts_path(task)
    if not f.exists():
        raise FileNotFoundError(f"[{task.name}] M_ask prediction files not found and no {f}; run report or budget "
                                "once where the prediction files are, and commit runs/")
    df = pd.read_csv(f, dtype=str, keep_default_na=False)
    missing = [j.label for j in jobs if j.label not in df]
    if missing:
        raise KeyError(f"[{task.name}] {f.name} has no verdicts for {missing}")
    gt = df.label.astype(int).to_numpy().astype(bool)
    P = np.column_stack([np.where(df[j.label].isin(["True", "False"]), df[j.label].eq("True"), ~gt) for j in jobs])
    print(f"  [{task.name}] real side from {f.name} ({len(df)} pairs)")
    return gt, P, [f"{s}|{t}" for s, t in zip(df.src, df.tgt)]


def real_side(task: Task, jobs) -> tuple[np.ndarray, np.ndarray, list[str]]:
    if not all(Path(j.paths.predictions_csv()).exists() for j in jobs):
        return real_side_from_export(task, jobs)
    ref = reference(task)
    frames = [m_ask_predictions(j) for j in jobs]
    keys = set.intersection(*[set(zip(f.src, f.tgt)) for f in frames])
    sizes = {len(f) for f in frames}
    if len(sizes) > 1 or len(keys) != max(sizes):
        print(f"  WARNING [{task.name}] M_ask differs across jobs (sizes {sorted(sizes)}); using the {len(keys)} common pairs")
    order = sorted(keys)
    gt = np.array([frozenset(k) in ref for k in order])
    P = np.zeros((len(order), len(jobs)), dtype=bool)
    for c, (job, f) in enumerate(zip(jobs, frames)):
        d = {(s, t): p for s, t, p in zip(f.src, f.tgt, f.pred)}
        col = np.array([d[k] for k in order], dtype=object)
        ok = np.array([v is True or v is False for v in col])
        P[:, c] = np.where(ok, col == True, ~gt)  # noqa: E712 - failed consultation counts as wrong
        ev = Path(job.paths.output_dir) / "evaluation_results.json"
        if ev.exists() and ok.all():
            reported = json.loads(ev.read_text()).get("oracle", {}).get("youdens_j")
            if reported is not None and abs(reported - youden(gt, P[:, c])) > 1e-6:
                print(f"  WARNING {job.label}: J recomputed {youden(gt, P[:, c]):.4f} != reported {reported:.4f}")
    return gt, P, [f"{s}|{t}" for s, t in order]


def probe_side(task: Task, probe_set: Path, jobs) -> tuple[pd.DataFrame, np.ndarray, list[int]]:
    labels = pd.read_csv(probe_set, sep="\t")
    gt = labels.label.to_numpy().astype(bool)
    P = np.zeros((len(labels), len(jobs)), dtype=bool)
    have = []
    for c, job in enumerate(jobs):
        f = task.out_dir(probe_set) / f"{job.slug}.csv"
        if not f.exists():
            print(f"  [{task.name}/{probe_set.stem}] no probe results for {job.label} -- excluded")
            continue
        r = pd.read_csv(f)
        m = labels[["src", "tgt"]].merge(r, left_on=["src", "tgt"], right_on=["Source", "Target"], how="left")
        ok = m.Prediction.astype(str).isin(["True", "False"]).to_numpy()
        P[:, c] = np.where(ok, m.Prediction.astype(str).eq("True").to_numpy(), ~gt)
        have.append(c)
    return labels, P, have


def analyse(task: Task, probe_set: Path, seed: int = 0) -> tuple[pd.DataFrame, dict] | None:
    rng = np.random.default_rng(seed)
    labels, Pp, have = probe_side(task, probe_set, task.jobs)
    if len(have) < 2:
        print(f"[{task.name}/{probe_set.stem}] need probe results for >= 2 jobs, have {len(have)} -- skipped")
        return None
    jobs = [task.jobs[i] for i in have]
    Pp = Pp[:, have]
    gp = labels.label.to_numpy().astype(bool)
    gm, Pm, _ = real_side(task, jobs)
    real, probe = jmat(gm, Pm), jmat(gp, Pp)
    table = pd.DataFrame({
        "model": [j.label for j in jobs], "real_J": real, "real_TPR": Pm[gm].mean(0), "real_TNR": (~Pm[~gm]).mean(0),
        "probe_J": probe, "probe_TPR": Pp[gp].mean(0), "probe_TNR": (~Pp[~gp]).mean(0)})
    for kind in sorted(labels[labels.label == 0].kind.unique()):
        m = (labels.kind == kind).to_numpy() & ~gp
        table[f"probe_TNR[{kind}]"] = (~Pp[m]).mean(0)
    table["real_rank"] = table.real_J.rank(ascending=False, method="min").astype(int)
    table["probe_rank"] = table.probe_J.rank(ascending=False, method="min").astype(int)

    boot = {"regret": [], "spearman": [], "ds_regret": [], "top_stays": []}
    true_top = int(np.argmax(real))
    for _ in range(N_BOOT):
        ip, im = _strat(gp, rng), _strat(gm, rng)
        rb, pb = jmat(gm[im], Pm[im]), jmat(gp[ip], Pp[ip])
        boot["regret"].append(regret(pb, rb))
        boot["spearman"].append(spearmanr(pb, rb)[0])
        boot["top_stays"].append(int(np.argmax(rb)) == true_top)
    labelled = {}
    for n in (30, 50):
        rs = []
        for _ in range(N_BOOT):
            ix = rng.choice(len(gm), n, replace=False)
            if gm[ix].all() or (~gm[ix]).all():
                continue
            rs.append(regret(jmat(gm[ix], Pm[ix]), real))
        labelled[n] = float(np.mean(rs))
    ds = dawid_skene(Pm)
    summ = {
        "task": task.name, "probe_set": probe_set.stem, "n_models": len(jobs), "n_probe": int(len(gp)),
        "n_probe_pos": int(gp.sum()), "n_m_ask": int(len(gm)), "m_ask_prevalence": float(gm.mean()),
        "spearman": float(spearmanr(probe, real)[0]), "kendall": float(kendalltau(probe, real)[0]),
        "top1": bool(np.argmax(probe) == true_top), "regret": regret(probe, real),
        "boot_mean_regret": float(np.mean(boot["regret"])),
        "boot_p_regret_le_0.02": float(np.mean(np.array(boot["regret"]) <= 0.02)),
        "boot_spearman_ci": [float(np.nanpercentile(boot["spearman"], 2.5)), float(np.nanpercentile(boot["spearman"], 97.5))],
        "noise_ceiling_top_stays": float(np.mean(boot["top_stays"])),
        "random_regret": float(np.mean(real.max() - real)),
        "labelled_regret_30": labelled[30], "labelled_regret_50": labelled[50],
        "dawid_skene_spearman": float(spearmanr(ds, real)[0]), "dawid_skene_regret": regret(ds, real),
    }
    return table, summ


def _md(df: pd.DataFrame) -> str:
    """Markdown table without the optional `tabulate` dependency."""
    fmt = lambda v: f"{v:.3f}" if isinstance(v, (float, np.floating)) else str(v)  # noqa: E731
    rows = ["| " + " | ".join(df.columns) + " |", "|" + "---|" * len(df.columns)]
    rows += ["| " + " | ".join(fmt(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join(rows)


def write(task: Task, probe_set: Path, table: pd.DataFrame, summ: dict) -> Path:
    out = task.out_dir(probe_set)
    out.mkdir(parents=True, exist_ok=True)
    table.to_csv(out / "report_table.csv", index=False)
    (out / "report_summary.json").write_text(json.dumps(summ, indent=2))
    t = table.sort_values("real_J", ascending=False)
    lines = [f"# {task.name} / {probe_set.stem}", "",
             f"{summ['n_models']} models; probe {summ['n_probe']} pairs ({summ['n_probe_pos']} positive); "
             f"M_ask {summ['n_m_ask']} pairs (prevalence {summ['m_ask_prevalence']:.2f}).", "",
             _md(t), "",
             "| | value |", "|---|---|",
             f"| Spearman (probe J vs real J) | {summ['spearman']:.2f} (bootstrap 95% CI {summ['boot_spearman_ci'][0]:.2f} to {summ['boot_spearman_ci'][1]:.2f}) |",
             f"| regret of the probe's pick | {summ['regret']:.3f} (bootstrap mean {summ['boot_mean_regret']:.3f}, P(<=0.02) {summ['boot_p_regret_le_0.02']:.2f}) |",
             f"| random pick, mean regret | {summ['random_regret']:.3f} |",
             f"| 30 / 50 labelled M_ask pairs, mean regret | {summ['labelled_regret_30']:.3f} / {summ['labelled_regret_50']:.3f} |",
             f"| Dawid-Skene on M_ask (no labels): Spearman / regret | {summ['dawid_skene_spearman']:.2f} / {summ['dawid_skene_regret']:.3f} |",
             f"| noise ceiling: real top model stays top under M_ask bootstrap | {summ['noise_ceiling_top_stays']:.2f} |", ""]
    (out / "report.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return out

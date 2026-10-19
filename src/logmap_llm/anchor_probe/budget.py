"""How good is each way of picking the oracle for a given budget n (pairs answered by every model)?

Every method is scored against the same real ranking, each model's Youden's J on the full M_ask:
  probe:<set>   n pairs of that probe set, drawn stratified by kind (positives and each negative type keep their
                share); models ranked by probe J on the free LogMap labels
  dawid_skene   n M_ask pairs drawn at random, no labels; models ranked by Dawid-Skene's estimated J
  labelled      n M_ask pairs drawn at random with their reference labels; models ranked by J on those pairs
                (needs n pairs labelled by hand: the reference to beat)
  random        a model picked at random (no calls)
n runs 50, 100, 150, ... up to each source's full size, which is always included (all pairs: one draw); smaller n
are averaged over `draws` subsamples without replacement. Per method and n: mean regret, mean Spearman, and
hit@k = P(the real best model is in the method's top k), k = 1..models (ties at the cut-off split at random, so a
random ranking scores k / models). Writes runs/<task>/budget.csv; plot_results.py draws budget.png and hit_at_k.png.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .inputs import Task
from .report import dawid_skene, jmat, probe_side, real_side, regret, spearmanr


def sizes(total: int, step: int) -> list[int]:
    return [n for n in range(step, total, step)] + [total]


def stratified(strata: list[np.ndarray], n: int, rng) -> np.ndarray:
    """n indices without replacement, shared out over the strata in proportion to their size (largest remainder)."""
    size = np.array([len(s) for s in strata])
    quota = n * size / size.sum()
    k = np.floor(quota).astype(int)
    k[np.argsort(k - quota, kind="stable")[: n - k.sum()]] += 1
    return np.concatenate([rng.choice(s, m, replace=False) for s, m in zip(strata, k) if m])


def hits(est: np.ndarray, best: int) -> np.ndarray:
    """hit@k for k = 1..len(est): is model `best` in the top k of `est`? Ties at the cut-off count fractionally
    (the chance a random tie-break keeps it in)."""
    above, tied = np.sum(est > est[best]), np.sum(est == est[best])
    return np.clip((np.arange(1, len(est) + 1) - above) / tied, 0.0, 1.0)


def curve(method: str, n: int, total: int, estimate, real: np.ndarray, draws: int) -> dict:
    """Score `estimate()` (one J estimate per model, from one random draw of n pairs) against the real J."""
    rs, ss, hs = [], [], []
    best = int(np.argmax(real))
    for _ in range(1 if n == total else draws):
        est = estimate()
        if est is None:  # labelled draw with a single class: J undefined
            continue
        rs.append(regret(est, real))
        ss.append(spearmanr(est, real)[0])
        hs.append(hits(est, best))
    rs, ss = np.array(rs), np.array(ss)
    return {"method": method, "n": n, "source_size": total, "draws": len(rs), "mean_regret": rs.mean(),
            "regret_q90": np.quantile(rs, 0.9), "p_best": float(np.mean(rs < 1e-12)),
            "mean_spearman": np.nanmean(ss), "spearman_q05": np.nanquantile(ss, 0.05),
            "spearman_q95": np.nanquantile(ss, 0.95)} | {f"hit@{k}": h for k, h in enumerate(np.mean(hs, 0), 1)}


def budget_table(probe: dict[str, tuple[pd.DataFrame, np.ndarray]], gm: np.ndarray, Pm: np.ndarray, *,
                 draws: int = 1000, step: int = 50, seed: int = 0) -> pd.DataFrame:
    """probe: set name -> (labels with `label` and `kind`, verdicts pairs x models); gm, Pm: M_ask truth and verdicts.
    Models are the columns, in the same order everywhere."""
    rng = np.random.default_rng(seed)
    real = jmat(gm, Pm)
    rows = [{"method": "random", "n": 0, "source_size": 0, "draws": 0, "mean_regret": float(np.mean(real.max() - real)),
             "p_best": 1 / len(real)} | {f"hit@{k}": k / len(real) for k in range(1, len(real) + 1)}]
    for name, (labels, Pp) in probe.items():
        gp = labels.label.to_numpy().astype(bool)
        strata = [np.flatnonzero((labels.kind == k).to_numpy()) for k in sorted(labels.kind.unique())]
        for n in sizes(len(gp), step):
            def est(n=n):
                ix = stratified(strata, n, rng)
                return jmat(gp[ix], Pp[ix])
            rows.append(curve(f"probe:{name}", n, len(gp), est, real, draws))
    m = len(gm)
    for n in sizes(m, step):
        def ds(n=n):
            return dawid_skene(Pm[rng.choice(m, n, replace=False)])

        def lab(n=n):
            ix = rng.choice(m, n, replace=False)
            return None if gm[ix].all() or (~gm[ix]).all() else jmat(gm[ix], Pm[ix])
        rows.append(curve("dawid_skene", n, m, ds, real, draws))
        rows.append(curve("labelled", n, m, lab, real, draws))
    return pd.DataFrame(rows)


def budget(task: Task, *, draws: int = 1000, step: int = 50, seed: int = 0) -> Path | None:
    sides = {ps.stem: probe_side(task, ps, task.jobs) for ps in task.probe_sets if ps.exists()}
    have = sorted(set.intersection(*(set(h) for _, _, h in sides.values()))) if sides else []
    for i, j in enumerate(task.jobs):
        if i not in have:
            print(f"  [{task.name}] {j.label}: missing probe results for some set -- excluded from every method")
    if len(have) < 2:
        print(f"[{task.name}] need >= 2 models with results on every probe set, have {len(have)} -- skipped")
        return None
    jobs = [task.jobs[i] for i in have]
    gm, Pm, _ = real_side(task, jobs)
    table = budget_table({k: (labels, Pp[:, have]) for k, (labels, Pp, _) in sides.items()}, gm, Pm,
                         draws=draws, step=step, seed=seed)
    table.insert(0, "task", task.name)
    table.insert(1, "n_models", len(jobs))
    out = task.output_root / task.name / "budget.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(out, index=False)
    show = table[["method", "n", "draws", "mean_regret", "p_best", "mean_spearman"]]
    print(f"[{task.name}] {len(jobs)} models, M_ask {len(gm)} pairs")
    print(f"{show.round(3).to_string(index=False)}\n  -> {out}")
    return out

"""What kind of false candidates are in M_ask, and which kinds do the probe sets contain? (No oracle calls.)

For each reference-negative pair (s, t), take the TRUE partner of s (or of t) in the reference alignment and type the
candidate by its relation to that partner in the ontology hierarchy (direct rdfs:subClassOf edges plus someValuesFrom
fillers, followed up to 3 steps):
    hierarchy : candidate is an ancestor or descendant of the true partner (granularity confusion)
    sibling   : candidate and true partner share a direct parent
    unrelated : the entity has a true partner, the candidate is neither of the above
    unmatched : neither entity has a partner in the reference
The reference is used for this ANALYSIS only. Per type: count, split-vote pairs (jobs disagree), mean job TNR, and
the Spearman correlation of job TNR on that type with job J on all of M_ask. The negatives of every probe set are
typed the same way for comparison.
"""
from __future__ import annotations

from collections import Counter, deque
from pathlib import Path

import numpy as np
import pandas as pd

from .build import _ontologies, hierarchy
from .inputs import Task, load_mapping_pairs
from .report import jmat, real_side, spearmanr

TYPES = ("hierarchy", "sibling", "unrelated", "unmatched", "same")


def _ancestors(up: dict, x: str, k: int = 3) -> set[str]:
    out, q = set(), deque([(x, 0)])
    while q:
        n, d = q.popleft()
        if d == k:
            continue
        for p in up.get(n, ()):
            if p not in out:
                out.add(p)
                q.append((p, d + 1))
    return out


def _relation(up: dict, partner: str, cand: str) -> str:
    if partner == cand:
        return "same"
    if cand in _ancestors(up, partner) or partner in _ancestors(up, cand):
        return "hierarchy"
    if up.get(partner, set()) & up.get(cand, set()):
        return "sibling"
    return "unrelated"


def classifier(task: Task):
    oa_s, oa_t = _ontologies(task)
    (ups, _), (upt, _) = hierarchy(oa_s), hierarchy(oa_t)
    path = task.extra.get("reference") or task.cfg.evaluation.reference_alignment_path
    s2t: dict[str, set[str]] = {}
    t2s: dict[str, set[str]] = {}
    for s, t in load_mapping_pairs(Path(path)):
        s2t.setdefault(s, set()).add(t)
        t2s.setdefault(t, set()).add(s)

    def kind(s: str, t: str) -> str:
        """Strongest relation over ALL true partners (the reference can be 1:n), so the result is deterministic."""
        rels = [_relation(upt, p, t) for p in s2t.get(s, ())] + [_relation(ups, p, s) for p in t2s.get(t, ())]
        if not rels:
            return "unmatched"
        return next((k for k in ("same", "hierarchy", "sibling") if k in rels), "unrelated")

    return kind


def negtypes(task: Task) -> pd.DataFrame:
    kind = classifier(task)
    gt, P, keys = real_side(task, task.jobs)
    real = jmat(gt, P)
    types = np.array([kind(*k.split("|")[:2]) for k in keys])
    rows = []
    for ty in TYPES:
        m = (types == ty) & ~gt
        if not m.any():
            continue
        tnr = (~P[m]).mean(0)
        rows.append({"type": ty, "n": int(m.sum()),
                     "split_vote": int(((P[m].mean(1) > 0) & (P[m].mean(1) < 1)).sum()),
                     "mean_TNR": float(tnr.mean()), "TNR_min": float(tnr.min()), "TNR_max": float(tnr.max()),
                     "spearman_TNR_vs_J": spearmanr(tnr, real)[0] if m.sum() >= 3 else float("nan")})
    df = pd.DataFrame(rows)
    print(f"\n[{task.name}] M_ask {len(gt)} pairs, {int((~gt).sum())} reference negatives, {len(task.jobs)} jobs")
    print(df.round(2).to_string(index=False))
    for ps in task.probe_sets:
        if not ps.exists():
            continue
        lab = pd.read_csv(ps, sep="\t")
        neg = lab[lab.label == 0]
        print(f"  {ps.stem} negatives ({len(neg)}) by the same typing: {dict(Counter(kind(s, t) for s, t in zip(neg.src, neg.tgt)))}")
    out = task.output_root / task.name
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "m_ask_negative_types.csv", index=False)
    return df

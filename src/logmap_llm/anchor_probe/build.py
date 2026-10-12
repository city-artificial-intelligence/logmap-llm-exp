"""Build probe sets from LogMap's own output. The reference alignment is used only to PRINT label noise.

v4  positives: masked anchors (shared names removed, remaining-name similarity in [lo, hi])
    negatives: hard-discarded candidates, sampled from the most name-similar `pool_frac`
v5  positives: identical procedure to v4 (same seed -> the same positives as v4 for the same n)
    negatives: granularity negatives. For an anchor a = b, the pair (a, parent-or-child of b), and symmetrically
               (parent-or-child of a, b). If a = b, neither can be equivalent to b's strict parent or child, so the
               label is free. Parents/children are direct rdfs:subClassOf edges, plus someValuesFrom fillers
               (part_of style restrictions). Hub classes (> max_children direct children) are excluded and every class is used in at most one
               negative. Sampled from the most name-similar `pool_frac`, like v4.
               Optionally mixed with `n_lexical` v4 hard-discarded negatives.
Both classes are rendered by the same masked renderer, so the surface form leaks no label.
"""
from __future__ import annotations

import random
from collections import defaultdict
from pathlib import Path

import pandas as pd
import rdflib
from rdflib.namespace import OWL, RDFS

from logmap_llm.ontology.access import load_ontologies
from logmap_llm.ontology.object import OntologyEntryAttr

from .inputs import Task, logmap_pairs, reference
from .render import masked_names, render, similarity

THING = {str(OWL.Thing), "http://www.w3.org/2002/07/owl#Thing"}


def _ontologies(task: Task):
    at = task.cfg.alignmentTask
    return load_ontologies(at.onto_source_filepath, at.onto_target_filepath, cache_dir=None,
                           vocabulary=at.resolved_vocabulary, stub_import_iris=at.stub_import_iris or None)


def _pools(task: Task):
    anchors = logmap_pairs(task, "anchors")
    m_ask = {frozenset(p) for p in logmap_pairs(task, "m_ask")}
    hard = logmap_pairs(task, "hard_discarded")
    blocked = {frozenset(p) for p in anchors} | m_ask
    anchors = [p for p in anchors if frozenset(p) not in m_ask]
    hard = [p for p in hard if frozenset(p) not in blocked]
    return anchors, hard, blocked


def _prep(pair, oa_s, oa_t):
    try:
        s, t = OntologyEntryAttr(pair[0], oa_s), OntologyEntryAttr(pair[1], oa_t)
        m = masked_names(s, t)
    except Exception:  # noqa: BLE001 - entity missing / unreadable: skip, as the chapter scripts do
        return None
    return (s, t, *m) if m else None


def _positives(anchors, oa_s, oa_t, lo, hi):
    out = []
    for p in anchors:
        x = _prep(p, oa_s, oa_t)
        if x and lo <= similarity(x[2], x[3]) <= hi:
            out.append((p, x))
    return out


def _lexical_negative_pool(hard, oa_s, oa_t, n_neg, pool_frac):
    neg_all = []
    for p in hard:
        x = _prep(p, oa_s, oa_t)
        if x:
            neg_all.append((similarity(x[2], x[3]), p, x))
    neg_all.sort(key=lambda r: -r[0])
    return neg_all[: max(n_neg, int(len(neg_all) * pool_frac))]


def hierarchy(onto) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Direct parents and children: named superclasses plus someValuesFrom fillers of superclass restrictions."""
    g: rdflib.Graph = onto.getGraph()
    up: dict[str, set[str]] = defaultdict(set)
    for c, p in g.subject_objects(RDFS.subClassOf):
        if not isinstance(c, rdflib.URIRef):
            continue
        if isinstance(p, rdflib.URIRef):
            target = p
        else:
            target = g.value(p, OWL.someValuesFrom)
            if not isinstance(target, rdflib.URIRef):
                continue
        if str(target) not in THING and target != c:
            up[str(c)].add(str(target))
    down: dict[str, set[str]] = defaultdict(set)
    for c, ps in up.items():
        for p in ps:
            down[p].add(c)
    return up, down


def _granularity_pool(anchors, blocked, oa_s, oa_t, n_neg, pool_frac, max_children):
    """Candidate (pair, kind, substituted entity) for every anchor neighbour, then the most name-similar `pool_frac`.

    Two filters keep the set close to the granularity confusions seen in M_ask:
      * a substituted class with more than `max_children` direct children is a hub ("disease", "malformation
        syndrome" in ORDO) and makes a trivial negative -> dropped;
      * every class (substituted or anchored side) is used at most once, keeping its most name-similar pairing,
        so one large family (e.g. 26 numbered subtypes of one disease) cannot dominate the sample.
    """
    up_s, down_s = hierarchy(oa_s)
    up_t, down_t = hierarchy(oa_t)
    cands: dict[frozenset, tuple[tuple[str, str], str, str, int]] = {}
    for a, b in anchors:
        for b2 in sorted(up_t.get(b, ())):
            cands.setdefault(frozenset((a, b2)), ((a, b2), "granularity_parent", b2, len(down_t.get(b2, ()))))
        for b2 in sorted(down_t.get(b, ())):
            cands.setdefault(frozenset((a, b2)), ((a, b2), "granularity_child", b2, len(down_t.get(b2, ()))))
        for a2 in sorted(up_s.get(a, ())):
            cands.setdefault(frozenset((a2, b)), ((a2, b), "granularity_parent", a2, len(down_s.get(a2, ()))))
        for a2 in sorted(down_s.get(a, ())):
            cands.setdefault(frozenset((a2, b)), ((a2, b), "granularity_child", a2, len(down_s.get(a2, ()))))
    n_hub = sum(1 for k, c in cands.items() if k not in blocked and c[3] > max_children)
    pool = []
    for key, (pair, kind, sub, n_children) in cands.items():
        if key in blocked or n_children > max_children:
            continue
        x = _prep(pair, oa_s, oa_t)
        if x:
            pool.append((similarity(x[2], x[3]), pair, x, kind, sub))
    pool.sort(key=lambda r: (-r[0], r[1]))
    seen, unique = set(), []
    for r in pool:  # every class (substituted or anchored side) appears in at most one negative
        if r[1][0] not in seen and r[1][1] not in seen:
            seen.update(r[1])
            unique.append(r)
    print(f"  granularity candidates: {len(cands)}; hubs dropped (> {max_children} children): {n_hub}; "
          f"usable: {len(pool)}; each class used once: {len(unique)}")
    return unique[: max(n_neg, int(len(unique) * pool_frac))]


def build(task: Task, version: str, n_pos: int, n_neg: int, out: Path, *, n_lexical: int = 0, lo: float = 0.3,
          hi: float = 0.8, pool_frac: float = 0.1, seed: int = 42, max_children: int = 50) -> pd.DataFrame:
    rng = random.Random(seed)
    anchors, hard, blocked = _pools(task)
    oa_s, oa_t = _ontologies(task)
    pos_c = _positives(anchors, oa_s, oa_t, lo, hi)
    print(f"[{task.name}] positives in band [{lo}, {hi}]: {len(pos_c)} / {len(anchors)} anchors")
    pos = rng.sample(pos_c, n_pos)
    rows = [(*p, 1, "anchor_masked", render(*x)) for p, x in pos]
    if version == "v4":
        neg_c = _lexical_negative_pool(hard, oa_s, oa_t, n_neg, pool_frac)
        print(f"  lexical negative pool {len(neg_c)}")
        neg = rng.sample(neg_c[:], n_neg)
        rows += [(*r[1], 0, "hard_discarded", render(*r[2])) for r in neg]
    elif version == "v5":
        gran = _granularity_pool(anchors, blocked, oa_s, oa_t, n_neg, pool_frac, max_children)
        rows += [(*r[1], 0, r[3], render(*r[2])) for r in rng.sample(gran, n_neg)]
        if n_lexical:
            lex = _lexical_negative_pool(hard, oa_s, oa_t, n_lexical, pool_frac)
            rows += [(*r[1], 0, "hard_discarded", render(*r[2])) for r in rng.sample(lex, n_lexical)]
    else:
        raise ValueError(f"unknown probe-set version {version!r}")
    rng.shuffle(rows)
    df = pd.DataFrame(rows, columns=["src", "tgt", "label", "kind", "entity_lines"])
    try:
        ref = reference(task)
        noisy = df.apply(lambda r: (frozenset((r.src, r.tgt)) in ref) != bool(r.label), axis=1)
        print("  label noise vs reference (reported, never filtered):",
              df.assign(noisy=noisy).groupby("kind").noisy.agg(["sum", "count"]).to_dict("index"))
    except Exception as e:  # noqa: BLE001 - no reference available is fine for building
        print(f"  (no reference check: {type(e).__name__}: {e})")
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, sep="\t", index=False)
    print(f"  -> {out}  ({int(df.label.sum())} positives, {int((df.label == 0).sum())} negatives)")
    return df

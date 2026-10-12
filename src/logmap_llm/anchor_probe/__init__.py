"""Anchor probe: score candidate oracles on free, LogMap-labelled pairs before they adjudicate M_ask.

A probe set is a small list of (src, tgt, label) pairs whose labels come from LogMap's own output, not from a
reference alignment:

* positives: LogMap anchors with every shared name removed ("masked anchors", set v4);
* negatives: either hard-discarded candidates with the most similar names (v4), or granularity negatives (v5):
  an anchor whose one side is replaced by its direct parent or child in the ontology hierarchy.

Every candidate oracle is consulted on the probe with exactly the configuration of an existing LogMapLLM job
(same [oracle] and [prompts] sections, same endpoint), and the probe's ranking of the candidates is compared with
their real ranking on M_ask (from the jobs' own prediction files and the reference alignment).

    python -m logmap_llm.anchor_probe --help
"""

"""Name handling and the masked renderer shared by every probe set.

Ported unchanged from the journal-chapter scripts make_anchor_pairs_v3.py / make_anchor_pairs_v4.py, so that the
probe sets built here are byte-identical to the ones already evaluated (checked by `build --verify`).
"""
from __future__ import annotations

import re
from difflib import SequenceMatcher

from logmap_llm.oracle.prompts.formatting import select_best_direct_entity_names_with_synonyms

# ma_0002401, nci_c12345, orphanet_2083: URI fragments that some ontologies also carry as labels
ID_LIKE = re.compile(r"^[a-z0-9]+[_:][a-z]*\d{3,}$")


def names(entity) -> set[str]:
    """Lower-cased preferred names and synonyms of an OntologyEntryAttr."""
    out = {str(n).lower() for n in entity.get_preferred_names()} | {str(s).lower() for s in entity.get_synonyms()}
    return {n for n in out if n and n != "thing"}


def clean_names(entity) -> set[str]:
    return {n for n in names(entity) if not ID_LIKE.match(n)}


def similarity(a: set[str], b: set[str]) -> float:
    """Best SequenceMatcher ratio over all name pairs."""
    return max((SequenceMatcher(None, x, y).ratio() for x in a for y in b), default=0.0)


def masked_names(src, tgt) -> tuple[set[str], set[str]] | None:
    """Names of each side with every name the two sides share removed; None if a side would be left empty."""
    na, nb = clean_names(src), clean_names(tgt)
    shared = na & nb
    ra, rb = na - shared, nb - shared
    return (ra, rb) if ra and rb else None


def render(src, tgt, ra: set[str], rb: set[str]) -> str:
    """The two entity lines of the `one_level_of_parents_and_synonyms` template, built from masked name sets.

    The rest of the prompt (domain preamble, question, response instruction) is added at consultation time from
    the job's own PromptContext, exactly as the template does.
    """
    sp, tp = select_best_direct_entity_names_with_synonyms(src, tgt)[:2]

    def line(label, entity, rest, parent):
        pref = [n for n in sorted(str(p).lower() for p in entity.get_preferred_names()) if n in rest]
        name = pref[0] if pref else sorted(rest)[0]
        syn = sorted(rest - {name})
        syn_txt = (", also known as " + ", ".join(f'"{s}"' for s in syn)) if syn else ""
        par_txt = f', which falls under the category "{parent}"' if parent and parent != "Thing" else ""
        return f'The {label} one is "{name}"{syn_txt}{par_txt}.'

    return line("first", src, ra, sp) + "\n" + line("second", tgt, rb, tp)

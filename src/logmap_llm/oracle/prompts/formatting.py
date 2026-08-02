"""
logmap_llm.oracle.prompts.formatting
Prompt formatting utilities (originally prompt_utils.py)
NOTE: mostly imported from prior code
"""
from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

# Type-only import: OntologyEntryAttr is used solely in annotations, which `from __future__
# import annotations` renders as lazy strings — so guarding it under TYPE_CHECKING keeps this
# module (and the pure formatting functions, e.g. format_domain_range_clause) importable without
# owlready2, which the CPU test env lacks.
if TYPE_CHECKING:
    from logmap_llm.ontology.object import OntologyEntryAttr

###
# Name formatting helpers (original prompt_utils.py)
###

def get_name_string(name_set: set | list | OntologyEntryAttr) -> str:
    """Get a string representation of the name set."""
    # If the name_set is a set or list, join the elements with a comma
    if isinstance(name_set, (set, list)):
        return ", ".join(sorted(name_set))
    return str(name_set)


def get_single_name(name_set: set | list | str | OntologyEntryAttr) -> str | None:
    """
    Get a single name from the name set.

    BUGFIX (PT-1, sev 1): this used `next(iter(name_set))`. On a SET that is an arbitrary element
    whose identity depends on PYTHONHASHSEED, which CPython randomises per process. So the same
    entity yielded a different name on different runs, and the PROMPT TEXT ITSELF was not
    reproducible. Sets stay sets; we just choose from them deterministically.
    """
    if isinstance(name_set, (set, frozenset)):
        return min(name_set) if name_set else None
    if isinstance(name_set, list):
        return name_set[0] if name_set else None
    return name_set


def get_deterministic_single_name(name_set: set | list | str | OntologyEntryAttr) -> str | None:
    """Get a single name from the name set (deterministic: minimum by lexicographic order)."""
    if isinstance(name_set, (set, frozenset)):
        return min(name_set) if name_set else None
    if isinstance(name_set, list):
        return name_set[0] if name_set else None
    return name_set


def select_best_direct_entity_names(
    src_entity: OntologyEntryAttr, tgt_entity: OntologyEntryAttr,
) -> list:
    """If there are multiple direct parents, select one and find child element for it."""
    src_parent = src_entity.get_direct_parent()
    tgt_parent = tgt_entity.get_direct_parent()
    return [
        get_name_string(x.get_preferred_names()) if x else None
        for x in [src_parent, tgt_parent, src_entity, tgt_entity]
    ]


def format_hierarchy(
    hierarchy_dict: dict[int, set[OntologyEntryAttr]],
    no_level: bool = False,
    add_thing: bool = True,
) -> list[str] | str:
    """Format a hierarchy dict into a displayable string or list."""
    formatted = []
    for level, parents in sorted(hierarchy_dict.items()):
        parent_name = get_name_string(
            sorted([get_name_string(i.get_preferred_names()) for i in parents])
        )

        if not add_thing and parent_name == "Thing":
            continue

        if no_level:
            formatted.append(parent_name)
        else:
            formatted.append(f"\tLevel {level}: {parent_name}")

    return formatted if no_level else "\n".join(formatted)


def select_best_direct_entity_names_with_synonyms(
    src_entity: OntologyEntryAttr,
    tgt_entity: OntologyEntryAttr,
    add_thing: bool = True,
) -> list:
    """Select preferred names and synonyms for source and target entities.

    Returns [src_parent, tgt_parent, src_name, tgt_name, src_synonyms, tgt_synonyms].
    """

    def get_parent_name(entity: OntologyEntryAttr) -> str | None:
        parent = entity.get_direct_parent()
        parent_name = get_name_string(parent.get_preferred_names()) if parent else None
        if parent_name == "Thing" and not add_thing:
            return None
        return parent_name

    def get_clean_synonyms(entity: OntologyEntryAttr) -> list[str]:
        # BUGFIX (PT-1, sev 1): `get_synonyms()` returns a set[str], and this iterated it directly.
        # CPython randomises str hashing per process (PYTHONHASHSEED), so set-iteration order changed
        # between runs and the SAME candidate was sent a DIFFERENT PROMPT STRING on every run — the
        # synonyms were listed in a different order. The prompts, and hence the whole experiment, were
        # not reproducible; and some of the run-to-run ΔJ this project has been attributing to
        # server-side sampling noise is in fact PROMPT noise. Sort them.
        synonyms = sorted(str(s) for s in entity.get_synonyms())
        entity_name = str(entity.thing_class.name)
        return [] if len(synonyms) == 1 and synonyms[0] == entity_name else synonyms

    src_parent_name = get_parent_name(src_entity)
    tgt_parent_name = get_parent_name(tgt_entity)

    src_entity_name = get_name_string(src_entity.get_preferred_names())
    tgt_entity_name = get_name_string(tgt_entity.get_preferred_names())
    src_synonyms = get_clean_synonyms(src_entity)
    tgt_synonyms = get_clean_synonyms(tgt_entity)

    return [
        src_parent_name,
        tgt_parent_name,
        src_entity_name,
        tgt_entity_name,
        src_synonyms,
        tgt_synonyms,
    ]


def select_best_sequential_hierarchy_with_synonyms(
    src_entity: OntologyEntryAttr,
    tgt_entity: OntologyEntryAttr,
    max_level: int,
) -> tuple[list[str], list[str], list[list[str]], list[list[str]]]:
    """Select synonyms for an entity and its hierarchical parents."""
    src_parents_by_levels = src_entity.get_parents_by_levels(max_level)
    tgt_parents_by_levels = tgt_entity.get_parents_by_levels(max_level)

    def get_synonyms_and_class(
        parents_by_levels: dict[int, set[OntologyEntryAttr]], idx: int
    ) -> tuple[list[str], str]:
        if len(parents_by_levels) > idx:
            # BUGFIX (PT-1): `next(iter(<set of parents>))` picked an ARBITRARY parent, and which one
            # depended on PYTHONHASHSEED — so a class with two parents got a different "falls under the
            # category X" clause on different runs. Choose deterministically (lowest URI), and sort the
            # synonyms for the same reason.
            level = parents_by_levels[idx]
            entry = min(level, key=lambda e: str(e.annotation.get("uri", ""))) if level else None
            if entry is None:
                return [], ""
            syns = sorted(str(s) for s in entry.get_synonyms()) if hasattr(entry, "get_synonyms") else []
            cls = str(entry.onto.getClassByURI(entry.annotation["uri"])).split(".")[-1]
            return syns, cls
        return [], ""

    def clean(synonyms: list, cls: str) -> list[str]:
        return (
            [] if len(synonyms) == 1 and next(iter(synonyms)) == cls else synonyms
        )

    src_results = [
        clean(*get_synonyms_and_class(src_parents_by_levels, i))
        for i in range(len(src_parents_by_levels))
    ]
    tgt_results = [
        clean(*get_synonyms_and_class(tgt_parents_by_levels, i))
        for i in range(len(tgt_parents_by_levels))
    ]

    return src_results[0], tgt_results[0], src_results[1:], tgt_results[1:]


###
# Sibling context formatting
###

def format_sibling_context(
    sibling_labels: list[str] | list[tuple[str, float]],
    parent_name: str,
) -> str:
    """Format sibling labels into a natural-language context clause."""
    if not sibling_labels:
        return ""

    labels = []
    for item in sibling_labels:
        if isinstance(item, tuple):
            labels.append(item[0])
        else:
            labels.append(item)

    if len(labels) == 1:
        sibling_text = f'"{labels[0]}"'
    else:
        sibling_text = ", ".join(f'"{s}"' for s in labels[:-1])
        sibling_text += f' and "{labels[-1]}"'

    return f'Other "{parent_name}" concepts include {sibling_text}.'


###
# Property prompt formatting helpers
###

def format_synonyms_parenthetical(synonyms: set[str], preferred_name: str) -> str:
    """Format synonyms as a parenthetical clause."""
    extra_syns = sorted(s for s in synonyms if s != preferred_name)
    if not extra_syns:
        return ""
    quoted = ", ".join(f'"{s}"' for s in extra_syns)
    return f" (also known as {quoted})"


def format_domain_range_clause(
    prop_label: str,
    domain_names: set[str],
    range_names: set[str],
    domain_synonyms: set[str] | None = None,
    range_synonyms: set[str] | None = None,
    include_synonyms: bool = False,
    is_data_property: bool = False,
) -> str:
    """Format a property with optional domain/range context.

    PT-2: a DATA property takes literal values of a datatype (its range is e.g. "date",
    "string"), not related individuals. Rendering it like an object property
    ('"birthDate" which connects "Person" to something') drops the datatype — the most
    discriminating feature of a data property — and makes DPROP indistinguishable from
    OPROP to the oracle. When is_data_property is set, render the datatype range instead
    ('"birthDate" on "Person" which has data values of type "date"').
    """
    desc = f'"{prop_label}"'

    if domain_names or range_names:
        domain_str = ", ".join(f'"{d}"' for d in sorted(domain_names)) if domain_names else "something"
        range_str = ", ".join(f'"{r}"' for r in sorted(range_names)) if range_names else "something"

        # deterministic:
        if include_synonyms:
            if domain_synonyms:
                dom_anchor = min(domain_names) if domain_names else ""
                dom_syn = format_synonyms_parenthetical(domain_synonyms, dom_anchor)
                domain_str += dom_syn
            if range_synonyms:
                rng_anchor = min(range_names) if range_names else ""
                rng_syn = format_synonyms_parenthetical(range_synonyms, rng_anchor)
                range_str += rng_syn

        if is_data_property:
            if domain_names:
                desc += f" on {domain_str}"
            desc += f" which has data values of type {range_str}"
        else:
            desc += f" which connects {domain_str} to {range_str}"

    return desc


###
# Restriction context formatting
###

def format_restriction_context(restrictions: list[dict]) -> str:
    """Format class restriction axioms as a natural-language clause."""
    if not restrictions:
        return ""

    VERBS = {
        'some': 'relates to some',
        'only': 'only relates to',
        'min': 'relates to at least',
        'max': 'relates to at most',
        'exactly': 'relates to exactly',
    }

    clauses = []
    for r in restrictions:
        verb = VERBS.get(r['restriction_type'], 'relates to')
        filler = f'"{r["filler_name"]}"' if r['filler_name'] else 'something'
        prop = f'"{r["property_name"]}"'

        if r['restriction_type'] in ('min', 'max', 'exactly') and r.get('cardinality') is not None:
            clauses.append(f'{verb} {r["cardinality"]} {filler} via {prop}')
        else:
            clauses.append(f'{verb} {filler} via {prop}')

    joined = " and ".join(clauses)
    return f"It {joined}."


###
# Relational signature formatting
###

def format_relational_signature(signature: dict) -> str:
    """Verbalise a class's relational signature as natural-language context."""
    domain_props = signature.get('as_domain', [])
    range_props = signature.get('as_range', [])

    if not domain_props and not range_props:
        return ""

    parts = []
    if domain_props:
        quoted = ", ".join(f'"{p}"' for p in domain_props[:4])
        parts.append(f'the domain of {quoted}')
    if range_props:
        quoted = ", ".join(f'"{p}"' for p in range_props[:4])
        parts.append(f'the range of {quoted}')

    joined = ", and as ".join(parts)
    return f"In its ontology, it appears as {joined}."


###
# Property characteristic formatting
###

def format_property_characteristics(characteristics: list[str], inverse_name: str | None) -> str:
    """Verbalise property characteristics and inverse as natural-language context."""
    parts = []

    if characteristics:
        char_text = " and ".join(characteristics)
        parts.append(f"a {char_text} property")

    if inverse_name:
        parts.append(f'the inverse of "{inverse_name}"')

    if not parts:
        return ""

    joined = " and ".join(parts)
    return f"It is {joined}."


###
# Instance prompt formatting helpers (KG track)
###

def format_instance_type_clause(type_names: list[str]) -> str:
    """Format rdf:type names into a natural-language clause."""
    if not type_names:
        return ""
    if len(type_names) == 1:
        return f'which is a "{type_names[0]}"'
    quoted = [f'a "{t}"' for t in type_names]
    return "which is " + " and ".join(quoted)


def _format_property_value(value: str, datatype: str) -> str:
    """Format a property value with type-appropriate quoting."""
    numeric_types = {"integer", "int", "float", "double", "decimal",
                     "long", "short", "nonNegativeInteger",
                     "positiveInteger", "negativeInteger"}
    if datatype in numeric_types:
        return value
    return f'"{value}"'


def format_instance_attribute_clause(properties: list[dict], max_properties: int = 5) -> str:
    """
    Format instance property-value pairs as natural-language clauses.
    Returns clauses joined by " and ", e.g.:
    'is "homeworld" "Tatooine" and is "affiliation" "Rebel Alliance"'
    """
    if not properties:
        return ""

    clauses = []
    for prop in properties[:max_properties]:
        pred_label = prop["predicate_label"]
        if "value" in prop:
            formatted_val = _format_property_value(prop["value"], prop.get("datatype", "string"))
            clauses.append(f'"{pred_label}" {formatted_val}')
        elif "object_label" in prop:
            clauses.append(f'"{pred_label}" "{prop["object_label"]}"')

    if not clauses:
        return ""

    return " and ".join(f"is {c}" for c in clauses)


def _get_property_value(prop: dict) -> str:
    """Extract a comparable value string from a property dict."""
    if "value" in prop:
        return str(prop["value"]).lower().strip()
    if "object_label" in prop:
        return str(prop["object_label"]).lower().strip()
    return ""


def _property_sort_key(prop: dict) -> tuple[str, ...]:
    """Return a total ordering for an instance property assertion.

    ``getInstanceContext()`` normally supplies already-sorted lists, but keeping the
    tie-break here makes selection deterministic for every caller (and for multiple
    values of the same predicate).  In particular, neither a set-derived label order
    nor rdflib's triple iteration order may decide which value reaches a prompt.
    """
    return (
        str(prop.get("predicate_label", "")).lower().strip(),
        str(prop.get("predicate_uri", "")),
        str(prop.get("value", "")),
        str(prop.get("datatype", "")),
        str(prop.get("object_uri", "")),
        str(prop.get("object_label", "")),
        str(prop.get("kind", "")),
    )


def _find_best_pair(src_entries: list[dict], tgt_entries: list[dict]) -> tuple[dict, dict]:
    """For a shared predicate with multiple values per side, find the best pair."""
    src_entries = sorted(src_entries, key=_property_sort_key)
    tgt_entries = sorted(tgt_entries, key=_property_sort_key)

    tgt_by_value = {}
    for t in tgt_entries:
        val = _get_property_value(t)
        if val and val not in tgt_by_value:
            tgt_by_value[val] = t

    for s in src_entries:
        val = _get_property_value(s)
        if val and val in tgt_by_value:
            return s, tgt_by_value[val]

    return src_entries[0], tgt_entries[0]


def select_intersecting_properties(
    src_props: list[dict],
    tgt_props: list[dict],
    max_properties: int = 5,
    intersection_only: bool = False,
    predicate_entropies: dict | None = None,
) -> tuple[list[dict], list[dict]]:
    """Select properties for prompt inclusion, prioritising shared predicates."""
    src_all_by_label: dict[str, list[dict]] = defaultdict(list)
    
    for p in src_props:
        label = p["predicate_label"].lower().strip()
        src_all_by_label[label].append(p)

    for entries in src_all_by_label.values():
        entries.sort(key=_property_sort_key)

    tgt_all_by_label: dict[str, list[dict]] = defaultdict(list)
    
    for p in tgt_props:
        label = p["predicate_label"].lower().strip()
        tgt_all_by_label[label].append(p)

    for entries in tgt_all_by_label.values():
        entries.sort(key=_property_sort_key)

    shared_labels = set(src_all_by_label.keys()) & set(tgt_all_by_label.keys())

    shared_best_pairs = {}
    
    for label in shared_labels:
        best_src, best_tgt = _find_best_pair(
            src_all_by_label[label], tgt_all_by_label[label]
        )
        shared_best_pairs[label] = (best_src, best_tgt)

    if predicate_entropies is not None and shared_labels:
        def _entropy_for_label(label):
            src_entry, tgt_entry = shared_best_pairs[label]
            src_uri = src_entry.get("predicate_uri", "")
            tgt_uri = tgt_entry.get("predicate_uri", "")
            return max(
                predicate_entropies.get(src_uri, 0.0),
                predicate_entropies.get(tgt_uri, 0.0),
            )
        # ``shared_labels`` is a set. Sorting it only by entropy left equal-entropy
        # labels in hash-table iteration order, so PYTHONHASHSEED changed both the
        # selected properties and their order in otherwise identical prompts.
        ranked_shared = sorted(
            shared_labels,
            key=lambda label: (-_entropy_for_label(label), label),
        )
    else:
        ranked_shared = sorted(shared_labels)

    src_selected = []
    tgt_selected = []
    selected_src_labels: set[str] = set()
    selected_tgt_labels: set[str] = set()

    for label in ranked_shared:
        if len(src_selected) >= max_properties:
            break
        best_src, best_tgt = shared_best_pairs[label]
        src_selected.append(best_src)
        tgt_selected.append(best_tgt)
        selected_src_labels.add(label)
        selected_tgt_labels.add(label)

    if not intersection_only:
        
        if len(src_selected) < max_properties:
            for label in sorted(set(src_all_by_label.keys()) - shared_labels):
                if label in selected_src_labels:
                    continue
                src_selected.append(src_all_by_label[label][0])
                selected_src_labels.add(label)
                if len(src_selected) >= max_properties:
                    break

        if len(tgt_selected) < max_properties:
            for label in sorted(set(tgt_all_by_label.keys()) - shared_labels):
                if label in selected_tgt_labels:
                    continue
                tgt_selected.append(tgt_all_by_label[label][0])
                selected_tgt_labels.add(label)
                if len(tgt_selected) >= max_properties:
                    break

    return src_selected, tgt_selected

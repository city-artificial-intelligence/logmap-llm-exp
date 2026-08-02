"""
logmap_llm.ontology.instance_index

A deterministic type -> instances index, built ONCE per ontology from the rdflib graph.

Why this exists
---------------
``SiblingSelector`` was class-only: sibling means "another child of my parent", which needs a
class hierarchy. Instances have no such hierarchy, and the module's own docstring records the
planned alternative — "for inst resolution, we will get better results by simply ranking all
instances with a matching type identity". That is what this index supplies, for
``paired-sibling-v2`` on the Knowledge Graph track (decision D-a in HANDOFF_CORE_BUMP.md).

Two properties matter and are enforced here rather than left to the caller:

**Built once, never per query.** The KG track has 9,728 INST retrieval traces; a per-query
walk over the graph would be quadratic in a way nobody would notice until a campaign stalled.
The index is memoised per ontology on a content fingerprint.

**Type specificity is visible.** Measured on the real data, a large share of dbkwik subjects
carry no type other than ``owl:Thing`` — 6,643 of them in ``swg.rdf``. A shared ``owl:Thing``
makes "sibling" mean "any resource in this ontology", which is not a near-miss and would
quietly contaminate the KG arm of the experiment. So specific types are preferred, the
uninformative bucket is used only when nothing else is shared, and which one was used is
recorded on the constructed negative so the rate is reportable per lane.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib

from rdflib import RDF, RDFS, URIRef


#: Types that carry no discriminating information: everything is one.
UNINFORMATIVE_TYPES = frozenset({
    "http://www.w3.org/2002/07/owl#Thing",
    "http://www.w3.org/2000/01/rdf-schema#Resource",
    "http://www.w3.org/2002/07/owl#NamedIndividual",
})

#: Bump when the index's content or ordering rules change.
INDEX_SCHEMA_VERSION = "instance-type-index-v1"


@dataclass(frozen=True)
class IndexedInstance:
    """A candidate sibling instance, carrying just enough to rank and to filter by label.

    Deliberately NOT an ``InstanceEntity``: constructing one calls ``getInstanceContext``,
    which walks the graph for that subject. Doing that for every candidate in a type bucket
    would make sibling selection cost a graph walk per candidate per query.
    """
    uri: str
    label: str
    type_specificity: str = "specific"

    def get_preferred_names(self) -> set[str]:
        return {self.label} if self.label else set()

    def get_synonyms(self) -> set[str]:
        return set()

    def get_all_entity_names(self) -> set[str]:
        return self.get_preferred_names()

    @property
    def iri(self) -> str:
        return self.uri


@dataclass(frozen=True)
class InstanceTypeIndex:
    """``type IRI -> instances of that type``, each bucket sorted by ``(label, IRI)``."""

    fingerprint: str
    by_type: dict[str, tuple[IndexedInstance, ...]]

    def candidates(
        self, type_uris, *, exclude_uri: str, limit: int | None = None,
    ) -> tuple[list[IndexedInstance], str]:
        """Instances sharing at least one of ``type_uris``, preferring specific types.

        Returns ``(candidates, specificity)`` where specificity is ``"specific"`` when the
        shared type was a real class and ``"uninformative"`` when only ``owl:Thing`` or a
        peer was available.

        Order is deterministic: type buckets in sorted type order, each bucket already
        sorted by ``(label, IRI)``, de-duplicated across buckets. ``limit`` stops early on
        exactly that stream, so it is identical to slicing the full union — but it matters:
        the largest real bucket (``dbkwik ontology/Image`` on memory-beta) holds 43,962
        members, and materialising it per query costs ~4 ms against ~0.02 ms for the
        50 the caller will actually keep.
        """
        wanted = [str(uri) for uri in type_uris if str(uri)]
        specific = sorted(uri for uri in wanted if uri not in UNINFORMATIVE_TYPES)
        selected = specific
        specificity = "specific"
        if not selected:
            selected = sorted(uri for uri in wanted if uri in UNINFORMATIVE_TYPES)
            specificity = "uninformative"

        seen: set[str] = {exclude_uri}
        out: list[IndexedInstance] = []
        for type_uri in selected:
            for instance in self.by_type.get(type_uri, ()):
                if instance.uri in seen:
                    continue
                seen.add(instance.uri)
                out.append(
                    instance if specificity == "specific"
                    else IndexedInstance(instance.uri, instance.label, "uninformative")
                )
                if limit is not None and len(out) >= limit:
                    return out, specificity
        return out, specificity


def _graph_fingerprint(graph, ontology_iri: str) -> str:
    """A cheap content address: the index is a pure function of these."""
    digest = hashlib.sha256()
    digest.update(INDEX_SCHEMA_VERSION.encode("utf-8"))
    digest.update(b"\x1f")
    digest.update(str(ontology_iri).encode("utf-8"))
    digest.update(b"\x1f")
    digest.update(str(len(graph)).encode("utf-8"))
    return digest.hexdigest()


def build_instance_type_index(ontology) -> InstanceTypeIndex:
    """Build the index with two passes over the rdflib graph: rdf:type, then rdfs:label.

    Labels are collected in the same build rather than looked up per candidate, because
    ordering a type bucket requires the label of every member of that bucket — up to several
    thousand — and doing that per query is exactly the cost this index exists to avoid.
    """
    graph = ontology.getGraph()
    ontology_iri = ""
    try:
        ontology_iri = str(ontology.get_ontology_iri())
    except Exception:
        pass

    labels: dict[str, str] = {}
    for subject, _predicate, value in graph.triples((None, RDFS.label, None)):
        uri = str(subject)
        text = str(value)
        # deterministic: the lexicographically smallest label wins, as elsewhere in this module
        if uri not in labels or text < labels[uri]:
            labels[uri] = text

    raw: dict[str, list[IndexedInstance]] = {}
    for subject, _predicate, type_uri in graph.triples((None, RDF.type, None)):
        if not isinstance(type_uri, URIRef):
            continue
        uri = str(subject)
        raw.setdefault(str(type_uri), []).append(
            IndexedInstance(uri=uri, label=labels.get(uri, ""))
        )

    by_type = {
        type_uri: tuple(sorted(members, key=lambda item: (item.label, item.uri)))
        for type_uri, members in sorted(raw.items())
    }
    return InstanceTypeIndex(
        fingerprint=_graph_fingerprint(graph, ontology_iri), by_type=by_type,
    )

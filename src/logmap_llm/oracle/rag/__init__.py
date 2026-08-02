"""
logmap_llm.oracle.rag

Query-specific RAG few-shot retrieval (spec §6). Public API (mirrors __all__ below):

    from logmap_llm.oracle.rag import (
        # value types
        EntityKind, Mode, Source, Direction, FallbackPolicy, RagConfig,
        QueryMapping, Example, ExampleRef, RetrievalTrace, RetrievalResult,
        # encoders / token counters
        Encoder, HashingEncoder, ClsPooledEncoder, SbertEncoder,
        TokenCounter, HeuristicTokenCounter, HFTokenCounter,
        # corpus / index / retriever
        TypedCorpus, EmbeddingIndex, compute_index_hash,
        RagRetriever, RagRetrievalError,
        # pipeline adapter
        mode_from_strategy, m_ask_exclusion_keys, build_typed_corpus_from_anchors,
        query_mappings_from_m_ask, build_retriever_from_pipeline,
    )

Design contract: framework/RAG_DESIGN.md.
"""
from .types import (
    EntityKind, Mode, Source, Direction, FallbackPolicy, RagConfig,
    QueryMapping, Example, ExampleRef, RetrievalTrace, RetrievalResult,
)
from .encoder import Encoder, HashingEncoder, ClsPooledEncoder, SbertEncoder
from .tokenizer import TokenCounter, HeuristicTokenCounter, HFTokenCounter
from .corpus import TypedCorpus
from .index import EmbeddingIndex, compute_index_hash
from .retriever import RagRetriever, RagRetrievalError
from .pipeline_adapter import (
    mode_from_strategy, m_ask_exclusion_keys, build_typed_corpus_from_anchors,
    query_mappings_from_m_ask, build_retriever_from_pipeline,
)

__all__ = [
    "EntityKind", "Mode", "Source", "Direction", "FallbackPolicy", "RagConfig",
    "QueryMapping", "Example", "ExampleRef", "RetrievalTrace", "RetrievalResult",
    "Encoder", "HashingEncoder", "ClsPooledEncoder", "SbertEncoder",
    "TokenCounter", "HeuristicTokenCounter", "HFTokenCounter",
    "TypedCorpus", "EmbeddingIndex", "compute_index_hash",
    "RagRetriever", "RagRetrievalError",
    "mode_from_strategy", "m_ask_exclusion_keys", "build_typed_corpus_from_anchors",
    "query_mappings_from_m_ask", "build_retriever_from_pipeline",
]

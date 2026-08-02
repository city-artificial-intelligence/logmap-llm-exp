'''
This module contains functionality that supports bridging
between the worlds of Python and Java.
'''

# PYTHON IMPORTS:

import math
from pathlib import Path

import pandas as pd

from logmap_llm.constants import (
    COL_CONFIDENCE,
    COL_ENTITY_TYPE,
    COL_RELATION,
    COL_SOURCE_ENTITY_URI,
    COL_TARGET_ENTITY_URI,
    DEFAULT_CONFIDENCE_FALLBACK,
    M_ASK_COLUMNS,
    EntityType,
    EntityRelation,
    PAIRS_SEPARATOR,
    VERBOSE,
)

from logmap_llm.utils.data import (
    dedupe_m_ask_by_uri_pair,
    filter_accepted_predictions,
)
from logmap_llm.utils.logging import debug, warning

# ENTITY TYPE REPRESENTATIONS:

# LogMap recognises 5 entity types in its <MappingObjectStr> objects,
# each one represented by a particular integer. The LogMap m_ask 
# output file uses string representations for the 5 entity types.
# LogMap-LLM maps the LogMap integer entity types to the same string
# representations and uses these alone, internally (in memory) and
# externally in LogMap-LLM output files.

# entityType_int_2_str := {0: 'CLS', 1: 'DPROP', 2: 'OPROP', 3: 'INST', 4: 'UNKNO'}
# entityType_str_2_int := {'CLS': 0, 'DPROP': 1, 'OPROP': 2, 'INST': 3, 'UNKNO': 4}

entityType_int_2_str = {
    0: EntityType.CLASS.value,
    1: EntityType.DATAPROPERTY.value,
    2: EntityType.OBJECTPROPERTY.value,
    3: EntityType.INSTANCE.value,
    4: EntityType.UNKNOWN.value,
}

entityType_str_2_int = {
    EntityType.CLASS.value: 0,
    EntityType.DATAPROPERTY.value: 1,
    EntityType.OBJECTPROPERTY.value: 2,
    EntityType.INSTANCE.value: 3,
    EntityType.UNKNOWN.value: 4,
}

# RELATION REPRESENTATIONS:

# LogMap recognises 3 relations in its <MappingObjectStr> objects,
# each one represented by a particular integer. The LogMap m_ask 
# output file uses string representations for the 3 relations.
# LogMap-LLM maps the LogMap integer relations to the same string
# representations and uses these alone, internally (in memory) and
# externally in LogMap-LLM output files.

#  0 - < - subClassOf    (src_entity subClassOf tgt_entity)  
# -1 - > - superClassOf  (src_entity superClassOf tgt_entity)
# -2 - = - equivalence   (src_entity equivalent tgt_entity)

# relation_int_2_str := {0: '<', -1: '>', -2: '='}
# relation_str_2_int := {'<': 0, '>': -1, '=': -2}

relation_int_2_str = {
    0: EntityRelation.SUBCLASSOF.value,
    -1: EntityRelation.SUPERCLASSOF.value,
    -2: EntityRelation.EQUIVALENCE.value,
}

relation_str_2_int = {
    EntityRelation.SUBCLASSOF.value: 0,
    EntityRelation.SUPERCLASSOF.value: -1,
    EntityRelation.EQUIVALENCE.value: -2,
}

# JAVA -> PYTHON OUTPUT FORMAT FOR M_ASK (MAPPINGS TO ASK):

# When LogMap produces a set of mappings to ask (M_ask), it
# collects together uncertain mappings that would usually be
# provided to a human oracle to obtain answers regarding the
# plausibility/correctness of each uncertain mapping. By dumping
# these mappings in a file, we can collect them and foward them
# to an LLM or any other valid oracle. The file that LogMap
# produces containing the uncertain mappings is structured
# according to the following header (in a .txt file):

# source_entity_uri|target_entity_uri|relation|confidence|entityType

# Example M_ASK row:
#   http://example.org/a#Widget|http://example.org/b#Gadget|=|0.73|CLS

# As such, we define the 'columns' for re-use later below
# (now imported from logmap_llm.constants.py)

# to obtain a mutable list, use the following fn:

def get_m_ask_column_names() -> list[str]:
    """
    Returns M_ASK_COLUMNS as a mutable list
    """
    return list(M_ASK_COLUMNS)


def load_m_ask_from_file(filepath: Path) -> pd.DataFrame:
    """
    Load a (headerless, pipe-delimited) LogMap m_ask file as a pd.DataFrame
    and set the column names to those defined above (M_ASK_COLUMNS). Duplicate
    (source, target) rows are collapsed (see dedupe_m_ask_by_uri_pair).
    """
    try:
        m_ask_df = pd.read_csv(filepath, sep=PAIRS_SEPARATOR, header=None)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=get_m_ask_column_names())
    m_ask_df.columns = get_m_ask_column_names()
    return dedupe_m_ask_by_uri_pair(m_ask_df)


###
# FUNCTIONS TO ENABLE ROUNDTRIPPING BETWEEN LOGMAP (JAVA) AND LOGMAP-LLM (PYTHON)
# (mostly retained from original LogMap-LLM codebase)
###

###
# CONFIDENCE COERCION AT THE JAVA BOUNDARY
# ---------------------------------------- 
# when the oracle accepts a mapping but no usable logprob token was emitted,
# calculate_logprobs_confidence returns float('nan'); passing NaN to LogMap
# for a confidence value via MappingObjectStr(..., double conf, ...) is technically
# type-correct, but may notbe semantically coherant; and could possibly cause some
# kind of failure mode within LogMap; to protect agaisnt this, we coerce NaN to a 
# concrete default (ie. 1.0; confident 'True' -- or "yes, this mapping is correct")
# which I'm quite sure is the 'expected behaviour' (the oracle is assumed to produce
# a binary answer, either yes or no) ... and this only fires for oracle predictions
# that predict the mapping to be true; so, this should be fine. (DEFAULT CONF = 1.0)
#       (see constants.py)
###

def _coerce_confidence_for_java(raw_conf, row_index: int | None = None) -> float:
    """
    normalises a python confidence value -> finite float for 'double conf':
    Handles NaN | None | any non-float value (should only be triggered when mapping=True)
    """
    if raw_conf is None:
        if VERBOSE:
            debug(f"(_coerce_confidence_for_java) None confidence at row {row_index}; hits fallback.")
        return DEFAULT_CONFIDENCE_FALLBACK

    try:
        conf = float(raw_conf)
    except (TypeError, ValueError):
        if VERBOSE:
            warning(f"(_coerce_confidence_for_java) non-numeric confidenceat row {row_index}; using fallback")
        return DEFAULT_CONFIDENCE_FALLBACK
    
    if math.isnan(conf) or math.isinf(conf):
        if VERBOSE:
            debug(f"(_coerce_confidence_for_java) NaN/inf confidence at row {row_index}; using fallback.")
        return DEFAULT_CONFIDENCE_FALLBACK
    
    return conf


###
# BRIDGING INTERFACE
# The implementation is mostly retained from the prior version.
# A slight stylistic modification has been applied to the guard clauses
# though, these are still functionally equivalent. The filtering behaviour
# is actually reused in other areas of the code, so we pull that out as a util.
# the same can be said about the coersion of NaN values (and how it relates to pd)
# eg. in erroneous cases (conf=0) or  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# when a mapping is true, but no confidence is specified (ie. conf=1.0)
###


def java_mappings_2_python(
    mappings_java,
    *,
    dedupe_uri_pairs: bool = False,
) -> pd.DataFrame:
    '''
    Convert ontology alignment mappings from LogMap's Java representation
    to LogMap-LLM's Python representation.

    Parameters
    ----------
    mappings_java : java.util.HashSet of LogMap <MappingObjectStr> objects
        Mappings generated by LogMap.
    dedupe_uri_pairs : bool, default=False
        Collapse duplicate directional URI pairs. Enable this only at the
        M_ask boundary, where asking the same candidate twice is undesirable.
        Full alignments must preserve rows that differ by relation or type.

    Returns
    -------
    mappings_df : Pandas DataFrame
        A dataframe representation of mappings_java.
    '''

    # convert java.util.HashSet to Object[] array
    mappings_java = mappings_java.toArray()

    # initialise containers for mapping elements
    src_entity_uris: list[str] = []
    tgt_entity_uris: list[str] = []
    relations: list[str] = []
    confidences: list[float] = []
    entity_types: list[str] = []

    # iterate over the mappings in their Java representation
    for mapping_java in mappings_java:

        # get the URIs of the two entities
        src_entity_uris.append(str(mapping_java.getIRIStrEnt1()))
        tgt_entity_uris.append(str(mapping_java.getIRIStrEnt2()))

        # convert LogMap's integer representation of the entity 
        # relation to a string representation

        relation_int = mapping_java.getMappingDirection()

        if relation_int not in relation_int_2_str:
            raise ValueError(f'Relation {relation_int} not recognised')
        
        relations.append(relation_int_2_str[relation_int])

        # get LogMap's confidence in the mapping
        confidences.append(float(mapping_java.getConfidence()))

        # convert LogMap's integer representation of the entity type
        # to a string representation
        entityType_int = mapping_java.getTypeOfMapping()
        if entityType_int not in entityType_int_2_str:
            raise ValueError(f'Entity type {entityType_int} not recognised')
            
        entity_types.append( entityType_int_2_str[entityType_int])

    # end: for

    mappings_df = pd.DataFrame(data={
        COL_SOURCE_ENTITY_URI: src_entity_uris,
        COL_TARGET_ENTITY_URI: tgt_entity_uris,
        COL_RELATION: relations,
        COL_CONFIDENCE: confidences,
        COL_ENTITY_TYPE: entity_types,
    })
    # BUGFIX (JAVA-ORDER): the rows arrive in java.util.HashSet iteration order, which is
    # UNSPECIFIED — it reaches the persisted predictions CSV and refined TSV row order,
    # and (via keep='first' dedupe below) even decides WHICH lane of a mixed-use predicate
    # survives as the asked candidate. Canonically sort at the boundary so every
    # downstream ordering is a function of content, not of JVM hashing. NOTE: this pins
    # artifact row order for new runs; rows from completed historical runs may appear in a
    # different (previously arbitrary) order.
    mappings_df = mappings_df.sort_values(
        by=[COL_SOURCE_ENTITY_URI, COL_TARGET_ENTITY_URI, COL_RELATION, COL_ENTITY_TYPE],
        kind="mergesort",
    ).reset_index(drop=True)
    if dedupe_uri_pairs:
        return dedupe_m_ask_by_uri_pair(mappings_df)
    return mappings_df



def python_oracle_mapping_predictions_2_java(m_ask_df_ext):
    '''
    Convert a set of Python LLM Oracle mapping predictions to a
    set of Java (LogMap) MappingObjectStr objects. 

    Note: In general, the LLM Oracle predictions will be a mix
    of True and False predictions. But LogMap expects to receive
    from an Oracle a set of True mappings only. So, in addition
    to converting between Python and Java datatypes, this
    function also *filters out* the mappings predicted to be False.

    Parameters
    ----------
    m_ask_df_ext : pandas DataFrame
        A Python representation of LogMap's m_ask output, extended with
        LLM Oracle predictions.

    Returns
    -------
    m_ask_oracle_preds_java : java.util.HashSet of LogMap <MappingObjectStr> objects
        The subset of the mappings in m_ask that an LLM Oracle predicted
        to be True mappings.
    '''
    # Keep Java imports at the actual Java boundary. Pure mapping-file helpers can
    # then be imported by planners/tests before a JVM has been started.
    from java.util import HashSet  # type: ignore
    from uk.ac.ox.krr.logmap2.mappings.objects import MappingObjectStr  # type: ignore

    # skip over (i.e. filter-out) everything except mappings with an Oracle prediction 
    # of True; this excludes mappings with Oracle prediction values of False and 'error'
    accepted = filter_accepted_predictions(m_ask_df_ext)

    # container for a collection of LogMap <MappingObjectStr> Java objects
    m_ask_oracle_preds_true: list = []

    # iterate over the DataFrame rows (Oracle mapping predictions) and
    # create a Python list of LogMap <MappingObjectStr> Java objects
    for row in accepted.itertuples():

        iri1 = row.source_entity_uri
        iri2 = row.target_entity_uri
        conf = _coerce_confidence_for_java(row.Oracle_confidence, row_index=row.Index)

        # for the relation, get the integer representation recognised by LogMap
        if row.relation not in relation_str_2_int:
            raise ValueError(f'Entity relation {row.relation} not recognised')
        
        relation_int = relation_str_2_int[row.relation]
        
        # for the entityType, get the integer representation recognised by LogMap
        if row.entityType not in entityType_str_2_int:
            raise ValueError(f'Entity type {row.entityType} not recognised')
        
        entityType_int = entityType_str_2_int[row.entityType]

        mos = MappingObjectStr(iri1, iri2, conf, relation_int, entityType_int)
        m_ask_oracle_preds_true.append(mos)
    
    # convert the Python list of <MappingObjectStr> Java objects to a
    # java.util.HashSet of <MappingObjectStr> Java objects
    m_ask_oracle_preds_java = HashSet(m_ask_oracle_preds_true)

    return m_ask_oracle_preds_java

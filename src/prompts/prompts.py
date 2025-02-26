from src.onto_object import OntologyEntryAttr

def prompt_with_hierarchy(src_entety: OntologyEntryAttr, tgt_entety: OntologyEntryAttr) -> str:
    return f"""
    Given two entities from different ontologies with their names, parent relationships, and child relationships, determine if these concepts are the same:

    1. Source Entity:
    All Entity names: {src_entety.get_all_entity_names()}
    Parent Entity Namings: {src_entety.get_parents_preferred_names()}
    Child Entity Namings: {src_entety.get_children_preferred_names()}

    2. Target Entity:
    All Entity names: {tgt_entety.get_all_entity_names()}
    Parent Entity Namings: {tgt_entety.get_parents_preferred_names()}
    Child Entity Namings: {tgt_entety.get_children_preferred_names()}

    Response with True or False
    """  # noqa: E501


def prompt_only_with_parents(src_entety: OntologyEntryAttr, tgt_entety: OntologyEntryAttr) -> str:
    return f"""
    Given two entities from different ontologies with their names and parent relationships, determine if these concepts are the same:

    1. Source Entity:
    All Entity names: {src_entety.get_all_entity_names()}
    Parent Entity Namings: {src_entety.get_parents_preferred_names()}

    2. Target Entity:
    All Entity names: {tgt_entety.get_all_entity_names()}
    Parent Entity Namings: {tgt_entety.get_parents_preferred_names()}

    Response with True or False
    """  # noqa: E501


def prompt_only_names(src_entety: OntologyEntryAttr, tgt_entety: OntologyEntryAttr) -> str:
    return f"""
    Given two entities from different ontologies with their names, determine if these concepts are the same:

    1. Source Entity:
    All Entity names: {src_entety.get_all_entity_names()}

    2. Target Entity:
    All Entity names: {tgt_entety.get_all_entity_names()}

    Response with True or False
    """


def prompt_only_with_children(src_entety: OntologyEntryAttr, tgt_entety: OntologyEntryAttr) -> str:
    return f"""
    Given two entities from different ontologies with their names and child relationships, determine if these concepts are the same:

    1. Source Entity:
    All Entity names: {src_entety.get_all_entity_names()}
    Child Entity Namings: {src_entety.get_children_preferred_names()}

    2. Target Entity:
    All Entity names: {tgt_entety.get_all_entity_names()}
    Child Entity Namings: {tgt_entety.get_children_preferred_names()}

    Response with True or False
    """  # noqa: E501


def prompt_synonyms_subsumption(source_entry: OntologyEntryAttr, target_entry: OntologyEntryAttr) -> str:
    """Create a prompt to determine if one entity's synonyms suggest it subsumes the other."""
    return f"""
    **Task Description:**
    Given two entities with their synonyms, determine if one entity subsumes the other.

    1. **Source Entity Synonyms:** {source_entry.get_synonyms()}
    2. **Target Entity Synonyms:** {target_entry.get_synonyms()}

    Response with True or False
    """


def prompt_one_name_one_synonym(source_entry: OntologyEntryAttr, target_entry: OntologyEntryAttr) -> str:
    """Create a prompt to determine if one entity's synonyms suggest it subsumes the other."""
    return f"""
    **Task Description:**
    Given two entities with their synonyms, determine if one entity subsumes the other.

    1. **Source Entity Synonyms:** {max(list(source_entry.get_synonyms()), key=len)}
    2. **Target Entity Names:** {max(list(target_entry.get_all_entity_names()), key=len)}

    Response with True or False
    """

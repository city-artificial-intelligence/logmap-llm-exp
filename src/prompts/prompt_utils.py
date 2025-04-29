from src.onto_object import OntologyEntryAttr

def get_name_string(name_set):
    """Get a string representation of the name set."""
    # If the name_set is a set or list, join the elements with a comma
    if isinstance(name_set, (set, list)):
        return ", ".join(name_set)
    return str(name_set)

def get_single_name(name_set):
    """Get a single name from the name set."""
    return next(iter(name_set), None) if isinstance(name_set, (set, list)) else name_set

def select_best_direct_entity_names(
    src_entity: OntologyEntryAttr, tgt_entity: OntologyEntryAttr
) -> list[OntologyEntryAttr, OntologyEntryAttr]:
    """If there are multiple direct parents, select one and find child element for it."""

    src_parents = next(iter(src_entity.get_direct_parents()))
    tgt_parents = next(iter(tgt_entity.get_direct_parents()))
    names = [get_name_string(x.get_preffered_names()) if x else None for x in [src_parents, tgt_parents, src_entity, tgt_entity]]

    return names

def format_hierarchy(hierarchy_dict: dict[int, set[OntologyEntryAttr]], no_level: bool = False, add_thing: bool = True) -> str:
    formatted = []
    for level, parents in sorted(hierarchy_dict.items()):
        parent_name = get_name_string([get_name_string(i.get_preffered_names()) for i in parents])

        if not add_thing:
            if parent_name == "Thing":
                continue

        if no_level:
            formatted.append(parent_name)
        else:
            formatted.append(f"\tLevel {level}: {parent_name}")

    if no_level:
        return formatted
    return "\n".join(formatted)

def select_best_direct_entity_names_with_synonyms(src_entity: OntologyEntryAttr, tgt_entity: OntologyEntryAttr, onto_src, onto_tgt, add_thing: bool = True) -> list:
    """Selects preferred names and synonyms for source and target entities and their direct parents."""

    def get_parent_name(entity):
        parent = next(iter(entity.get_direct_parents()), None)
        parent_name = get_name_string(parent.get_preffered_names()) if parent else None
        if parent_name == "Thing" and not add_thing:
            return None
        return parent_name

    def get_clean_synonyms(entity, is_src):
        synonyms = list(entity.get_synonyms())
        if is_src:
            entity_class = str(onto_src.getClassByURI(entity.annotation["uri"])).split('.')[-1]
        else:
            entity_class = str(onto_tgt.getClassByURI(entity.annotation["uri"])).split('.')[-1]
        return [] if len(synonyms) == 1 and synonyms[0] == entity_class else synonyms

    src_parent_name = get_parent_name(src_entity)
    tgt_parent_name = get_parent_name(tgt_entity)

    src_entity_name = get_name_string(src_entity.get_preffered_names())
    tgt_entity_name = get_name_string(tgt_entity.get_preffered_names())

    src_synonyms = get_clean_synonyms(src_entity, True)
    tgt_synonyms = get_clean_synonyms(tgt_entity, False)

    return [
        src_parent_name,  # string
        tgt_parent_name,  # string
        src_entity_name,  # string
        tgt_entity_name,  # string
        src_synonyms,     # list of strings
        tgt_synonyms      # list of strings
    ]


def select_best_sequential_hierarchy_with_synonyms(src_parents_by_levels, tgt_parents_by_levels, onto_src, onto_tgt):
    """Selects the best synonyms for an entity and its hierarchical parents."""
    def get_synonyms_and_class(parents_by_levels, idx, is_src):
        if len(parents_by_levels) > idx:
            entry = next(iter(parents_by_levels[idx]))
            syns = entry.get_synonyms() if hasattr(entry, "get_synonyms") else []

            if is_src:
                cls = str(onto_src.getClassByURI(entry.annotation["uri"])).split('.')[-1]
            else:
                cls = str(onto_tgt.getClassByURI(entry.annotation["uri"])).split('.')[-1]

            return syns, cls
        return [], ""

    def clean(synonyms, cls):
        return [] if len(synonyms) == 1 and next(iter(synonyms)) == cls else synonyms

    src_results = [get_synonyms_and_class(src_parents_by_levels, i, True) for i in range(len(src_parents_by_levels))]
    tgt_results = [get_synonyms_and_class(tgt_parents_by_levels, i, False) for i in range(len(tgt_parents_by_levels))]

    src_cleaned = [clean(syns, cls) for syns, cls in src_results]
    tgt_cleaned = [clean(syns, cls) for syns, cls in tgt_results]

    return src_cleaned + tgt_cleaned

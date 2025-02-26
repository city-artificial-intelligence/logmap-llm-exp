import pandas as pd
from pprint import pprint
from src.onto_object import OntologyEntryAttr


def print_results_entry(res_df:pd.DataFrame, onto_tgt, onto_src, pair_type:str="FP", idx:int=0) -> None:
    source_uri = res_df[res_df["Type"] == pair_type].iloc[idx]["Source"]
    target_uri = res_df[res_df["Type"] == pair_type].iloc[idx]["Target"]

    try:
        source_entry = OntologyEntryAttr(source_uri, onto_src)
        target_entry = OntologyEntryAttr(target_uri, onto_tgt)
    except Exception:
        source_entry = OntologyEntryAttr(source_uri, onto_tgt)
        target_entry = OntologyEntryAttr(target_uri, onto_src)

    print(f"Processing pair {idx} of type {pair_type}")
    pprint("Source Entry:\n")
    pprint(source_entry.annotation)
    pprint("Target Entry:\n")
    pprint(target_entry.annotation)

    print(f"Parent of Source Concept: {source_entry.get_parents_preferred_names()}")
    print(f"Parent of Target Concept: {target_entry.get_parents_preferred_names()}")
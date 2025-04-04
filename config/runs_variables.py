DATASET_SUBSETS_MAP = {
    "bioml-2024": {"ncit-doid", "omim-ordo", "snomed-fma.body", "snomed-ncit.neoplas", "snomed-ncit.pharm"},
    "largebio": {"fma-nci", "fma-snomed", "snomed-nci"},
    "anatomy": {"human-mouse"},
}

SUBSET_TO_DATASET_MAP = {
    set_name: dataset_name for dataset_name, set_names in DATASET_SUBSETS_MAP.items() for set_name in set_names
}

RUNS_METADATA = [
    ("2025-04-04_19-41-28", "gemini-2.0-flash", "human-mouse", "anatomy"),
    ("2025-04-04_19-23-47", "gemini-2.0-flash-lite", "human-mouse", "anatomy"),
    ("2025-04-04_00-43-16", "gemini-2.0-flash-lite", "human-mouse", "anatomy"),
    ("2025-03-28_10-56-40", "gpt-4o-mini", "fma-snomed", "largebio"),
    ("2025-03-28_10-15-04", "gpt-4o-mini", "fma-nci", "largebio"),
    ("2025-03-19_23-32-20", "gpt-4o-mini", "omim-ordo", "bioml-2024"),
    ("2025-03-19_22-17-52", "gpt-4o-mini", "ncit-doid", "bioml-2024"),
    ("2025-03-19_19-48-41", "gpt-4o-mini", "human-mouse", "anatomy"),
    ("2025-03-14_00-40-55", "gpt-4o-mini", "ncit-doid", "bioml-2024"),
    ("2025-03-12_17-21-53", "gpt-4o-mini", "human-mouse", "anatomy"),
    ("2025-03-12_14-43-32", "gpt-4o-mini", "omim-ordo", "bioml-2024"),
]

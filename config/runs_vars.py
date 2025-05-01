DATASET_SUBSETS_MAP = {
    "bioml-2024": {"ncit-doid", "omim-ordo", "snomed-fma.body", "snomed-ncit.neoplas", "snomed-ncit.pharm"},
    "largebio": {"fma-nci", "fma-snomed", "snomed-nci"},
    "anatomy": {"human-mouse", "mouse-human"},
}

SUBSET_TO_DATASET_MAP = {
    set_name: dataset_name for dataset_name, set_names in DATASET_SUBSETS_MAP.items() for set_name in set_names
}

PROMPT_EXPERIMENTS = [
    "direct_entity",
    "direct_entity_ontological",
    "sequential_hierarchy",
    "sequential_hierarchy_ontological",
    "direct_entity_with_synonyms",
    "sequential_hierarchy_with_synonyms",
]

RUNS_METADATA = [
    ('2025-05-01_11-47-16', 'gemini-2.0-flash', 'snomed-nci', 'largebio'),
    ('2025-05-01_11-37-30', 'gemini-2.0-flash-lite', 'snomed-nci', 'largebio'),
    ('2025-05-01_11-24-31', 'gemini-2.0-flash', 'fma-snomed', 'largebio'),
    ('2025-05-01_11-19-48', 'gemini-2.0-flash-lite', 'fma-snomed', 'largebio'),
    ('2025-05-01_11-15-05', 'gemini-2.0-flash', 'snomed-ncit.pharm', 'bioml-2024'),
    ('2025-05-01_11-12-35', 'gemini-2.0-flash-lite', 'snomed-ncit.pharm', 'bioml-2024'),
    ('2025-05-01_11-07-00', 'gemini-2.0-flash', 'snomed-ncit.neoplas', 'bioml-2024'),
    ('2025-05-01_11-06-39', 'gemini-2.0-flash-lite', 'snomed-ncit.neoplas', 'bioml-2024'),
    ('2025-05-01_10-56-46', 'gemini-2.0-flash', 'snomed-fma.body', 'bioml-2024'),
    ('2025-05-01_10-50-33', 'gemini-2.0-flash-lite', 'snomed-fma.body', 'bioml-2024'),
    ('2025-05-01_10-13-02', 'gemini-2.0-flash-lite', 'fma-snomed', 'largebio'),
    ('2025-04-10_22-11-36', 'gemini-2.0-flash', 'ncit-doid', 'bioml-2024'),
    ('2025-04-10_00-33-19', 'gemini-2.0-flash-lite', 'ncit-doid', 'bioml-2024'),
    ('2025-04-06_22-05-02', 'gemini-2.0-flash-lite', 'omim-ordo', 'bioml-2024'),
    ('2025-04-06_19-27-41', 'gemini-2.0-flash', 'omim-ordo', 'bioml-2024'),
    ('2025-04-06_14-51-00', 'gemini-2.0-flash-lite', 'fma-nci', 'largebio'),
    ('2025-04-06_14-18-46', 'gemini-2.0-flash', 'fma-nci', 'largebio'),
    ('2025-04-04_19-41-28', 'gemini-2.0-flash', 'human-mouse', 'anatomy'),
    ('2025-04-04_19-23-47', 'gemini-2.0-flash-lite', 'human-mouse', 'anatomy'),
    ('2025-04-04_00-43-16', 'gemini-2.0-flash', 'fma-snomed', 'largebio'),
    ('2025-03-28_10-15-04', 'gpt-4o-mini', 'fma-nci', 'largebio'),
    ('2025-03-19_23-32-20', 'gpt-4o-mini', 'omim-ordo', 'bioml-2024'),
    ('2025-03-19_22-17-52', 'gpt-4o-mini', 'ncit-doid', 'bioml-2024'),
    ('2025-03-19_19-48-41', 'gpt-4o-mini', 'human-mouse', 'anatomy'),
    ('2025-03-14_00-40-55', 'gpt-4o-mini', 'ncit-doid', 'bioml-2024'),
    ('2025-03-12_17-21-53', 'gpt-4o-mini', 'human-mouse', 'anatomy'),
    ('2025-03-12_14-43-32', 'gpt-4o-mini', 'omim-ordo', 'bioml-2024')
 ]
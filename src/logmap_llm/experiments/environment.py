"""
logmap_llm.experiments.environment

The resolved Python environment a batch was generated in, as a deterministic payload.

WHY THIS IS IN THE PACKAGE

``source_digest()`` hashes only ``*.py`` under ``logmap_llm``, so ``core_sha256`` identifies
the LogMap-LLM source and nothing else. The Java matcher *is* bound, through
``input_fingerprints["alignmentTask.logmap_parameters_dirpath"]``. What was not bound is the
Python dependency set: two runs with an identical ``core_sha256`` may have used different
``torch``, ``transformers``, ``numpy`` or ``owlready2``. The drift is real — the checked-in
runtime-RAG figures were rendered under Matplotlib 3.11.0 while ``uv.lock`` pinned 3.11.1.

``campaign/record_environment.py`` recorded this *beside* a campaign as advisory provenance
because binding it required editing ``src/``. This bump does that edit, so the payload moves
here and the campaign tool imports it — ``plan.py`` cannot import from ``campaign/``, so
"reuse it rather than reimplementing" has to run in this direction.

WHAT IT IS AND IS NOT

It is an OPTIONAL top-level manifest key, covered by the seal, so it cannot be edited after
generation. It is **not** part of run identity: ``condition_id``, ``execution_hash``,
``_job_id``, ``_alignment_id`` and ``plan_hash`` are built from explicit dicts that never see
the manifest's top level, and deliberately so — two hosts running the same campaign must
produce the same job identities even though their virtualenvs differ. Comparisons across
hosts therefore compare manifests *modulo* ``environment`` and ``seal``.
"""
from __future__ import annotations

import platform
from importlib import metadata
from pathlib import Path
from typing import Any

#: Packages whose version can plausibly change a *result*: the encoders and their runtime,
#: the ontology and RDF layers, the oracle transport and its validation, the numeric and
#: dataframe layer, and the figure renderer. Deliberately fixed and sorted so the payload is
#: stable and reviewable rather than a full freeze of the virtualenv.
TRACKED_PACKAGES = (
    "JPype1",
    "matplotlib",
    "numpy",
    "openai",
    "owlready2",
    "pandas",
    "pydantic",
    "rdflib",
    "torch",
    "transformers",
)

SCHEMA_VERSION = 1


def resolved_packages() -> dict[str, str]:
    """Installed versions for the tracked names; absent packages are omitted.

    A missing package is normal — the ``rag`` extra is optional — and is never an error.
    ``importlib.metadata`` normalises distribution names, so ``JPype1`` and ``jpype1``
    resolve identically.
    """
    versions: dict[str, str] = {}
    for name in sorted(TRACKED_PACKAGES):
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            continue
    return versions


def environment_payload(repo: Path | None = None) -> dict[str, Any]:
    """The deterministic environment record embedded in a sealed manifest."""
    record: dict[str, Any] = {
        "schema": SCHEMA_VERSION,
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "packages": resolved_packages(),
    }
    if repo is not None:
        lock = Path(repo) / "uv.lock"
        if lock.is_file():
            import hashlib

            digest = hashlib.sha256()
            with lock.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1 << 20), b""):
                    digest.update(chunk)
            record["uv_lock_sha256"] = digest.hexdigest()
    return record


def environments_differ(left: Any, right: Any) -> list[str]:
    """Names of tracked packages whose versions differ, for a legible operator message."""
    left_packages = (left or {}).get("packages", {}) if isinstance(left, dict) else {}
    right_packages = (right or {}).get("packages", {}) if isinstance(right, dict) else {}
    names = set(left_packages) | set(right_packages)
    return sorted(
        name for name in names if left_packages.get(name) != right_packages.get(name)
    )

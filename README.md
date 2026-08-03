# logmap-llm-exp

LogMapLLM experimental.

## LogMapLLM

LogMapLLM is a research codebase that extends the [LogMap](https://github.com/ernestojimenezruiz/logmap-matcher) ontology-matching system with an LLM oracle. LogMap can ask a human oracle about the mappings it is unsure of; here that role is played by a language model reached over any OpenAI-compatible API (OpenRouter, vLLM, SGLang, OpenAI), with everything around it — prompt construction, few-shot retrieval, refinement, evaluation, batch experiments.

## The idea

A classical LogMap run (Java, driven from Python via JPype) produces (i) an initial alignment between the source and target ontologies, and (ii) a subset of candidate mappings it considers uncertain (the "mappings to ask" the oracle), written here as $M_{ask}$. For each candidate in $M_{ask}$ the pipeline renders a natural-language question grounded in ontology context (labels, synonyms, parents, siblings, domain and range, instance attributes), optionally prepends retrieved few-shot demonstrations, and asks the LLM for a True/False (or Yes/No; structured/unstructured) verdict on whether the two entities match.

The verdicts are then folded back into the alignment: 

$refined_{pre-repair} = (initial − M_{ask}) \cup \left\lbrace\ m \in M_{ask} : oracle(m) = True\ \right\rbrace,$

either through LogMap's own Java refinement (which also resolves logical conflicts). The refined alignment can finally be scored against a reference, including OAEI Knowledge Graph track semantics for partial gold standards, and every successful run publishes a machine-readable `run_result.json` recording parameters, counts, timings and sha256 artifact hashes.

## Usage

```sh
python -m logmap_llm --config path/to/config.toml
```

with a config like:

```toml
[alignmentTask]
task_name = "mouse-human"
onto_source_filepath = "data/mouse.owl"
onto_target_filepath = "data/human.owl"

[oracle]
model_name = "qwen/qwen3-32b"
api_key = "ENV:OPENROUTER_API_KEY"    # or "EMPTY" for a local vLLM/SGLang server

[outputs]
logmapllm_output_dirpath = "output/logmapllm"
logmap_initial_alignment_output_dirpath = "output/initial-alignment"
logmap_refined_alignment_output_dirpath = "output/refined-alignment"

# optional: score the refined alignment against a reference
[evaluation]
evaluate = true
reference_alignment_path = "data/reference.rdf"
```

The config is a TOML file validated by a strict Pydantic schema; at minimum it needs `[alignmentTask]` (task name and the two ontology paths), `[oracle]` (model name), and `[outputs]` (three output directories). You also need a LogMap bundle on disk (`logmap-matcher-4.0.jar`, `java-dependencies/`, `parameters.txt`), found under `./logmap` by default or wherever `alignmentTask.logmap_parameters_dirpath` points. 

The CLI flags:

- `--config PATH` (or `-c`) — the TOML configuration file; defaults to `configs/default_config.toml`.
- `--reuse-align` — reuse an existing LogMap alignment instead of re-running the matcher.
- `--reuse-prompts` — reuse previously built oracle prompts; implies `--reuse-align`.
- `--no-cache` — disable owlready2 quadstore caching and parse the ontologies from scratch.
- `--run-root DIR` — root all outputs under `DIR`, creating `logmapllm-outputs`, `logmap-initial-alignment` and `logmap-refined-alignment` subdirectories.

The run executes five phases in order — align, prompt build, oracle consultation, refinement, evaluation — followed by reporting. Prompt building and evaluation each run in their own subprocess: owlready2 cannot coexist with JPype in one process, and the DeepOnto evaluator needs its own JVM.

## License

[Apache License 2.0](./LICENSE)
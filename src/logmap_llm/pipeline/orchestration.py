"""
logmap_llm.pipeline.orchestration

Ported from jd-extended, see:

    https://github.com/jonathondilworth/logmap-llm/blob/jd-extended/pipeline_steps.py

With some modifications (ready for future branches/features).
"""
from __future__ import annotations

import sys
import os
import subprocess
import json
import pandas as pd
import numpy as np

from logmap_llm.pipeline.context import PipelineContext
from logmap_llm.pipeline.contracts import (
    AlignmentResult,
    PromptBuildResult,
    OracleResult,
    RefinementResult,
    EvaluationResult,
)
from logmap_llm.constants import (
    AlignMode,
    PromptBuildMode,
    ConsultMode,
    RefineMode,
    RefinementStrategy,
    PAIRS_SEPARATOR,
    COL_SOURCE_ENTITY_URI,
    COL_TARGET_ENTITY_URI,
    COL_RELATION,
    COL_CONFIDENCE,
    COL_ENTITY_TYPE,
    DEFAULT_CONFIDENCE_FALLBACK,
)
from logmap_llm.utils.data import (
    normalise_prediction_column,
    filter_accepted_predictions,
)
from logmap_llm.utils.io import atomic_json_write_strict, atomic_write_text_strict
from logmap_llm.utils.logging import (
    fatal,
    critical,
    warning,
    warn,
    step,
    success,
)



# NOTE: Do NOT import oracle_prompt_building or onto_access here.
# Those modules transitively import owlready2, which cannot coexist
# with JPype in the same process.  Prompt building runs in a subprocess.



# PRIVATE HELPERS
#################

def _subprocess_context_args(ctx: PipelineContext) -> list[str]:
    """Arguments that keep child processes in the parent's run namespace."""
    args: list[str] = []
    if ctx.run_paths.run_root is not None:
        args.extend(["--run-root", str(ctx.run_paths.run_root)])
    if ctx.no_cache:
        args.append("--no-cache")
    return args




def _detect_bidirectional(prompts: dict) -> bool:
    """
    Detect whether prompts were built in bidirectional mode; bidirectional prompt keys 
    have a direction suffix, specifically: 'src_uri|tgt_uri|REVERSE', whereas standard
    keys are just: 'src_uri|tgt_uri'
    """
    if not prompts:
        return False
    return any(key.count(PAIRS_SEPARATOR) >= 2 for key in prompts)


def _configured_oracle_params(oracle_cfg, capabilities: dict | None = None) -> dict:
    """Serializable inference controls, including no-candidate consultations."""
    capabilities = capabilities or {}
    return {
        "model_name": oracle_cfg.model_name,
        "interaction_style": oracle_cfg.interaction_style,
        "temperature": oracle_cfg.temperature,
        "top_p": oracle_cfg.top_p,
        "max_completion_tokens": oracle_cfg.max_completion_tokens,
        "reasoning_effort": oracle_cfg.reasoning_effort,
        "reasoning_token_budget": oracle_cfg.reasoning_token_budget,
        "enable_thinking": oracle_cfg.enable_thinking,
        "max_workers": oracle_cfg.max_workers,
        "answer_format": oracle_cfg.answer_format,
        "response_mode": oracle_cfg.response_mode,
        "request_timeout_seconds": oracle_cfg.request_timeout_seconds,
        "connect_timeout_seconds": oracle_cfg.connect_timeout_seconds,
        "transient_retries": oracle_cfg.transient_retries,
        "seed": oracle_cfg.seed,
        "request_logprobs": oracle_cfg.request_logprobs,
        "openrouter_provider": oracle_cfg.openrouter_provider,
        "openrouter_allow_fallbacks": oracle_cfg.openrouter_allow_fallbacks,
        "openrouter_require_parameters": oracle_cfg.openrouter_require_parameters,
        "logprobs_requested": capabilities.get(
            "logprobs_requested", oracle_cfg.request_logprobs
        ),
        "logprobs_effective": capabilities.get(
            "logprobs_effective", oracle_cfg.request_logprobs
        ),
        "capability_downgrades": capabilities.get("downgrades", []),
    }



def _validate_prompt_keys(prompts: dict, bidirectional: bool, template_name: str = "") -> None:
    """
    Validates that the prompt key format matches the consultation mode.
    """
    if not prompts:
        return
    
    keys_have_direction = _detect_bidirectional(prompts)
    
    if bidirectional and not keys_have_direction:
        raise ValueError(
            f"Bidirectional template '{template_name}' selected but prompts   "
            f"lack direction keys (eg. '...|REVERSE'). The prompt JSON was    "
            f"likely built with a non-bidirectional template. Rebuild prompts "
            f"or select a matching template."
        )
    if not bidirectional and keys_have_direction:
        raise ValueError(
            f"Standard template '{template_name}' selected but prompts have  "
            f"direction keys (eg. '...|REVERSE'). The prompt JSON was likely "
            f"built with a bidirectional template. Rebuild prompts or select "
            f"a matching template."
        )



def _load_few_shot_artifact(
    path,
    *,
    few_shot_cfg,
    oracle_cfg,
    expected_query_keys,
):
    """Load few-shot JSON, revalidating strict prebuilt handoffs before inference."""
    with open(path, encoding="utf-8") as stream:
        loaded = json.load(stream)

    if few_shot_cfg.prebuilt_few_shot_bundle_path is not None:
        # Stage two is a subprocess. Revalidate its persisted handoff in this
        # consumer process so a stale or modified artifact cannot become a
        # shared prefix or silently drop one query to zero-shot.
        from logmap_llm.pipeline.rag_fewshot import (
            validate_prebuilt_few_shot_examples,
        )

        validate_prebuilt_few_shot_examples(
            loaded,
            expected_query_keys=expected_query_keys,
            k=few_shot_cfg.few_shot_k,
            answer_format=oracle_cfg.answer_format,
            response_mode=oracle_cfg.response_mode,
        )

    if isinstance(loaded, dict):
        if few_shot_cfg.prebuilt_few_shot_bundle_path is None:
            # BUGFIX (FS-COVERAGE): the ordinary stage-two dict artifact needs the SAME
            # key-coverage guarantee the prebuilt revalidation above provides. Without it,
            # the {} sentinel that _handle_rag_generation_failure / the k=0 branch persist
            # (stage_two.py) survives a --reuse-prompts retry: an empty dict is falsy, so
            # consultation passes few_shot_examples=None for EVERY query and a few_shot_k>0
            # run silently executes zero-shot while being sealed as 'succeeded' under the
            # requested condition. A partial dict likewise drops individual queries to
            # zero-shot via per_query_examples.get(key). stage_two always writes one entry
            # per prompt key (zero-shot fallbacks keep their key with an empty pair list),
            # so exact coverage is the invariant of a fresh, matching artifact.
            expected = {str(key) for key in expected_query_keys}
            actual = {str(key) for key in loaded}
            if actual != expected:
                missing = sorted(expected - actual)
                extra = sorted(actual - expected)
                raise ValueError(
                    "Few-shot artifact keys do not cover the prompt keys — the artifact is "
                    "stale for this configuration (e.g. left over from a k=0 run or a failed "
                    "RAG generation under --reuse-prompts); rebuild prompts to regenerate it "
                    f"(missing={missing[:5]!r}, extra={extra[:5]!r})"
                )
        return {
            key: [tuple(pair) for pair in pairs]
            for key, pairs in loaded.items()
        }
    if isinstance(loaded, list):
        if not loaded:
            raise ValueError(
                "Few-shot artifact is an empty list while few_shot_k > 0; refusing to run "
                "the condition as an undeclared zero-shot baseline. Rebuild prompts to "
                "regenerate the artifact."
            )
        return [tuple(pair) for pair in loaded]
    raise ValueError("Few-shot artifact must contain a JSON object or list")


def _resolve_accepted_confidences(accepted_subset: pd.DataFrame, oracle_accepted: pd.DataFrame, retain_logprobs_conf: bool) -> np.ndarray | None:
    """
    Return logprobs-derived confidences to overwrite LogMap; 
    or None to keep LogMap confidence.
    """
    if not retain_logprobs_conf:
        return None
    
    if COL_CONFIDENCE not in accepted_subset.columns:
        warn(f"retain_logprobs_conf=True but '{COL_CONFIDENCE}' absent from initial alignment; keeping LogMap confidences.")
        return None
    
    if "Oracle_confidence" not in oracle_accepted.columns:
        warn("retain_logprobs_conf=True but 'Oracle_confidence' absent from oracle predictions; keeping LogMap confidences.")
        return None
    
    raw = oracle_accepted["Oracle_confidence"].to_numpy()
    return np.where(np.isfinite(raw), raw, DEFAULT_CONFIDENCE_FALLBACK)



def _kg_refine_in_python(ctx: PipelineContext, oracle_result: OracleResult, retain_logprobs_conf: bool = False) -> None:
    r"""
    Produce refined alignment for KG track in Python.

    Computes: refined = { initial - M_ask } U { m \in M_ask : oracle(m) = True }

    Prior to patching, LogMap's Java refinement crashes with NullPointerExceptions for instance matching.
    Additionally, the alignment stage does take a while (eg. when a KG has > 1m instances); this can be
    offset through by-passing the initial aligning (with --reuse-align). However, the refinement stage 
    (similarly) takes a long time; as such, this provides an optional means to quickly calculate an
    approximation to what the refinement ought to look like, but lacks final conflict resolution.
    Though, for KGs and instance matching, I am not sure how impactful the conflict resolution is 
    anyway; since LogMap was not originally designed for this specific use case.

    NOTE: since patching LogMap, the new build appears to work as intended.

    TODO: _kg_refine_in_python should handle both pipe and tab separators, or use the same format detection 
    logic as evaluate.py (updated note -- 14th April -- can't quite recall what this TODO was for, exactly;
    revisit later).

    NOTE: setting retain_logprobs_conf = True will overwrite the LogMap confidence with the LogProbs confidence
    """
    # load initial alignment
    initial_path = ctx.run_paths.logmap_mappings()
    initial_df = pd.read_csv(initial_path, sep=PAIRS_SEPARATOR, header=None)
    initial_df.columns = [
        COL_SOURCE_ENTITY_URI,
        COL_TARGET_ENTITY_URI,
        COL_RELATION,
        COL_CONFIDENCE,
        COL_ENTITY_TYPE
    ][:len(initial_df.columns)]

    # build set of m_ask pairs
    preds = oracle_result.predictions
    m_ask_pairs = set()

    # reference the URI columns BY NAME when available (robust to any stray index column that
    # slipped past the REUSE normaliser); fall back to positional order otherwise (refine-bridge-1).
    _src_col = COL_SOURCE_ENTITY_URI if COL_SOURCE_ENTITY_URI in preds.columns else preds.columns[0]
    _tgt_col = COL_TARGET_ENTITY_URI if COL_TARGET_ENTITY_URI in preds.columns else preds.columns[1]

    for _, row in preds.iterrows():
        m_ask_pairs.add((str(row[_src_col]), str(row[_tgt_col])))

    # retain rows disjoint from m_ask (ie. the initial mapping)
    keep_mask = initial_df.apply(
        lambda row: (str(row.iloc[0]), str(row.iloc[1])) not in m_ask_pairs,
        axis=1
    )
    retained = initial_df[keep_mask]

    # m_ask entries where oracle predicted true
    oracle_accepted = filter_accepted_predictions(preds)

    # take the first N columns matching the initial alignment format (combine)
    ncols = len(initial_df.columns)
    accepted_subset = oracle_accepted.iloc[:, :ncols].copy()
    accepted_subset.columns = initial_df.columns

    # logprob confidence override (patch April 19th):
    resolved = _resolve_accepted_confidences(
        accepted_subset, 
        oracle_accepted, retain_logprobs_conf
    )
    if resolved is not None:
        accepted_subset[COL_CONFIDENCE] = resolved

    refined = pd.concat([retained, accepted_subset], ignore_index=True)

    # write to the refined output directory (atomically: a crash mid-write must not leave
    # a truncated TSV that validate_run_artifacts and the evaluation harness would accept)
    output_path = ctx.run_paths.refined_mappings_tsv()
    os.makedirs(ctx.run_paths.refined_dir, exist_ok=True)
    atomic_write_text_strict(
        output_path, lambda fp: refined.to_csv(fp, sep='\t', header=False, index=False)
    )
    conf_source = "logprobs" if resolved is not None else "logmap"

    step(f"[Step 4] KG refined alignment: {len(refined)} mappings "
        f"({len(retained)} retained + {len(accepted_subset)} oracle-accepted, "
        f"accepted-subset confidence source: {conf_source})")


###
# END: PRIVATE HELPERS; START: PIPELINE FNS
# align -> prompt_build -> consult_oracle -> refine_alignment -> evaluate
###



def align(ctx: PipelineContext) -> AlignmentResult:
    """
    Step 1: Pass the neccesary files to LogMap to perform an initial alignment and get M_ask.
    `import bridging as br` allows for mapping LogMap IO between java and python (and vice versa)
    """
    import logmap_llm.bridging as br

    step("[Step 1] Align ontologies and obtain mappings to ask an Oracle")

    match ctx.cfg.pipeline.align_ontologies:

        case AlignMode.ALIGN:

            step("[Step 1] Performing fresh initial LogMap alignment")
            if ctx.logmap is None:
                fatal("Fresh alignment requires an initialized LogMap JVM")
            logmap = ctx.logmap
            logmap.perform_alignment()
            return AlignmentResult(
                m_ask_df=br.java_mappings_2_python(
                    logmap.get_mappings_for_llm(),
                    dedupe_uri_pairs=True,
                ),
                mappings=br.java_mappings_2_python(
                    logmap.get_mappings()
                ),
            )

        case AlignMode.REUSE:

            step(f"[Step 1] Loading mappings from file: {ctx.run_paths.logmap_m_ask()}")
            try:
                mappings = pd.read_csv(
                    ctx.run_paths.logmap_mappings(),
                    sep=PAIRS_SEPARATOR,
                    header=None,
                )
            except pd.errors.EmptyDataError:
                mappings = pd.DataFrame(columns=range(5))
            return AlignmentResult(
                m_ask_df=br.load_m_ask_from_file(
                    ctx.run_paths.logmap_m_ask()
                ),
                mappings=mappings,
            )

        case AlignMode.BYPASS:
            warn("Bypassing initial LogMap alignment")
            return AlignmentResult()

        case _:
            fatal(f"config: align_ontologies param not recognised: {ctx.cfg.pipeline.align_ontologies}")

    fatal(f"unable to match on: {ctx.cfg.pipeline.align_ontologies}")



def prompt_build(ctx: PipelineContext, initial_alignment: AlignmentResult) -> PromptBuildResult:
    """
    Step 2: Build user prompts for oracle consultation.
    In BUILD mode, dispatches to pipeline/stage_two.py as a subprocess (isolates JVMs & owlready2).
    """
    step("\n[Step 2] Build user prompts for oracle consultation")

    match ctx.cfg.pipeline.build_oracle_prompts:

        case PromptBuildMode.BUILD:
            
            step("[Step 2] Building fresh oracle user prompts via subprocess")
            
            if not ctx.config_path:
                fatal("Stage 2 in BUILD mode without a valid config path.") # @raises

            prompts_path = ctx.run_paths.prompts_json()
            prompts_path.unlink(missing_ok=True)

            cmd = [
                sys.executable, "-m", "logmap_llm.pipeline.stage_two",
                "--config", ctx.config_path,
                *_subprocess_context_args(ctx),
            ]

            proc = subprocess.run(cmd, capture_output=False)
            if proc.returncode != 0:
                fatal(f"Stage 2 subprocess failed with return code {proc.returncode}") # @raises

            # read the prompts back from the JSON file
            if not prompts_path.exists():
                if initial_alignment.n_m_ask == 0:
                    atomic_json_write_strict(prompts_path, {})
                    if ctx.cfg.few_shot.few_shot_k > 0:
                        atomic_json_write_strict(ctx.run_paths.few_shot_json(), {})
                else:
                    fatal(
                        f"Stage 2 succeeded but did not publish required prompts: {prompts_path}",
                        FileNotFoundError,
                    )
            
            with open(prompts_path) as fp:
                prompts = json.load(fp)
            if not isinstance(prompts, dict):
                fatal(f"Prompts artifact must contain a JSON object: {prompts_path}")
            if initial_alignment.n_m_ask > 0 and not prompts:
                fatal(
                    "Stage 2 produced zero prompts for a non-empty M_ask; refusing to "
                    "continue with an undeclared baseline fallback."
                )
            
            bidirectional = _detect_bidirectional(prompts)
            return PromptBuildResult(
                prompts=prompts,
                bidirectional=bidirectional,
            )

        case PromptBuildMode.REUSE:

            step(f"[Step 2] Loading LLM oracle user prompts from: {ctx.run_paths.prompts_json()}")

            with open(ctx.run_paths.prompts_json()) as fp:
                prompts = json.load(fp)
            if not isinstance(prompts, dict):
                fatal(
                    f"Prompts artifact must contain a JSON object: {ctx.run_paths.prompts_json()}"
                )
            if initial_alignment.n_m_ask > 0 and not prompts:
                fatal("Cannot reuse an empty prompts artifact for a non-empty M_ask")

            bidirectional = _detect_bidirectional(prompts)

            _validate_prompt_keys(
                prompts, bidirectional,
                template_name=ctx.cfg.prompts.cls_usr_prompt_template_name,
            )
            return PromptBuildResult(
                prompts=prompts,
                bidirectional=bidirectional,
            )

        case PromptBuildMode.BYPASS:

            warn("Bypassing use of LLM oracle user prompts")
            return PromptBuildResult()

        case _:
            fatal(f"config: build_oracle_prompts param not recognised: {ctx.cfg.pipeline.build_oracle_prompts}")    

    fatal(f"unable to match on: {ctx.cfg.pipeline.build_oracle_prompts}")



def consult_oracle(ctx: PipelineContext, initial_alignment: AlignmentResult, prompt_build_result: PromptBuildResult) -> OracleResult:
    """
    Step 3: Consult Oracle for mappings to ask.
    """
    import logmap_llm.oracle.prompts.developer as dp
    import logmap_llm.oracle.consultation as oc

    step("\n[Step 3] Consult Oracle for mappings to ask")
    
    ###
    # CLS PROMPT
    ###

    developer_prompt_map = {}

    cls_dev_prompt_text = dp.get_developer_prompt(
        name=ctx.cfg.prompts.cls_dev_prompt_template_name,
        answer_format=ctx.cfg.oracle.answer_format,
        response_mode=ctx.cfg.oracle.response_mode,
    )

    ###
    # PROPERTY PROMPT: templates will morph to accomodate both data and object properties
    ###

    prop_dev_prompt_text = None
    if (
        ctx.cfg.prompts.prop_usr_prompt_template_name
        or ctx.cfg.prompts.dprop_usr_prompt_template_name
    ):
        prop_dev_prompt_text = dp.get_developer_prompt(
            ctx.cfg.prompts.prop_dev_prompt_template_name,
            answer_format=ctx.cfg.oracle.answer_format,
            response_mode=ctx.cfg.oracle.response_mode,
        )
        if ctx.cfg.prompts.prop_usr_prompt_template_name:
            developer_prompt_map["OPROP"] = prop_dev_prompt_text
        developer_prompt_map["DPROP"] = prop_dev_prompt_text

    ###
    # INSTANCE PROMPT
    ###

    inst_dev_prompt_text = None
    if ctx.cfg.prompts.inst_usr_prompt_template_name:
        inst_dev_prompt_text = dp.get_developer_prompt(
            ctx.cfg.prompts.inst_dev_prompt_template_name,
            answer_format=ctx.cfg.oracle.answer_format,
            response_mode=ctx.cfg.oracle.response_mode,
        )
        developer_prompt_map["INST"] = inst_dev_prompt_text

    if len(developer_prompt_map.keys()) == 0:
        developer_prompt_map = None

    ###
    # SWITCH ON CONSULT MODE (SPECIFIED IN CONFIG)
    ###

    match ctx.cfg.pipeline.consult_oracle:

        case ConsultMode.CONSULT:
            
            if prompt_build_result.prompts is None or len(prompt_build_result.prompts) == 0:
                if initial_alignment.n_m_ask > 0:
                    fatal(
                        "No prompts are available for a non-empty M_ask; refusing to "
                        "silently treat the condition as a zero-consultation baseline."
                    )
                warn("[Step 3] M_ask is empty — publishing an explicit empty predictions artifact")
                empty_predictions = initial_alignment.m_ask_df.copy()
                empty_predictions["Oracle_prediction"] = pd.Series(dtype="object")
                empty_predictions["Oracle_confidence"] = pd.Series(dtype="float64")
                empty_predictions["Oracle_input_tokens"] = pd.Series(dtype="Int64")
                empty_predictions["Oracle_output_tokens"] = pd.Series(dtype="Int64")
                atomic_write_text_strict(
                    ctx.run_paths.predictions_csv(),
                    lambda fp: empty_predictions.to_csv(fp, na_rep="nan", index=False),
                )
                return OracleResult(
                    predictions=empty_predictions,
                    oracle_params=_configured_oracle_params(ctx.cfg.oracle),
                )
            
            # else: check few-shot configuration
            few_shot_examples = None
            if ctx.cfg.few_shot.few_shot_k > 0:
                few_shot_fp = ctx.run_paths.few_shot_json()
                
                if os.path.isfile(few_shot_fp):
                    few_shot_examples = _load_few_shot_artifact(
                        few_shot_fp,
                        few_shot_cfg=ctx.cfg.few_shot,
                        oracle_cfg=ctx.cfg.oracle,
                        expected_query_keys=prompt_build_result.prompts,
                    )
                    # RAG (spec §6): stage_two now writes a DICT {m_ask_key -> [[user,assistant], ...]}
                    # (query-specific few-shot). Legacy static few-shot is a flat LIST of pairs. A dict is
                    # dispatched per-consultation; a list is the shared frozen prefix.
                    if isinstance(few_shot_examples, dict):
                        success(f"Loaded query-specific few-shot for {len(few_shot_examples)} M_ask keys from {few_shot_fp}")
                    else:
                        success(f"Loaded {len(few_shot_examples)} (shared) few-shot examples from {few_shot_fp}")
                
                else: # failed to find few-shot file
                    fatal(
                        f"few_shot_k={ctx.cfg.few_shot.few_shot_k} but the required "
                        f"few-shot artifact is missing: {few_shot_fp}",
                        FileNotFoundError,
                    )
                
            # END: FEW-SHOT-HANDLER

            ###
            # EXECUTE CONSULTATION
            ###

            ctx.run_paths.predictions_csv().unlink(missing_ok=True)

            oracle_kwargs = dict(
                m_ask_prompts=prompt_build_result.prompts,
                m_ask_init_alignment_df=initial_alignment.m_ask_df,
                oracle_cfg=ctx.cfg.oracle,
                developer_prompt_text=cls_dev_prompt_text,
                developer_prompt_map=developer_prompt_map,
                few_shot_examples=few_shot_examples,
                **ctx.cfg.oracle.consult_kwargs,
            )
            
            if prompt_build_result.bidirectional:
                step(f"[Step 3] Consulting LLM oracle (bidirectional) with model: {ctx.cfg.oracle.model_name}")
                oracle_predictions_df = oc.consult_oracle_bidirectional(**oracle_kwargs)
            else:
                step(f"[Step 3] Consulting LLM oracle with model: {ctx.cfg.oracle.model_name}")
                oracle_predictions_df = oc.consult_oracle_for_mappings_to_ask(**oracle_kwargs)

            if oracle_predictions_df is None:
                fatal(
                    "Oracle consultation aborted before producing predictions; no partial "
                    "condition will be reported as successful.",
                    RuntimeError,
                )

            capabilities = oracle_predictions_df.attrs.get("oracle_capabilities", {})

            oracle_result = OracleResult(
                predictions=oracle_predictions_df,
                oracle_params=_configured_oracle_params(ctx.cfg.oracle, capabilities),
                bidirectional=prompt_build_result.bidirectional,
            )
            atomic_write_text_strict(
                ctx.run_paths.predictions_csv(),
                lambda fp: oracle_result.predictions.to_csv(fp, na_rep="nan", index=False),
            ) # BUGFIX (refine-bridge-1): index=False so REUSE re-read does not gain a phantom
              # 'Unnamed: 0' column that shifts every positional column right by one and corrupts
              # the Python set-union refinement. Atomic so a crash mid-write cannot leave a
              # truncated CSV a later --reuse step silently accepts as complete.
            return oracle_result

        case ConsultMode.REUSE:

            step(f"[Step 3] Loading LLM oracle predictions from: {ctx.run_paths.predictions_csv()}")
            predictions_df = pd.read_csv(ctx.run_paths.predictions_csv())
            # belt-and-braces: drop any legacy 'Unnamed:*' index column from CSVs written before
            # the index=False fix, so positional access stays aligned (refine-bridge-1).
            predictions_df = predictions_df.loc[:, ~predictions_df.columns.str.startswith("Unnamed:")]
            predictions_df = normalise_prediction_column(predictions_df) # pred.str_T/F/Y/N -> bool
            return OracleResult(
                predictions=predictions_df,
                oracle_params=_configured_oracle_params(ctx.cfg.oracle),
                # BIDIR-DECOMP columns are written only by bidirectional runs, so their
                # presence identifies one; REUSE used to drop the flag (misreported runs).
                bidirectional="Oracle_fwd_prediction" in predictions_df.columns,
            )

        case ConsultMode.LOCAL:

            step(f"[Step 3] Local oracle predictions from: {ctx.cfg.oracle.local_oracle_predictions_dirpath}")
            return OracleResult(
                local_dir=ctx.cfg.oracle.local_oracle_predictions_dirpath,
                predictions=None,
            )

        case ConsultMode.BYPASS:

            warn("Bypassing oracle consultations")
            return OracleResult()

        case _:
            fatal(f"config: consult_oracle param not recognised: {ctx.cfg.pipeline.consult_oracle}")

    fatal(f"unable to match on: {ctx.cfg.pipeline.consult_oracle}")



def refine_alignment(ctx: PipelineContext, oracle_result: OracleResult) -> RefinementResult:
    """
    Step 4: Refine alignment using oracle mapping predictions.
    """
    import logmap_llm.bridging as br

    step("\n[Step 4] Refine alignment using oracle mapping predictions")

    match ctx.cfg.pipeline.refine_alignment:

        case RefineMode.REFINE:

            # BUGFIX (REFINE-FRESH): every other stage unlinks its output before producing
            # it (run_result, prompts, predictions, eval_json). Without this, a refined TSV
            # left by a previous run of the same task passed validate_run_artifacts and was
            # silently evaluated and sealed as THIS run's artifact.
            ctx.run_paths.refined_mappings_tsv().unlink(missing_ok=True)

            if not oracle_result.has_predictions and not oracle_result.is_local:

                warn("[Step 4] No oracle predictions — skipping refinement (initial alignment is final)")

                import shutil

                # moves the initial mappings to the refined dir
                src = ctx.run_paths.logmap_mappings_tsv()
                dst = ctx.run_paths.refined_mappings_tsv()

                if not src.exists():
                    # previously a silent skip: no refined artifact, no error, and the run
                    # continued toward evaluation with nothing to evaluate
                    fatal(
                        f"[Step 4] Initial alignment TSV is missing: {src}; cannot "
                        "publish a refined alignment."
                    )
                os.makedirs(ctx.run_paths.refined_dir, exist_ok=True)
                shutil.copy2(str(src), str(dst))
                step(f"[Step 4] Initial alignment copied to refined dir: {dst.name}")

                return RefinementResult()

            # KG track: there exists a bug in the LogMap KG track execution path
            # For now, we bypass LogMap's Java refinement (since it crashes with NPEs 
            # on instance mappings) and produce refined alignment in Python
            # Note: the version of LogMap shipped with this repository can actually
            # refine the KG track via LogMap (and can therefore resolve any remaining
            # mappings associated with logical conflicts -- which is reccomended)
            # However, we cannot be certain that other users have the latest changes
            # (for example, if they use a custom LogMap version built from src)
            # therefore, we also include the PYTHON_SET_UNION bypass (see below):

            if (ctx.cfg.pipeline.refinement_strategy == RefinementStrategy.PYTHON_SETUNION and oracle_result.has_predictions):

                step("[Step 4] Python-based refinement (set-union bypass)")
                _kg_refine_in_python(ctx, oracle_result)
                return RefinementResult()

            if oracle_result.has_predictions:
                if ctx.logmap is None:
                    fatal("LogMap refinement requires an initialized LogMap JVM")
                logmap = ctx.logmap
                logmap.set_output_dir(ctx.run_paths.refined_dir)
                
                step("[Step 4] Refining initial LogMap alignment with LLM Oracle predictions")
                preds_java = br.python_oracle_mapping_predictions_2_java(
                    oracle_result.predictions
                )
                step(f"[Step 4] Number of mappings predicted True by Oracle given to LogMap: {len(preds_java)}")
                logmap.refine_alignment(preds_java)
                mappings_java = logmap.get_mappings()
                step(f"[Step 4] Number of mappings in LogMap refined alignment: {len(mappings_java)}")
                return RefinementResult(
                    refined_mappings=br.java_mappings_2_python(mappings_java)
                )

            elif oracle_result.is_local:
                if ctx.logmap is None:
                    fatal("Local-oracle refinement requires an initialized LogMap JVM")
                logmap = ctx.logmap
                logmap.set_output_dir(ctx.run_paths.refined_dir)
                
                step("[Step 4] Refining initial LogMap alignment with local Oracle predictions")
                logmap.refine_alignment(str(oracle_result.local_dir))
                mappings_java = logmap.get_mappings()
                step(f"[Step 4] Number of mappings in LogMap refined alignment: {len(mappings_java)}")
                return RefinementResult(
                    refined_mappings=br.java_mappings_2_python(mappings_java)
                )

            else:
                critical("Check your config to ensure 'refine_alignment' is set appropriately!")
                critical("The oracle response is empty and no local predictions file is specified.")
                fatal(
                    "Oracle payload passed to `refine_alignment` is either "
                    "malformed or is empty.",
                    IOError,
                )

        case RefineMode.BYPASS:

            warn("Bypassing alignment refinement")
            return RefinementResult()

        case _:
            fatal(f"config: refine_alignment param not recognised: {ctx.cfg.pipeline.refine_alignment}")

    fatal(f"unable to match on: {ctx.cfg.pipeline.refine_alignment}")



def evaluate(ctx) -> EvaluationResult:
    """
    Step 5: Evaluate the refined alignment.
    Similarly to step two (build_prompts), the evaluate method (which uses the DeepOnto evaluator
    by default -- which requires the use of another JVM) dispatches to logmap_llm.evaluation.harness
    as a subprocess; again, this is for JVM isolation (due to DeepOnto); however, we should note that
    this is not !! strictly !! neccesary, since we also implement our own evalution under the
        CustomEvaluationEngine class in logmap_llm.evaluation.engines.custom
    The architectural design decision to use extendable evaluation engines is based on the knowledge
    that actually multiple evaluators exist, eg. 'MELT', 'HOBBIT', 'SEALS', 'DeepOnto', and so forth
        (users should be able to extend the EvaluationEngine class and make use of their preffered 
         evaluator of choice; many of which do utilise another JVM instance, so isolating the evaluate
         procedure as a subprocess is _arguably_ _fairly_ sensible, though, not required for instances
         that use the CustomEvaluationEngine -- worth noting)
    Note: Evaluation can be skipped by setting 'evaluate = false' under '[evaluation]' in config.toml
    """
    step("\n[Step 5] Evaluation")

    if not ctx.cfg.evaluation.evaluate:
        warn("Evaluation disabled in config")
        return EvaluationResult()

    if not ctx.config_path:
        warning("No config path available for evaluation subprocess")
        return EvaluationResult(subprocess_failed=True)

    cmd = [
        sys.executable, "-m", "logmap_llm.evaluation.harness",
        "--config", ctx.config_path,
        *_subprocess_context_args(ctx),
    ]

    step("[Step 5] Running evaluation subprocess")
    ctx.run_paths.eval_json().unlink(missing_ok=True)

    proc = subprocess.run(cmd, capture_output=False)
    
    subprocess_failed = proc.returncode != 0
    
    if subprocess_failed:
        warning(f"Evaluation subprocess exited with code {proc.returncode}")

    eval_results_path = ctx.run_paths.eval_json()
    
    # only trust the results file if the subprocess succeeded
    if not subprocess_failed and eval_results_path.exists():
        with open(eval_results_path) as fp:
            results_dict = json.load(fp)

        success(f"Evaluation results loaded from: {eval_results_path}")
        return EvaluationResult(results=results_dict)
    
    if not subprocess_failed:
        warning(
            f"Evaluation subprocess succeeded but required result is missing: {eval_results_path}"
        )
        subprocess_failed = True

    # A stale result is never trusted after a failed or incomplete child.
    return EvaluationResult(subprocess_failed=subprocess_failed)

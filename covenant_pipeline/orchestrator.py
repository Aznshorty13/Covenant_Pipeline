"""Pipeline orchestration."""

from __future__ import annotations

from pathlib import Path

from covenant_pipeline.config import PipelinePaths
from covenant_pipeline.phases.audit import run_audit
from covenant_pipeline.phases.chunker import run_chunker
from covenant_pipeline.phases.compiler import run_compiler
from covenant_pipeline.phases.extraction import run_extraction
from covenant_pipeline.phases.glossary import run_glossary
from covenant_pipeline.phases.router import run_router
from covenant_pipeline.phases.validation import run_validation
from covenant_pipeline.viewer import launch_dev


def run_full_pipeline(
    paths: PipelinePaths,
    *,
    skip_llm: bool = False,
    serve_ui: bool = False,
    html_report: bool = True,
) -> Path:
    """Run all pipeline stages in order; return path to final audited JSON."""
    paths.output_dir.mkdir(parents=True, exist_ok=True)

    print("\n=== Stage: chunk ===")
    run_chunker(paths)

    print("\n=== Stage: route ===")
    run_router(paths)

    print("\n=== Stage: glossary ===")
    run_glossary(paths)

    if not skip_llm:
        print("\n=== Stage: extract ===")
        run_extraction(paths)

        print("\n=== Stage: compile ===")
        run_compiler(paths)

        print("\n=== Stage: audit ===")
        run_audit(paths)

        print("\n=== Stage: validate ===")
        run_validation(paths)

        if html_report:
            print("\n=== Stage: report ===")
            from covenant_pipeline.report.html_report import generate_html_report

            generate_html_report(paths)
    else:
        print("\nSkipping LLM stages (extract, compile, audit, validate) due to --skip-llm.")

    result = paths.audited if not skip_llm else paths.phase1_payload

    if serve_ui:
        if skip_llm:
            print("\nWarning: --serve-ui skipped because --skip-llm was used (no audited JSON).")
        else:
            launch_dev(paths)

    return result


def run_stage(stage: str, paths: PipelinePaths) -> Path:
    """Run a single pipeline stage by name."""
    stages = {
        "chunk": run_chunker,
        "route": run_router,
        "extract": run_extraction,
        "glossary": run_glossary,
        "compile": run_compiler,
        "audit": run_audit,
        "validate": run_validation,
    }

    if stage not in stages:
        raise ValueError(f"Unknown stage: {stage}. Choose from: {', '.join(stages)}")

    paths.output_dir.mkdir(parents=True, exist_ok=True)
    return stages[stage](paths)

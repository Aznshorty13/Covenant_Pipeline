"""Command-line interface for the covenant extraction pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from covenant_pipeline.config import DEFAULT_OUTPUT_DIR, PipelinePaths
from covenant_pipeline.orchestrator import run_full_pipeline, run_stage
from covenant_pipeline.report.html_report import generate_html_report
from covenant_pipeline.viewer import launch_dev

STAGES = ("chunk", "route", "extract", "glossary", "compile", "audit", "validate")


def _build_paths(args: argparse.Namespace) -> PipelinePaths:
    return PipelinePaths(
        output_dir=Path(args.output_dir),
        pdf_path=Path(args.pdf) if getattr(args, "pdf", None) else None,
        routing_config_json=Path(args.config) if getattr(args, "config", None) else None,
        extraction_model=args.model,
        rate_limit_seconds=args.rate_limit,
        enable_adversarial_test=getattr(args, "adversarial", False),
    )


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"Directory for pipeline artifacts (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--config",
        help="Path to covenant_config.json (default: repo config/covenant_config.json)",
    )
    parser.add_argument(
        "--model",
        default="gemini-3.1-flash-lite",
        help="Gemini model for extract and validate stages",
    )
    parser.add_argument(
        "--rate-limit",
        type=float,
        default=2.0,
        help="Seconds to sleep between LLM API calls",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Credit agreement covenant extraction pipeline",
        prog="covenant-pipeline",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the full pipeline")
    _add_common_args(run_parser)
    run_parser.add_argument("--pdf", help="Path to source PDF")
    run_parser.add_argument(
        "--skip-llm",
        action="store_true",
        help="Run deterministic stages only (chunk, route, glossary)",
    )
    run_parser.add_argument(
        "--adversarial",
        action="store_true",
        help="Enable chaos injection during validation (non-production)",
    )
    run_parser.add_argument(
        "--serve-ui",
        action="store_true",
        help="Launch the Covenant Viewer after the pipeline completes",
    )
    run_parser.add_argument(
        "--no-html-report",
        action="store_true",
        help="Skip generating covenant_audit_report.html after validation",
    )

    report_parser = subparsers.add_parser(
        "report",
        help="Generate HTML audit report from existing pipeline output",
    )
    _add_common_args(report_parser)
    report_parser.add_argument(
        "--pdf",
        help="Path to source PDF (default: output-dir/Credit_Agreement_Hallador.pdf)",
    )

    serve_parser = subparsers.add_parser("serve", help="Launch viewer for existing pipeline output")
    _add_common_args(serve_parser)
    serve_parser.add_argument(
        "--pdf",
        help="Path to source PDF (default: output-dir/Credit_Agreement_Hallador.pdf)",
    )
    serve_parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not open a browser tab automatically",
    )

    chunk_parser = subparsers.add_parser("chunk", help="Phase 0: PDF chunking")
    _add_common_args(chunk_parser)
    chunk_parser.add_argument("--pdf", required=True, help="Path to source PDF")

    route_parser = subparsers.add_parser("route", help="Tier 1 routing")
    _add_common_args(route_parser)

    extract_parser = subparsers.add_parser("extract", help="Phase 1 LLM extraction")
    _add_common_args(extract_parser)

    glossary_parser = subparsers.add_parser("glossary", help="Phase 2a glossary builder")
    _add_common_args(glossary_parser)

    compile_parser = subparsers.add_parser("compile", help="Phase 2b relational compiler")
    _add_common_args(compile_parser)

    audit_parser = subparsers.add_parser("audit", help="Phase 3a database audit")
    _add_common_args(audit_parser)

    validate_parser = subparsers.add_parser("validate", help="Phase 3b LLM validation")
    _add_common_args(validate_parser)
    validate_parser.add_argument(
        "--adversarial",
        action="store_true",
        help="Enable chaos injection during validation (non-production)",
    )

    args = parser.parse_args(argv)
    paths = _build_paths(args)

    try:
        if args.command == "run":
            result = run_full_pipeline(
                paths,
                skip_llm=args.skip_llm,
                serve_ui=getattr(args, "serve_ui", False),
                html_report=not getattr(args, "no_html_report", False),
            )
        elif args.command == "report":
            result = generate_html_report(paths)
        elif args.command == "serve":
            launch_dev(paths, open_browser=not args.no_browser)
            result = paths.audited
        else:
            result = run_stage(args.command, paths)

        print(f"\nDone. Output: {result}")
        return 0
    except (FileNotFoundError, EnvironmentError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

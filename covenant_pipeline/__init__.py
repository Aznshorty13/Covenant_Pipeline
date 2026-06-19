"""
Covenant Pipeline — credit agreement covenant extraction.

Usage (after install)::

    pip install -e .
    covenant-pipeline run --pdf Credit_Agreement_Hallador.pdf

    # Individual stages
    covenant-pipeline chunk --pdf agreement.pdf
    covenant-pipeline route
    covenant-pipeline extract
    covenant-pipeline glossary
    covenant-pipeline compile
    covenant-pipeline audit
    covenant-pipeline validate

    # Launch viewer for existing output
    covenant-pipeline serve --pdf agreement.pdf

    # Run pipeline and open viewer when done
    covenant-pipeline run --pdf agreement.pdf --serve-ui

LLM stages (extract, validate) require ``GEMINI_API_KEY``. Copy
``.env.example`` to ``.env`` in the project root, or export the variable in
your shell.

Programmatic usage::

    from covenant_pipeline.config import PipelinePaths
    from covenant_pipeline.orchestrator import run_full_pipeline

    paths = PipelinePaths(pdf_path="agreement.pdf")
    run_full_pipeline(paths)
"""

__version__ = "0.1.0"

from covenant_pipeline.config import PipelinePaths
from covenant_pipeline.orchestrator import run_full_pipeline, run_stage

__all__ = ["PipelinePaths", "run_full_pipeline", "run_stage", "__version__"]

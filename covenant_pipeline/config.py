"""Pipeline path and model configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_EXTRACTION_MODEL = "gemini-3.1-flash-lite"
INPUT_PRICE_PER_MILLION = 0.25
OUTPUT_PRICE_PER_MILLION = 1.50
DEFAULT_RATE_LIMIT_SECONDS = 2.0


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


DEFAULT_OUTPUT_DIR = _repo_root() / "out"


@dataclass
class PipelinePaths:
    """Centralized artifact paths for all pipeline stages."""

    output_dir: Path = field(default_factory=lambda: DEFAULT_OUTPUT_DIR)
    pdf_path: Path | None = None
    routing_config_json: Path | None = None
    extraction_model: str = DEFAULT_EXTRACTION_MODEL
    rate_limit_seconds: float = DEFAULT_RATE_LIMIT_SECONDS
    enable_adversarial_test: bool = False

    spatial_map_csv: str = "final_spatial_map.csv"
    covenants_csv: str = "final_extracted_covenants.csv"
    phase1_payload_csv: str = "final_extracted_covenants_phase1_payload.csv"
    dispatch_queue_json: str = "dispatch_queue_output.json"
    phase1_nodes_json: str = "phase1_extracted_nodes.json"
    glossary_json: str = "resolved_definitions.json"
    compiled_json: str = "final_compiled_payload.json"
    audited_json: str = "final_compiled_payload_audited.json"

    def __post_init__(self) -> None:
        self.output_dir = Path(self.output_dir).resolve()
        if self.pdf_path is None:
            self.pdf_path = self.output_dir / "Credit_Agreement_Hallador.pdf"
        else:
            self.pdf_path = Path(self.pdf_path).resolve()
        if self.routing_config_json is None:
            self.routing_config_json = _repo_root() / "config" / "covenant_config.json"
        else:
            self.routing_config_json = Path(self.routing_config_json).resolve()

    def path(self, filename: str) -> Path:
        return self.output_dir / filename

    @property
    def spatial_map(self) -> Path:
        return self.path(self.spatial_map_csv)

    @property
    def covenants(self) -> Path:
        return self.path(self.covenants_csv)

    @property
    def phase1_payload(self) -> Path:
        return self.path(self.phase1_payload_csv)

    @property
    def dispatch_queue(self) -> Path:
        return self.path(self.dispatch_queue_json)

    @property
    def phase1_nodes(self) -> Path:
        return self.path(self.phase1_nodes_json)

    @property
    def glossary(self) -> Path:
        return self.path(self.glossary_json)

    @property
    def compiled(self) -> Path:
        return self.path(self.compiled_json)

    @property
    def audited(self) -> Path:
        return self.path(self.audited_json)


def viewer_env(paths: PipelinePaths) -> dict[str, str]:
    """Environment variables for the viewer backend subprocess."""
    if paths.pdf_path is None:
        raise ValueError("pdf_path is required to launch the viewer")
    return {
        "COVENANT_AUDITED_JSON": str(paths.audited.resolve()),
        "COVENANT_PDF_PATH": str(paths.pdf_path.resolve()),
        "COVENANT_OUTPUT_DIR": str(paths.output_dir.resolve()),
        "COVENANT_DISPATCH_QUEUE_JSON": str(paths.dispatch_queue.resolve()),
    }


def viewer_root() -> Path:
    """Path to the viewer package at repo root."""
    return _repo_root() / "viewer"

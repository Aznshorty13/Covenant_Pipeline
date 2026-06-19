"""JSON and file I/O helpers."""

import json
from pathlib import Path
from typing import Any


def load_json(path: Path | str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path | str, data: Any, *, indent: int = 4) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)


def require_file(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")

"""Launch the Covenant Pipeline viewer (FastAPI + Vite dev servers)."""

from __future__ import annotations

import atexit
import os
import shutil
import signal
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

from covenant_pipeline.config import PipelinePaths, viewer_env, viewer_root

_CHILDREN: list[subprocess.Popen] = []


def _npm_executable() -> str:
    npm = shutil.which("npm.cmd") or shutil.which("npm")
    if not npm:
        raise EnvironmentError("npm is required to launch the viewer frontend. Install Node.js.")
    return npm


def _terminate_children() -> None:
    for proc in _CHILDREN:
        if proc.poll() is None:
            proc.terminate()
    for proc in _CHILDREN:
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def _spawn_process(cmd: list[str], *, cwd: Path, env: dict[str, str]) -> subprocess.Popen:
    creationflags = 0
    if sys.platform == "win32":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        env=env,
        creationflags=creationflags,
    )
    _CHILDREN.append(proc)
    return proc


def launch_dev(paths: PipelinePaths, *, open_browser: bool = True) -> None:
    """Start viewer backend and frontend dev servers; block until Ctrl+C."""
    if not paths.audited.exists():
        raise FileNotFoundError(
            f"Audited payload not found: {paths.audited}. "
            "Run the full pipeline (without --skip-llm) before launching the viewer."
        )
    if not paths.pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {paths.pdf_path}")

    root = viewer_root()
    backend_dir = root / "backend"
    frontend_dir = root / "frontend"

    if not backend_dir.is_dir() or not frontend_dir.is_dir():
        raise FileNotFoundError(f"Viewer package not found at {root}")

    base_env = os.environ.copy()
    base_env.update(viewer_env(paths))

    print("\nStarting Covenant Viewer...")
    print(f"  Audited JSON: {paths.audited}")
    print(f"  PDF:          {paths.pdf_path}")

    backend_proc = _spawn_process(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=backend_dir,
        env=base_env,
    )

    frontend_env = base_env.copy()
    frontend_proc = _spawn_process(
        [_npm_executable(), "run", "dev"],
        cwd=frontend_dir,
        env=frontend_env,
    )

    atexit.register(_terminate_children)

    def _handle_signal(signum, frame):
        _terminate_children()
        raise SystemExit(0)

    signal.signal(signal.SIGINT, _handle_signal)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, _handle_signal)

    time.sleep(2)

    if open_browser:
        webbrowser.open("http://localhost:5173")

    print("\nCovenant Viewer running:")
    print("  Frontend: http://localhost:5173")
    print("  Backend:  http://127.0.0.1:8000")
    print("\nPress Ctrl+C to stop.\n")

    try:
        while True:
            if backend_proc.poll() is not None:
                raise RuntimeError("Viewer backend exited unexpectedly.")
            if frontend_proc.poll() is not None:
                raise RuntimeError("Viewer frontend exited unexpectedly.")
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        _terminate_children()

#!/usr/bin/env python3
"""Regenerate Qt Python sources from the package-local editable inputs."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "src" / "leomoon_jalalitray"
UI_DIRECTORY = PACKAGE / "ui"
GENERATED_DIRECTORY = PACKAGE / "_generated"


def qt_tool(name: str) -> Path:
    """Return a Qt tool installed alongside the active Python interpreter."""
    suffix = ".exe" if sys.platform == "win32" else ""
    candidate = Path(sys.executable).parent / f"{name}{suffix}"
    if not candidate.is_file():
        message = f"{name} is not installed in the active virtual environment: {candidate}"
        raise SystemExit(message)
    return candidate


def run(*command: Path, cwd: Path) -> None:
    subprocess.run([str(item) for item in command], check=True, cwd=cwd)


def normalize_ui_import(path: Path) -> None:
    """Make the generated resource import valid within this package."""
    content = path.read_text(encoding="utf-8")
    content = content.replace("import resources_rc\n", "from . import resources_rc\n")
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    GENERATED_DIRECTORY.mkdir(exist_ok=True)
    ui_output = GENERATED_DIRECTORY / "main_window.py"
    resource_output = GENERATED_DIRECTORY / "resources_rc.py"

    run(qt_tool("pyside6-uic"), UI_DIRECTORY / "main_window.ui", "-o", ui_output, cwd=ROOT)
    normalize_ui_import(ui_output)
    run(qt_tool("pyside6-rcc"), UI_DIRECTORY / "resources.qrc", "-o", resource_output, cwd=UI_DIRECTORY)


if __name__ == "__main__":
    main()

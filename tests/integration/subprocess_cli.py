"""Subprocess wrapper for the `logistic_churn` executable."""

from __future__ import annotations

import subprocess
from pathlib import Path


def run_churn(
    logistic_churn: Path,
    cwd: Path,
    args: list[str],
    stdin: str,
    *,
    timeout: int = 120,
) -> subprocess.CompletedProcess[str]:
    """Runs the CLI with UTF-8 text stdin and captures stdout/stderr."""
    return subprocess.run(
        [str(logistic_churn), *args],
        input=stdin,
        text=True,
        cwd=cwd,
        capture_output=True,
        timeout=timeout,
        encoding="utf-8",
        errors="replace",
    )

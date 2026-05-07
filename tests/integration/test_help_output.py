"""Integration checks for `logistic_churn --help` output (FR-01 / CLI contract).

Each test feeds no stdin and asserts that a documented substring is present in stdout.
This guards the user-facing help text against accidental regressions.
"""

from __future__ import annotations

import pytest

from tests.integration.subprocess_cli import run_churn

HELP_SNIPPETS = [
    "Customer Churn Predictor - Command Line Interface",
    "Customer Churn Predictor",
    "Command Line Interface",
    "Usage:",
    "./logistic_churn [OPTION]",
    "Options:",
    "--help",
    "--train",
    "--train --evaluate",
    "--predict",
    "Show this help message and exit",
    "Train a new model",
    "evaluate its accuracy",
    "Predict churn using an existing trained model",
    "Examples:",
    "./logistic_churn --train",
    "./logistic_churn --train --evaluate",
    "./logistic_churn --predict",
    "logs/",
    "timestamped names.",
    "--------------------------------------------------",
    "and exit",
    "[OPTION]",
]


@pytest.mark.parametrize("snippet", HELP_SNIPPETS, ids=lambda s: s[:40].replace("/", "_").replace(" ", "_"))
def test_help_stdout_contains_documented_snippet(
    logistic_churn, project_root, snippet: str
):
    """Runs `--help` and verifies a stable fragment of the help banner remains available."""
    result = run_churn(logistic_churn, project_root, ["--help"], "")
    assert result.returncode == 0, result.stderr
    assert snippet in result.stdout


def test_help_does_not_write_to_stderr(logistic_churn, project_root):
    """Sanity check: help should be quiet on stderr for successful runs."""
    result = run_churn(logistic_churn, project_root, ["--help"], "")
    assert result.stderr.strip() == ""


def test_help_stdout_is_substantial_multiline_banner(logistic_churn, project_root):
    """Ensures help is not accidentally truncated to a single short line."""
    result = run_churn(logistic_churn, project_root, ["--help"], "")
    lines = [ln for ln in result.stdout.splitlines() if ln.strip()]
    assert len(lines) >= 8

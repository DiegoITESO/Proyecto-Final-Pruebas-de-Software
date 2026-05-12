"""System-level BDD tests: require the compiled ``logistic_churn`` binary."""

from __future__ import annotations

import pytest

from tests.integration._helpers import binary_exists

pytest_plugins = ["tests.system.steps.cli_steps"]


@pytest.fixture
def bdd_ctx() -> dict:
    """Per-scenario scratch space for the last subprocess and temp paths."""
    return {"proc": None}


@pytest.fixture(autouse=True)
def _require_logistic_churn_binary() -> None:
    if not binary_exists():
        pytest.skip("Build `logistic_churn` at repo root (e.g. `make`) before system BDD tests.")

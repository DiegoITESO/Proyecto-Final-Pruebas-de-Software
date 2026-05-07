"""Shared fixtures for subprocess-based integration tests against `logistic_churn`."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.integration.cli_io import train_stdin
from tests.integration.subprocess_cli import run_churn


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _resolve_executable(root: Path) -> Path:
    for name in ("logistic_churn.exe", "logistic_churn"):
        candidate = root / name
        if candidate.is_file():
            return candidate
    pytest.skip(
        "Executable not found. From the project root run: `make` (produces logistic_churn)."
    )


@pytest.fixture(scope="session")
def project_root() -> Path:
    return _project_root()


@pytest.fixture(scope="session")
def logistic_churn(project_root: Path) -> Path:
    return _resolve_executable(project_root)


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    return Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def run_churn_factory(logistic_churn: Path):
    def _run(cwd: Path, args: list[str], stdin: str, **kwargs):
        return run_churn(logistic_churn, cwd, args, stdin, **kwargs)

    return _run


@pytest.fixture(scope="module")
def module_trained_model(
    project_root: Path,
    logistic_churn: Path,
    fixtures_dir: Path,
    tmp_path_factory: pytest.TempPathFactory,
) -> Path:
    """Trains once per module so predict tests can share a valid JSON model artifact."""
    work = tmp_path_factory.mktemp("module_model")
    model_path = work / "weights.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model_path.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="80",
    )
    result = run_churn(logistic_churn, project_root, ["--train"], stdin)
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert model_path.is_file()
    return model_path

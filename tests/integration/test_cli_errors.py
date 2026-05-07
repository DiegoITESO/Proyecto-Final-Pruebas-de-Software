"""Negative-path integration tests: invalid flags, missing files, and bad CSV layouts."""

from __future__ import annotations

from pathlib import Path

from tests.integration.cli_io import predict_stdin, train_stdin
from tests.integration.subprocess_cli import run_churn


def test_unknown_option_nonzero_exit(logistic_churn: Path, project_root: Path):
    """ArgParser should surface `Unknown option` and fail fast for unsupported flags."""
    result = run_churn(logistic_churn, project_root, ["--not-a-real-flag"], "")
    assert result.returncode != 0


def test_unknown_option_message_on_stderr_or_stdout(
    logistic_churn: Path, project_root: Path
):
    """The runtime error text should be visible to the user (libc++ may route to stderr)."""
    result = run_churn(logistic_churn, project_root, ["--bogus"], "")
    combined = result.stdout + result.stderr
    assert "Unknown option" in combined


def test_train_missing_input_file_fails(
    logistic_churn: Path, project_root: Path, tmp_path: Path
):
    """CSVReader throws when the dataset path cannot be opened."""
    model = tmp_path / "missing.json"
    missing = tmp_path / "does_not_exist.csv"
    stdin = train_stdin(
        str(missing.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="10",
    )
    result = run_churn(logistic_churn, project_root, ["--train"], stdin)
    assert result.returncode != 0


def test_train_rejects_inconsistent_csv_rows(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """FR-03: inconsistent column counts should abort before training."""
    model = tmp_path / "bad.csv.json"
    bad = fixtures_dir / "malformed_inconsistent_columns.csv"
    stdin = train_stdin(
        str(bad.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="10",
    )
    result = run_churn(logistic_churn, project_root, ["--train"], stdin)
    assert result.returncode != 0


def test_train_invalid_header_response_fails(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Only `y`/`n` are accepted for the header prompt; anything else should error."""
    model = tmp_path / "hdr.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = f"{train_csv.resolve()}\n{model.resolve()}\nx\n3\n\n0.05\n10\n"
    result = run_churn(logistic_churn, project_root, ["--train"], stdin)
    assert result.returncode != 0


def test_predict_missing_weights_file_fails(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Loading a non-existent JSON model path should terminate with an error."""
    out = tmp_path / "out.csv"
    data = fixtures_dir / "synthetic_churn_predict.csv"
    ghost = tmp_path / "nope.json"
    stdin = predict_stdin(
        str(ghost.resolve()),
        str(data.resolve()),
        str(out.resolve()),
        header_yes=True,
    )
    result = run_churn(logistic_churn, project_root, ["--predict"], stdin)
    assert result.returncode != 0


def test_predict_missing_dataset_file_fails(
    logistic_churn: Path, project_root: Path, module_trained_model: Path, tmp_path: Path
):
    """Predict mode should fail when the scoring CSV is missing."""
    out = tmp_path / "out2.csv"
    ghost_data = tmp_path / "missing_data.csv"
    stdin = predict_stdin(
        str(module_trained_model.resolve()),
        str(ghost_data.resolve()),
        str(out.resolve()),
        header_yes=True,
    )
    result = run_churn(logistic_churn, project_root, ["--predict"], stdin)
    assert result.returncode != 0


def test_evaluate_missing_dataset_fails(
    logistic_churn: Path, project_root: Path, tmp_path: Path
):
    """Evaluate still reads CSV first; a bad path should behave like train failures."""
    model = tmp_path / "eval_bad.json"
    missing = tmp_path / "ghost_train.csv"
    stdin = train_stdin(
        str(missing.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="10",
    )
    result = run_churn(logistic_churn, project_root, ["--train", "--evaluate"], stdin)
    assert result.returncode != 0

"""Evaluate integration tests (`--train --evaluate`) covering FR-08 metric lines."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tests.integration.cli_io import train_stdin
from tests.integration.subprocess_cli import run_churn


def test_evaluate_exits_zero(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Drives evaluate mode with the synthetic dataset and expects a clean process exit."""
    model = tmp_path / "eval_model.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="70",
    )
    result = run_churn(logistic_churn, project_root, ["--train", "--evaluate"], stdin)
    assert result.returncode == 0, (result.stdout, result.stderr)


def test_evaluate_prints_accuracy_line(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """FR-08 requires `Accuracy:` to appear on stdout alongside the numeric score."""
    model = tmp_path / "eval_a.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="65",
    )
    result = run_churn(logistic_churn, project_root, ["--train", "--evaluate"], stdin)
    assert "Accuracy:" in result.stdout


def test_evaluate_prints_precision_line(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Validates the precision metric label is forwarded to the console."""
    model = tmp_path / "eval_b.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="65",
    )
    result = run_churn(logistic_churn, project_root, ["--train", "--evaluate"], stdin)
    assert "Precision:" in result.stdout


def test_evaluate_prints_recall_line(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Validates the recall metric label is forwarded to the console."""
    model = tmp_path / "eval_c.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="65",
    )
    result = run_churn(logistic_churn, project_root, ["--train", "--evaluate"], stdin)
    assert "Recall:" in result.stdout


def test_evaluate_prints_f1_line(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Validates the F1 score label matches `handleEvaluate` formatting."""
    model = tmp_path / "eval_d.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="65",
    )
    result = run_churn(logistic_churn, project_root, ["--train", "--evaluate"], stdin)
    assert "F1 score:" in result.stdout


def test_evaluate_metric_lines_are_parseable_floats(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Each metric line should end with a floating value between 0 and 1 (inclusive)."""
    model = tmp_path / "eval_e.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="70",
    )
    result = run_churn(logistic_churn, project_root, ["--train", "--evaluate"], stdin)
    for label in ("Accuracy:", "Precision:", "Recall:", "F1 score:"):
        m = re.search(rf"{re.escape(label)}\s*([0-9.eE+-]+)", result.stdout)
        assert m, f"missing numeric for {label}"
        val = float(m.group(1))
        assert 0.0 <= val <= 1.0


def test_evaluate_still_persists_model_json(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Evaluate mode trains first; the weights file must still be written like vanilla `--train`."""
    model = tmp_path / "eval_f.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="60",
    )
    run_churn(logistic_churn, project_root, ["--train", "--evaluate"], stdin)
    payload = json.loads(model.read_text(encoding="utf-8"))
    assert "Weights" in payload and "Bias" in payload


def test_evaluate_stdout_contains_training_progress(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Even in evaluate mode, the training loop should emit `Progress:` markers."""
    model = tmp_path / "eval_g.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="50",
    )
    result = run_churn(logistic_churn, project_root, ["--train", "--evaluate"], stdin)
    assert "Progress:" in result.stdout


def test_evaluate_stderr_empty_on_success(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Mirrors other happy-path CLI tests: stderr stays clean when no failure occurs."""
    model = tmp_path / "eval_h.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="55",
    )
    result = run_churn(logistic_churn, project_root, ["--train", "--evaluate"], stdin)
    assert result.returncode == 0
    assert result.stderr.strip() == ""


def test_evaluate_metrics_lines_occur_after_training_progress(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Ordering guard: metric reporting should appear after progress spam, not before."""
    model = tmp_path / "eval_i.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="55",
    )
    result = run_churn(logistic_churn, project_root, ["--train", "--evaluate"], stdin)
    prog = result.stdout.rfind("Progress:")
    acc = result.stdout.find("Accuracy:")
    assert prog != -1 and acc != -1 and acc > prog


def test_evaluate_four_metric_lines_present(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Ensures we did not drop one of the four required metric labels."""
    model = tmp_path / "eval_j.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="60",
    )
    result = run_churn(logistic_churn, project_root, ["--train", "--evaluate"], stdin)
    for needle in ("Accuracy:", "Precision:", "Recall:", "F1 score:"):
        assert result.stdout.count(needle) >= 1


def test_evaluate_with_no_header_dataset(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Evaluate should tolerate the headerless fixture used elsewhere in integration tests."""
    model = tmp_path / "eval_nohdr.json"
    train_csv = fixtures_dir / "synthetic_no_header_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=False,
        churn_index=3,
        alpha="0.05",
        epochs="65",
    )
    result = run_churn(logistic_churn, project_root, ["--train", "--evaluate"], stdin)
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert "Accuracy:" in result.stdout

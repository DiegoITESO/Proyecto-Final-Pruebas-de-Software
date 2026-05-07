"""Training-mode integration tests (`--train`) with real CSV I/O and JSON export."""

from __future__ import annotations

import json
from pathlib import Path

from tests.integration.cli_io import train_stdin
from tests.integration.subprocess_cli import run_churn


def test_train_happy_path_exits_zero(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Drives the interactive train prompts with a valid fixture and expects a clean exit code."""
    model = tmp_path / "out_train.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="60",
    )
    result = run_churn(logistic_churn, project_root, ["--train"], stdin)
    assert result.returncode == 0, (result.stdout, result.stderr)


def test_train_writes_model_json_file(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Verifies FR-07: the destination path receives a persisted model file after training."""
    model = tmp_path / "weights_a.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="60",
    )
    run_churn(logistic_churn, project_root, ["--train"], stdin)
    assert model.is_file()


def test_train_json_contains_weights_array(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Asserts the on-disk JSON exposes the `Weights` array produced by `LogisticRegression::save`."""
    model = tmp_path / "weights_b.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="60",
    )
    run_churn(logistic_churn, project_root, ["--train"], stdin)
    data = json.loads(model.read_text(encoding="utf-8"))
    assert "Weights" in data
    assert isinstance(data["Weights"], list)


def test_train_json_contains_bias_scalar(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Asserts the JSON also stores the scalar `Bias` term required for inference."""
    model = tmp_path / "weights_c.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="60",
    )
    run_churn(logistic_churn, project_root, ["--train"], stdin)
    data = json.loads(model.read_text(encoding="utf-8"))
    assert "Bias" in data
    assert isinstance(data["Bias"], (int, float))


def test_train_weights_list_is_non_empty(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """After preprocessing, feature dimension must be positive; saved weights should not be empty."""
    model = tmp_path / "weights_d.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="60",
    )
    run_churn(logistic_churn, project_root, ["--train"], stdin)
    data = json.loads(model.read_text(encoding="utf-8"))
    assert len(data["Weights"]) > 0


def test_train_stdout_reports_progress_percentages(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Training logs epoch progress to stdout; this test ensures the UI hook still prints `Progress:`."""
    model = tmp_path / "weights_e.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="80",
    )
    result = run_churn(logistic_churn, project_root, ["--train"], stdin)
    assert "Progress:" in result.stdout


def test_train_stdout_reaches_100_percent(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Confirms the training loop runs through the final progress tick (100%)."""
    model = tmp_path / "weights_f.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="80",
    )
    result = run_churn(logistic_churn, project_root, ["--train"], stdin)
    assert "100%" in result.stdout


def test_train_without_csv_header(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Uses `hasHeader = n` and targets the last column index for labels (still `yes`/`no`)."""
    model = tmp_path / "weights_nohdr.json"
    train_csv = fixtures_dir / "synthetic_no_header_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=False,
        churn_index=3,
        alpha="0.05",
        epochs="70",
    )
    result = run_churn(logistic_churn, project_root, ["--train"], stdin)
    assert result.returncode == 0, (result.stdout, result.stderr)


def test_train_with_small_epoch_budget(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Even a tiny epoch budget should complete; useful for fast smoke coverage."""
    model = tmp_path / "weights_small_ep.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="5",
    )
    result = run_churn(logistic_churn, project_root, ["--train"], stdin)
    assert result.returncode == 0, (result.stdout, result.stderr)


def test_train_with_low_learning_rate(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Stability check: a smaller `alpha` should still yield a successful training run."""
    model = tmp_path / "weights_low_lr.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.01",
        epochs="50",
    )
    result = run_churn(logistic_churn, project_root, ["--train"], stdin)
    assert result.returncode == 0, (result.stdout, result.stderr)


def test_train_success_has_quiet_stderr(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """A successful CLI run should not emit diagnostic text on stderr (under normal conditions)."""
    model = tmp_path / "weights_err.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="40",
    )
    result = run_churn(logistic_churn, project_root, ["--train"], stdin)
    assert result.returncode == 0
    assert result.stderr.strip() == ""


def test_train_weights_are_finite_floats(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Guards against NaN/inf weights that would break downstream prediction."""
    model = tmp_path / "weights_fin.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="60",
    )
    run_churn(logistic_churn, project_root, ["--train"], stdin)
    data = json.loads(model.read_text(encoding="utf-8"))
    for w in data["Weights"]:
        assert w == w and abs(w) != float("inf")


def test_train_json_is_pretty_indented(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """`nlohmann::json::dump(4)` should produce a human-readable multi-line file."""
    model = tmp_path / "weights_pretty.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="40",
    )
    run_churn(logistic_churn, project_root, ["--train"], stdin)
    text = model.read_text(encoding="utf-8")
    assert "\n" in text


def test_train_creates_logs_directory(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """FR-12: logger should ensure `logs/` exists under the process working directory."""
    model = tmp_path / "weights_log.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="30",
    )
    run_churn(logistic_churn, project_root, ["--train"], stdin)
    assert (project_root / "logs").is_dir()


def test_train_second_run_overwrites_model_file(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """Idempotence check: training twice to the same path should refresh the artifact."""
    model = tmp_path / "weights_overwrite.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="35",
    )
    run_churn(logistic_churn, project_root, ["--train"], stdin)
    first = model.read_bytes()
    stdin2 = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.08",
        epochs="40",
    )
    run_churn(logistic_churn, project_root, ["--train"], stdin2)
    second = model.read_bytes()
    assert first != second


def test_train_bias_is_finite(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """The bias term must deserialize as a finite floating value."""
    model = tmp_path / "weights_bias.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="55",
    )
    run_churn(logistic_churn, project_root, ["--train"], stdin)
    data = json.loads(model.read_text(encoding="utf-8"))
    b = float(data["Bias"])
    assert b == b and abs(b) != float("inf")


def test_train_timestamped_log_mentions_model_save(
    logistic_churn: Path, project_root: Path, fixtures_dir: Path, tmp_path: Path
):
    """FR-12: newest log under `logs/` should capture the post-training persistence message."""
    model = tmp_path / "weights_logmsg.json"
    train_csv = fixtures_dir / "synthetic_churn_train.csv"
    stdin = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=True,
        churn_index=3,
        alpha="0.05",
        epochs="45",
    )
    run_churn(logistic_churn, project_root, ["--train"], stdin)
    logs_dir = project_root / "logs"
    assert logs_dir.is_dir()
    log_files = sorted(logs_dir.glob("CCP_*"), key=lambda p: p.stat().st_mtime)
    assert log_files, "expected at least one CCP_* log file"
    text = log_files[-1].read_text(encoding="utf-8", errors="replace")
    assert "Model saved" in text or "Success" in text

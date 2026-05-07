"""Prediction-mode integration tests (`--predict`) using a shared trained model artifact."""

from __future__ import annotations

from pathlib import Path

from tests.integration.cli_io import predict_stdin, train_stdin
from tests.integration.subprocess_cli import run_churn


def test_predict_happy_path_exits_zero(
    logistic_churn: Path,
    project_root: Path,
    fixtures_dir: Path,
    module_trained_model: Path,
    tmp_path: Path,
):
    """Runs predict with the module-scoped weights file and expects a successful exit."""
    out = tmp_path / "pred_a.csv"
    data = fixtures_dir / "synthetic_churn_predict.csv"
    stdin = predict_stdin(
        str(module_trained_model.resolve()),
        str(data.resolve()),
        str(out.resolve()),
        header_yes=True,
    )
    result = run_churn(logistic_churn, project_root, ["--predict"], stdin)
    assert result.returncode == 0, (result.stdout, result.stderr)


def test_predict_writes_output_csv(
    logistic_churn: Path,
    project_root: Path,
    fixtures_dir: Path,
    module_trained_model: Path,
    tmp_path: Path,
):
    """FR-10: prediction output path must exist after a successful run."""
    out = tmp_path / "pred_b.csv"
    data = fixtures_dir / "synthetic_churn_predict.csv"
    stdin = predict_stdin(
        str(module_trained_model.resolve()),
        str(data.resolve()),
        str(out.resolve()),
        header_yes=True,
    )
    run_churn(logistic_churn, project_root, ["--predict"], stdin)
    assert out.is_file()


def test_predict_line_count_matches_dataset_rows(
    logistic_churn: Path,
    project_root: Path,
    fixtures_dir: Path,
    module_trained_model: Path,
    tmp_path: Path,
):
    """Each input row should emit exactly one probability line (no header in output)."""
    out = tmp_path / "pred_c.csv"
    data = fixtures_dir / "synthetic_churn_predict.csv"
    stdin = predict_stdin(
        str(module_trained_model.resolve()),
        str(data.resolve()),
        str(out.resolve()),
        header_yes=True,
    )
    run_churn(logistic_churn, project_root, ["--predict"], stdin)
    lines = [ln for ln in out.read_text(encoding="utf-8").splitlines() if ln.strip()]
    data_lines = len(data.read_text(encoding="utf-8").strip().splitlines()) - 1
    assert len(lines) == data_lines


def test_predict_each_line_is_float(
    logistic_churn: Path,
    project_root: Path,
    fixtures_dir: Path,
    module_trained_model: Path,
    tmp_path: Path,
):
    """Output rows must be parseable as floating point numbers."""
    out = tmp_path / "pred_d.csv"
    data = fixtures_dir / "synthetic_churn_predict.csv"
    stdin = predict_stdin(
        str(module_trained_model.resolve()),
        str(data.resolve()),
        str(out.resolve()),
        header_yes=True,
    )
    run_churn(logistic_churn, project_root, ["--predict"], stdin)
    for ln in out.read_text(encoding="utf-8").splitlines():
        if ln.strip():
            float(ln.strip())


def test_predict_probabilities_are_between_zero_and_one(
    logistic_churn: Path,
    project_root: Path,
    fixtures_dir: Path,
    module_trained_model: Path,
    tmp_path: Path,
):
    """Sigmoid outputs should stay within the closed unit interval."""
    out = tmp_path / "pred_e.csv"
    data = fixtures_dir / "synthetic_churn_predict.csv"
    stdin = predict_stdin(
        str(module_trained_model.resolve()),
        str(data.resolve()),
        str(out.resolve()),
        header_yes=True,
    )
    run_churn(logistic_churn, project_root, ["--predict"], stdin)
    for ln in out.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        v = float(ln.strip())
        assert 0.0 <= v <= 1.0


def test_predict_with_no_header_dataset(
    logistic_churn: Path,
    project_root: Path,
    fixtures_dir: Path,
    tmp_path: Path,
):
    """End-to-end predict when the scoring CSV omits a header row (`n` response)."""
    model = tmp_path / "pm.json"
    train_csv = fixtures_dir / "synthetic_no_header_train.csv"
    train_in = train_stdin(
        str(train_csv.resolve()),
        str(model.resolve()),
        header_yes=False,
        churn_index=3,
        alpha="0.05",
        epochs="70",
    )
    run_churn(logistic_churn, project_root, ["--train"], train_in)
    out = tmp_path / "pred_nohdr.csv"
    pred_csv = fixtures_dir / "synthetic_no_header_predict.csv"
    stdin = predict_stdin(
        str(model.resolve()),
        str(pred_csv.resolve()),
        str(out.resolve()),
        header_yes=False,
    )
    result = run_churn(logistic_churn, project_root, ["--predict"], stdin)
    assert result.returncode == 0, (result.stdout, result.stderr)


def test_predict_output_is_non_empty(
    logistic_churn: Path,
    project_root: Path,
    fixtures_dir: Path,
    module_trained_model: Path,
    tmp_path: Path,
):
    """Sanity check that we did not produce a zero-byte predictions file."""
    out = tmp_path / "pred_f.csv"
    data = fixtures_dir / "synthetic_churn_predict.csv"
    stdin = predict_stdin(
        str(module_trained_model.resolve()),
        str(data.resolve()),
        str(out.resolve()),
        header_yes=True,
    )
    run_churn(logistic_churn, project_root, ["--predict"], stdin)
    assert out.stat().st_size > 0


def test_predict_stderr_clean_on_success(
    logistic_churn: Path,
    project_root: Path,
    fixtures_dir: Path,
    module_trained_model: Path,
    tmp_path: Path,
):
    """Mirrors the train smoke test: stderr should remain silent on success."""
    out = tmp_path / "pred_g.csv"
    data = fixtures_dir / "synthetic_churn_predict.csv"
    stdin = predict_stdin(
        str(module_trained_model.resolve()),
        str(data.resolve()),
        str(out.resolve()),
        header_yes=True,
    )
    result = run_churn(logistic_churn, project_root, ["--predict"], stdin)
    assert result.returncode == 0
    assert result.stderr.strip() == ""


def test_predict_first_row_is_probability_token(
    logistic_churn: Path,
    project_root: Path,
    fixtures_dir: Path,
    module_trained_model: Path,
    tmp_path: Path,
):
    """The first emitted value should look like a decimal probability (not categorical text)."""
    out = tmp_path / "pred_h.csv"
    data = fixtures_dir / "synthetic_churn_predict.csv"
    stdin = predict_stdin(
        str(module_trained_model.resolve()),
        str(data.resolve()),
        str(out.resolve()),
        header_yes=True,
    )
    run_churn(logistic_churn, project_root, ["--predict"], stdin)
    first = out.read_text(encoding="utf-8").splitlines()[0].strip()
    assert "." in first or first in {"0", "1"}


def test_predict_can_target_second_output_path(
    logistic_churn: Path,
    project_root: Path,
    fixtures_dir: Path,
    module_trained_model: Path,
    tmp_path: Path,
):
    """Regression guard: a second prediction file path should also work with the same weights."""
    out1 = tmp_path / "pred_i1.csv"
    out2 = tmp_path / "pred_i2.csv"
    data = fixtures_dir / "synthetic_churn_predict.csv"
    for target in (out1, out2):
        stdin = predict_stdin(
            str(module_trained_model.resolve()),
            str(data.resolve()),
            str(target.resolve()),
            header_yes=True,
        )
        result = run_churn(logistic_churn, project_root, ["--predict"], stdin)
        assert result.returncode == 0
    assert out1.read_text() == out2.read_text()


def test_predict_trained_model_json_has_expected_top_level_keys(
    module_trained_model: Path,
):
    """Lightweight contract test on the shared artifact before predict scenarios run."""
    import json

    payload = json.loads(module_trained_model.read_text(encoding="utf-8"))
    assert set(payload.keys()) >= {"Weights", "Bias"}


def test_predict_stdout_stays_quiet_or_minimal(
    logistic_churn: Path,
    project_root: Path,
    fixtures_dir: Path,
    module_trained_model: Path,
    tmp_path: Path,
):
    """Predict mode should not spam progress lines like training; stdout is expected to be empty or tiny."""
    out = tmp_path / "pred_j.csv"
    data = fixtures_dir / "synthetic_churn_predict.csv"
    stdin = predict_stdin(
        str(module_trained_model.resolve()),
        str(data.resolve()),
        str(out.resolve()),
        header_yes=True,
    )
    result = run_churn(logistic_churn, project_root, ["--predict"], stdin)
    assert result.returncode == 0
    assert "Progress:" not in result.stdout

"""Gherkin steps: black-box ``logistic_churn`` CLI (no browser)."""

from __future__ import annotations

import shlex
from pathlib import Path
from subprocess import CompletedProcess

from pytest_bdd import given, parsers, then, when

from tests.integration._helpers import (
    churn_labeled_csv,
    features_only_csv,
    predict_stdin,
    run_cli,
    train_stdin,
)


def _proc(ctx: dict) -> CompletedProcess:
    proc = ctx.get("proc")
    assert proc is not None, "No CLI run yet; use a When step first."
    return proc


@when(parsers.parse('I run the CLI with argv "{argv}" and empty stdin'))
def step_run_cli_empty_stdin(bdd_ctx: dict, argv: str) -> None:
    bdd_ctx["proc"] = run_cli(shlex.split(argv), "", timeout=60)


@when(parsers.parse('I run the CLI with argv "{argv}" and stdin from scenario'))
def step_run_cli_scenario_stdin(bdd_ctx: dict, argv: str) -> None:
    stdin = bdd_ctx.get("stdin", "")
    cwd = bdd_ctx.get("cwd")
    bdd_ctx["proc"] = run_cli(shlex.split(argv), stdin, cwd=cwd, timeout=180)


@given("the training workspace is prepared")
def step_prepare_train_workspace(bdd_ctx: dict, tmp_path: Path) -> None:
    bdd_ctx["cwd"] = tmp_path
    train_csv = tmp_path / "train_data.csv"
    train_csv.write_text(churn_labeled_csv(34), encoding="utf-8")
    bdd_ctx["train_csv"] = train_csv
    bdd_ctx["model_json"] = tmp_path / "model_weights.json"
    feat_csv = tmp_path / "predict_features.csv"
    feat_csv.write_text(features_only_csv(11), encoding="utf-8")
    bdd_ctx["feat_csv"] = feat_csv


@when("I run training with scripted stdin")
def step_run_train(bdd_ctx: dict) -> None:
    stdin = train_stdin(
        str(bdd_ctx["train_csv"]),
        str(bdd_ctx["model_json"]),
        epochs=28,
    )
    bdd_ctx["proc"] = run_cli(["--train"], stdin, cwd=bdd_ctx["cwd"], timeout=180)


@when("I run prediction with scripted stdin")
def step_run_predict(bdd_ctx: dict) -> None:
    out = bdd_ctx["cwd"] / "predictions.csv"
    bdd_ctx["pred_out"] = out
    stdin = predict_stdin(
        str(bdd_ctx["model_json"]),
        str(bdd_ctx["feat_csv"]),
        str(out),
    )
    bdd_ctx["proc"] = run_cli(["--predict"], stdin, cwd=bdd_ctx["cwd"], timeout=120)


@given("a missing CSV path for training")
def step_missing_csv_train(bdd_ctx: dict, tmp_path: Path) -> None:
    bdd_ctx["cwd"] = tmp_path
    missing = tmp_path / "does_not_exist.csv"
    out = tmp_path / "out.json"
    bdd_ctx["stdin"] = train_stdin(str(missing), str(out), epochs=5)


@then("the exit code is 0")
def step_exit_zero(bdd_ctx: dict) -> None:
    assert _proc(bdd_ctx).returncode == 0


@then("the exit code is not 0")
def step_exit_nonzero(bdd_ctx: dict) -> None:
    assert _proc(bdd_ctx).returncode != 0


@then(parsers.parse('stdout contains "{fragment}"'))
def step_stdout_contains(bdd_ctx: dict, fragment: str) -> None:
    assert fragment in (_proc(bdd_ctx).stdout or "")


@then(parsers.parse('combined output contains "{fragment}"'))
def step_combined_contains(bdd_ctx: dict, fragment: str) -> None:
    proc = _proc(bdd_ctx)
    blob = (proc.stdout or "") + (proc.stderr or "")
    assert fragment in blob


@then("the model JSON file was written")
def step_model_written(bdd_ctx: dict) -> None:
    assert bdd_ctx["model_json"].is_file()


@then("each prediction line is a float between 0 and 1")
def step_pred_floats(bdd_ctx: dict) -> None:
    out = bdd_ctx["pred_out"]
    assert out.is_file(), "prediction output file missing"
    text = out.read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        value = float(line)
        assert 0.0 <= value <= 1.0

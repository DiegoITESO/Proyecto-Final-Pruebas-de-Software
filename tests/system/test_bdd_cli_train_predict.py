"""System BDD: train then predict flow."""

from __future__ import annotations

from pathlib import Path

from pytest_bdd import scenarios

_FEATURES = Path(__file__).resolve().parent / "features"
scenarios("cli_train_predict.feature", features_base_dir=str(_FEATURES))

"""Loads every Gherkin file under `features/` as pytest-bdd scenarios."""

from pathlib import Path

from pytest_bdd import scenarios

_FEATURE_DIR = Path(__file__).resolve().parent / "features"

for _feature_path in sorted(_FEATURE_DIR.glob("*.feature")):
    scenarios(_feature_path.as_posix())

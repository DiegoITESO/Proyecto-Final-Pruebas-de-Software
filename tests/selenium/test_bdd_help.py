"""BDD: CLI help HTML fixture (pytest-bdd scenarios)."""

from pathlib import Path

from pytest_bdd import scenarios

_FEATURES = Path(__file__).resolve().parent / "features"
scenarios("help.feature", features_base_dir=str(_FEATURES))

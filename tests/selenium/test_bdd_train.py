"""BDD: training wizard HTML fixture."""

from pathlib import Path

from pytest_bdd import scenarios

_FEATURES = Path(__file__).resolve().parent / "features"
scenarios("train.feature", features_base_dir=str(_FEATURES))

"""BDD: architecture and persistence HTML fixtures."""

from pathlib import Path

from pytest_bdd import scenarios

_FEATURES = Path(__file__).resolve().parent / "features"
scenarios("architecture_persistence.feature", features_base_dir=str(_FEATURES))

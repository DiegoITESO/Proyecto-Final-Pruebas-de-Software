"""Stdin builders for the interactive CLI (train / predict / evaluate)."""


def train_stdin(
    train_csv: str,
    model_json: str,
    *,
    header_yes: bool,
    churn_index: int,
    alpha: str,
    epochs: str,
) -> str:
    """Builds stdin for training or evaluate flows; drop columns are left blank."""
    yn = "y" if header_yes else "n"
    return f"{train_csv}\n{model_json}\n{yn}\n{churn_index}\n\n{alpha}\n{epochs}\n"


def predict_stdin(
    weights_json: str,
    dataset_csv: str,
    predictions_csv: str,
    *,
    header_yes: bool,
) -> str:
    """Builds stdin for prediction; drop columns are left blank."""
    yn = "y" if header_yes else "n"
    return f"{weights_json}\n{dataset_csv}\n{predictions_csv}\n{yn}\n\n"

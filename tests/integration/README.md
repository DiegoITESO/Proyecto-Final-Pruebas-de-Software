# Integration tests

Python tests under `tests/integration/` drive the compiled `logistic_churn` binary (stdin + subprocess). Build the app first, install deps, then run pytest from the **repository root**.

**Prerequisites:** `make` produced `logistic_churn` (or `logistic_churn.exe` on Windows) in the project root; Python 3.10+.

```bash
pip install -r tests/integration/requirements.txt
make
pytest tests/integration
```

To run a single file:

```bash
pytest tests/integration/test_train_integration.py -q
```

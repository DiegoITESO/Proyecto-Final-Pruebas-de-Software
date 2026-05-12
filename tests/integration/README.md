# Integration tests

These tests call the **real C++ executable** (`logistic_churn` / `logistic_churn.exe`) in a subprocess from the repo root, with scripted stdin—same as you would in a terminal.

## Requirements

- Python **3.10+**
- Dependencies: `pip install -r tests/requirements.txt` (from repo root)
- Built **`logistic_churn`** at the **repository root** as `logistic_churn` (Linux/macOS) or `logistic_churn.exe` (Windows), **or** set **`LOGISTIC_CHURN_PATH`** to the full path of that executable
- **Windows:** if the binary fails to start from pytest, ensure **MSYS2 MinGW/UCRT `bin`** is on `PATH` (same as when you built the project) so MinGW DLLs resolve

## Run (no skips)

From the **repository root**:

```bash
pytest tests/integration -v
```

Build first, e.g. `make` (Linux/macOS) or your project’s `build.ps1` / `build.sh` (Windows).

## Expected result

All tests **execute** (none skipped for “binary missing”). On success: **exit code 0** and every test **passed**.

Gherkin-style system scenarios (same binary) live in **`tests/system`** (`pytest tests/system`).

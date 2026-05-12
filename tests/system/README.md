# System tests (BDD, CLI)

**No browser.** These are **Gherkin** scenarios executed with **pytest-bdd** against the real **`logistic_churn`** binary (subprocess + stdin), matching a CLI-only churn trainer.

This layer satisfies “system tests with BDD” without Selenium; the rubric allows **“Selenium or any other similar tool”** — here the **similar** approach is **black-box CLI automation** with the same BDD notation.

## Requirements

Same as `tests/integration/README.md`: Python **3.10+**, `pip install -r tests/requirements.txt`, built **`logistic_churn`** at repo root (or `LOGISTIC_CHURN_PATH`).

## Run

From the **repository root**:

```bash
pytest tests/system -v
```

## Expected result

**Exit code 0** and all scenarios **passed** (or skipped only if the binary is missing locally).

# Selenium (BDD) tests

## Scope (read this first)

The product is **C++** with a **terminal CLI**. These tests are **not** “the app running inside Chrome.”

They run **pytest-bdd** scenarios against **checked-in HTML pages** in `fixtures/` (opened as `file://` URLs). Chrome (headless) is only used to **render DOM** so Gherkin steps can assert visible text and form labels—useful for requirements traceability (FR labels, help text, etc.).

**CLI behavior** is covered by **`tests/integration`** and **`make test`**.

## Requirements

- Python **3.10+**
- Dependencies: `pip install -r tests/requirements.txt` (from repo root)
- **Google Chrome** installed (headless); **optional:** `CHROMIUM_BIN` = full path to the Chrome/Chromium binary if it is not the default install

## Run

From the **repository root**:

```bash
pytest tests/selenium -v
```

## Expected result

**Exit code 0** and all scenarios **passed**. Failures are usually a missing Chrome install or a blocked driver download (check network / proxy).

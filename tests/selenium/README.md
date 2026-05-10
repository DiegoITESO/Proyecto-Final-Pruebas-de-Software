# Selenium (BDD) tests

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

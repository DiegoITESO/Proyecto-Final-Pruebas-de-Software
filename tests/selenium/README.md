# Selenium BDD tests

UI checks use **pytest-bdd** (Gherkin in `features/`, step definitions in `conftest.py`) and **headless Chrome** against static HTML under `tests/selenium/fixtures/`. Install Chrome (or Chromium) and Python deps, then run from the **repository root**.

```bash
pip install -r tests/selenium/requirements-selenium.txt
pytest tests/selenium
```

To collect scenarios without executing:

```bash
pytest tests/selenium --collect-only
```

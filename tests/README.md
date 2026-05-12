# Tests layout

The **C++ application** is exercised in the terminal. Automated checks use three separate layers:

| Layer | What it runs | Purpose |
|--------|----------------|----------|
| **C++ (Catch2)** | `make test` → `run_tests` | Unit tests for vectors, matrix, logger, etc. (`tests/*.cpp`). |
| **Python bootstrap** | `pytest tests/bootstrap` | **Compila si falta** el ejecutable y hace smoke de **`--help`** (arranque reproducible sin navegador). |
| **Python integration** | `pytest tests/integration` | Detailed **CLI** coverage with `unittest` (subprocess + stdin/stdout). |
| **Python system BDD** | `pytest tests/system` | **Gherkin + pytest-bdd** black-box scenarios against the same **`logistic_churn`** binary—**no browser** (replaces Selenium for this CLI project). |

**Canonical tree:** everything lives under `tests/` (`integration/`, `system/`, and `*.cpp` for Catch). Do not add a parallel `pruebas/` tree.

Details: `integration/README.md`, `system/README.md`.

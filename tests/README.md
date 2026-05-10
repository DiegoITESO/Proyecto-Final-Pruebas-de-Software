# Tests layout

The **C++ application** is exercised in the terminal. Automated checks use three separate layers:

| Layer | What it runs | Purpose |
|--------|----------------|----------|
| **C++ (Catch2)** | `make test` → `run_tests` | Unit tests for vectors, matrix, logger, etc. (`tests/*.cpp`). |
| **Python integration** | `pytest tests/integration` | End-to-end **CLI**: subprocess + stdin/stdout against the real `logistic_churn` binary. |
| **Python Selenium (BDD)** | `pytest tests/selenium` | **Acceptance / traceability**: opens **local HTML fixtures** under `tests/selenium/fixtures/` (file URLs). Chrome is only the driver for those static pages; it does **not** replace C++ tests or run a GUI version of the app. |

**Canonical tree:** everything lives under `tests/` (`integration/`, `selenium/`, and `*.cpp` for Catch). Do not add a parallel `pruebas/` tree.

Details: `integration/README.md`, `selenium/README.md`.

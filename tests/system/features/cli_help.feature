Feature: System CLI help
  Black-box checks for the compiled ``logistic_churn`` help output (replaces browser-based BDD).

  Scenario: Help exits zero and documents core modes
    When I run the CLI with argv "--help" and empty stdin
    Then the exit code is 0
    And stdout contains "--train"
    And stdout contains "--predict"
    And stdout contains "--evaluate"
    And stdout contains "Customer Churn Predictor"

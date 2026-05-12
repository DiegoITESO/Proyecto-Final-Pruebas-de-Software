Feature: System CLI error handling
  Invalid flags and missing inputs must fail without a successful exit code.

  Scenario: Unknown primary option fails
    When I run the CLI with argv "--bogusflag" and empty stdin
    Then the exit code is not 0
    And combined output contains "Unknown"

  Scenario: Training on missing dataset fails
    Given a missing CSV path for training
    When I run the CLI with argv "--train" and stdin from scenario
    Then the exit code is not 0

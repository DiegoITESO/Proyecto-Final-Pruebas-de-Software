Feature: Help fixture mirrors CLI --help output

  Scenario: Help root container is visible
    When I open the HTML fixture help.html
    Then test id "cli-help-root" is displayed

  Scenario: Help title matches product name
    When I open the HTML fixture help.html
    Then element id "help-title" contains "Customer Churn Predictor"

  Scenario: Help lists --train option
    When I open the HTML fixture help.html
    Then test id "opt-train" contains "--train"

  Scenario: Help lists --predict option
    When I open the HTML fixture help.html
    Then test id "opt-predict" contains "--predict"

  Scenario: Help documents train with evaluate combo
    When I open the HTML fixture help.html
    Then test id "opt-train-eval" contains "--evaluate"
    And test id "opt-train-eval" contains "--train"

  Scenario: Help mentions logs directory
    When I open the HTML fixture help.html
    Then test id "logs-note" contains "logs/"

  Scenario: Usage references executable name
    When I open the HTML fixture help.html
    Then element id "usage-line" contains "logistic_churn"

  Scenario: Example block includes train command
    When I open the HTML fixture help.html
    Then test id "ex-train" contains "./logistic_churn --train"

  Scenario: Example block includes evaluate command
    When I open the HTML fixture help.html
    Then test id "ex-eval" contains "--evaluate"

  Scenario: Example block includes predict command
    When I open the HTML fixture help.html
    Then test id "ex-predict" contains "./logistic_churn --predict"

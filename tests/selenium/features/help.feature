Feature: CLI help documentation fixture
  Mirrors the C++ ArgParser::showHelp output as static HTML for regression checks.

  Scenario: Help root container is visible
    Given I open the HTML fixture "help.html"
    Then the element with data-testid "cli-help-root" should be visible

  Scenario: Help title matches program branding
    Given I open the HTML fixture "help.html"
    Then the element with id "help-title" should contain "Customer Churn Predictor"

  Scenario: Help documents the train option
    Given I open the HTML fixture "help.html"
    Then the element with data-testid "opt-train" should contain "--train"

  Scenario: Help documents the predict option
    Given I open the HTML fixture "help.html"
    Then the element with data-testid "opt-predict" should contain "--predict"

  Scenario: Help documents train with evaluate
    Given I open the HTML fixture "help.html"
    Then the element with data-testid "opt-train-eval" should contain "--evaluate"
    And the element with data-testid "opt-train-eval" should contain "--train"

  Scenario: Help mentions log directory layout
    Given I open the HTML fixture "help.html"
    Then the element with data-testid "logs-note" should contain "logs/"

  Scenario: Usage line names the executable
    Given I open the HTML fixture "help.html"
    Then the element with id "usage-line" should contain "logistic_churn"

  Scenario: Example block shows train command
    Given I open the HTML fixture "help.html"
    Then the element with data-testid "ex-train" should contain "./logistic_churn --train"

  Scenario: Example block shows evaluate flow
    Given I open the HTML fixture "help.html"
    Then the element with data-testid "ex-eval" should contain "--evaluate"

  Scenario: Example block shows predict command
    Given I open the HTML fixture "help.html"
    Then the element with data-testid "ex-predict" should contain "./logistic_churn --predict"

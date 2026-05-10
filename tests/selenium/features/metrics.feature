Feature: Evaluation metrics fixture
  Static sample output aligned with handleEvaluate console metrics.

  Scenario: Accuracy label is present
    Given I open the HTML fixture "metrics.html"
    Then the element with data-testid "lbl-accuracy" should contain "Accuracy"

  Scenario: Precision label is present
    Given I open the HTML fixture "metrics.html"
    Then the element with data-testid "lbl-precision" should contain "Precision"

  Scenario: Recall label is present
    Given I open the HTML fixture "metrics.html"
    Then the element with data-testid "lbl-recall" should contain "Recall"

  Scenario: F1 label is present
    Given I open the HTML fixture "metrics.html"
    Then the element with data-testid "lbl-f1" should contain "F1"

  Scenario: Sample CLI block matches evaluate format
    Given I open the HTML fixture "metrics.html"
    Then the element with data-testid "sample-cli-out" should contain "Accuracy:"
    And the element with data-testid "sample-cli-out" should contain "F1 score:"

  Scenario: FR-08 trace note is visible
    Given I open the HTML fixture "metrics.html"
    Then the element with data-testid "fr08" should contain "FR-08"

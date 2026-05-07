Feature: Evaluation metrics fixture

  Scenario: Accuracy label is shown
    When I open the HTML fixture metrics.html
    Then test id "lbl-accuracy" contains "Accuracy"

  Scenario: Precision label is shown
    When I open the HTML fixture metrics.html
    Then test id "lbl-precision" contains "Precision"

  Scenario: Recall label is shown
    When I open the HTML fixture metrics.html
    Then test id "lbl-recall" contains "Recall"

  Scenario: F1 label is shown
    When I open the HTML fixture metrics.html
    Then test id "lbl-f1" contains "F1"

  Scenario: Sample CLI output mirrors evaluate formatting
    When I open the HTML fixture metrics.html
    Then test id "sample-cli-out" contains "Accuracy:"
    And test id "sample-cli-out" contains "F1 score:"

  Scenario: FR-08 note is visible
    When I open the HTML fixture metrics.html
    Then test id "fr08" contains "FR-08"

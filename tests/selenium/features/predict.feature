Feature: Prediction wizard fixture
  Documents the interactive --predict CLI prompts.

  Scenario: Predict page declares prediction flow
    Given I open the HTML fixture "predict.html"
    Then the element with data-testid "predict-title" should contain "Prediction wizard"

  Scenario: Weights file input is required
    Given I open the HTML fixture "predict.html"
    Then the input with data-testid "input-weights" should be required

  Scenario: Predict dataset input is required
    Given I open the HTML fixture "predict.html"
    Then the input with data-testid "input-predict-dataset" should be required

  Scenario: Predict output path is required
    Given I open the HTML fixture "predict.html"
    Then the input with data-testid "input-predict-output" should be required

  Scenario: Predict header no option is selectable
    Given I open the HTML fixture "predict.html"
    When I click the radio with data-testid "pheader-n"
    Then the radio with data-testid "pheader-n" should be selected

  Scenario: FR-09 trace note is visible
    Given I open the HTML fixture "predict.html"
    Then the element with data-testid "fr09-note" should contain "FR-09"

  Scenario: JSON model hint is visible
    Given I open the HTML fixture "predict.html"
    Then the element with data-testid "json-hint" should contain "JSON"

  Scenario: CSV output references FR-10
    Given I open the HTML fixture "predict.html"
    Then the element with data-testid "csv-hint" should contain "FR-10"

  Scenario: Filled predict form shows result panel
    Given I open the HTML fixture "predict.html"
    When I type "m.json" into data-testid "input-weights"
    And I type "d.csv" into data-testid "input-predict-dataset"
    And I type "p.csv" into data-testid "input-predict-output"
    And I click the button with data-testid "btn-predict-run"
    Then the element with data-testid "predict-result" should become visible within seconds

  Scenario: Weights placeholder references JSON weights
    Given I open the HTML fixture "predict.html"
    Then the input with data-testid "input-weights" placeholder should contain "weights.json"

  Scenario: Predict optional drops area is visible
    Given I open the HTML fixture "predict.html"
    Then the element with data-testid "input-predict-drops" should be visible

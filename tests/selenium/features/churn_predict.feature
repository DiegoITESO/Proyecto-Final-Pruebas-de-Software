Feature: Predict wizard fixture

  Scenario: Predict page title references prediction flow
    When I open the HTML fixture predict.html
    Then test id "predict-title" contains "Prediction wizard"

  Scenario: Weights file input is required
    When I open the HTML fixture predict.html
    Then test id "input-weights" has required attribute

  Scenario: Predict dataset input is required
    When I open the HTML fixture predict.html
    Then test id "input-predict-dataset" has required attribute

  Scenario: Predict output path is required
    When I open the HTML fixture predict.html
    Then test id "input-predict-output" has required attribute

  Scenario: Header no toggle can be selected
    When I open the HTML fixture predict.html
    When I click test id "pheader-n"
    Then test id "pheader-n" is selected

  Scenario: FR-09 note is visible
    When I open the HTML fixture predict.html
    Then test id "fr09-note" contains "FR-09"

  Scenario: JSON hint documents model format
    When I open the HTML fixture predict.html
    Then test id "json-hint" contains "JSON"

  Scenario: CSV hint references FR-10
    When I open the HTML fixture predict.html
    Then test id "csv-hint" contains "FR-10"

  Scenario: Filled predict form shows result panel
    When I open the HTML fixture predict.html
    When I type "m.json" into test id "input-weights"
    When I type "d.csv" into test id "input-predict-dataset"
    When I type "p.csv" into test id "input-predict-output"
    When I submit predict form
    Then test id "predict-result" becomes visible

  Scenario: Weights placeholder references JSON file
    When I open the HTML fixture predict.html
    Then test id "input-weights" placeholder contains "weights.json"

  Scenario: Optional drops area is visible
    When I open the HTML fixture predict.html
    Then test id "input-predict-drops" is displayed

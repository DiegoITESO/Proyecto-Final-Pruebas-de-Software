Feature: Train wizard fixture

  Scenario: Train page title references training flow
    When I open the HTML fixture train.html
    Then test id "train-page-title" contains "Training wizard"

  Scenario: Train form is visible
    When I open the HTML fixture train.html
    Then test id "train-form" is displayed

  Scenario: Dataset path is marked required for accessibility
    When I open the HTML fixture train.html
    Then test id "input-dataset" has aria-required true

  Scenario: Output path is marked required for accessibility
    When I open the HTML fixture train.html
    Then test id "input-output" has aria-required true

  Scenario: Header yes option can be selected
    When I open the HTML fixture train.html
    When I click test id "header-y"
    Then test id "header-y" is selected

  Scenario: Header no option can be selected
    When I open the HTML fixture train.html
    When I click test id "header-n"
    Then test id "header-n" is selected

  Scenario: Default churn column index matches fixture
    When I open the HTML fixture train.html
    Then test id "input-churn" attribute "value" equals "5"

  Scenario: Drop columns hint mentions correlation guidance
    When I open the HTML fixture train.html
    Then test id "drop-hint" contains "weakly correlated"

  Scenario: Default learning rate matches fixture
    When I open the HTML fixture train.html
    Then test id "input-alpha" attribute "value" equals "0.01"

  Scenario: Default epochs match fixture
    When I open the HTML fixture train.html
    Then test id "input-epochs" attribute "value" equals "100"

  Scenario: Valid train form shows summary panel
    When I open the HTML fixture train.html
    When I type "data/x.csv" into test id "input-dataset"
    When I type "models/w.json" into test id "input-output"
    When I submit train form
    Then test id "train-result" becomes visible
    Then test id "train-result-text" contains "Summary"

  Scenario: Empty dataset path shows validation error
    When I open the HTML fixture train.html
    When I clear test id "input-dataset"
    When I type "out.json" into test id "input-output"
    When I submit train form
    Then test id "train-error" becomes visible
    Then test id "train-error" contains substring "required" case-insensitive

  Scenario: Dataset placeholder cites sample CSV name
    When I open the HTML fixture train.html
    Then test id "input-dataset" placeholder contains "customer_data.csv"

  Scenario: Output placeholder cites weights JSON
    When I open the HTML fixture train.html
    Then test id "input-output" placeholder contains "weights.json"

  Scenario: FR-02 trace note is visible
    When I open the HTML fixture train.html
    Then test id "fr02-note" contains "FR-02"

  Scenario: Normalization documentation references mean zero
    When I open the HTML fixture train.html
    Then test id "norm-doc" contains "mean 0"

  Scenario: Encoding documentation mentions one-hot
    When I open the HTML fixture train.html
    Then test id "encode-doc" contains "one-hot"

  Scenario: Drop list uses multiline textarea
    When I open the HTML fixture train.html
    Then test id "input-drops" tag name is "textarea"

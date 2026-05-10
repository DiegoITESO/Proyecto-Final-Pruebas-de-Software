Feature: Training wizard fixture
  Documents the interactive --train CLI prompts.

  Scenario: Train page declares training flow
    Given I open the HTML fixture "train.html"
    Then the element with data-testid "train-page-title" should contain "Training wizard"

  Scenario: Train parameter form is visible
    Given I open the HTML fixture "train.html"
    Then the element with data-testid "train-form" should be visible

  Scenario: Dataset path is marked required for accessibility
    Given I open the HTML fixture "train.html"
    Then the element with data-testid "input-dataset" attribute "aria-required" should equal "true"

  Scenario: Model output path is marked required
    Given I open the HTML fixture "train.html"
    Then the element with data-testid "input-output" attribute "aria-required" should equal "true"

  Scenario: Header yes radio can be selected
    Given I open the HTML fixture "train.html"
    When I click the radio with data-testid "header-y"
    Then the radio with data-testid "header-y" should be selected

  Scenario: Header no radio can be selected
    Given I open the HTML fixture "train.html"
    When I click the radio with data-testid "header-n"
    Then the radio with data-testid "header-n" should be selected

  Scenario: Default churn column index matches fixture
    Given I open the HTML fixture "train.html"
    Then the input with data-testid "input-churn" value should equal "5"

  Scenario: Drop-columns hint references weak correlation
    Given I open the HTML fixture "train.html"
    Then the element with data-testid "drop-hint" should contain "weakly correlated"

  Scenario: Default learning rate matches fixture
    Given I open the HTML fixture "train.html"
    Then the input with data-testid "input-alpha" value should equal "0.01"

  Scenario: Default epochs value matches fixture
    Given I open the HTML fixture "train.html"
    Then the input with data-testid "input-epochs" value should equal "100"

  Scenario: Valid train paths show summary panel
    Given I open the HTML fixture "train.html"
    When I type "data/x.csv" into data-testid "input-dataset"
    And I type "models/w.json" into data-testid "input-output"
    And I click the button with data-testid "btn-submit-train"
    Then the element with data-testid "train-result" should become visible within seconds
    And the element with data-testid "train-result-text" should contain "Summary"

  Scenario: Empty dataset path shows validation error
    Given I open the HTML fixture "train.html"
    When I clear the input with data-testid "input-dataset"
    And I type "out.json" into data-testid "input-output"
    And I click the button with data-testid "btn-submit-train"
    Then the element with data-testid "train-error" should become visible within seconds
    And the element with data-testid "train-error" should contain ignoring case "required"

  Scenario: Dataset placeholder references sample CSV
    Given I open the HTML fixture "train.html"
    Then the input with data-testid "input-dataset" placeholder should contain "customer_data.csv"

  Scenario: Output placeholder references weights JSON
    Given I open the HTML fixture "train.html"
    Then the input with data-testid "input-output" placeholder should contain "weights.json"

  Scenario: FR-02 trace note is visible
    Given I open the HTML fixture "train.html"
    Then the element with data-testid "fr02-note" should contain "FR-02"

  Scenario: Normalization doc references mean centering
    Given I open the HTML fixture "train.html"
    Then the element with data-testid "norm-doc" should contain "mean 0"

  Scenario: Encoding doc mentions one-hot
    Given I open the HTML fixture "train.html"
    Then the element with data-testid "encode-doc" should contain "one-hot"

  Scenario: Drop columns input is a textarea
    Given I open the HTML fixture "train.html"
    Then the element with data-testid "input-drops" tag name should be "textarea"

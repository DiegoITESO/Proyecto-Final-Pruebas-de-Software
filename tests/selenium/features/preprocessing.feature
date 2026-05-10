Feature: Preprocessing documentation fixture
  Describes CSVReader preprocessing rules.

  Scenario: Yes or no maps to floating targets
    Given I open the HTML fixture "preprocessing.html"
    Then the element with data-testid "yes-no-map" should contain "1.0"

  Scenario: Z-score normalization is documented
    Given I open the HTML fixture "preprocessing.html"
    Then the element with data-testid "norm-text" should contain "z-score"

  Scenario: One-hot encoding for categoricals is documented
    Given I open the HTML fixture "preprocessing.html"
    Then the element with data-testid "onehot-text" should contain "one-hot"

  Scenario: FR-03 CSV row validation is documented
    Given I open the HTML fixture "preprocessing.html"
    Then the element with data-testid "fr03-csv" should contain "unequal"

  Scenario: Train or test split ratio is documented
    Given I open the HTML fixture "preprocessing.html"
    Then the element with data-testid "split8020" should contain "80%"
    And the element with data-testid "split8020" should contain "20%"

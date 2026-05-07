Feature: Preprocessing documentation fixture

  Scenario: Yes or no mapping documents numeric targets
    When I open the HTML fixture preprocessing.html
    Then test id "yes-no-map" contains "1.0"

  Scenario: Normalization section references z-score
    When I open the HTML fixture preprocessing.html
    Then test id "norm-text" contains "z-score"

  Scenario: One-hot section is documented
    When I open the HTML fixture preprocessing.html
    Then test id "onehot-text" contains "one-hot"

  Scenario: CSV validation references uneven rows
    When I open the HTML fixture preprocessing.html
    Then test id "fr03-csv" contains "unequal"

  Scenario: Train test split documents 80 and 20 percent
    When I open the HTML fixture preprocessing.html
    Then test id "split8020" contains "80%"
    And test id "split8020" contains "20%"

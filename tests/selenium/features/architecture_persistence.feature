Feature: Architecture and persistence documentation fixtures
  High-level module map and requirement traceability.

  Scenario: Architecture lists Vector module
    Given I open the HTML fixture "architecture.html"
    Then the element with data-testid "mod-vector" should contain "Vector"

  Scenario: Architecture lists Matrix module
    Given I open the HTML fixture "architecture.html"
    Then the element with data-testid "mod-matrix" should contain "Matrix"

  Scenario: Architecture lists Splitter module
    Given I open the HTML fixture "architecture.html"
    Then the element with data-testid "mod-splitter" should contain "Splitter"

  Scenario: Architecture documents unknown CLI option error
    Given I open the HTML fixture "architecture.html"
    Then the element with data-testid "cli-unknown" should contain "Unknown option"

  Scenario: Persistence page references FR-07 JSON export
    Given I open the HTML fixture "persistence.html"
    Then the element with data-testid "fr07" should contain "FR-07"

  Scenario: Persistence page references FR-11 model load
    Given I open the HTML fixture "persistence.html"
    Then the element with data-testid "fr11" should contain "FR-11"

  Scenario: Persistence page references FR-06 SGD training
    Given I open the HTML fixture "persistence.html"
    Then the element with data-testid "fr06" should contain "FR-06"

  Scenario: Persistence mentions Catch2 unit tests
    Given I open the HTML fixture "persistence.html"
    Then the element with data-testid "nfr-tests" should contain "Catch2"

  Scenario: Architecture documents Logger log directory
    Given I open the HTML fixture "architecture.html"
    Then the element with data-testid "mod-logger" should contain "logs/"

  Scenario: Architecture lists CSVReader module
    Given I open the HTML fixture "architecture.html"
    Then the element with data-testid "mod-csv" should contain "CSVReader"

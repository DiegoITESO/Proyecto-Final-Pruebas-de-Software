Feature: Architecture and persistence documentation fixtures

  Scenario: Architecture lists Vector module
    When I open the HTML fixture architecture.html
    Then test id "mod-vector" contains "Vector"

  Scenario: Architecture lists Matrix module
    When I open the HTML fixture architecture.html
    Then test id "mod-matrix" contains "Matrix"

  Scenario: Architecture lists Splitter module
    When I open the HTML fixture architecture.html
    Then test id "mod-splitter" contains "Splitter"

  Scenario: Architecture documents unknown CLI option error
    When I open the HTML fixture architecture.html
    Then test id "cli-unknown" contains "Unknown option"

  Scenario: Architecture documents Logger and logs directory
    When I open the HTML fixture architecture.html
    Then test id "mod-logger" contains "logs/"

  Scenario: Architecture lists CSVReader module
    When I open the HTML fixture architecture.html
    Then test id "mod-csv" contains "CSVReader"

  Scenario: Persistence page cites FR-07 JSON export
    When I open the HTML fixture persistence.html
    Then test id "fr07" contains "FR-07"

  Scenario: Persistence page cites FR-11 model loading
    When I open the HTML fixture persistence.html
    Then test id "fr11" contains "FR-11"

  Scenario: Persistence page cites FR-06 training
    When I open the HTML fixture persistence.html
    Then test id "fr06" contains "FR-06"

  Scenario: Persistence page references Catch2 unit tests
    When I open the HTML fixture persistence.html
    Then test id "nfr-tests" contains "Catch2"

Feature: Product dashboard fixture
  Entry page linking to documentation fixtures.

  Scenario: Dashboard shows product name
    Given I open the HTML fixture "dashboard.html"
    Then the element with data-testid "dashboard-title" should contain "Customer Churn"

  Scenario: Dashboard help link targets help fixture
    Given I open the HTML fixture "dashboard.html"
    Then the link with data-testid "nav-help" href should end with "help.html"

  Scenario: Dashboard mentions logistic regression
    Given I open the HTML fixture "dashboard.html"
    Then the element with data-testid "blurb-logistic" should contain "logistic regression"

  Scenario: Dashboard mentions CSVReader
    Given I open the HTML fixture "dashboard.html"
    Then the element with data-testid "blurb-csv" should contain "CSVReader"

  Scenario: Dashboard mentions stochastic gradient descent
    Given I open the HTML fixture "dashboard.html"
    Then the element with data-testid "blurb-sgd" should contain "stochastic gradient descent"

  Scenario: Dashboard help navigation loads help DOM
    Given I open the HTML fixture "dashboard.html"
    When I click the element with data-testid "nav-help"
    Then the element with data-testid "cli-help-root" should become visible within seconds
    And the element with id "help-title" should contain "Command Line Interface"

  Scenario: Architecture nav link target
    Given I open the HTML fixture "dashboard.html"
    Then the link with data-testid "nav-arch" href should end with "architecture.html"

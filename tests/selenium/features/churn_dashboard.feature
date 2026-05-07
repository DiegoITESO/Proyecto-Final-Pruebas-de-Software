Feature: Dashboard fixture navigation and copy

  Scenario: Dashboard shows product title
    When I open the HTML fixture dashboard.html
    Then test id "dashboard-title" contains "Customer Churn"

  Scenario: Help navigation link targets help.html
    When I open the HTML fixture dashboard.html
    Then test id "nav-help" href ends with "help.html"

  Scenario: Blurb mentions logistic regression
    When I open the HTML fixture dashboard.html
    Then test id "blurb-logistic" contains "logistic regression"

  Scenario: Blurb references CSVReader
    When I open the HTML fixture dashboard.html
    Then test id "blurb-csv" contains "CSVReader"

  Scenario: Blurb documents SGD
    When I open the HTML fixture dashboard.html
    Then test id "blurb-sgd" contains "stochastic gradient descent"

  Scenario: Clicking help navigates to help DOM
    When I open the HTML fixture dashboard.html
    When I click test id "nav-help"
    Then test id "cli-help-root" is present
    Then element id "help-title" contains "Command Line Interface"

  Scenario: Architecture link points to architecture fixture
    When I open the HTML fixture dashboard.html
    Then test id "nav-arch" href ends with "architecture.html"

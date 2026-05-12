Feature: System CLI train and predict
  End-to-end model training and probability export using the real binary and stdin prompts.

  Scenario: Train a model then emit churn probabilities
    Given the training workspace is prepared
    When I run training with scripted stdin
    Then the exit code is 0
    And the model JSON file was written
    When I run prediction with scripted stdin
    Then the exit code is 0
    And each prediction line is a float between 0 and 1

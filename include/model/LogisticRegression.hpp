#ifndef CUSTOMER_CHURN_PREDICTION_LOGISTICREGRESSION_HPP
#define CUSTOMER_CHURN_PREDICTION_LOGISTICREGRESSION_HPP
#include <cmath>
#include <cstddef>
#include <iostream>
#include <stdexcept>
#include <vector>

#include "../core/Matrix.hpp"
#include "../core/ProcessedData.hpp"
#include "../core/Vector.hpp"
#include "../log/Logger.hpp"
#include "../utils/json.hpp"

/**
 * @class LogisticRegression
 * @brief Implements a logistic regression model for binary classification.
 */
class LogisticRegression {
  friend struct LogisticRegressionTester;

 public:
  /**
   * @brief Constructs a Logistic Regression model.
   * @param n_features The number of features in the input data.
   */
  explicit LogisticRegression(size_t n_features);

  /**
   * @brief Predicts the probability of the positive class (churn) for a single
   * input vector.
   * @param x The input feature vector.
   * @return The predicted probability [0.0, 1.0].
   */
  double predict(const Vector& x) const;

  /**
   * @brief Trains the model using stochastic gradient descent.
   * @param data The preprocessed training data.
   * @param alpha The learning rate.
   * @param epochs The number of training epochs.
   */
  void train(const ProcessedData& data, double alpha, int epochs);

  /**
   * @brief Computes the accuracy of the model on test data.
   * @param test The preprocessed testing data.
   * @return The accuracy [0.0, 1.0].
   */
  double accuracy(const ProcessedData& test) const;

  /**
   * @brief Computes the precision of the model on test data.
   * Of all customers predicted to churn, how many really did?
   * @param test The preprocessed testing data.
   * @return The precision [0.0, 1.0].
   */
  double precision(const ProcessedData& test) const;

  /**
   * @brief Computes the recall of the model on test data.
   * Of all real churners, how many were correctly identified?
   * @param test The preprocessed testing data.
   * @return The recall [0.0, 1.0].
   */
  double recall(const ProcessedData& test) const;

  /**
   * @brief Computes the F1 Score of the model on test data.
   * @param test The preprocessed testing data.
   * @return The F1 Score [0.0, 1.0].
   */
  double f1Score(const ProcessedData& test) const;

  /**
   * @brief Saves the trained model parameters (weights and bias) to a JSON
   * file.
   * @param filename The output JSON file path.
   */
  void save(const std::string& filename) const;

  /**
   * @brief Loads model parameters (weights and bias) from a JSON file.
   * @param filename The input JSON file path.
   */
  void load(const std::string& filename);

 private:
  Vector weights;  ///< The learned feature weights.
  double bias;     ///< The learned bias term.
  double loss;     ///< Current loss value during training.

  /**
   * @brief Computes the sigmoid activation function.
   * @param z The linear combination (w*x + b).
   * @return The sigmoid probability.
   */
  static double sigmoid(const double z);

  /**
   * @brief Calculates the Cross Entropy Loss for a single prediction.
   * @param y_true The true label (0.0 or 1.0).
   * @param y_pred The predicted probability.
   * @return The loss value.
   */
  static double computeLoss(const double y_true, const double y_pred);

  /**
   * @brief Updates weights and bias based on a single training example.
   * @param data The preprocessed data.
   * @param alpha The learning rate.
   */
  void updateWeights(const ProcessedData& data, const double& alpha);
};

#endif
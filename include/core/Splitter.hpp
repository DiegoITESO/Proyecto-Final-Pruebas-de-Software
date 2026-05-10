#ifndef CUSTOMER_CHURN_PREDICTION_SPLITTER_HPP
#define CUSTOMER_CHURN_PREDICTION_SPLITTER_HPP
#include <algorithm>
#include <cstddef>
#include <iostream>
#include <random>
#include <stdexcept>
#include <vector>

#include "Matrix.hpp"
#include "ProcessedData.hpp"
#include "Vector.hpp"
/**
 * @struct Splitter
 * @brief Abstract base class for splitting data into training and testing sets.
 */
struct Splitter {
  /**
   * @brief Splits the provided data according to the given ratio.
   * @param data The processed data to split.
   * @param ratio The ratio of the data to keep for training (e.g., 0.8 for
   * 80%).
   * @return A pair containing the training data and testing data respectively.
   */
  virtual std::pair<ProcessedData, ProcessedData> split(
      const ProcessedData& data, const double ratio) = 0;
  
  /**
   * @brief Virtual destructor.
   */
  virtual ~Splitter() = default;
};

/**
 * @struct RandomSplitter
 * @brief Implementation of Splitter that randomly shuffles and splits the data.
 */
struct RandomSplitter : public Splitter {
  /**
   * @brief Splits the provided data randomly.
   * @param data The processed data to split.
   * @param ratio The ratio of the data to keep for training.
   * @return A pair containing the training data and testing data respectively.
   */
  std::pair<ProcessedData, ProcessedData> split(const ProcessedData& data,
                                                const double ratio) override;
};
#endif
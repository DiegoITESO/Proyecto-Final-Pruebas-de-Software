#ifndef CUSTOMER_CHURN_PREDICTION_PROCESSEDDATA_HPP
#define CUSTOMER_CHURN_PREDICTION_PROCESSEDDATA_HPP
#include <string>
#include <vector>

#include "Matrix.hpp"
#include "Vector.hpp"
/**
 * @struct ProcessedData
 * @brief Holds preprocessed data ready for model training or prediction.
 */
struct ProcessedData {
  Matrix features;                   ///< Matrix containing the feature vectors.
  std::vector<std::string> headers;  ///< List of feature names (headers).
  Vector churnResults;  ///< Vector containing the target labels (e.g., churn: 1
                        ///< or 0).
};
#endif
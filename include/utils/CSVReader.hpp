#ifndef CUSTOMER_CHURN_PREDICTION_CSVREADER_HPP
#define CUSTOMER_CHURN_PREDICTION_CSVREADER_HPP
#include <algorithm>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "../core/Matrix.hpp"
#include "../core/Vector.hpp"
#include "../include/core/ProcessedData.hpp"
#include "../include/utils/StringHandling.hpp"
/**
 * @namespace CSVReader
 * @brief Provides functionality to read and preprocess CSV files.
 */
namespace CSVReader {

/**
 * @brief Reads a CSV file and parses it into a 2D string array.
 * @param filePath The path to the CSV file.
 * @return A vector of string vectors representing rows and columns.
 */
std::vector<std::vector<std::string>> readCSV(const std::string& filePath);

/**
 * @brief Preprocesses the raw CSV data into numeric features and labels.
 * 
 * Handles string conversions, one-hot encoding for categorical variables,
 * dropping specified columns, and separating the target label.
 * 
 * @param data The raw 2D string data.
 * @param hasHeader True if the first row is a header.
 * @param churnColumn The index of the target column (label).
 * @param dropColumns A vector of column indices to remove.
 * @return A ProcessedData structure containing the ready-to-use data.
 */
ProcessedData preprocess(const std::vector<std::vector<std::string>>& data,
                         bool hasHeader, size_t churnColumn,
                         std::vector<size_t> dropColumns);

/**
 * @brief Normalizes the features in the ProcessedData structure (Z-score normalization).
 * @param data The ProcessedData containing the features to normalize.
 */
void normalizeFeatures(ProcessedData& data);

}  // namespace CSVReader
#endif
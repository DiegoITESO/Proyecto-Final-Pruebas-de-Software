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
namespace CSVReader {
std::vector<std::vector<std::string>> readCSV(const std::string& filePath);
ProcessedData preprocess(const std::vector<std::vector<std::string>>& data,
                         bool hasHeader, size_t churnColumn,
                         std::vector<size_t> dropColumns);
void normalizeFeatures(ProcessedData& data);
}  // namespace CSVReader
#endif
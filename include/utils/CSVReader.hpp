#ifndef CUSTOMER_CHURN_PREDICTION_CSVREADER_HPP
#define CUSTOMER_CHURN_PREDICTION_CSVREADER_HPP
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <vector>
#include <string>
#include <stdexcept>
#include <unordered_map>
#include <unordered_set>
#include "../core/Vector.hpp"
#include "../core/Matrix.hpp"
#include "../include/utils/StringHandling.hpp"
#include "../include/core/ProcessedData.hpp"
namespace CSVReader
{
    std::vector<std::vector<std::string>> readCSV(const std::string& filePath);
    ProcessedData preprocess( const std::vector<std::vector<std::string>>& data,
                                    bool hasHeader,
                                    size_t churnColumn,
                                    std::vector<size_t> dropColumns);
    void normalizeFeatures(ProcessedData& data);
}
#endif
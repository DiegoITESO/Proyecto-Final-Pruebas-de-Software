#ifndef CUSTOMER_CHURN_PREDICTION_PROCESSEDDATA_HPP
#define CUSTOMER_CHURN_PREDICTION_PROCESSEDDATA_HPP
#include <vector>
#include <string>
#include "Matrix.hpp"
#include "Vector.hpp"
struct ProcessedData
{
    Matrix features;
    std::vector<std::string> headers;
    Vector churnResults;
};
#endif
#ifndef CUSTOMER_CHURN_PREDICTION_SPLITTER_HPP
#define CUSTOMER_CHURN_PREDICTION_SPLITTER_HPP
#include <iostream>
#include <stdexcept>
#include <cstddef>
#include <algorithm>
#include <random>
#include <vector>
#include "Matrix.hpp"
#include "Vector.hpp"
#include "ProcessedData.hpp"
struct Splitter
{
    virtual std::pair<ProcessedData, ProcessedData> split(const ProcessedData& data, const double ratio) = 0;
    virtual ~Splitter() = default;
};

struct RandomSplitter : public Splitter
{
    std::pair<ProcessedData, ProcessedData> split(const ProcessedData& data, const double ratio) override;
};
#endif
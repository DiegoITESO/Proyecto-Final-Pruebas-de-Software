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
struct Splitter {
  virtual std::pair<ProcessedData, ProcessedData> split(
      const ProcessedData& data, const double ratio) = 0;
  virtual ~Splitter() = default;
};

struct RandomSplitter : public Splitter {
  std::pair<ProcessedData, ProcessedData> split(const ProcessedData& data,
                                                const double ratio) override;
};
#endif
#ifndef CUSTOMER_CHURN_PREDICTION_STRINGHANDLING_HPP
#define CUSTOMER_CHURN_PREDICTION_STRINGHANDLING_HPP
#include <algorithm>
#include <cctype>
#include <sstream>
#include <string>
namespace StringHandling {
bool isNumber(const std::string& s);
std::string toLower(const std::string& s);
}  // namespace StringHandling
#endif
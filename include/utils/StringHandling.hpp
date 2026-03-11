#ifndef CUSTOMER_CHURN_PREDICTION_STRINGHANDLING_HPP
#define CUSTOMER_CHURN_PREDICTION_STRINGHANDLING_HPP
#include <string>
#include <algorithm>
#include <sstream>
#include <cctype>
namespace StringHandling
{
    bool isNumber(const std::string& s);
    std::string toLower(const std::string& s);
}
#endif
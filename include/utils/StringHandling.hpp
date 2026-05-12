#ifndef CUSTOMER_CHURN_PREDICTION_STRINGHANDLING_HPP
#define CUSTOMER_CHURN_PREDICTION_STRINGHANDLING_HPP
#include <algorithm>
#include <cctype>
#include <sstream>
#include <string>
/**
 * @namespace StringHandling
 * @brief Utility functions for processing and validating strings.
 */
namespace StringHandling {

/**
 * @brief Checks if a string represents a valid numeric value.
 * @param s The string to check.
 * @return True if the string is numeric, false otherwise.
 */
bool isNumber(const std::string& s);

/**
 * @brief Converts a string to lowercase.
 * @param s The input string.
 * @return The lowercase version of the string.
 */
std::string toLower(const std::string& s);

}  // namespace StringHandling
#endif
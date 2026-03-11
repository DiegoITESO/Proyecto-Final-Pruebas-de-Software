#include "../../include/utils/StringHandling.hpp"
bool StringHandling::isNumber(const std::string& s)
{
    std::istringstream iss(s);
    double d;
    return (iss >> std::noskipws >> d) && iss.eof();
};
std::string StringHandling::toLower(const std::string& s)
{
    std::string myString = s;
    myString.erase(std::remove_if(myString.begin(), myString.end(),
                     [](char c) { return std::isspace(c); }), myString.end());
    std::transform(myString.begin(), myString.end(), myString.begin(),
                   [](unsigned char c){ return std::tolower(c); });
    return myString;
};
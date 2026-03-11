#ifndef CUSTOMER_CHURN_PREDICTION_LOGGER_HPP
#define CUSTOMER_CHURN_PREDICTION_LOGGER_HPP
#include<fstream>
#include<string>
#include<cstddef>
#include<stdexcept>
#include<mutex>
#include<ctime>
#include<iomanip>
#include<iostream>
class Logger
{
    public:
        static Logger& instance();
        void set_file(const std::string& filename);
        void log(const std::string& message);
        void reset();
    private:
        std::ofstream file_;
        std::mutex mutex_;
        Logger() = default;
        Logger(const Logger&) = delete;
        Logger& operator= (const Logger&) = delete;
        Logger(Logger&&) = delete;
        Logger& operator=(Logger&&) = delete;
};
#endif
#include"../../include/log/Logger.hpp"

//----------Logger methods----------//
Logger& Logger::instance()
{
    static Logger instance;
    return instance;
};

void Logger::set_file(const std::string& filename)
{
    std::lock_guard<std::mutex> lock(mutex_);
    file_.open(filename);
};

void Logger::log(const std::string& message)
{
    std::lock_guard<std::mutex> lock(mutex_);
    std::time_t now = std::time(nullptr);
    std::tm* local_tm = std::localtime(&now);
    if(file_.is_open())
        file_ << std::put_time(local_tm, "%Y-%m-%d %H:%M:%S") << " | " << message << std::endl;
    else
        std::cerr << std::put_time(local_tm, "%Y-%m-%d %H:%M:%S") << " | " << message << std::endl;
};

void Logger::reset()
{
    std::lock_guard<std::mutex> lock(mutex_);
    file_.close();
    file_.clear();
};
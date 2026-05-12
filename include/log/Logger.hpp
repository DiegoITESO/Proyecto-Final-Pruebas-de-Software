#ifndef CUSTOMER_CHURN_PREDICTION_LOGGER_HPP
#define CUSTOMER_CHURN_PREDICTION_LOGGER_HPP
#include <cstddef>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <mutex>
#include <stdexcept>
#include <string>
/**
 * @class Logger
 * @brief Singleton class for logging messages to a file.
 */
class Logger {
 public:
  /**
   * @brief Retrieves the singleton instance of the Logger.
   * @return Reference to the Logger instance.
   */
  static Logger& instance();

  /**
   * @brief Sets the output log file.
   * @param filename The name of the file to write logs to.
   */
  void set_file(const std::string& filename);

  /**
   * @brief Logs a message to the currently set log file in a thread-safe
   * manner.
   * @param message The message to log.
   */
  void log(const std::string& message);

  /**
   * @brief Closes the current log file if open.
   */
  void reset();

 private:
  std::ofstream file_;  ///< The output file stream.
  std::mutex mutex_;    ///< Mutex for thread-safe logging.

  /**
   * @brief Private constructor to enforce Singleton pattern.
   */
  Logger() = default;

  // Deleted copy and move constructors/assignment operators.
  Logger(const Logger&) = delete;
  Logger& operator=(const Logger&) = delete;
  Logger(Logger&&) = delete;
  Logger& operator=(Logger&&) = delete;
};
#endif
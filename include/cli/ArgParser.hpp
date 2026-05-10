#ifndef CUSTOMER_CHURN_PREDICTION_ARGPARSER_HPP
#define CUSTOMER_CHURN_PREDICTION_ARGPARSER_HPP
#include <chrono>
#include <cmath>
#include <format>
#include <iostream>
#include <string>
#include <vector>

#include "../core/ProcessedData.hpp"
#include "../core/Splitter.hpp"
#include "../log/Logger.hpp"
#include "../model/LogisticRegression.hpp"
#include "../utils/CSVReader.hpp"

/**
 * @class ArgParser
 * @brief Handles parsing of command-line arguments and orchestrates the execution mode.
 * 
 * The ArgParser class interprets the user's input arguments and delegates control
 * to the appropriate handler functions for training, evaluating, or predicting.
 */
class ArgParser {
 public:
  /**
   * @brief Constructs an ArgParser object.
   * @param argc The number of command-line arguments.
   * @param argv Array of command-line arguments.
   */
  ArgParser(int argc, char* argv[]);

  /**
   * @brief Executes the main logic based on the parsed arguments.
   */
  void run();

 private:
  std::vector<std::string> args; ///< Stores the command-line arguments.

  /**
   * @brief Displays the help message to the standard output.
   */
  static void showHelp();

  /**
   * @brief Handles the model training process.
   */
  void handleTrain();

  /**
   * @brief Handles the prediction process using a trained model.
   */
  void handlePredict();

  /**
   * @brief Handles the model training and evaluation process.
   */
  void handleEvaluate();

  /**
   * @brief Saves a vector of prediction probabilities to a CSV file.
   * @param predictions The prediction probabilities.
   * @param destinationPath The path to the output CSV file.
   */
  static void saveToCSVFile(const std::vector<double>& predictions,
                            std::string destinationPath);

  /**
   * @brief Collects user input required for training a model.
   * @param filePath Reference to store the dataset file path.
   * @param destinationPath Reference to store the output model path.
   * @param hasHeader Reference to store whether the dataset has a header.
   * @param churnColumn Reference to store the index of the target column.
   * @param dropColumns Reference to store indices of columns to drop.
   * @param alpha Reference to store the learning rate.
   * @param epochs Reference to store the number of epochs.
   */
  static void collectTrainData(std::string& filePath,
                               std::string& destinationPath, bool& hasHeader,
                               size_t& churnColumn,
                               std::vector<size_t>& dropColumns, double& alpha,
                               int& epochs);

  /**
   * @brief Collects user input required for making predictions.
   * @param filePath Reference to store the dataset file path.
   * @param weightsPath Reference to store the model weights path.
   * @param destinationPath Reference to store the output predictions path.
   * @param hasHeader Reference to store whether the dataset has a header.
   * @param dropColumns Reference to store indices of columns to drop.
   */
  static void collectPredictData(std::string& filePath,
                                 std::string& weightsPath,
                                 std::string& destinationPath, bool& hasHeader,
                                 std::vector<size_t>& dropColumns);
};

#endif
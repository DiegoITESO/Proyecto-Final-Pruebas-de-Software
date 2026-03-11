#ifndef CUSTOMER_CHURN_PREDICTION_ARGPARSER_HPP
#define CUSTOMER_CHURN_PREDICTION_ARGPARSER_HPP
#include <string>
#include <vector>
#include <iostream>
#include <chrono>
#include <format>
#include <cmath>
#include "../log/Logger.hpp"
#include "../model/LogisticRegression.hpp"
#include "../core/ProcessedData.hpp"
#include "../core/Splitter.hpp"
#include "../utils/CSVReader.hpp"

class ArgParser
{
    public:
        ArgParser(int argc, char* argv[]);
        void run();
    private:
        std::vector<std::string> args;
        void showHelp() const;
        void handleTrain();
        void handlePredict();
        void handleEvaluate();
        void saveToCSVFile(std::vector<double>& predictions, std::string destinationPath);
        void collectTrainData(  std::string& filePath,
                                std::string& destinationPath,
                                bool& hasHeader,
                                size_t& churnColumn,
                                std::vector<size_t>& dropColumns,
                                double& alpha,
                                int& epochs);
        void collectPredictData(  std::string& filePath,
                                std::string& weightsPath,
                                std::string& destinationPath,
                                bool& hasHeader,
                                std::vector<size_t>& dropColumns);
};

#endif
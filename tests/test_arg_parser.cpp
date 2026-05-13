#include "catch.hpp"
#include "../include/cli/ArgParser.hpp"

#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdio> 

class CinRedirector {
private:
    std::streambuf* old_buf;
    std::istringstream iss;
public:
    explicit CinRedirector(const std::string& input) : iss(input) {
        old_buf = std::cin.rdbuf(iss.rdbuf());
    }
    ~CinRedirector() {
        std::cin.rdbuf(old_buf);
    }
};

class CoutSuppressor {
private:
    std::streambuf* old_buf;
    std::ostringstream oss;
public:
    CoutSuppressor() {
        old_buf = std::cout.rdbuf(oss.rdbuf());
    }
    ~CoutSuppressor() {
        std::cout.rdbuf(old_buf);
    }
};

TEST_CASE("ArgParser Initialization and Option Parsing", "[ArgParser][run]") {
    CoutSuppressor suppress; 

    SECTION("Throws runtime_error on unknown options") {
        const char* argv[] = { "./logistic_churn", "--unknown-flag" };
        ArgParser parser(2, const_cast<char**>(argv));
        
        REQUIRE_THROWS_AS(parser.run(), std::runtime_error);
        REQUIRE_THROWS_WITH(parser.run(), Catch::Matchers::Contains("Unknown option: --unknown-flag"));
    }

    SECTION("Executes help option without throwing") {
        const char* argv[] = { "./logistic_churn", "--help" };
        ArgParser parser(2, const_cast<char**>(argv));
        
        REQUIRE_NOTHROW(parser.run());
    }
}

TEST_CASE("ArgParser Data Collection Routines", "[ArgParser][I/O]") {
    CoutSuppressor suppress;
    const char* argv[] = { "./logistic_churn" };
    ArgParser parser(1, const_cast<char**>(argv));

    SECTION("collectTrainData gathers correct inputs") {
        std::string simulated_input = 
            "data/train.csv\n"
            "models/weights.bin\n"
            "y\n"
            "5\n"
            "0 1 2\n"
            "0.01\n"
            "1000\n";
        
        CinRedirector cin_redirect(simulated_input);

        std::string filePath, destinationPath;
        bool hasHeader = false;
        size_t churnColumn = 0;
        std::vector<size_t> dropColumns;
        double alpha = 0.0;
        int epochs = 0;

        REQUIRE_NOTHROW(parser.collectTrainData(filePath, destinationPath, hasHeader, 
                                                churnColumn, dropColumns, alpha, epochs));

        CHECK(filePath == "data/train.csv");
        CHECK(destinationPath == "models/weights.bin");
        CHECK(hasHeader == true);
        CHECK(churnColumn == 5);
        
        REQUIRE(dropColumns.size() == 3);
        CHECK(dropColumns[0] == 0);
        CHECK(dropColumns[1] == 1);
        CHECK(dropColumns[2] == 2);
        
        CHECK(alpha == 0.01);
        CHECK(epochs == 1000);
    }

    SECTION("collectTrainData throws on invalid header response") {
        std::string simulated_input = 
            "data.csv\n"
            "out.bin\n"
            "invalid_response\n"; 
        
        CinRedirector cin_redirect(simulated_input);

        std::string filePath, destinationPath;
        bool hasHeader;
        size_t churnColumn;
        std::vector<size_t> dropColumns;
        double alpha;
        int epochs;

        REQUIRE_THROWS_AS(
            parser.collectTrainData(filePath, destinationPath, hasHeader, churnColumn, dropColumns, alpha, epochs),
            std::runtime_error
        );
    }

    SECTION("collectPredictData gathers correct inputs") {
        std::string simulated_input = 
            "models/weights.bin\n"
            "data/new_customers.csv\n"
            "results/predictions.csv\n"
            "n\n"
            "0\n";
        
        CinRedirector cin_redirect(simulated_input);

        std::string filePath, weightsPath, destinationPath;
        bool hasHeader = true; 
        std::vector<size_t> dropColumns;

        REQUIRE_NOTHROW(parser.collectPredictData(filePath, weightsPath, destinationPath, 
                                                  hasHeader, dropColumns));

        CHECK(weightsPath == "models/weights.bin");
        CHECK(filePath == "data/new_customers.csv");
        CHECK(destinationPath == "results/predictions.csv");
        CHECK(hasHeader == false);
        
        REQUIRE(dropColumns.size() == 1);
        CHECK(dropColumns[0] == 0);
    }
}

TEST_CASE("ArgParser File Writing Operations", "[ArgParser][saveToCSVFile]") {
    const char* argv[] = { "./logistic_churn" };
    ArgParser parser(1, const_cast<char**>(argv));
    std::string test_filepath = "test_predictions_output.csv";

    SECTION("Successfully writes double precision vectors to file") {
        std::vector<double> mock_predictions = {0.05, 0.98, 0.45, 0.12};

        REQUIRE_NOTHROW(parser.saveToCSVFile(mock_predictions, test_filepath));

        std::ifstream inFile(test_filepath);
        REQUIRE(inFile.is_open());

        double value;
        std::vector<double> read_predictions;
        while (inFile >> value) {
            read_predictions.push_back(value);
        }
        inFile.close();

        REQUIRE(read_predictions.size() == mock_predictions.size());
        for (size_t i = 0; i < mock_predictions.size(); ++i) {
            CHECK(read_predictions[i] == mock_predictions[i]);
        }

        std::remove(test_filepath.c_str());
    }

    SECTION("Throws runtime error when unable to open destination directory") {
        std::string invalid_filepath = "/invalid_root_dir_that_does_not_exist/test.csv";
        std::vector<double> dummy_data = {1.0, 2.0};

        REQUIRE_THROWS_AS(parser.saveToCSVFile(dummy_data, invalid_filepath), std::runtime_error);
    }
}
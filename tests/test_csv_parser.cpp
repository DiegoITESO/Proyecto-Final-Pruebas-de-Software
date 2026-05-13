/**
 * @file test_csv_parser.cpp
 * @brief Unit tests for the CSVReader and data preprocessing routines.
 */
#include "catch.hpp"
#include "../include/utils/CSVReader.hpp"
#include <fstream>
#include <cstdio>
#include <cmath>

struct TempCSV {
    std::string filename;
    TempCSV(const std::string& name, const std::string& content) : filename(name) {
        std::ofstream out(filename);
        if (out.is_open()) {
            out << content;
        }
    }
    ~TempCSV() {
        std::remove(filename.c_str());
    }
};

/**
 * @brief Checks the file parsing capabilities of CSVReader, ensuring valid data is loaded correctly and exceptions are thrown for missing or inconsistent files.
 */
TEST_CASE("CSVReader::readCSV File Parsing", "[CSVReader][I/O]") {
    SECTION("Successfully reads a valid, well-formed CSV") {
        std::string content = 
            "ID,Age,Balance,Churn\n"
            "1,25,100.50,no\n"
            "2,35,250.00,yes\n";
        TempCSV temp("valid_test.csv", content);

        auto data = CSVReader::readCSV("valid_test.csv");
        
        REQUIRE(data.size() == 3);
        REQUIRE(data[0].size() == 4);
        CHECK(data[1][1] == "25");
        CHECK(data[2][3] == "yes");
    }

    SECTION("Throws invalid_argument for missing file") {
        REQUIRE_THROWS_AS(CSVReader::readCSV("nonexistent_ghost_file.csv"), std::invalid_argument);
    }

    SECTION("Throws invalid_argument for inconsistent column counts") {
        std::string content = 
            "ID,Age,Balance\n"
            "1,25\n"
            "2,35,250.00\n";
        TempCSV temp("inconsistent_test.csv", content);

        REQUIRE_THROWS_AS(CSVReader::readCSV("inconsistent_test.csv"), std::invalid_argument);
    }
}

/**
 * @brief Verifies the preprocessing logic including dropping columns, handling categorical values (one-hot encoding), mapping targets, and catching invalid arguments.
 */
TEST_CASE("CSVReader::preprocess Logic and Transformation", "[CSVReader][preprocess]") {
    std::vector<std::vector<std::string>> raw_data = {
        {"ID", "Age", "PlanType", "Churn"},
        {"101", "20", "Basic", "no"},
        {"102", "30", "Premium", "yes"},
        {"103", "40", "Basic", "yes"}
    };

    SECTION("Correctly processes features, drops columns, one-hot encodes, and maps churn") {
        bool hasHeader = true;
        size_t churnCol = 3;
        std::vector<size_t> dropCols = {0};

        ProcessedData result = CSVReader::preprocess(raw_data, hasHeader, churnCol, dropCols);

        REQUIRE(result.churnResults.size() == 3);
        CHECK(result.churnResults[0] == 0.0);
        CHECK(result.churnResults[1] == 1.0);
        CHECK(result.churnResults[2] == 1.0);
        REQUIRE(result.features.size() == 3);

        double expected_stddev = std::sqrt(200.0 / 3.0);
        
        CHECK(std::abs(result.features[0][0] - ((20.0 - 30.0) / expected_stddev)) < 0.01);
        CHECK(std::abs(result.features[1][0] - 0.0) < 0.001);
        CHECK(std::abs(result.features[2][0] - ((40.0 - 30.0) / expected_stddev)) < 0.01);

        CHECK(result.headers[0] == "Age");
    }

    SECTION("Throws invalid_argument when target column contains invalid data") {
        std::vector<std::vector<std::string>> bad_data = {
            {"Age", "Churn"},
            {"25", "maybe"}
        };
        
        REQUIRE_THROWS_AS(CSVReader::preprocess(bad_data, true, 1, {}), std::invalid_argument);
    }

    SECTION("Throws invalid_argument if attempting to drop too many columns") {
        REQUIRE_THROWS_AS(CSVReader::preprocess(raw_data, true, 3, {0, 1, 2, 3}), std::invalid_argument);
    }
}

/**
 * @brief Validates the isolated mathematical operations used to normalize feature vectors to a standard normal distribution.
 */
TEST_CASE("CSVReader::normalizeFeatures isolated math verification", "[CSVReader][normalize]") {
    SECTION("Standardizes a matrix to zero mean and unit variance") {
        ProcessedData data;
        data.features = Matrix({
            Vector({2.0, 10.0}),
            Vector({4.0, 10.0}),
            Vector({4.0, 10.0}),
            Vector({4.0, 10.0}),
            Vector({5.0, 10.0}),
            Vector({5.0, 10.0}),
            Vector({7.0, 10.0}),
            Vector({9.0, 10.0})
        });

        CSVReader::normalizeFeatures(data);

        CHECK(std::abs(data.features[0][0] - ((2.0 - 5.0) / 2.0)) < 0.001);
        CHECK(std::abs(data.features[7][0] - ((9.0 - 5.0) / 2.0)) < 0.001);

        CHECK(std::abs(data.features[0][1] - 0.0) < 0.001);
        CHECK(std::abs(data.features[7][1] - 0.0) < 0.001);
    }
}
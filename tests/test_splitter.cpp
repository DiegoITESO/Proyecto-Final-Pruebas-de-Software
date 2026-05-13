#include "catch.hpp"
#include "../include/core/Splitter.hpp"

ProcessedData generateDummyData(size_t size) {
    ProcessedData data;
    std::vector<Vector> featureRows;
    std::vector<double> churnResults;
    std::vector<std::string> headers = {"ID_Feature", "Value_Feature"};

    for (size_t i = 0; i < size; ++i) {
        std::vector<double> row = {static_cast<double>(i), static_cast<double>(i * 10)};
        featureRows.push_back(Vector(row));
        churnResults.push_back(static_cast<double>(i % 2));
    }

    data.features = Matrix(featureRows);
    data.churnResults = Vector(churnResults);
    data.headers = headers;

    return data;
}

TEST_CASE("RandomSplitter division and bounds", "[Splitter]") {
    RandomSplitter splitter;

    SECTION("Standard 80/20 split calculates sizes correctly") {
        ProcessedData data = generateDummyData(100);
        auto [train, test] = splitter.split(data, 0.8);

        REQUIRE(train.features.size() == 80);
        REQUIRE(train.churnResults.size() == 80);
        REQUIRE(test.features.size() == 20);
        REQUIRE(test.churnResults.size() == 20);

        REQUIRE(train.headers == data.headers);
        REQUIRE(test.headers == data.headers);
    }

    SECTION("Edge case: 100% training data (ratio 1.0)") {
        ProcessedData data = generateDummyData(50);
        auto [train, test] = splitter.split(data, 1.0);

        REQUIRE(train.features.size() == 50);
        REQUIRE(train.churnResults.size() == 50);
        REQUIRE(test.features.size() == 0);
        REQUIRE(test.churnResults.size() == 0);
    }

    SECTION("Edge case: 0% training data (ratio 0.0)") {
        ProcessedData data = generateDummyData(50);
        auto [train, test] = splitter.split(data, 0.0);

        REQUIRE(train.features.size() == 0);
        REQUIRE(train.churnResults.size() == 0);
        REQUIRE(test.features.size() == 50);
        REQUIRE(test.churnResults.size() == 50);
    }

    SECTION("Data integrity is maintained (no duplication or loss)") {
        size_t n = 100;
        ProcessedData data = generateDummyData(n);
        auto [train, test] = splitter.split(data, 0.75);

        double expected_sum = (n * (n - 1)) / 2.0;
        double actual_sum = 0.0;

        for (size_t i = 0; i < train.features.size(); ++i) {
            actual_sum += train.features[i][0]; 
        }
        
        for (size_t i = 0; i < test.features.size(); ++i) {
            actual_sum += test.features[i][0];
        }

        REQUIRE(actual_sum == expected_sum);
    }
}
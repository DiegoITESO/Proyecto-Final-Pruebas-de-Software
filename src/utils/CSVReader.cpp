#include "../../include/utils/CSVReader.hpp"
//----------Util CSVReader functions----------//
std::vector<std::vector<std::string>> CSVReader::readCSV(const std::string& filePath)
{
    std::ifstream file(filePath);
    if(!file.is_open()) throw std::invalid_argument("Could not open file " + filePath);
    std::vector<std::vector<std::string>> data;
    std::string line;
    while(std::getline(file, line))
    {
        std::vector<std::string> row;
        std::stringstream ss(line);
        std::string cell;
        while(std::getline(ss, cell, ',')) row.push_back(cell);
        if(data.size() && (row.size() != data[0].size()))
            throw std::invalid_argument("The number of columns in the file is inconsistent");
        data.push_back(row);
    }
    return data;
}
ProcessedData CSVReader::preprocess( const std::vector<std::vector<std::string>>& data,
                                bool hasHeader,
                                size_t churnColumn,
                                std::vector<size_t> dropColumns)
//~~~~MAPPING YES/NO TO 1.0/0.0 AND USING ONE-HOT ENCODING FOR STRING PARAMETERS~~~~//
{
    // MAPPING THE ONE HOT ENCODING //
    if (dropColumns.size() >= data[0].size()-1) throw std::invalid_argument(
        "The number of columns to be dropped must be strictly less than the number of columns avaliable."
        );
    std::unordered_map<size_t, std::unordered_set<std::string>> columnsEncoded;
    bool skippedHeader = false;
    for(const std::vector<std::string>& row : data)
    {
        if(hasHeader && !skippedHeader)
        {
            skippedHeader = true;
            continue;
        }
        for(size_t i = 0; i < row.size(); ++i)
        {
            if(std::find(dropColumns.begin(), dropColumns.end(), i) != dropColumns.end())
                continue;
            std::string lowercaseString = StringHandling::toLower(row[i]);
            if( !StringHandling::isNumber(row[i]) &&
                lowercaseString != "yes" &&
                lowercaseString != "no")
                columnsEncoded[i].insert(row[i]);
        }
    }

    // PROCESSING THE DATA //
    ProcessedData result;
    skippedHeader = false;
    std::unordered_map<std::string, size_t> encoding_map; //SAVE EACH NEW VALUE ENCODED AND ITS INDEX
    size_t nextFreeColumn = data[0].size()-dropColumns.size();
    size_t offset; //AN OFFSET:
                        /*
                            EACH OF THE COLUMNS THAT WILL BE "ONE HOT ENCODED" WILL HAVE TO BE ELIMINATED
                            THUS, THE PURPOSE OF THE OFFSET IS TO SKIP THOSE COLUMNS WHEN CALCULATING WHERE
                            THE NEXT PARAMETER WILL BE INSERTED
                        */
    // START ITERATING THROUGH ALL THE ROWS //
    size_t newSize = data[0].size()-dropColumns.size();
    for(const auto& column : columnsEncoded) newSize += column.second.size();
    std::vector<Vector> processedData;
    std::vector<double> churnResults;
    for(const auto& row : data)
    {
        if(hasHeader && !skippedHeader)
        {
            skippedHeader = true;
            continue;
        }
        std::vector<double> processedRow(newSize); //VALUE OF EACH OF THE NEW PARAMETERS
        offset = 0;
        for(size_t i = 0; i<row.size(); ++i)
        {
            std::string lowercaseString = StringHandling::toLower(row[i]); //STANDARDIZE THE STRINGS
            if(i == churnColumn)
            {
                if(lowercaseString == "yes") churnResults.push_back(1.0);
                else if(lowercaseString == "no") churnResults.push_back(0.0);
                else{
                    // Print ASCII values to see hidden characters
                    std::cout << "ASCII values: ";
                    for(char c : lowercaseString) {
                        std::cout << static_cast<int>(c) << " ";
                    }
                    std::cout << std::endl;
                    throw std::invalid_argument("Churn results must be expressed as yes/no values. Value found: '" + lowercaseString + "'");
                }
                offset++;
                continue;
            }
            if(std::find(dropColumns.begin(), dropColumns.end(), i) != dropColumns.end()) {offset++; continue;}
            if(lowercaseString == "yes") processedRow[i-offset] = 1.0;
            else if(lowercaseString == "no") processedRow[i-offset] = 0.0;
            else if(StringHandling::isNumber(lowercaseString))
            {
             processedRow[i-offset] = std::stod(lowercaseString);
            }
            else
            {
                if (encoding_map.find(lowercaseString) != encoding_map.end())
                {
                    processedRow[encoding_map[lowercaseString]] = 1.0;
                    offset++;
                }
                else
                {
                    encoding_map[lowercaseString] = nextFreeColumn;
                    processedRow[nextFreeColumn++] = 1.0;
                    offset++;
                }
            }
        }
        processedData.emplace_back(processedRow);
    }
    result.features = Matrix(processedData);
    result.churnResults = churnResults;

    // GET THE HEADERS //
    if(hasHeader)
    {
        std::vector<std::string> headers;
        for(size_t i = 0; i < data[0].size(); ++i)
        {
            if(i == churnColumn) continue;
            if(std::find(dropColumns.begin(), dropColumns.end(), i) != dropColumns.end()) continue;
            headers.push_back(data[0][i]);
        }
        std::vector<std::pair<std::string, size_t>> sortedEncoding(
            encoding_map.begin(), encoding_map.end());
        std::sort(sortedEncoding.begin(), sortedEncoding.end(),
                  [](const auto& a, const auto& b) { return a.second < b.second; });
        for (const auto& [value, _] : sortedEncoding) {
            headers.push_back(value);
        }
        result.headers = headers;
    }
    CSVReader::normalizeFeatures(result);
    return result;
};

void CSVReader::normalizeFeatures(ProcessedData& data)
{
    size_t numSamples = data.features.size();
    size_t numFeatures = data.features[0].size();
    std::vector<double> means(numFeatures, 0.0);
    std::vector<double> stddevs(numFeatures, 0.0);
    for (size_t j = 0; j < numFeatures; ++j)
    {
        for (size_t i = 0; i < numSamples; ++i)
            means[j] += data.features[i][j];
        means[j] /= numSamples;
    }
    for (size_t j = 0; j < numFeatures; ++j)
    {
        for (size_t i = 0; i < numSamples; ++i)
            stddevs[j] += (data.features[i][j] - means[j]) * (data.features[i][j] - means[j]);
        stddevs[j] = std::sqrt(stddevs[j] / numSamples);
        if (stddevs[j] == 0) stddevs[j] = 1.0;
    }

    for (size_t i = 0; i < numSamples; ++i)
    {
        for (size_t j = 0; j < numFeatures; ++j)
            data.features[i][j] = (data.features[i][j] - means[j]) / stddevs[j];
    }
}

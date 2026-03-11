#include"../../include/core/Matrix.hpp"

//----------Matrix methods----------//
Matrix::Matrix(std::vector<Vector> rows)
{
    if(!rows.empty())
    {
        size_t columns = rows[0].size();
        for(const Vector& row : rows)
            if(row.size() != columns) throw std::invalid_argument("Inconsistent matrix size");
    }
    rows_ = std::move(rows);
};
Matrix::Matrix(std::initializer_list<Vector> rows)
{
    if(!rows.size()) return;
    size_t columns = rows.begin()->size();
    for(const Vector& row : rows)
        if(row.size() != columns) throw std::invalid_argument("Inconsistent matrix size");
    rows_.reserve(rows.size());
    for (auto& row : rows) rows_.push_back(row);
};
Matrix::Matrix(size_t rows, size_t cols) : rows_(rows, Vector(cols)) {};
Matrix Matrix::transpose() const
{
    Matrix result(rows_[0].size(), rows_.size());
    for(size_t i = 0; i < rows_.size(); ++i)
        for(size_t j = 0; j < rows_[0].size(); ++j)        //we know the matrix has a regular number of columns in each row
            result[j][i] = rows_[i][j];
    return result;
};
size_t Matrix::size() const { return rows_.size(); };
Vector Matrix::operator*(const Vector& times)
{
    if(times.size() != rows_[0].size())
        throw std::invalid_argument(
            "The number of elements in vector must be equal to the number of columns in matrix"
        );
    std::vector<double> result;
    for(Vector& row : rows_)
        result.push_back(row.dot(times));
    return Vector(result);
};
Matrix Matrix::operator*(const double scalar)
{
    Matrix result = *this;
    for(size_t row = 0; row < rows_.size(); ++row)
        for(size_t col = 0; col < rows_[0].size(); ++col)
            result[row][col] *= scalar;
    return result;
};
Matrix Matrix::operator*(const Matrix& times)
{
    if(times.size() != rows_[0].size())
        throw std::invalid_argument(
            "The number of rows in the first matrix must be equal to the number of columns in the second matrix"
        );
    std::vector<Vector> result;
    for(size_t i = 0; i < rows_.size(); ++i)
    {
        std::vector<double> row;
        for(size_t k = 0; k < times.size(); ++k)
        {
            double ans = 0.0;
            for(size_t j = 0; j < rows_[0].size(); ++j)
            {
                ans += rows_[i][j] * times[j][k];
            }
            row.push_back(ans);
        }
        result.push_back(Vector(row));
    }
    return Matrix(result);
};
Vector& Matrix::operator[](size_t index)
{
    if(index >= rows_.size()) throw std::out_of_range("Index out of range");
    return rows_[index];
};
const Vector& Matrix::operator[](size_t index) const
{
    if(index >= rows_.size()) throw std::out_of_range("Index out of range");
    return rows_[index];
};
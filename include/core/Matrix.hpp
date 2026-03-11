#ifndef CUSTOMER_CHURN_PREDICTION_MATRIX_HPP
#define CUSTOMER_CHURN_PREDICTION_MATRIX_HPP
#include <vector>
#include <stdexcept>
#include <cstddef>
#include <initializer_list>
#include "Vector.hpp"
class Matrix
{
    public:
        Matrix() = default;
        Matrix(std::vector<Vector> rows);
        Matrix(std::initializer_list<Vector> rows);
        explicit Matrix(size_t rows, size_t cols);
        Matrix transpose() const;
        size_t size() const;
        Vector operator*(const Vector& times);
        Matrix operator*(const double scalar);
        Matrix operator*(const Matrix& times);
        Vector& operator[](size_t index);
        const Vector& operator[](size_t index) const;
    private:
        std::vector<Vector> rows_;
};
#endif
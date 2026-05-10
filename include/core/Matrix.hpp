#ifndef CUSTOMER_CHURN_PREDICTION_MATRIX_HPP
#define CUSTOMER_CHURN_PREDICTION_MATRIX_HPP
#include <cstddef>
#include <initializer_list>
#include <stdexcept>
#include <vector>

#include "Vector.hpp"
/**
 * @class Matrix
 * @brief Represents a 2D matrix and provides basic matrix operations.
 */
class Matrix {
 public:
  /**
   * @brief Default constructor.
   */
  Matrix() = default;

  /**
   * @brief Constructs a matrix from a vector of vectors (rows).
   * @param rows The rows of the matrix.
   * @throws std::invalid_argument if rows have inconsistent sizes.
   */
  explicit Matrix(std::vector<Vector> rows);

  /**
   * @brief Constructs a matrix from an initializer list of vectors.
   * @param rows The initializer list of vectors.
   * @throws std::invalid_argument if rows have inconsistent sizes.
   */
  Matrix(std::initializer_list<Vector> rows);

  /**
   * @brief Constructs a matrix with specified rows and columns initialized to 0.
   * @param rows Number of rows.
   * @param cols Number of columns.
   */
  explicit Matrix(size_t rows, size_t cols);

  /**
   * @brief Computes the transpose of the matrix.
   * @return A new transposed Matrix.
   */
  Matrix transpose() const;

  /**
   * @brief Returns the number of rows in the matrix.
   * @return The number of rows.
   */
  size_t size() const;

  /**
   * @brief Multiplies the matrix by a vector.
   * @param times The vector to multiply with.
   * @return The resulting vector.
   * @throws std::invalid_argument if dimension mismatch occurs.
   */
  Vector operator*(const Vector& times);

  /**
   * @brief Multiplies the matrix by a scalar value.
   * @param scalar The scalar value.
   * @return The resulting matrix.
   */
  Matrix operator*(const double scalar);

  /**
   * @brief Multiplies this matrix by another matrix.
   * @param times The matrix to multiply with.
   * @return The resulting matrix.
   * @throws std::invalid_argument if dimension mismatch occurs.
   */
  Matrix operator*(const Matrix& times);

  /**
   * @brief Accesses a specific row in the matrix.
   * @param index The index of the row.
   * @return Reference to the vector representing the row.
   * @throws std::out_of_range if index is out of bounds.
   */
  Vector& operator[](size_t index);

  /**
   * @brief Accesses a specific row in the matrix (const).
   * @param index The index of the row.
   * @return Const reference to the vector representing the row.
   * @throws std::out_of_range if index is out of bounds.
   */
  const Vector& operator[](size_t index) const;

 private:
  std::vector<Vector> rows_; ///< Stores the rows of the matrix.
};
#endif
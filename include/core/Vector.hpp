#ifndef CUSTOMER_CHURN_PREDICTION_VECTOR_HPP
#define CUSTOMER_CHURN_PREDICTION_VECTOR_HPP
#include <cmath>
#include <cstddef>
#include <initializer_list>
#include <stdexcept>
#include <type_traits>
#include <vector>
/**
 * @class Vector
 * @brief Represents a mathematical vector and provides basic vector operations.
 */
class Vector {
 public:
  /**
   * @brief Default constructor.
   */
  Vector();

  /**
   * @brief Constructs a vector from an std::vector.
   * @tparam T Type of elements, must be convertible to double.
   * @param array The input std::vector.
   */
  template <typename T,
            typename = std::enable_if_t<std::is_convertible_v<T, double>>>
  explicit Vector(const std::vector<T>& array) {
    data_.reserve(array.size());
    // cppcheck-suppress useStlAlgorithm
    for (const auto& element : array) {
      data_.push_back(static_cast<double>(element));
    }
  }

  /**
   * @brief Constructs a vector from an initializer list.
   * @tparam T Type of elements, must be convertible to double.
   * @param array The input initializer list.
   */
  template <typename T,
            typename = std::enable_if_t<std::is_convertible_v<T, double>>>
  Vector(std::initializer_list<T> array) {
    data_.reserve(array.size());
    // cppcheck-suppress useStlAlgorithm
    for (const auto& element : array) {
      data_.push_back(static_cast<double>(element));
    }
  }

  /**
   * @brief Constructs a vector of a given size initialized to 0.
   * @param size The size of the vector.
   * @throws std::invalid_argument if size is negative.
   */
  explicit Vector(long long size);

  /**
   * @brief Returns the size of the vector.
   * @return The size.
   */
  size_t size() const;

  /**
   * @brief Computes the dot product with another vector.
   * @param other The other vector.
   * @return The dot product result.
   * @throws std::invalid_argument if vectors have different sizes.
   */
  double dot(const Vector& other) const;

  /**
   * @brief Computes the magnitude (L2 norm) of the vector.
   * @return The magnitude.
   */
  double magnitude() const;

  /**
   * @brief Adds another vector to this vector.
   * @param other The vector to add.
   * @return The resulting vector.
   * @throws std::invalid_argument if vectors have different sizes.
   */
  Vector operator+(const Vector& other) const;

  /**
   * @brief Subtracts another vector from this vector.
   * @param other The vector to subtract.
   * @return The resulting vector.
   * @throws std::invalid_argument if vectors have different sizes.
   */
  Vector operator-(const Vector& other) const;

  /**
   * @brief Multiplies the vector by a scalar.
   * @param scalar The scalar value.
   * @return The resulting vector.
   */
  Vector operator*(double scalar) const;

  /**
   * @brief Checks if this vector is equal to another.
   * @param other The vector to compare with.
   * @return True if elements are approximately equal, false otherwise.
   */
  bool operator==(const Vector& other) const;

  /**
   * @brief Checks if this vector is not equal to another.
   * @param other The vector to compare with.
   * @return True if elements are not equal, false otherwise.
   */
  bool operator!=(const Vector& other) const;

  /**
   * @brief Accesses an element at a specific index.
   * @param index The index.
   * @return Reference to the element.
   * @throws std::out_of_range if index is out of bounds.
   */
  double& operator[](size_t index);

  /**
   * @brief Accesses an element at a specific index (const).
   * @param index The index.
   * @return Const reference to the element.
   * @throws std::out_of_range if index is out of bounds.
   */
  const double& operator[](size_t index) const;

 private:
  std::vector<double> data_;  ///< Internal storage for vector elements.
};
#endif
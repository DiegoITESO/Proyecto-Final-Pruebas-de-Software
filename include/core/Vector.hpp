#ifndef CUSTOMER_CHURN_PREDICTION_VECTOR_HPP
#define CUSTOMER_CHURN_PREDICTION_VECTOR_HPP
#include <vector>
#include <initializer_list>
#include <cstddef>
#include <type_traits>
#include <stdexcept>
#include <cmath>
class Vector
{
    public:
        Vector();
        template<typename T, typename = std::enable_if_t<std::is_convertible_v<T, double>>>
        Vector(const std::vector<T>& array)
        {
            data_.reserve(array.size());
            for (auto& element : array) data_.push_back(static_cast<double>(element));
        }
        template<typename T, typename = std::enable_if_t<std::is_convertible_v<T, double>>>
        Vector(std::initializer_list<T> array)
        {
            data_.reserve(array.size());
            for (auto& element : array) data_.push_back(static_cast<double>(element));
        }
        explicit Vector(long long size);
        size_t size() const;
        double dot(const Vector& other) const;
        double magnitude() const;
        Vector operator+(const Vector& other) const;
        Vector operator-(const Vector& other) const;
        Vector operator*(double scalar) const;
        bool operator==(const Vector& other) const;
        bool operator!=(const Vector& other) const;
        double& operator[](size_t index);
        const double& operator[](size_t index) const;
    private:
        std::vector<double> data_;
};
#endif
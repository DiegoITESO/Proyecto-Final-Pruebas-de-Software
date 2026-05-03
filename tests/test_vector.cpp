#include "catch.hpp"
#include "../include/core/Vector.hpp"
#include "vector"

TEST_CASE("INIIALIZAR VECTOR", "[vector]")
{
    std::vector<double> array(10, 12);
    Vector v1(array);
    Vector v2 = Vector(array);
    Vector v3 = Vector();
    Vector v4 = Vector(10);
    Vector v5;
    REQUIRE(v1.size() == 10);
    REQUIRE(v1[0] == 12);
    REQUIRE(v2.size() == 10);
    REQUIRE(v2[0] == 12);
    REQUIRE(v3.size() == 0);
    REQUIRE_THROWS_AS(v3[0], std::out_of_range);
    REQUIRE(v4.size() == 10);
    REQUIRE(v5.size() == 0);
}

TEST_CASE("SUMAR VECTORES", "[vector]")
{
    Vector v1 = {1, 2, 3, 4};
    Vector v2 = {1, 2, 3, 4};
    Vector v3 = v1 + v2;
    REQUIRE(v3 == Vector({2, 4, 6, 8}));
}

TEST_CASE("RESTAR VECTORES", "[vector]")
{
    Vector v1 = {1, 2, 3, 4};
    Vector v2 = {1, 2, 3, 4};
    Vector v3 = v1 - v2;
    REQUIRE(v3 == Vector({0, 0, 0, 0}));
    REQUIRE(v2 - Vector({1, 1, 1, 1}) == Vector({0, 1, 2, 3}));
}

TEST_CASE("PRODUCTO PUNTO", "[vector]")
{
    Vector v1 = {51, 74, 22, 98};
    Vector v2 = {27, 31, 55, 2};
    double scalar = v1.dot(v2);
    REQUIRE(scalar == 5077.0);
    REQUIRE(Vector({0, 0, 0, 0}).dot(v2) == 0);
}

TEST_CASE("PRODUCTO POR ESCALAR", "[]")
{
    Vector v1 = {1, 2, 3, 4};
    Vector v2 = {1, 2, 3, 4};
    double scalar = 8;
    REQUIRE(v1*scalar == Vector({8, 16, 24, 32}));
    double dotProduct = v2.dot(v2);
    REQUIRE(dotProduct*scalar == 240);
}

TEST_CASE("PRUEBA DE IGUALDAD", "[vector]")
{
    Vector v1 = {1, 2, 3, 4};
    Vector v2 = {1, 2, 3, 4};
    Vector v3 = {5, 6, 7, 8};
    Vector v4 = {5.000000001, 6.0, 7.0, 8.0};
    Vector v5 = {5, 6, 7, 8};
    REQUIRE(v1 == v2);
    REQUIRE(v1 == Vector({1, 2, 3, 4}));
    REQUIRE(v1 != v3);
    REQUIRE(v1 != Vector({15, 35, 55, 7}));
    REQUIRE(v4 == v5);
}

TEST_CASE("OPERACIONES CON DIFERENTES TAMAÑOS", "[vector]")
{
    Vector v1 = {1, 2, 3};
    Vector v2 = {4, 5};
    REQUIRE_THROWS_AS(v1 + v2, std::invalid_argument);
    REQUIRE_THROWS_AS(v1 - v2, std::invalid_argument);
    REQUIRE_THROWS_AS(v1.dot(v2), std::invalid_argument);
}

TEST_CASE("NORMA DE UN VECTOR", "[vector]")
{
    Vector v1 = {1, 2, 3, 4};
    REQUIRE(v1.magnitude() == Approx(5.477225575).epsilon(1e-9));
    REQUIRE(v1.magnitude() == Vector({4, 3, 2, 1}).magnitude());
}

TEST_CASE("COPY Y MOVE", "[vector]")
{
    Vector v1 = {51, 74, 22, 98};
    Vector v2 = {27, 31, 55, 2};
    Vector v3 = v1;
    v3[1] = 12.4;
    REQUIRE(v3 != v1);
    Vector v4 = std::move(v2);
    REQUIRE(v4 == Vector({27, 31, 55, 2}));
    REQUIRE(v2.size() == 0);
}
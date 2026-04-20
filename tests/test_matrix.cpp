#include "../include/core/Matrix.hpp"
#include "../include/core/Vector.hpp"
#include "catch.hpp"

TEST_CASE("CONSTRUCTOR DESDE VECTOR DE FILAS VALIDA LA CONSISTENCIA", "[matrix]") {
    Vector row1({1.0, 2.0});
    Vector row2({3.0, 4.0});
    REQUIRE_NOTHROW(Matrix({row1, row2}));

    Vector badRow({5.0});
    REQUIRE_THROWS_AS(Matrix({row1, badRow}), std::invalid_argument);
}

TEST_CASE("CONSTRUCTOR EXPLICITO CON DIMENSIONES CREA MATRIZ NULA", "[matrix]") {
    Matrix m(2, 3);
    REQUIRE(m.size() == 2);
    REQUIRE(m[0].size() == 3);
    for (size_t i = 0; i < 2; ++i)
        for (size_t j = 0; j < 3; ++j)
            REQUIRE(m[i][j] == Approx(0.0));
}

TEST_CASE("OPERADOR DE ACCESO VALIDA INDICES", "[matrix]") {
    Matrix m({Vector({1,2,3}), Vector({4,5,6})});
    REQUIRE_NOTHROW(m[0]);
    REQUIRE_NOTHROW(m[1]);
    REQUIRE_THROWS_AS(m[2], std::out_of_range);
}

TEST_CASE("TRANSPUESTA DE MATRIZ SE CALCULA CORRECTAMENTE", "[matrix]") {
    Matrix m({
        Vector({1, 2}),
        Vector({3, 4}),
        Vector({5, 6})
    });

    Matrix t = m.transpose();

    REQUIRE(t.size() == 2);
    REQUIRE(t[0][0] == Approx(1));
    REQUIRE(t[0][1] == Approx(3));
    REQUIRE(t[0][2] == Approx(5));
    REQUIRE(t[1][0] == Approx(2));
    REQUIRE(t[1][1] == Approx(4));
    REQUIRE(t[1][2] == Approx(6));
}

TEST_CASE("PRODUCTO ESCALAR CON MATRIZ", "[matrix]") {
    Matrix m({
        Vector({1, 2}),
        Vector({3, 4})
    });

    Matrix result = m * 2.0;

    REQUIRE(result[0][0] == Approx(2));
    REQUIRE(result[0][1] == Approx(4));
    REQUIRE(result[1][0] == Approx(6));
    REQUIRE(result[1][1] == Approx(8));
}

TEST_CASE("PRODUCTO MATRIZ POR VECTOR", "[matrix]") {
    Matrix m({
        Vector({1, 2}),
        Vector({3, 4}),
        Vector({5, 6})
    });

    Vector v({1, 1});
    Vector result = m * v;

    REQUIRE(result.size() == 3);
    REQUIRE(result[0] == Approx(3));
    REQUIRE(result[1] == Approx(7));
    REQUIRE(result[2] == Approx(11));
}

TEST_CASE("PRODUCTO MATRIZ POR MATRIZ", "[matrix]") {
    Matrix A({
        Vector({1, 2}),
        Vector({3, 4})
    });

    Matrix B({
        Vector({5, 6}),
        Vector({7, 8})
    });

    Matrix C = A * B;

    REQUIRE(C.size() == 2);
    REQUIRE(C[0][0] == Approx(19));
    REQUIRE(C[0][1] == Approx(22));
    REQUIRE(C[1][0] == Approx(43));
    REQUIRE(C[1][1] == Approx(50));
}
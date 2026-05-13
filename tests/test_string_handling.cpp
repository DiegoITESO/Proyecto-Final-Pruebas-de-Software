#include "catch.hpp"
#include "../include/utils/StringHandling.hpp"

TEST_CASE("StringHandling::isNumber validates numeric formats", "[StringHandling][isNumber]") {
    SECTION("Accepts valid integers and floating-point numbers") {
        CHECK(StringHandling::isNumber("123"));
        CHECK(StringHandling::isNumber("-42"));
        CHECK(StringHandling::isNumber("0"));
        CHECK(StringHandling::isNumber("3.14159"));
        CHECK(StringHandling::isNumber("-0.001"));
        CHECK(StringHandling::isNumber("1e5"));
    }

    SECTION("Rejects non-numeric strings and mixed characters") {
        CHECK_FALSE(StringHandling::isNumber("abc"));
        CHECK_FALSE(StringHandling::isNumber("123a"));
        CHECK_FALSE(StringHandling::isNumber("a123"));
        CHECK_FALSE(StringHandling::isNumber(""));
    }

    SECTION("Rejects valid numbers padded with whitespace (due to noskipws)") {
        CHECK_FALSE(StringHandling::isNumber(" 42"));
        CHECK_FALSE(StringHandling::isNumber("42 "));
        CHECK_FALSE(StringHandling::isNumber("  3.14  "));
        CHECK_FALSE(StringHandling::isNumber("\t100\n"));
    }
}

TEST_CASE("StringHandling::toLower transforms casing and strips whitespace", "[StringHandling][toLower]") {
    SECTION("Converts uppercase and mixed-case letters to lowercase") {
        CHECK(StringHandling::toLower("HELLO") == "hello");
        CHECK(StringHandling::toLower("MixedCase") == "mixedcase");
        CHECK(StringHandling::toLower("alreadylower") == "alreadylower");
    }

    SECTION("Silently removes all whitespace characters (Deceptive behavior)") {
        CHECK(StringHandling::toLower("Hello World") == "helloworld");
        CHECK(StringHandling::toLower("  leading  ") == "leading");
        CHECK(StringHandling::toLower("tabs\tand\nnewlines") == "tabsandnewlines");
    }

    SECTION("Leaves numbers and special characters unchanged") {
        CHECK(StringHandling::toLower("CHURN_2026!") == "churn_2026!");
    }
}
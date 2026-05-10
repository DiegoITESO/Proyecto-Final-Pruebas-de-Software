/**
 * @file test_logger.cpp
 * @brief Unit tests for the Logger singleton class using Catch2.
 */
#include "../include/log/Logger.hpp"
#include "catch.hpp"
#include "filesystem"
#include "iostream"

/**
 * @brief Verifies the Singleton pattern implementation.
 * Ensures that multiple calls to instance() return the same memory address.
 */
TEST_CASE("UNA SOLA INSTANCIA (SINGLETON)", "[logger]") {
  Logger::instance().reset();
  REQUIRE(&Logger::instance() == &Logger::instance());
}

/**
 * @brief Verifies that setting a log file actually creates the file on the filesystem.
 */
TEST_CASE("CREAR ARCHIVO DE LOGGING", "[logger]") {
  Logger::instance().reset();
  std::string filename = "logs/test.log";
  std::filesystem::remove(filename);
  Logger::instance().set_file(filename);
  Logger::instance().log("Initial log");
  REQUIRE(std::filesystem::exists(filename));
}

/**
 * @brief Verifies that messages are properly written and appended to the target log file.
 */
TEST_CASE("ESCRIBIR MENSAJE EN EL ARCHIVO", "[logger]") {
  Logger::instance().reset();
  std::string filename = "logs/log_output.txt";
  std::filesystem::remove(filename);
  Logger::instance().set_file(filename);
  std::string message = "Hello Logger";
  Logger::instance().log(message);
  std::ifstream file(filename);
  std::string line;
  std::getline(file, line);
  file.close();
  REQUIRE(line.find(message) != std::string::npos);
}

/**
 * @brief Verifies that if no file is set, the logger falls back to writing to std::cerr.
 */
TEST_CASE("IMPRIMIR A STD::CERR COMO FALLBACK", "[logger]") {
  Logger::instance().reset();
  std::stringstream buffer;
  std::streambuf* old_cerr = std::cerr.rdbuf(buffer.rdbuf());
  Logger::instance().log("Mensaje sin archivo");
  std::cerr.rdbuf(old_cerr);
  std::string output = buffer.str();
  REQUIRE(output.find("Mensaje sin archivo") != std::string::npos);
}
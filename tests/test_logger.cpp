#include"catch.hpp"
#include"../include/log/Logger.hpp"
#include"iostream"
#include"filesystem"

TEST_CASE("UNA SOLA INSTANCIA (SINGLETON)", "[logger]")
{
    Logger::instance().reset();
    REQUIRE(&Logger::instance() == &Logger::instance());
}

TEST_CASE("CREAR ARCHIVO DE LOGGING", "[logger]")
{
    Logger::instance().reset();
    std::string filename = "logs/test.log";
    std::filesystem::remove(filename);
    Logger::instance().set_file(filename);
    Logger::instance().log("Initial log");
    REQUIRE(std::filesystem::exists(filename));
}

TEST_CASE("ESCRIBIR MENSAJE EN EL ARCHIVO", "[logger]")
{
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

TEST_CASE("IMPRIMIR A STD::CERR COMO FALLBACK", "[logger]")
{
    Logger::instance().reset();
    std::stringstream buffer;
    std::streambuf* old_cerr = std::cerr.rdbuf(buffer.rdbuf());
    Logger::instance().log("Mensaje sin archivo");
    std::cerr.rdbuf(old_cerr);
    std::string output = buffer.str();
    REQUIRE(output.find("Mensaje sin archivo") != std::string::npos);
}
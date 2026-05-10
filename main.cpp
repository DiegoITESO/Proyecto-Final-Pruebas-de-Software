#include <iostream>

#include "./include/cli/ArgParser.hpp"
using namespace std;

/**
 * @brief Main entry point of the application.
 * 
 * Initializes the ArgParser with the command line arguments and
 * begins the execution cycle.
 * 
 * @param argc Number of command-line arguments.
 * @param argv Array of command-line arguments.
 * @return 0 on successful execution.
 */
int main(int argc, char* argv[]) {
  ArgParser parser(argc, argv);
  parser.run();
  return 0;
}
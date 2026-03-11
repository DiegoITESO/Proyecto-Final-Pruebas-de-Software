#include <iostream>
#include "./include/cli/ArgParser.hpp"
using namespace std;
int main(int argc, char* argv[])
{
    ArgParser parser(argc, argv);
    parser.run();
    return 0;
}
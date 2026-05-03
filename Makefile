CXX = g++
CXXFLAGS = -g -std=c++20 -Wall -Iinclude
SRC = $(wildcard src/**/*.cpp)
TESTS = $(wildcard tests/*.cpp)
TAGS ?=

all: main

main: main.cpp $(SRC)
	$(CXX) $(CXXFLAGS) -o logistic_churn main.cpp $(SRC)

test: $(TESTS) $(SRC)
	$(CXX) $(CXXFLAGS) -DUNIT_TESTING -o run_tests $(TESTS) $(SRC)
	./run_tests $(TAGS)

clean:
	rm -f logistic_churn run_tests
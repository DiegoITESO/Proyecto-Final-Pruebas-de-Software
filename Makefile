CXX = g++
CXXFLAGS = -g -std=c++20 -Wall -Iinclude
SRC = $(wildcard src/**/*.cpp)
TAGS ?=

all: main

main: main.cpp $(SRC)
	$(CXX) $(CXXFLAGS) -o logistic_churn main.cpp $(SRC)

clean:
	rm -f logistic_churn 
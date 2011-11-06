CXX := g++
CXXFLAGS := -Wall -W -O2 `xapian-config --cxxflags`
LIBS := `xapian-config --libs`

all: index1

index1: index1.cc
	$(CXX) $(CXXFLAGS) -o index1 index1.cc $(LIBS)

.PHONY: all index1

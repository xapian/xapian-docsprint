CXX := g++
CXXFLAGS := -Wall -W -O2 `xapian-config --cxxflags`
LIBS := `xapian-config --libs`

all: index1 search1 delete1

index1: index1.cc
	$(CXX) $(CXXFLAGS) -o index1 index1.cc $(LIBS)

search1: search1.cc
	$(CXX) $(CXXFLAGS) -o search1 search1.cc $(LIBS)

delete1: delete1.cc
	$(CXX) $(CXXFLAGS) -o delete1 delete1.cc $(LIBS)

.PHONY: all

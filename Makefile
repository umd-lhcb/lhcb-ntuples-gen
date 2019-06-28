# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Thu Jun 27, 2019 at 04:35 AM -0400

BINPATH	:=	bin
SRCPATH	:=	src

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags) -ggdb
LINKFLAGS	:=	$(shell root-config --libs)

.PHONY: all

all: $(BINPATH)/tuple_dump

clean:
	@rm -rf $(BINPATH)/*

# Utilities
$(BINPATH)/%: $(SRCPATH)/%.cpp
	$(COMPILER) $(CXXFLAGS) -o $(BINPATH)/$(@F) $(SRCPATH)/$(@F).cpp $(LINKFLAGS)

# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Fri Jun 28, 2019 at 04:36 PM -0400

BINPATH	:=	bin
SRCPATH	:=	src

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
ADDFLAGS	:=	-ggdb
LINKFLAGS	:=	$(shell root-config --libs)

.PHONY: all utils

all: 2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.yml

utils: $(BINPATH)/tuple_dump

clean:
	@rm -rf $(BINPATH)/*

####################
# Generic patterns #
####################

%.yml: %.root $(BINPATH)/tuple_dump
	$(BINPATH)/tuple_dump $(@D)/$(basename $(@F)).root $@ "/DecayTree"

#############
# Utilities #
#############

$(BINPATH)/%: $(SRCPATH)/%.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDFLAGS) -o $(BINPATH)/$(@F) $(SRCPATH)/$(@F).cpp $(LINKFLAGS)

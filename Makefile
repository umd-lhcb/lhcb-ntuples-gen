# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Jul 01, 2019 at 04:33 AM -0400

BINPATH	:=	bin
SRCPATH	:=	src

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
ADDFLAGS	:=	-ggdb
LINKFLAGS	:=	$(shell root-config --libs)

.PHONY: all utils

all: 2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands_postprocess.root

utils: $(BINPATH)/tuple_dump

clean:
	@rm -rf $(BINPATH)/*

###################################
# 2012-b2D0MuXB2DMuNuForTauMuLine #
###################################

2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands_postprocess.root: \
	2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.root $(BINPATH)/YCands_postprocess
	$(BINPATH)/YCands_postprocess $< $@

$(SRCPATH)/YCands_postprocess.cpp: \
	babymaker.py 2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.yml
	./babymaker.py \
		-i 2012-b2D0MuXB2DMuNuForTauMuLine/ntuple_postprocess.yml \
		-d 2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.yml \
		-o $@ -g PostProcess
	clang-format -i $@

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

# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sat Jul 06, 2019 at 09:37 PM -0400

BINPATH	:=	bin
SRCPATH	:=	gen

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
LINKFLAGS	:=	$(shell root-config --libs)
ADDFLAGS	:=	-Iinclude

.PHONY: all utils clean

all: 2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands_postprocess.root

utils: $(BINPATH)/tuple_dump

clean:
	@rm -rf $(BINPATH)/*
	find . -name '*_postprocess.root' -delete

###################################
# 2012-b2D0MuXB2DMuNuForTauMuLine #
###################################

2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands_postprocess.root: \
	2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.root \
	$(BINPATH)/YCands_postprocess
	$(BINPATH)/YCands_postprocess $< $@

$(SRCPATH)/YCands_postprocess.cpp: \
	2012-b2D0MuXB2DMuNuForTauMuLine/ntuple_postprocess.yml \
	2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.root \
	include/functor/*.h
	babymaker \
		-i $< -o $@
		-d 2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.root \
	clang-format -i $@

####################
# Generic patterns #
####################

$(BINPATH)/%: $(SRCPATH)/%.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDFLAGS) -o $(BINPATH)/$(@F) $(SRCPATH)/$(@F).cpp $(LINKFLAGS)

# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sat Jul 06, 2019 at 10:02 PM -0400

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
	@rm -rf $(BINPATH)/*.exe
	@rm -rf $(SRCPATH)/*
	@find . -name '*_postprocess.root' -delete

###################################
# 2012-b2D0MuXB2DMuNuForTauMuLine #
###################################

2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands_postprocess.root: \
	2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.root \
	$(BINPATH)/YCands_postprocess.exe
	$(BINPATH)/YCands_postprocess.exe $< $@

$(SRCPATH)/YCands_postprocess.cpp: \
	2012-b2D0MuXB2DMuNuForTauMuLine/ntuple_postprocess.yml \
	2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.root \
	include/functor/*.h
	babymaker \
		-i $< -o $@ \
		-d 2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.root

####################
# Generic patterns #
####################

$(BINPATH)/%.exe: $(SRCPATH)/%.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDFLAGS) -o $@ $(SRCPATH)/$(basename $(@F)).cpp $(LINKFLAGS)

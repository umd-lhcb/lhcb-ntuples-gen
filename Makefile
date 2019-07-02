# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Jul 02, 2019 at 12:51 AM -0400

BINPATH	:=	bin
SRCPATH	:=	src

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
ADDFLAGS	:=	-ggdb
LINKFLAGS	:=	$(shell root-config --libs)

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
	2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.root $(BINPATH)/YCands_postprocess
	$(BINPATH)/YCands_postprocess $< $@

$(SRCPATH)/YCands_postprocess.cpp: \
	2012-b2D0MuXB2DMuNuForTauMuLine/ntuple_postprocess.yml \
	2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.yml \
	babymaker.py
	./babymaker.py \
		-i $< -d 2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.yml \
		-o $@ -g PostProcess
	clang-format -i $@

####################
# Generic patterns #
####################

%.yml: %.root $(BINPATH)/tuple_dump
	$(BINPATH)/tuple_dump $(@D)/$(basename $(@F)).root $@

$(BINPATH)/%: $(SRCPATH)/%.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDFLAGS) -o $(BINPATH)/$(@F) $(SRCPATH)/$(@F).cpp $(LINKFLAGS)

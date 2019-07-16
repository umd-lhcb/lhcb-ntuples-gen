# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Jul 15, 2019 at 11:08 PM -0400

BINPATH	:=	bin
SRCPATH	:=	gen

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
LINKFLAGS	:=	$(shell root-config --libs)
ADDFLAGS	:=	-Iinclude

.PHONY: all clean

all: 2012-b2D0MuXB2DMuNuForTauMuLine/BCands_Dst-data-postprocess.root

clean:
	@rm -rf $(BINPATH)/*.exe
	@rm -rf $(SRCPATH)/*
	@find . -name '*-postprocess.root' -delete

###################################
# 2012-b2D0MuXB2DMuNuForTauMuLine #
###################################

2012-b2D0MuXB2DMuNuForTauMuLine/BCands_Dst-data-postprocess.root: \
	2012-b2D0MuXB2DMuNuForTauMuLine/BCands_Dst-data.root \
	$(BINPATH)/BCands_Dst-data-postprocess.exe
	$(BINPATH)/BCands_Dst-data-postprocess.exe $< $@

$(SRCPATH)/BCands_Dst-data-postprocess.cpp: \
	2012-b2D0MuXB2DMuNuForTauMuLine/postprocess-sample.yml \
	2012-b2D0MuXB2DMuNuForTauMuLine/BCands_Dst-data.root \
	include/functor/*.h
	babymaker \
		-i $< -o $@ \
		-d 2012-b2D0MuXB2DMuNuForTauMuLine/BCands_Dst-data.root

####################
# Generic patterns #
####################

$(BINPATH)/%.exe: $(SRCPATH)/%.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDFLAGS) -o $@ $(SRCPATH)/$(basename $(@F)).cpp $(LINKFLAGS)

# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Sep 05, 2019 at 03:21 AM -0400

BINPATH	:=	bin
SRCPATH	:=	gen

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
LINKFLAGS	:=	$(shell root-config --libs)
ADDFLAGS	:=	-Iinclude

.PHONY: all clean

all: gen/run1-Dst-step2/BCands_Dst-data-2012-mag_down-step2.root

clean:
	@rm -rf $(BINPATH)/*
	@rm -rf $(SRCPATH)/*
	@find . -name '*-step2.root' -delete

###################################
# 2012-b2D0MuXB2DMuNuForTauMuLine #
###################################

gen/run1-Dst-step2/BCands_Dst-data-2012-mag_down-step2.root: \
	2012-b2D0MuXB2DMuNuForTauMuLine/ntuples/run1-Dst/BCands_Dst-yipeng-data-2012-mag_down.root \
	$(BINPATH)/Dst-data
	$(BINPATH)/Dst-data $< $@

$(SRCPATH)/Dst-data.cpp: \
	2012-b2D0MuXB2DMuNuForTauMuLine/postprocess/Dst-data.yml \
	2012-b2D0MuXB2DMuNuForTauMuLine/BCands_Dst-data.root \
	include/functor/*.h
	babymaker \
		-i $< -o $@ \
		-d 2012-b2D0MuXB2DMuNuForTauMuLine/ntuples/run1-Dst/BCands_Dst-yipeng-data-2012-mag_down.root

####################
# Generic patterns #
####################

$(BINPATH)/%: $(SRCPATH)/%.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDFLAGS) -o $@ $< $(LINKFLAGS)

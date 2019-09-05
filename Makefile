# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Sep 05, 2019 at 06:56 PM -0400

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

###############
# Run 1: 2012 #
###############

gen/run1-Dst-step2/BCands_Dst-data-2012-mag_down-step2.root: \
	run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/run1-Dst/BCands_Dst-yipeng-data-2012-mag_down.root \
	$(BINPATH)/run1-Dst-data
	$(BINPATH)/run1-Dst-data $< $@

$(SRCPATH)/run1-Dst-data.cpp: \
	run1-b2D0MuXB2DMuNuForTauMuLine/postprocess/Dst-data.yml \
	run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/run1-Dst/BCands_Dst-yipeng-data-2012-mag_down.root \
	include/functor/*.h
	babymaker \
		-i $< -o $@ \
		-d run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/run1-Dst/BCands_Dst-yipeng-data-2012-mag_down.root

####################
# Generic patterns #
####################

$(BINPATH)/%: $(SRCPATH)/%.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDFLAGS) -o $@ $< $(LINKFLAGS)

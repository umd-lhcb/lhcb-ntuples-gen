# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Sep 09, 2019 at 05:07 PM -0400

BINPATH	:=	bin
SRCPATH	:=	gen

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
LINKFLAGS	:=	$(shell root-config --libs)
ADDFLAGS	:=	-Iinclude

.PHONY: all clean

all: \
	gen/run1-Dst-step2/BCands_Dst-phoebe-data-2012-mag_down-step2.root \
	gen/run1-Dst-step2/BCands_Dst-yipeng-data-2012-mag_down-step2.root \
	gen/run2-Dst-step2/BCands_Dst-yipeng-data-2016-mag_down-step2.root

clean:
	@rm -rf $(BINPATH)/*
	@find ./gen -name '*-step2.root' -delete
	@find ./gen -name '*.cpp' -delete


#########################
# Run 1, Phoebe's: 2012 #
#########################

gen/run1-Dst-step2/BCands_Dst-phoebe-data-2012-mag_down-step2.root: \
	run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/run1-Dst/BCands_Dst-phoebe-data-2012-mag_down.root \
	$(BINPATH)/run1-Dst-data-phoebe
	$(word 2, $^) $< $@

$(SRCPATH)/run1-Dst-data-phoebe.cpp: \
	run1-b2D0MuXB2DMuNuForTauMuLine/postprocess/Dst-data-phoebe.yml \
	run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/run1-Dst/BCands_Dst-phoebe-data-2012-mag_down.root \
	include/functor/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)


#########################
# Run 1, Yipeng's: 2012 #
#########################

gen/run1-Dst-step2/BCands_Dst-yipeng-data-2012-mag_down-step2.root: \
	run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/run1-Dst/BCands_Dst-yipeng-data-2012-mag_down.root \
	$(BINPATH)/run1-Dst-data-yipeng
	$(word 2, $^) $< $@

$(SRCPATH)/run1-Dst-data-yipeng.cpp: \
	run1-b2D0MuXB2DMuNuForTauMuLine/postprocess/Dst-data-yipeng.yml \
	run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/run1-Dst/BCands_Dst-yipeng-data-2012-mag_down.root \
	include/functor/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)


#########################
# Run 2, Yipeng's: 2016 #
#########################

gen/run2-Dst-step2/BCands_Dst-yipeng-data-2016-mag_down-step2.root: \
	run2-b2D0MuXB2DMuForTauMuLine/ntuples/run2-Dst/BCands_Dst-yipeng-data-2016-mag_down.root \
	$(BINPATH)/run2-Dst-data-yipeng
	$(word 2, $^) $< $@

$(SRCPATH)/run2-Dst-data-yipeng.cpp: \
	run2-b2D0MuXB2DMuForTauMuLine/postprocess/Dst-data-yipeng.yml \
	run2-b2D0MuXB2DMuForTauMuLine/ntuples/run2-Dst/BCands_Dst-yipeng-data-2016-mag_down.root \
	include/functor/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)


####################
# Generic patterns #
####################

$(BINPATH)/%: $(SRCPATH)/%.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDFLAGS) -o $@ $< $(LINKFLAGS)

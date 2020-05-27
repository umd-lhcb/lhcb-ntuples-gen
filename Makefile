# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed May 27, 2020 at 05:04 AM +0800

BINPATH	:=	bin
SRCPATH	:=	gen

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
LINKFLAGS	:=	$(shell root-config --libs)
ADDFLAGS	:=	-Iinclude

.PHONY: all clean \
	cutflow-RDst cutflow-RDst-web \
	cutflow-RDst-data cutflow-RDst-data-web \
	cutflow-RDst-detail-individual cutflow-RDst-detail-individual-web

all: \
	gen/run1-Dst-step2/BCands_Dst-phoebe-data-2012-mag_down-step2.root \
	gen/run1-Dst-step2/BCands_Dst-yipeng-data-2012-mag_down-step2.root \
	gen/run2-Dst-step2/BCands_Dst-yipeng-data-2016-mag_down-step2.root \
	gen/run1-Dst-step2/BCands_Dst-yipeng-cutflow_data-2012-mag_down-step2.root \
	gen/run2-Dst-step2/BCands_Dst-yipeng-cutflow_data-2016-mag_down-step2.root

clean:
	@rm -rf $(BINPATH)/*
	@find ./gen -name '*-step2.root' -delete
	@find ./gen -name '*.cpp' -delete


############
# Cutflows #
############

# Cutflow for R(D(*))
cutflow-RDst: \
	run1-b2D0MuXB2DMuNuForTauMuLine/cutflow/output-run1.yml \
	run2-b2D0MuXB2DMuForTauMuLine/cutflow/output-run2.yml
	@./utils/cutflow_gen.py -o $(word 1, $^) -t $(word 2, $^) | tabgen.py -f latex_booktabs_raw

cutflow-RDst-web: \
	run1-b2D0MuXB2DMuNuForTauMuLine/cutflow/output-run1.yml \
	run2-b2D0MuXB2DMuForTauMuLine/cutflow/output-run2.yml
	@./utils/cutflow_gen.py -o $(word 1, $^) -t $(word 2, $^) -n | tabgen.py -f github

# Cutflow for R(D(*)), with real data
cutflow-RDst-data: \
	run1-b2D0MuXB2DMuNuForTauMuLine/cutflow/output-run1-data.yml \
	run2-b2D0MuXB2DMuForTauMuLine/cutflow/output-run2-data.yml
	@./utils/cutflow_gen.py -o $(word 1, $^) -t $(word 2, $^) | tabgen.py -f latex_booktabs_raw

cutflow-RDst-data-web: \
	run1-b2D0MuXB2DMuNuForTauMuLine/cutflow/output-run1-data.yml \
	run2-b2D0MuXB2DMuForTauMuLine/cutflow/output-run2-data.yml
	@./utils/cutflow_gen.py -o $(word 1, $^) -t $(word 2, $^) -n | tabgen.py -f github

# Cutflow for R(D(*)), detail: individual
cutflow-RDst-detail-individual: \
	run1-b2D0MuXB2DMuNuForTauMuLine/cutflow/output-run1-individual.yml \
	run2-b2D0MuXB2DMuForTauMuLine/cutflow/output-run2-individual.yml
	@./utils/cutflow_gen.py -o $(word 1, $^) -t $(word 2, $^) -n | tabgen.py -f latex_booktabs_raw

cutflow-RDst-detail-individual-web: \
	run1-b2D0MuXB2DMuNuForTauMuLine/cutflow/output-run1-individual.yml \
	run2-b2D0MuXB2DMuForTauMuLine/cutflow/output-run2-individual.yml
	@./utils/cutflow_gen.py -o $(word 1, $^) -t $(word 2, $^) -n | tabgen.py -f github


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

gen/run1-Dst-step2/BCands_Dst-yipeng-cutflow_data-2012-mag_down-step2.root: \
	run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/cutflow-Dst/BCands_Dst-yipeng-cutflow_data-2012-mag_down.root \
	$(BINPATH)/run1-Dst-cutflow_data-yipeng  # NOTE the binary name here!
	$(word 2, $^) $< $@

$(SRCPATH)/run1-Dst-data-yipeng.cpp: \
	run1-b2D0MuXB2DMuNuForTauMuLine/postprocess/Dst-data-yipeng.yml \
	run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/run1-Dst/BCands_Dst-yipeng-data-2012-mag_down.root \
	include/functor/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)

$(SRCPATH)/run1-Dst-cutflow_data-yipeng.cpp: \
	run1-b2D0MuXB2DMuNuForTauMuLine/postprocess/Dst-cutflow_data-yipeng.yml \
	run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/cutflow-Dst/BCands_Dst-yipeng-cutflow_data-2012-mag_down.root \
	include/functor/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)


#########################
# Run 2, Yipeng's: 2016 #
#########################

gen/run2-Dst-step2/BCands_Dst-yipeng-data-2016-mag_down-step2.root: \
	run2-b2D0MuXB2DMuForTauMuLine/ntuples/run2-Dst/BCands_Dst-yipeng-data-2016-mag_down.root \
	$(BINPATH)/run2-Dst-data-yipeng
	$(word 2, $^) $< $@

gen/run2-Dst-step2/BCands_Dst-yipeng-cutflow_data-2016-mag_down-step2.root: \
	run2-b2D0MuXB2DMuForTauMuLine/ntuples/cutflow-Dst/BCands_Dst-yipeng-cutflow_data-2016-mag_down.root \
	$(BINPATH)/run2-Dst-data-yipeng
	$(word 2, $^) $< $@

$(SRCPATH)/run2-Dst-data-yipeng.cpp: \
	run2-b2D0MuXB2DMuForTauMuLine/postprocess/Dst-data-yipeng.yml \
	run2-b2D0MuXB2DMuForTauMuLine/ntuples/run2-Dst/BCands_Dst-yipeng-data-2016-mag_down.root \
	include/functor/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)


#########
# Tests #
#########

.PHONY: test-cutflow

test-cutflow: \
	gen/run1-Dst-step2/200522-Dst-cutflow_mc-2011-md-dv45-subset-no_stripping-step2.root
	@echo 'Yes'

gen/run1-Dst-step2/200522-Dst-cutflow_mc-2011-md-dv45-subset-no_stripping-step2.root: \
	run1-b2D0MuXB2DMuNuForTauMuLine/samples/200522-Dst-cutflow_mc-2011-md-dv45-subset-no_stripping.root \
	$(BINPATH)/run1-Dst-full_cuts
	$(word 2, $^) $< $@

$(SRCPATH)/run1-Dst-full_cuts.cpp: \
	run1-b2D0MuXB2DMuNuForTauMuLine/postprocess/Dst-full_cuts.yml \
	run1-b2D0MuXB2DMuNuForTauMuLine/samples/200522-Dst-cutflow_mc-2011-md-dv45-subset-no_stripping.root \
	include/functor/*.h \
	include/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)


####################
# Generic patterns #
####################

$(BINPATH)/%: $(SRCPATH)/%.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDFLAGS) -o $@ $< $(LINKFLAGS)

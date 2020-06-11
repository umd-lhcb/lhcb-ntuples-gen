# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Jun 11, 2020 at 10:24 PM +0800

BINPATH	:=	bin
SRCPATH	:=	gen

export PATH := test:utils:$(BINPATH):$(PATH)

VPATH := run1-b2D0MuXB2DMuNuForTauMuLine/samples:run2-b2D0MuXB2DMuForTauMuLine/samples
VPATH := run1-b2D0MuXB2DMuNuForTauMuLine/cutflow:run2-b2D0MuXB2DMuForTauMuLine/cutflow:$(VPATH)
VPATH := ntuples/0.9.0-cutflow/Dst-cutflow_mc:$(VPATH)
VPATH := gen/run2-Dst-step2:gen/run1-Dst-step2:$(VPATH)
VPATH := $(BINPATH):utils:$(VPATH)

# System env
OS := $(shell uname)

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
LINKFLAGS	:=	$(shell root-config --libs)
ADDFLAGS	:=	-Iinclude

.PHONY: all clean history \
	docker-dv \
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
	@find ./gen -name '*.root' -delete
	@find ./gen -name '*.cpp' -delete
	@find ./gen -name '*.yml' -delete

history:
	@git tag -l -n99


#####################
# Run docker images #
#####################

ifeq ($(OS),Darwin)
DV_CMD = "docker run --rm -it -v $$(pwd):/data -e UID=$$(id -u) -e GID=$$(id -g) --net=host umdlhcb/lhcb-stack-cc7:DaVinci-v45r3-SL"
else
DV_CMD = "docker run --rm -it -v $$(pwd):/data -v $$HOME/.Xauthority:/home/physicist/.Xauthority -e DISPLAY -e UID=$$(id -u) -e GID=$$(id -g) --net=host umdlhcb/lhcb-stack-cc7:DaVinci-v45r3-SL"
endif

docker-dv:
	@eval $(DV_CMD)


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


# Cutflow for D*, bare
cutflow-Dst-bare: \
	gen/cutflow/output-run1-bare.yml \
	gen/cutflow/output-run2-bare.yml
	@cutflow_gen.py -o $< -t $(word 2, $^) -n | tabgen.py -f latex_booktabs_raw

cutflow-Dst-bare-web: \
	gen/cutflow/output-run1-bare.yml \
	gen/cutflow/output-run2-bare.yml
	@cutflow_gen.py -o $< -t $(word 2, $^) -n | tabgen.py -f github


gen/cutflow/output-run1-bare.yml: \
	Dst--20_06_05--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	Dst--20_06_05--cutflow_mc--cocktail--2011--md--bare-step2.root \
	input-run1-bare.yml \
	cutflow_output_yml_gen-bare.py
	@$(word 4, $^) $< $(word 2, $^) $(word 3, $^) $@ run1

gen/cutflow/output-run2-bare.yml: \
	Dst--20_06_05--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	Dst--20_06_05--cutflow_mc--cocktail--2016--md--bare-step2.root \
	input-run2-bare.yml \
	cutflow_output_yml_gen-bare.py
	@$(word 4, $^) $< $(word 2, $^) $(word 3, $^) $@ run2


#########
# Run 1 #
#########

gen/run1-Dst-step2/BCands_Dst-phoebe-data-2012-mag_down-step2.root: \
	run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/run1-Dst/BCands_Dst-phoebe-data-2012-mag_down.root \
	$(BINPATH)/run1-Dst-data-phoebe
	$(word 2, $^) $< $@


$(SRCPATH)/run1-Dst-data-phoebe.cpp: \
	run1-b2D0MuXB2DMuNuForTauMuLine/postprocess/Dst-data-phoebe.yml \
	run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/run1-Dst/BCands_Dst-phoebe-data-2012-mag_down.root \
	include/functor/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)

gen/run1-Dst-step2/Dst--20_06_05--cutflow_mc--cocktail--2011--md--bare-step2.root: \
	Dst--20_06_05--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	run1-Dst-stripping
	$(word 2, $^) $< $@


#########
# Run 1 #
#########

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


#########
# Run 2 #
#########

# Dst, std, 2016
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


# Dst, cutflow_mc, 2016
gen/run2-Dst-step2/Dst--20_06_05--cutflow_mc--cocktail--2016--md--bare-step2.root: \
	Dst--20_06_05--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	run2-Dst-stripping
	$(word 2, $^) $< $@


#########
# Tests #
#########

.PHONY: test-naming-conv test-cutflow-run1 test-cutflow-run2

test-naming-conv:
	@test_filename_convention.py


test-cutflow-run1: \
	gen/test/Dst--cutflow_mc--cocktail--2011--md--subset-bare-step2.root \
	gen/test/Dst--cutflow_mc--cocktail--2011--md--subset-dv_strip-step2.root \
	Dst--20_06_04--cutflow_mc--cocktail--2011--md--dv45-subset-dv_strip.root
	@echo "===="
	@echo "Test results:"
	@test_ntuple_identical.py -n $< -N $(word 3, $^) -t b0dst -T TupleB0/DecayTree
	@test_ntuple_identical.py -n $(word 2, $^) -N $(word 3, $^) -t b0dst -T TupleB0/DecayTree


gen/test/Dst--cutflow_mc--cocktail--2011--md--subset-bare-step2.root: \
	Dst--20_06_04--cutflow_mc--cocktail--2011--md--dv45-subset-bare.root \
	run1-Dst-stripping
	$(word 2, $^) $< $@

gen/test/Dst--cutflow_mc--cocktail--2011--md--subset-dv_strip-step2.root: \
	Dst--20_06_04--cutflow_mc--cocktail--2011--md--dv45-subset-dv_strip.root \
	run1-Dst-stripping
	$(word 2, $^) $< $@

$(SRCPATH)/run1-Dst-stripping.cpp: \
	run1-b2D0MuXB2DMuNuForTauMuLine/postprocess/Dst-stripping.yml \
	Dst--20_06_04--cutflow_mc--cocktail--2011--md--dv45-subset-dv_strip.root \
	include/functor/*.h \
	include/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)


test-cutflow-run2: \
	gen/test/Dst--cutflow_mc--cocktail--2016--md--subset-dv_strip-step2.root \
	gen/test/Dst--cutflow_mc--cocktail--2016--md--subset-bare-step2.root \
	Dst--20_06_04--cutflow_mc--cocktail--2016--md--dv45-subset-dv_strip.root
	@echo "===="
	@echo "Test results:"
	@test_ntuple_identical.py -n $< -N $(word 3, $^) -t b0dst -T TupleB0/DecayTree
	@test_ntuple_identical.py -n $(word 2, $^) -N $(word 3, $^) -t b0dst -T TupleB0/DecayTree


gen/test/Dst--cutflow_mc--cocktail--2016--md--subset-dv_strip-step2.root: \
	Dst--20_06_04--cutflow_mc--cocktail--2016--md--dv45-subset-dv_strip.root \
	run2-Dst-stripping
	$(word 2, $^) $< $@

gen/test/Dst--cutflow_mc--cocktail--2016--md--subset-bare-step2.root: \
	Dst--20_06_04--cutflow_mc--cocktail--2016--md--dv45-subset-bare.root \
	run2-Dst-stripping
	$(word 2, $^) $< $@

$(SRCPATH)/run2-Dst-stripping.cpp: \
	run2-b2D0MuXB2DMuForTauMuLine/postprocess/Dst-stripping.yml \
	Dst--20_06_04--cutflow_mc--cocktail--2016--md--dv45-subset-dv_strip.root \
	include/functor/*.h \
	include/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)


####################
# Generic patterns #
####################

$(BINPATH)/%: $(SRCPATH)/%.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDFLAGS) -o $@ $< $(LINKFLAGS)

%: $(SRCPATH)/%.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDFLAGS) -o $(BINPATH)/$@ $< $(LINKFLAGS)

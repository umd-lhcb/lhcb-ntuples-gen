# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Oct 12, 2020 at 03:17 PM +0800

BINPATH	:=	bin

export PATH := test:scripts:$(BINPATH):$(PATH)

VPATH := postprocess:test:scripts:$(BINPATH)

# Sub-makefiles for different analyses
include ./postprocess/make/rdx.mk  # R(D(*))

# System env
OS := $(shell uname)
PWD := $(shell pwd)

# In-house Python libraries
LIB_PY := $(wildcard lib/python/*)

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
LINKFLAGS	:=	$(shell root-config --libs)
ADDFLAGS	:=	-Iinclude

DAVINCI_VERSION=DaVinci-v45r4-SL


.PHONY: all clean history tagdate install-dep

all: \
	gen/run1-Dst-step2/Dst--19_09_05--std--data--2012--md--step2.root \
	gen/run2-Dst-step2/Dst--19_09_09--std--data--2016--md--step2.root

clean:
	@rm -rf $(BINPATH)/*
	@find ./gen -name '*.root' -delete
	@find ./gen -name '*.cpp' -delete
	@find ./gen -name '*.yml' -delete

history:
	@git tag -l -n99

tagdate:
	@git log --date-order --tags --simplify-by-decoration --pretty='format:%C(green)%ad %C(red)%h %C(reset)%D' --date=short

install-dep:
	@echo "Installing third-party Python libraries..."
	@pip install -U -r ./requirements.txt
	@echo "Installing in-house Python libraries..."
	@for p in $(LIB_PY); do \
			cd $(PWD)/$$p; \
			pip install --force-reinstall .; \
		done;


#####################
# Run docker images #
#####################

.PHONY: docker-dv

ifeq ($(OS),Darwin)
DV_CMD = "docker run --rm -it -v $(PWD):/data -e UID=$$(id -u) -e GID=$$(id -g) --net=host umdlhcb/lhcb-stack-cc7:${DAVINCI_VERSION}"
else
DV_CMD = "docker run --rm -it -v $(PWD):/data -v $$HOME/.Xauthority:/home/physicist/.Xauthority -e DISPLAY -e UID=$$(id -u) -e GID=$$(id -g) --net=host umdlhcb/lhcb-stack-cc7:${DAVINCI_VERSION}"
endif

docker-dv:
	@eval $(DV_CMD)


#########################
# Tests: required files #
#########################

# For test on the equivalence betwen run 1 bare and dv_strip ntuples
gen/test/Dst--20_06_04--cutflow_mc--cocktail--2011--md--subset-bare-step2.root: \
	Dst--20_06_04--cutflow_mc--cocktail--2011--md--dv45-subset-bare.root \
	rdst-run1-strip.pp
	$(word 2, $^) $< $@

gen/test/Dst--20_06_04--cutflow_mc--cocktail--2011--md--subset-dv_strip-step2.root: \
	Dst--20_06_04--cutflow_mc--cocktail--2011--md--dv45-subset-dv_strip.root \
	rdst-run1-strip.pp
	$(word 2, $^) $< $@


# For test on the equivalence betwen run 2 bare and dv_strip ntuples.
gen/test/Dst--20_06_04--cutflow_mc--cocktail--2016--md--subset-dv_strip-step2.root: \
	Dst--20_06_04--cutflow_mc--cocktail--2016--md--dv45-subset-dv_strip.root \
	rdst-run2-strip.pp
	$(word 2, $^) $< $@

gen/test/Dst--20_06_04--cutflow_mc--cocktail--2016--md--subset-bare-step2.root: \
	Dst--20_06_04--cutflow_mc--cocktail--2016--md--dv45-subset-bare.root \
	rdst-run2-strip.pp
	$(word 2, $^) $< $@


# Cutflow re-stripped ntuples for D*.
gen/tes/Dst--20_06_05--cutflow_mc--cocktail--2011--md--bare-step2.root: \
	Dst--20_06_05--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	rdst-run1-strip.pp
	$(word 2, $^) $< $@

gen/run2-Dst-step2/Dst--20_06_05--cutflow_mc--cocktail--2016--md--bare-step2.root: \
	Dst--20_06_05--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	rdst-run2-strip.pp
	$(word 2, $^) $< $@


# Cutflow re-triggered and re-stripped ntuples for D*.
gen/test/Dst--20_06_05--cutflow_mc--cocktail--2011--md--bare-step2-triggered.root: \
	Dst--20_06_05--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	rdst-run1-trig_strip.pp
	$(word 2, $^) $< $@

gen/test/Dst--20_06_05--cutflow_mc--cocktail--2016--md--bare-step2-triggered.root: \
	Dst--20_06_05--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	rdst-run2-trig_strip.pp
	$(word 2, $^) $< $@


# Verify step-2 cuts with Phoebe's 2011 step-1 and step-2 ntuples
gen/test/Dst--20_07_02--mix--data--2011--md--phoebe-step2.root: \
	Dst--20_07_02--mix--all--2011-2012--md-mu--phoebe.root \
	rdst-2011-mix.pp
	$(word 2, $^) $< $@

gen/test/Dst--20_09_16--std--data--2011--md--phoebe-step2.root: \
	Dst--20_09_16--std--data--2011--md--phoebe.root \
	rdst-2011-data.pp
	$(word 2, $^) $< $@


#########
# Tests #
#########

.PHONY: test-all test-naming-conv test-cutflow-run1 test-cutflow-run2


test-all: \
	test-naming-conv \
	test-cutflow-run1 \
	test-cutflow-run2 \
	test-cutflow-consistency


# Test if specific files follow naming conventions.
test-naming-conv:
	@test_filename_convention.py


# Tests for the equivalence between local bare and dv_strip ntuples.
test-cutflow-run1: \
	gen/test/Dst--20_06_04--cutflow_mc--cocktail--2011--md--subset-bare-step2.root \
	gen/test/Dst--20_06_04--cutflow_mc--cocktail--2011--md--subset-dv_strip-step2.root \
	Dst--20_06_04--cutflow_mc--cocktail--2011--md--dv45-subset-dv_strip.root
	@echo "===="
	@echo "Test results:"
	@test_ntuple_identical.py -n $< -N $(word 3, $^) -t b0dst -T TupleB0/DecayTree
	@test_ntuple_identical.py -n $(word 2, $^) -N $(word 3, $^) -t b0dst -T TupleB0/DecayTree

test-cutflow-run2: \
	gen/test/Dst--20_06_04--cutflow_mc--cocktail--2016--md--subset-dv_strip-step2.root \
	gen/test/Dst--20_06_04--cutflow_mc--cocktail--2016--md--subset-bare-step2.root \
	Dst--20_06_04--cutflow_mc--cocktail--2016--md--dv45-subset-dv_strip.root
	@echo "===="
	@echo "Test results:"
	@test_ntuple_identical.py -n $< -N $(word 3, $^) -t b0dst -T TupleB0/DecayTree
	@test_ntuple_identical.py -n $(word 2, $^) -N $(word 3, $^) -t b0dst -T TupleB0/DecayTree


# Test if the number of events used in the cutflow generation is consistent.
test-cutflow-consistency: \
	gen/test/Dst--20_06_05--cutflow_mc--cocktail--2011--md--bare-step2-triggered.root \
	gen/test/Dst--20_06_05--cutflow_mc--cocktail--2016--md--bare-step2-triggered.root


####################
# Generic patterns #
####################

%.pp: gen/%.cpp \
	include/functor/*.h \
	include/*.h
	$(COMPILER) $(CXXFLAGS) $(ADDFLAGS) -o $(BINPATH)/$@ $< $(LINKFLAGS)

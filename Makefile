# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Sep 17, 2020 at 08:37 PM +0800

BINPATH	:=	bin

export PATH := test:scripts:$(BINPATH):$(PATH)

VPATH := test:scripts:$(BINPATH)
VPATH := run1-b2D0MuXB2DMuNuForTauMuLine/samples:run2-b2D0MuXB2DMuForTauMuLine/samples:$(VPATH)
VPATH := run1-b2D0MuXB2DMuNuForTauMuLine/cutflow:run2-b2D0MuXB2DMuForTauMuLine/cutflow:$(VPATH)
VPATH := ntuples/pre-0.9.0/Dst-std:$(VPATH)
VPATH := ntuples/pre-0.9.0/Dst-cutflow_mc:ntuples/pre-0.9.0/Dst-cutflow_data:$(VPATH)
VPATH := ntuples/0.9.0-cutflow/Dst-cutflow_mc:$(VPATH)
VPATH := ntuples/0.9.1-dst_partial_refit/Dst_D0-cutflow_mc:$(VPATH)
VPATH := ntuples/ref-rdx-run1/Dst-std:$(VPATH)
VPATH := ntuples/ref-rdx-run1/Dst-mix:$(VPATH)
VPATH := gen/run2-Dst-step2:gen/run1-Dst-step2:$(VPATH)
VPATH := postprocess:$(VPATH)

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
	gen/run1-Dst-step2/Dst--19_09_05--std--data--2012--md--phoebe-step2.root \
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


###########################
# Cutflow: required files #
###########################

# Cutflow output YAML for D*, MC, bare.
gen/cutflow/output-run1-bare.yml: \
	Dst--20_06_05--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	input-run1-bare.yml \
	cutflow_output_yml_gen.py
	@$(word 3, $^) $< $(word 2, $^) $@ run1-bare -t 'TupleB0/DecayTree'

gen/cutflow/output-run2-bare.yml: \
	Dst--20_06_05--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	input-run2-bare.yml \
	cutflow_output_yml_gen.py
	@$(word 3, $^) $< $(word 2, $^) $@ run2-bare -t 'TupleB0/DecayTree'


# Cutflow output YAML for D*, MC.
gen/cutflow/output-run1.yml: \
	Dst--20_03_18--cutflow_mc--cocktail--2011--md.root \
	input-run1.yml \
	cutflow_output_yml_gen_pre_0.9.0.py
	@$(word 3, $^) $< $(word 2, $^) $@ run1 -t 'TupleB0/DecayTree'

gen/cutflow/output-run2.yml: \
	Dst--20_03_18--cutflow_mc--cocktail--2016--md.root \
	input-run2.yml \
	cutflow_output_yml_gen_pre_0.9.0.py
	@$(word 3, $^) $< $(word 2, $^) $@ run2 -t 'TupleB0/DecayTree'


# Cutflow output YAML for D*, data.
gen/cutflow/output-run1-data.yml: \
	Dst--20_04_03--cutflow_data--data--2012--md.root \
	input-run1-data.yml \
	cutflow_output_yml_gen_pre_0.9.0.py
	@$(word 3, $^) $< $(word 2, $^) $@ run1 -t 'TupleB0/DecayTree'

gen/cutflow/output-run2-data.yml: \
	Dst--20_04_03--cutflow_data--data--2016--md.root \
	input-run2-data.yml \
	cutflow_output_yml_gen_pre_0.9.0.py
	@$(word 3, $^) $< $(word 2, $^) $@ run2-data -t 'TupleB0/DecayTree'


# Cutflow output YAML for signal, normalization, and D** yield, run 1
gen/cutflow/output-run1-%.yml: \
	Dst--20_06_05--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	cutflow_components.py
	@$(word 2, $^) $< $@ run1-$* -t 'TupleB0/DecayTree'


# Cutflow output YAML for signal, normalization, and D** yield, run 2
gen/cutflow/output-run2-%.yml: \
	Dst--20_06_05--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	cutflow_components.py
	@$(word 2, $^) $< $@ run2-$* -t 'TupleB0/DecayTree'


# UNUSED: Cutflow for D*, detail: individual
gen/cutflow/output-run1-individual.yml: \
	Dst--20_03_18--cutflow_mc--cocktail--2011--md.root \
	cutflow_detail.py
	@$(word 2, $^) $< $@ run1

gen/cutflow/output-run2-individual.yml: \
	Dst--20_03_18--cutflow_mc--cocktail--2016--md.root \
	cutflow_detail.py
	@$(word 2, $^) $< $@ run2


# Study the effect of refit D* only
gen/cutflow/output-run2-cocktail-refit_dst_only-%.yml: \
	Dst_D0--20_08_18--cutflow_mc--refit_dst_only--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	cutflow_components.py
	@$(word 2, $^) $< $@ run2-$* -t 'TupleB0/DecayTree'

gen/cutflow/output-run2-cocktail-full_refit-%.yml: \
	Dst_D0--20_08_18--cutflow_mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	cutflow_components.py
	@$(word 2, $^) $< $@ run2-$* -t 'TupleB0/DecayTree'


###########
# Cutflow #
###########

.PHONY: cutflow-Dst-bare cutflow-Dst-bare-web \
	cutflow-Dst-data cutflow-Dst-data-web \
	cutflow-Dst cutflow-Dst-web \
	cutflow-sig-nor-dss-run1 cutflow-sig-nor-dss-run2 \
	cutflow-all


# All cutflow studies:
cutflow-all: \
	cutflow-Dst cutflow-Dst-bare cutflow-Dst-data \
	cutflow-sig-nor-dss-run1 cutflow-sig-nor-dss-run2


# Cutflow for D*, MC, bare.
cutflow-Dst-bare: \
	gen/cutflow/output-run1-bare.yml \
	gen/cutflow/output-run2-bare.yml \
	cutflow_gen.py
	@$(word 3, $^) -o $< -t $(word 2, $^) -n | tabgen.py -f latex_booktabs_raw

cutflow-Dst-bare-web: \
	gen/cutflow/output-run1-bare.yml \
	gen/cutflow/output-run2-bare.yml \
	cutflow_gen.py
	@$(word 3, $^) -o $< -t $(word 2, $^) -n | tabgen.py -f github


# Cutflow for D*, MC.
cutflow-Dst: \
	gen/cutflow/output-run1.yml \
	gen/cutflow/output-run2.yml \
	cutflow_gen.py
	@$(word 3, $^) -o $< -t $(word 2, $^) -n | tabgen.py -f latex_booktabs_raw

cutflow-Dst-web: \
	gen/cutflow/output-run1.yml \
	gen/cutflow/output-run2.yml \
	cutflow_gen.py
	@$(word 3, $^) -o $< -t $(word 2, $^) -n | tabgen.py -f github


# Cutflow for D*, data.
cutflow-Dst-data: \
	gen/cutflow/output-run1-data.yml \
	gen/cutflow/output-run2-data.yml \
	cutflow_gen.py
	@$(word 3, $^) -o $< -t $(word 2, $^) -n | tabgen.py -f latex_booktabs_raw

cutflow-Dst-data-web: \
	gen/cutflow/output-run1-data.yml \
	gen/cutflow/output-run2-data.yml \
	cutflow_gen.py
	@$(word 3, $^) -o $< -t $(word 2, $^) -n | tabgen.py -f github


# Cutflow for signal, normalization, and D** yield, run 1
cutflow-sig-nor-dss-run1: \
	gen/cutflow/output-run1-sig.yml \
	gen/cutflow/output-run1-nor.yml \
	gen/cutflow/output-run1-dss.yml \
	table_cutflow_components.py
	@$(word 4, $^) -s $(word 1, $^) -n $(word 2, $^) -d $(word 3, $^) | tabgen.py -f latex_booktabs_raw


# Cutflow for signal, normalization, and D** yield, run 2
cutflow-sig-nor-dss-run2: \
	gen/cutflow/output-run2-sig.yml \
	gen/cutflow/output-run2-nor.yml \
	gen/cutflow/output-run2-dss.yml \
	table_cutflow_components.py
	@$(word 4, $^) -s $(word 1, $^) -n $(word 2, $^) -d $(word 3, $^) | tabgen.py -f latex_booktabs_raw


# UNUSED: Cutflow for D*, detail: individual
cutflow-Dst-detail-individual: \
	gen/cutflow/output-run1-individual.yml \
	gen/cutflow/output-run2-individual.yml \
	cutflow_gen.py
	@$(word 3, $^) -o $(word 1, $^) -t $(word 2, $^) -n | tabgen.py -f latex_booktabs_raw


# Study the effect of refit D* only
cutflow-sig-nor-dss-run2-cocktail-refit_dst_only: \
	gen/cutflow/output-run2-cocktail-refit_dst_only-sig.yml \
	gen/cutflow/output-run2-cocktail-refit_dst_only-nor.yml \
	gen/cutflow/output-run2-cocktail-refit_dst_only-dss.yml \
	table_cutflow_components.py
	@$(word 4, $^) -s $(word 1, $^) -n $(word 2, $^) -d $(word 3, $^) | tabgen.py -f github

cutflow-sig-nor-dss-run2-cocktail-full_refit: \
	gen/cutflow/output-run2-cocktail-full_refit-sig.yml \
	gen/cutflow/output-run2-cocktail-full_refit-nor.yml \
	gen/cutflow/output-run2-cocktail-full_refit-dss.yml \
	table_cutflow_components.py
	@$(word 4, $^) -s $(word 1, $^) -n $(word 2, $^) -d $(word 3, $^) | tabgen.py -f github


#########
# Run 1 #
#########

# Dst, std, 2012
gen/run1-Dst-step2/Dst--19_09_05--std--data--2012--md--step2.root: \
	Dst--19_09_05--std--data--2012--md.root \
	run1-Dst-data
	$(word 2, $^) $< $@

# Dst, std, 2012, Phoebe
gen/run1-Dst-step2/Dst--19_09_05--std--data--2012--md--phoebe-step2.root: \
	Dst--19_09_05--std--data--2012--md--phoebe.root \
	run1-Dst-data-phoebe
	$(word 2, $^) $< $@


# Generator for Dst, std, 2012
gen/run1-Dst-data.cpp: \
	run1-b2D0MuXB2DMuNuForTauMuLine/postprocess/Dst-data.yml \
	Dst--19_09_05--std--data--2012--md.root \
	include/functor/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)

# Generator for Dst, std, 2012, Phoebe
gen/run1-Dst-data-phoebe.cpp: \
	run1-b2D0MuXB2DMuNuForTauMuLine/postprocess/Dst-data-phoebe.yml \
	Dst--19_09_05--std--data--2012--md--phoebe.root \
	include/functor/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)


#########
# Run 2 #
#########

# Dst, std, 2016
gen/run2-Dst-step2/Dst--19_09_09--std--data--2016--md--step2.root: \
	Dst--19_09_09--std--data--2016--md.root \
	run2-Dst-data
	$(word 2, $^) $< $@

# Dst_D0, cutflow MC, cocktail, 2016
gen/run2-Dst_D0-step2/Dst_D0--20_08_18--cutflow_mc--cocktail--2016--md--step2.root: \
	Dst_D0--20_08_18--cutflow_mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	run2-Dst_D0-mc
	$(word 2, $^) $< $@


# Generator for Dst, std, 2016
gen/run2-Dst-data.cpp: \
	run2-b2D0MuXB2DMuForTauMuLine/postprocess/Dst-data.yml \
	Dst--19_09_09--std--data--2016--md.root \
	include/functor/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)

# Generator for Dst_D0, MC
gen/run2-Dst_D0-mc.cpp: \
	postprocess/rdx-run2-mc.yml \
	Dst_D0--20_08_18--cutflow_mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	postprocess/cpp_templates/rdx.cpp \
	include/functor/*.h
	babymaker -i $< -o $@ -d $(word 2, $^) -t $(word 3, $^)


#########################
# Tests: required files #
#########################

# For test on the equivalence betwen run 1 bare and dv_strip ntuples
gen/test/Dst--20_06_04--cutflow_mc--cocktail--2011--md--subset-bare-step2.root: \
	Dst--20_06_04--cutflow_mc--cocktail--2011--md--dv45-subset-bare.root \
	run1-Dst-stripping
	$(word 2, $^) $< $@

gen/test/Dst--20_06_04--cutflow_mc--cocktail--2011--md--subset-dv_strip-step2.root: \
	Dst--20_06_04--cutflow_mc--cocktail--2011--md--dv45-subset-dv_strip.root \
	run1-Dst-stripping
	$(word 2, $^) $< $@


# For test on the equivalence betwen run 2 bare and dv_strip ntuples.
gen/test/Dst--20_06_04--cutflow_mc--cocktail--2016--md--subset-dv_strip-step2.root: \
	Dst--20_06_04--cutflow_mc--cocktail--2016--md--dv45-subset-dv_strip.root \
	run2-Dst-stripping
	$(word 2, $^) $< $@

gen/test/Dst--20_06_04--cutflow_mc--cocktail--2016--md--subset-bare-step2.root: \
	Dst--20_06_04--cutflow_mc--cocktail--2016--md--dv45-subset-bare.root \
	run2-Dst-stripping
	$(word 2, $^) $< $@


# Cutflow re-stripped ntuples for D*.
gen/tes/Dst--20_06_05--cutflow_mc--cocktail--2011--md--bare-step2.root: \
	Dst--20_06_05--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	run1-Dst-stripping
	$(word 2, $^) $< $@

gen/run2-Dst-step2/Dst--20_06_05--cutflow_mc--cocktail--2016--md--bare-step2.root: \
	Dst--20_06_05--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	run2-Dst-stripping
	$(word 2, $^) $< $@


# Cutflow re-triggered and re-stripped ntuples for D*.
gen/test/Dst--20_06_05--cutflow_mc--cocktail--2011--md--bare-step2-triggered.root: \
	Dst--20_06_05--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	run1-Dst-triggering-stripping
	$(word 2, $^) $< $@

gen/test/Dst--20_06_05--cutflow_mc--cocktail--2016--md--bare-step2-triggered.root: \
	Dst--20_06_05--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	run2-Dst-triggering-stripping
	$(word 2, $^) $< $@


# Verify step-2 cuts with Phoebe's 2011 step-1 and step-2 ntuples
gen/rdst-2011-mix.cpp: \
	ref-rdx-run1/rdst-2011-mix.yml \
	Dst--20_07_02--mix--all--2011-2012--md-mu--phoebe.root \
	include/functor/*.h \
	include/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)

gen/test/Dst--20_07_02--mix--data--2011--md--step2--phoebe-step2.root: \
	Dst--20_07_02--mix--all--2011-2012--md-mu--phoebe.root \
	rdst-2011-mix
	$(word 2, $^) $< $@


# Re-stripping for bare ntuples.
gen/run1-Dst-stripping.cpp: \
	run1-b2D0MuXB2DMuNuForTauMuLine/postprocess/Dst-stripping.yml \
	Dst--20_06_04--cutflow_mc--cocktail--2011--md--dv45-subset-dv_strip.root \
	include/functor/*.h \
	include/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)

gen/run2-Dst-stripping.cpp: \
	run2-b2D0MuXB2DMuForTauMuLine/postprocess/Dst-stripping.yml \
	Dst--20_06_04--cutflow_mc--cocktail--2016--md--dv45-subset-dv_strip.root \
	include/functor/*.h \
	include/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)


# Re-stripping and trigger-filtering for bare ntuples.
gen/run1-Dst-triggering-stripping.cpp: \
	run1-b2D0MuXB2DMuNuForTauMuLine/postprocess/Dst-triggering-stripping.yml \
	Dst--20_06_04--cutflow_mc--cocktail--2011--md--dv45-subset-dv_strip.root \
	include/functor/*.h \
	include/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)

gen/run2-Dst-triggering-stripping.cpp: \
	run2-b2D0MuXB2DMuForTauMuLine/postprocess/Dst-triggering-stripping.yml \
	Dst--20_06_04--cutflow_mc--cocktail--2016--md--dv45-subset-dv_strip.root \
	include/functor/*.h \
	include/*.h
	babymaker -i $< -o $@ -d $(word 2, $^)


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

$(BINPATH)/%: gen/%.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDFLAGS) -o $@ $< $(LINKFLAGS)

%: gen/%.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDFLAGS) -o $(BINPATH)/$@ $< $(LINKFLAGS)

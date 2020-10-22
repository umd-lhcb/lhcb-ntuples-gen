# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Oct 22, 2020 at 01:14 PM +0200
# Description: Targets for R(D(*))

VPATH := run1-rdx/samples:run2-rdx/samples:$(VPATH)
VPATH := run1-rdx/cutflow:run2-rdx/cutflow:$(VPATH)
VPATH := ntuples/pre-0.9.0/Dst-std:$(VPATH)
VPATH := ntuples/pre-0.9.0/Dst-cutflow_mc:ntuples/pre-0.9.0/Dst-cutflow_data:$(VPATH)
VPATH := ntuples/0.9.0-cutflow/Dst-cutflow_mc:$(VPATH)
VPATH := ntuples/0.9.1-partial_refit/Dst_D0-cutflow_mc:$(VPATH)
VPATH := ntuples/0.9.2-2011_production/Dst_D0-std:$(VPATH)
VPATH := ntuples/ref-rdx-run1/Dst-std:$(VPATH)
VPATH := ntuples/ref-rdx-run1/Dst-mix:$(VPATH)
VPATH := gen/run1-Dst-step2:gen/run2-Dst-step2:$(VPATH)


#########
# Run 1 #
#########

# Dst_D0, std, 2011
gen/run1-Dst_D0-step2/Dst_D0--20_10_12--std--data--2011--md--step2.root: \
	Dst_D0--20_10_12--std--LHCb_Collision11_Beam3500GeV-VeloClosed-MagDown_Real_Data_Reco14_Stripping21r1_90000000_SEMILEPTONIC.DST.root \
	rdx-run1-data.pp
	$(word 2, $^) $< $@

# Sample, Dst_D0, MC, 2012
gen/run1-Dst_D0-step2/Dst_D0--20_10_14--mc--Bd2DstTauNu--2012--md--py6-sim08a-dv45-subset-step1.1.root: \
	Dst_D0--20_10_14--mc--Bd2DstTauNu--2012--md--py6-sim08a-dv45-subset.root \
	rdx-run1-mc-Bd2DstTauNu.pp
	$(word 2, $^) $< $@


#########
# Run 2 #
#########

# Dst, std, 2016
gen/run2-Dst-step2/Dst--19_09_09--std--data--2016--md--step2.root: \
	Dst--19_09_09--std--data--2016--md.root \
	rdx-run2-data.pp
	$(word 2, $^) $< $@

# Dst_D0, cutflow MC, cocktail, 2016
gen/run2-Dst_D0-step2/Dst_D0--20_08_18--cutflow_mc--cocktail--2016--md--step2.root: \
	Dst_D0--20_08_18--cutflow_mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	rdx-run2-mc.pp
	$(word 2, $^) $< $@


#######################
# Babymaker C++ files #
#######################

# Special postprocessing for comparing 2011 data
gen/rdst-2011-mix.cpp: \
	ref-rdx-run1/rdst-2011-mix.yml \
	Dst--20_07_02--mix--all--2011-2012--md-mu--phoebe.root \
	cpp_templates/rdx.cpp
	babymaker -i $< -o $@ -d $(word 2, $^) -t $(word 3, $^)

gen/rdst-2011-data.cpp: \
	ref-rdx-run1/rdst-2011-data.yml \
	Dst--20_09_16--std--data--2011--md--phoebe.root \
	cpp_templates/rdx.cpp
	babymaker -i $< -o $@ -d $(word 2, $^) -t $(word 3, $^)


# Dst, data, run 2
gen/rdx-run2-data.cpp: \
	rdx-run2/rdx-run2-data.yml \
	Dst--19_09_09--std--data--2016--md.root \
	cpp_templates/rdx.cpp
	babymaker -i $< -o $@ -d $(word 2, $^) -t $(word 3, $^)


# Dst_D0, data, run 1
gen/rdx-run1-data.cpp: \
	rdx-run1/rdx-run1.yml \
	Dst_D0--20_10_12--std--LHCb_Collision11_Beam3500GeV-VeloClosed-MagDown_Real_Data_Reco14_Stripping21r1_90000000_SEMILEPTONIC.DST.root \
	cpp_templates/rdx.cpp
	babymaker -i $< -o $@ -d $(word 2, $^) -t $(word 3, $^)


# Dst_D0, MC, run 1, Bd2DstTauNu
gen/rdx-run1-mc-Bd2DstTauNu.cpp: \
	rdx-run1/rdx-run1.yml \
	Dst_D0--20_10_14--mc--Bd2DstTauNu--2012--md--py6-sim08a-dv45-subset.root \
	cpp_templates/rdx.cpp
	babymaker -i $< -o $@ -d $(word 2, $^) -t $(word 3, $^)

# Dst_D0, MC, run 2
gen/rdx-run2-mc.cpp: \
	rdx-run2/rdx-run2-mc.yml \
	Dst_D0--20_08_18--cutflow_mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	cpp_templates/rdx.cpp
	babymaker -i $< -o $@ -d $(word 2, $^) -t $(word 3, $^)


# Re-stripping for bare ntuples
gen/rdst-run1-strip.cpp: \
	rdx-run1/rdst-run1-strip.yml \
	Dst--20_06_04--cutflow_mc--cocktail--2011--md--dv45-subset-dv_strip.root
	babymaker -i $< -o $@ -d $(word 2, $^)

gen/rdst-run2-strip.cpp: \
	rdx-run2/rdst-run2-strip.yml \
	Dst--20_06_04--cutflow_mc--cocktail--2016--md--dv45-subset-dv_strip.root
	babymaker -i $< -o $@ -d $(word 2, $^)


# Re-stripping and trigger-filtering for bare ntuples.
gen/rdst-run1-trig_strip.cpp: \
	rdx-run1/rdst-run1-trig_strip.yml \
	Dst--20_06_04--cutflow_mc--cocktail--2011--md--dv45-subset-dv_strip.root
	babymaker -i $< -o $@ -d $(word 2, $^)

gen/rdst-run2-trig_strip.cpp: \
	rdx-run2/rdst-run2-trig_strip.yml \
	Dst--20_06_04--cutflow_mc--cocktail--2016--md--dv45-subset-dv_strip.root
	babymaker -i $< -o $@ -d $(word 2, $^)


###########################
# Cutflow: required files #
###########################

# Cutflow output YAML for D*, MC, bare.
gen/cutflow/output-rdst-run1-bare.yml: \
	Dst--20_06_05--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	input-run1-bare.yml \
	cutflow_output_yml_gen.py
	@$(word 3, $^) $< $(word 2, $^) $@ run1-bare -t 'TupleB0/DecayTree'

gen/cutflow/output-rdst-run2-bare.yml: \
	Dst--20_06_05--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	input-run2-bare.yml \
	cutflow_output_yml_gen.py
	@$(word 3, $^) $< $(word 2, $^) $@ run2-bare -t 'TupleB0/DecayTree'


# Cutflow output YAML for D*, MC.
gen/cutflow/output-rdst-run1.yml: \
	Dst--20_03_18--cutflow_mc--cocktail--2011--md.root \
	input-run1.yml \
	cutflow_output_yml_gen_pre_0.9.0.py
	@$(word 3, $^) $< $(word 2, $^) $@ run1 -t 'TupleB0/DecayTree'

gen/cutflow/output-rdst-run2.yml: \
	Dst--20_03_18--cutflow_mc--cocktail--2016--md.root \
	input-run2.yml \
	cutflow_output_yml_gen_pre_0.9.0.py
	@$(word 3, $^) $< $(word 2, $^) $@ run2 -t 'TupleB0/DecayTree'


# Cutflow output YAML for D*, data.
gen/cutflow/output-rdst-run1-data.yml: \
	Dst--20_04_03--cutflow_data--data--2012--md.root \
	input-run1-data.yml \
	cutflow_output_yml_gen_pre_0.9.0.py
	@$(word 3, $^) $< $(word 2, $^) $@ run1 -t 'TupleB0/DecayTree'

gen/cutflow/output-rdst-run2-data.yml: \
	Dst--20_04_03--cutflow_data--data--2016--md.root \
	input-run2-data.yml \
	cutflow_output_yml_gen_pre_0.9.0.py
	@$(word 3, $^) $< $(word 2, $^) $@ run2-data -t 'TupleB0/DecayTree'


# Cutflow output YAML for signal, normalization, and D** yield, run 1
gen/cutflow/output-rdst-run1-%.yml: \
	Dst--20_06_05--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	cutflow_components.py
	@$(word 2, $^) $< $@ run1-$* -t 'TupleB0/DecayTree'


# Cutflow output YAML for signal, normalization, and D** yield, run 2
gen/cutflow/output-rdst-run2-%.yml: \
	Dst--20_06_05--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	cutflow_components.py
	@$(word 2, $^) $< $@ run2-$* -t 'TupleB0/DecayTree'


# UNUSED: Cutflow for D*, detail: individual
gen/cutflow/output-rdst-run1-individual.yml: \
	Dst--20_03_18--cutflow_mc--cocktail--2011--md.root \
	cutflow_detail.py
	@$(word 2, $^) $< $@ run1

gen/cutflow/output-rdst-run2-individual.yml: \
	Dst--20_03_18--cutflow_mc--cocktail--2016--md.root \
	cutflow_detail.py
	@$(word 2, $^) $< $@ run2


# Study the effect of refit D* only
gen/cutflow/output-rdst-run2-cocktail-refit_dst_only-%.yml: \
	Dst_D0--20_08_18--cutflow_mc--refit_dst_only--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	cutflow_components.py
	@$(word 2, $^) $< $@ run2-$* -t 'TupleB0/DecayTree'

gen/cutflow/output-rdst-run2-cocktail-full_refit-%.yml: \
	Dst_D0--20_08_18--cutflow_mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root \
	cutflow_components.py
	@$(word 2, $^) $< $@ run2-$* -t 'TupleB0/DecayTree'


###########
# Cutflow #
###########

# All cutflow studies:
.PHONY: cutflow-rdst-all
cutflow-rdst-all: \
	cutflow-rdst cutflow-rdst-bare cutflow-rdst-data \
	cutflow-rdst-run1-sig-nor-dss cutflow-rdst-run2-sig-nor-dss


# Cutflow for D*, MC, bare.
.PHONY: cutflow-rdst-bare cutflow-rdst-bare-web
cutflow-rdst-bare: \
	gen/cutflow/output-rdst-run1-bare.yml \
	gen/cutflow/output-rdst-run2-bare.yml \
	cutflow_gen.py
	@$(word 3, $^) -o $< -t $(word 2, $^) -n | tabgen.py -f latex_booktabs_raw

cutflow-rdst-bare-web: \
	gen/cutflow/output-rdst-run1-bare.yml \
	gen/cutflow/output-rdst-run2-bare.yml \
	cutflow_gen.py
	@$(word 3, $^) -o $< -t $(word 2, $^) -n | tabgen.py -f github


# Cutflow for D*, MC.
.PHONY: cutflow-rdst cutflow-rdst-web
cutflow-rdst: \
	gen/cutflow/output-rdst-run1.yml \
	gen/cutflow/output-rdst-run2.yml \
	cutflow_gen.py
	@$(word 3, $^) -o $< -t $(word 2, $^) -n | tabgen.py -f latex_booktabs_raw

cutflow-rdst-web: \
	gen/cutflow/output-rdst-run1.yml \
	gen/cutflow/output-rdst-run2.yml \
	cutflow_gen.py
	@$(word 3, $^) -o $< -t $(word 2, $^) -n | tabgen.py -f github


# Cutflow for D*, data.
.PHONY: cutflow-rdst-data cutflow-rdst-data-web
cutflow-rdst-data: \
	gen/cutflow/output-rdst-run1-data.yml \
	gen/cutflow/output-rdst-run2-data.yml \
	cutflow_gen.py
	@$(word 3, $^) -o $< -t $(word 2, $^) -n | tabgen.py -f latex_booktabs_raw

cutflow-rdst-data-web: \
	gen/cutflow/output-rdst-run1-data.yml \
	gen/cutflow/output-rdst-run2-data.yml \
	cutflow_gen.py
	@$(word 3, $^) -o $< -t $(word 2, $^) -n | tabgen.py -f github


# Cutflow for signal, normalization, and D** yield, run 1
.PHONY: cutflow-rdst-run1-sig-nor-dss
cutflow-rdst-run1-sig-nor-dss: \
	gen/cutflow/output-rdst-run1-sig.yml \
	gen/cutflow/output-rdst-run1-nor.yml \
	gen/cutflow/output-rdst-run1-dss.yml \
	table_cutflow_components.py
	@$(word 4, $^) -s $(word 1, $^) -n $(word 2, $^) -d $(word 3, $^) | tabgen.py -f latex_booktabs_raw


# Cutflow for signal, normalization, and D** yield, run 2
.PHONY: cutflow-rdst-run2-sig-nor-dss
cutflow-rdst-run2-sig-nor-dss: \
	gen/cutflow/output-rdst-run2-sig.yml \
	gen/cutflow/output-rdst-run2-nor.yml \
	gen/cutflow/output-rdst-run2-dss.yml \
	table_cutflow_components.py
	@$(word 4, $^) -s $(word 1, $^) -n $(word 2, $^) -d $(word 3, $^) | tabgen.py -f latex_booktabs_raw


# UNUSED: Cutflow for D*, detail: individual
.PHONY: cutflow-rdst-detail-individual
cutflow-rdst-detail-individual: \
	gen/cutflow/output-rdst-run1-individual.yml \
	gen/cutflow/output-rdst-run2-individual.yml \
	cutflow_gen.py
	@$(word 3, $^) -o $(word 1, $^) -t $(word 2, $^) -n | tabgen.py -f latex_booktabs_raw


# Study the effect of refit D* only
.PHONY: cutflow-rdst-run2-sig-nor-dss-cocktail-refit_dst_only \
	cutflow-rdst-run2-sig-nor-dss-cocktail-full_refit
cutflow-rdst-run2-sig-nor-dss-cocktail-refit_dst_only: \
	gen/cutflow/output-rdst-run2-cocktail-refit_dst_only-sig.yml \
	gen/cutflow/output-rdst-run2-cocktail-refit_dst_only-nor.yml \
	gen/cutflow/output-rdst-run2-cocktail-refit_dst_only-dss.yml \
	table_cutflow_components.py
	@$(word 4, $^) -s $(word 1, $^) -n $(word 2, $^) -d $(word 3, $^) | tabgen.py -f github

cutflow-rdst-run2-sig-nor-dss-cocktail-full_refit: \
	gen/cutflow/output-rdst-run2-cocktail-full_refit-sig.yml \
	gen/cutflow/output-rdst-run2-cocktail-full_refit-nor.yml \
	gen/cutflow/output-rdst-run2-cocktail-full_refit-dss.yml \
	table_cutflow_components.py
	@$(word 4, $^) -s $(word 1, $^) -n $(word 2, $^) -d $(word 3, $^) | tabgen.py -f github


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

# Tests for the equivalence between local bare and dv_strip ntuples.
.PHONY: test-cutflow-rdst-run1 test-cutflow-rdst-run2
test-cutflow-rdst-run1: \
	gen/test/Dst--20_06_04--cutflow_mc--cocktail--2011--md--subset-bare-step2.root \
	gen/test/Dst--20_06_04--cutflow_mc--cocktail--2011--md--subset-dv_strip-step2.root \
	Dst--20_06_04--cutflow_mc--cocktail--2011--md--dv45-subset-dv_strip.root
	@echo "===="
	@echo "Test results:"
	@test_ntuple_identical.py -n $< -N $(word 3, $^) -t b0dst -T TupleB0/DecayTree
	@test_ntuple_identical.py -n $(word 2, $^) -N $(word 3, $^) -t b0dst -T TupleB0/DecayTree

test-cutflow-rdst-run2: \
	gen/test/Dst--20_06_04--cutflow_mc--cocktail--2016--md--subset-dv_strip-step2.root \
	gen/test/Dst--20_06_04--cutflow_mc--cocktail--2016--md--subset-bare-step2.root \
	Dst--20_06_04--cutflow_mc--cocktail--2016--md--dv45-subset-dv_strip.root
	@echo "===="
	@echo "Test results:"
	@test_ntuple_identical.py -n $< -N $(word 3, $^) -t b0dst -T TupleB0/DecayTree
	@test_ntuple_identical.py -n $(word 2, $^) -N $(word 3, $^) -t b0dst -T TupleB0/DecayTree


# Test if the number of events used in the cutflow generation is consistent.
.PHONY: test-cutflow-consistency-rdst
test-cutflow-consistency-rdst: \
	gen/test/Dst--20_06_05--cutflow_mc--cocktail--2011--md--bare-step2-triggered.root \
	gen/test/Dst--20_06_05--cutflow_mc--cocktail--2016--md--bare-step2-triggered.root

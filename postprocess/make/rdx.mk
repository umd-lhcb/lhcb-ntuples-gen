# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Oct 12, 2020 at 03:19 PM +0800
# Description: Targets for R(D(*))

VPATH := run1-rdx/samples:run2-rdx/samples:$(VPATH)
VPATH := run1-rdx/cutflow:run2-rdx/cutflow:$(VPATH)
VPATH := ntuples/pre-0.9.0/Dst-std:$(VPATH)
VPATH := ntuples/pre-0.9.0/Dst-cutflow_mc:ntuples/pre-0.9.0/Dst-cutflow_data:$(VPATH)
VPATH := ntuples/0.9.0-cutflow/Dst-cutflow_mc:$(VPATH)
VPATH := ntuples/0.9.1-dst_partial_refit/Dst_D0-cutflow_mc:$(VPATH)
VPATH := ntuples/ref-rdx-run1/Dst-std:$(VPATH)
VPATH := ntuples/ref-rdx-run1/Dst-mix:$(VPATH)
VPATH := gen/run1-Dst-step2:gen/run2-Dst-step2:$(VPATH)


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
	rdx-run1-data.pp
	$(word 2, $^) $< $@

# Sample, Dst_D0, MC, 2012
gen/run1-Dst_D0-step2/Dst_D0--20_10_01--mc--Bd2DstTauNu--2012--md--py6-sim08a-dv45-subset-step1.1.root: \
	Dst_D0--20_10_01--mc--Bd2DstTauNu--2012--md--py6-sim08a-dv45-subset.root \
	rdx-run1.pp
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


# Dst, data, run 1
gen/rdx-run1-data.cpp: \
	rdx-run1/rdx-run1-data.yml \
	Dst--19_09_05--std--data--2012--md.root \
	cpp_templates/rdx.cpp
	babymaker -i $< -o $@ -d $(word 2, $^) -t $(word 3, $^)

# Dst, data, run 2
gen/rdx-run2-data.cpp: \
	rdx-run2/rdx-run2-data.yml \
	Dst--19_09_09--std--data--2016--md.root \
	cpp_templates/rdx.cpp
	babymaker -i $< -o $@ -d $(word 2, $^) -t $(word 3, $^)


# Dst_D0, all, run 1
gen/rdx-run1.cpp: \
	rdx-run1/rdx-run1.yml \
	Dst_D0--20_10_01--mc--Bd2DstTauNu--2012--md--py6-sim08a-dv45-subset.root \
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

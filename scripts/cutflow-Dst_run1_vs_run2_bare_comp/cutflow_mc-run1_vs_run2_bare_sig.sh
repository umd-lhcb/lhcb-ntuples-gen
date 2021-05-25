#!/usr/bin/env bash
# NOTE: This is just an example! To generate all bare component cutflows, go to
#       project root, then 'make rdx-cutflow'

RUN1_NTP_MU=../../ntuples/0.9.4-trigger_emulation/Dst_D0-cutflow_mc/Dst_D0--21_05_14--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagUp-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root
RUN1_NTP_MD=../../ntuples/0.9.4-trigger_emulation/Dst_D0-cutflow_mc/Dst_D0--21_05_14--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root
RUN1_INPUT_YML=../../run1-rdx/cutflow/21_05_23-run1_bare.yml

RUN2_NTP_MU=../../ntuples/0.9.4-trigger_emulation/Dst_D0-cutflow_mc/Dst_D0--21_05_14--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagUp-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root
RUN2_NTP_MD=../../ntuples/0.9.4-trigger_emulation/Dst_D0-cutflow_mc/Dst_D0--21_05_14--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root
RUN2_INPUT_YML=../../run2-rdx/cutflow/21_05_23-run2_bare.yml

# Run 1
../cutflow_output_yml_gen.py ${RUN1_NTP_MU} ${RUN1_NTP_MD} \
    -i ${RUN1_INPUT_YML} -o ./cutflow_run1.yml \
    -m run1-Dst-bare-sig

# Run 2
../cutflow_output_yml_gen.py ${RUN2_NTP_MU} ${RUN2_NTP_MD} \
    -i ${RUN2_INPUT_YML} -o ./cutflow_run2.yml \
    -m run2-Dst-bare-sig

# Actual cutflow table
../cutflow_gen.py -o ./cutflow_run1.yml -t ./cutflow_run2.yml -n > ./cutflow.csv
cat ./cutflow.csv | tabgen.py -f latex_booktabs_raw > ./cutflow.tex
cat ./cutflow.csv | tabgen.py -f github > ./cutflow.md

#!/usr/bin/env bash

# 2012 MC
./selection_efficiency.py \
    ../../ntuples/0.9.3-production_for_validation/Dst_D0-mc/Dst_D0--21_01_30--mc--MC_2012_Beam4000GeV-2012-MagDown-Nu2.5-Pythia8_Sim08e_Digi13_Trig0x409f0045_Reco14a_Stripping20Filtered_11574020_DSTTAUNU.SAFESTRIPTRIG.DST.root \
    -H 2012-md-mc \
    -c sel_eff_run1_mc.csv \
    -b nothing \
    -t run1

# 2016 MC
./selection_efficiency.py \
    ../../ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root \
    -H 2016-md-mc \
    -c sel_eff_run2_mc.csv \
    -t run2

# 2011 data
./selection_efficiency.py \
    ../../ntuples/0.9.2-2011_production/Dst_D0-std/Dst_D0--20_10_12--std--LHCb_Collision11_Beam3500GeV-VeloClosed-MagDown_Real_Data_Reco14_Stripping21r1_90000000_SEMILEPTONIC.DST.root \
    -H 2011-md-data \
    -c sel_eff_run1_data.csv \
    -t run1

# 2016 data
./selection_efficiency.py \
    ../../ntuples/0.9.4-trigger_emulation/Dst_D0-std/Dst_D0--21_04_27--std--LHCb_Collision16_Beam6500GeV-VeloClosed-MagDown_Real_Data_Reco16_Stripping28r1_90000000_SEMILEPTONIC.DST.root \
    -H 2016-md-data \
    -c sel_eff_run2_data.csv \
    -t run2

# Merge the files
cat ./sel_eff_run1_data.csv > ./sel_eff_iso_tight.csv
tail -n +2 ./sel_eff_run2_data.csv  >> ./sel_eff_iso_tight.csv
tail -n +2 ./sel_eff_run1_mc.csv  >> ./sel_eff_iso_tight.csv
tail -n +2 ./sel_eff_run2_mc.csv  >> ./sel_eff_iso_tight.csv

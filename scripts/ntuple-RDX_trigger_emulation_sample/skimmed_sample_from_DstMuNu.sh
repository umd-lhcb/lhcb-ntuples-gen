#!/bin/sh

# Generate the base ntuple
../../tools/haddcut.py \
    rdx-tracker_only.root \
    ../../ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root \
    -c ./trigger_emulation_sample.yml

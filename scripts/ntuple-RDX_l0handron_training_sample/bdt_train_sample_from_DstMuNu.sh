#!/bin/sh

# Generate the base ntuple
../../tools/haddcut.py \
    bdt_sample_raw.root \
    ../../ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root \
    -c ./l0hadron_bdt_train_sample.yml

# Generate the emulated HCAL ET
../../lib/python/TrackerOnlyEmu/scripts/run2-rdx-l0_hadron.py \
    ../../ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root \
    emu_l0_hadron.root \
    -t TupleB0/DecayTree

# Merge the two
rm -rf ./bdt_sample_tmp.root
../../tools/haddcut.py \
    bdt_sample_tmp.root \
    ./emu_l0_hadron.root ./bdt_sample_raw.root \
    -c ./l0hadron_bdt_train_sample.yml \
    -m friend

# Skim final output file
../../tools/haddcut.py \
    rdx-bdt_train_sample.root ./bdt_sample_tmp.root \
    -c ./l0hadron_bdt_train_sample.yml

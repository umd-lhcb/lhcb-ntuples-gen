#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
L0EMU=$DIR/../../lib/python/TrackerOnlyEmu/scripts/run2-rdx-l0_hadron.py
INPUT_NTP=$DIR/../../ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root

# Generate the base ntuple
../../scripts/haddcut.py \
    $DIR/bdt_sample_raw.root \
    ${INPUT_NTP} \
    -c $DIR/l0hadron_bdt_train_sample.yml

# Generate the emulated HCAL ET
$L0EMU ${INPUT_NTP} $DIR/emu_l0_hadron.root -t TupleB0/DecayTree

# Merge the two
rm -rf ./bdt_sample_tmp.root
../../scripts/haddcut.py \
    $DIR/bdt_sample_tmp.root \
    $DIR/bdt_sample_raw.root $DIR/emu_l0_hadron.root \
    -c $DIR/l0hadron_bdt_train_sample.yml \
    -m friend

# Skim final output file
../../scripts/haddcut.py \
    $DIR/rdx-bdt_train_sample.root $DIR/bdt_sample_tmp.root \
    -c $DIR/l0hadron_bdt_train_sample.yml

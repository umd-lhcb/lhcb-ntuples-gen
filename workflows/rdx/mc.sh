#!/usr/bin/env bash
#Author: Yipeng Sun
#License: GPLv2
#Last Change: Thu Apr 15, 2021 at 06:30 PM +0200

INPUT_NTP=$1

plot_hlt_eff() {
    NTP=$1
    TREE=$2
    OUTPUT_PREFIX=$3
    TRIGGER=$4
    TITLE=$5
    EXT=$6

    plot_trigger_efficiency_comp.py \
        -n "${NTP}" -o "${OUTPUT_PREFIX}" -T ${TRIGGER} \
        -t "${TREE}" --title "${TITLE}" --ext "${EXT}"
}


# Hlt1 emulation
run2-rdx-hlt1.py ${INPUT_NTP} emu_hlt1_b0.root -t TupleB0/DecayTree -B b0
run2-rdx-hlt1.py ${INPUT_NTP} emu_hlt1_b.root -t TupleBminus/DecayTree -B b

# Plot efficiencies
plot_hlt_eff emu_hlt1_b0.root "TupleB0/DecayTree" b0 \
    "d0_hlt1_twotrackmva_tos d0_hlt1_twotrackmva_tos_emu" \
    "Hlt1TwoTrackMVA TOS" png

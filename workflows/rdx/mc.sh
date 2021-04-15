#!/usr/bin/env bash
# Author: Yipeng Sun
# Last Change: Thu Apr 15, 2021 at 06:44 PM +0200

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


# Hlt1 emulation: Hlt1TwoTrackMVA & Hlt1TrackMVA
run2-rdx-hlt1.py ${INPUT_NTP} emu_hlt1_b0.root -t TupleB0/DecayTree -B b0
run2-rdx-hlt1.py ${INPUT_NTP} emu_hlt1_b.root -t TupleBminus/DecayTree -B b


# Plot efficiencies: Hlt1TwoTrackMVA
#   D*
plot_hlt_eff emu_hlt1_b0.root "TupleB0/DecayTree" b0 \
    "d0_hlt1_twotrackmva_tos d0_hlt1_twotrackmva_tos_emu" \
    "Hlt1TwoTrackMVA TOS" png
plot_hlt_eff emu_hlt1_b0.root "TupleB0/DecayTree" b0 \
    "d0_hlt1_twotrackmva_tos d0_hlt1_twotrackmva_tos_emu" \
    "Hlt1TwoTrackMVA TOS" pdf
#   D0
plot_hlt_eff emu_hlt1_b.root "TupleBminus/DecayTree" b \
    "d0_hlt1_twotrackmva_tos d0_hlt1_twotrackmva_tos_emu" \
    "Hlt1TwoTrackMVA TOS" png
plot_hlt_eff emu_hlt1_b.root "TupleBminus/DecayTree" b \
    "d0_hlt1_twotrackmva_tos d0_hlt1_twotrackmva_tos_emu" \
    "Hlt1TwoTrackMVA TOS" pdf


# Plot efficiencies: Hlt1TrackMVA
#   D*
plot_hlt_eff emu_hlt1_b0.root "TupleB0/DecayTree" b0 \
    "d0_hlt1_trackmva_tos d0_hlt1_trackmva_tos_emu" \
    "Hlt1TrackMVA TOS" png
plot_hlt_eff emu_hlt1_b0.root "TupleB0/DecayTree" b0 \
    "d0_hlt1_trackmva_tos d0_hlt1_trackmva_tos_emu" \
    "Hlt1TrackMVA TOS" pdf
#   D0
plot_hlt_eff emu_hlt1_b.root "TupleBminus/DecayTree" b \
    "d0_hlt1_trackmva_tos d0_hlt1_trackmva_tos_emu" \
    "Hlt1TrackMVA TOS" png
plot_hlt_eff emu_hlt1_b.root "TupleBminus/DecayTree" b \
    "d0_hlt1_trackmva_tos d0_hlt1_trackmva_tos_emu" \
    "Hlt1TrackMVA TOS" pdf

#!/usr/bin/env bash
# Author: Yipeng Sun
# Last Change: Mon Apr 19, 2021 at 08:53 PM +0200

INPUT_NTP=$1

plot_hlt_eff() {
    NTP=$1
    TREE=$2
    OUTPUT_PREFIX=$3
    TRIGGER=$4
    TITLE=$5

    plot_trigger_efficiency_comp.py \
        -n "${NTP}" -o "${OUTPUT_PREFIX}" -T ${TRIGGER} \
        -t "${TREE}" --title "${TITLE}"
}

plot_l0_eff() {
    NTP=$1
    TREE=$2
    OUTPUT_PREFIX=$3
    TRIGGER=$4
    TITLE=$5

    plot_trigger_efficiency_comp.py \
        -n "${NTP}" -o "${OUTPUT_PREFIX}" -T ${TRIGGER} \
        -t "${TREE}" --title "${TITLE}" \
        -c \
        -k "q2" "mmiss2" "el" \
        -D -10 10 -10 8 0 3
}


# Hlt1 emulation: Hlt1TwoTrackMVA & Hlt1TrackMVA
run2-rdx-hlt1.py ${INPUT_NTP} emu_hlt1_b0.root \
    -t TupleB0/DecayTree -B b0 --debug
run2-rdx-hlt1.py ${INPUT_NTP} emu_hlt1_b.root \
    -t TupleBminus/DecayTree -B b --debug

# L0 emulation: L0Hadron
run2-rdx-l0_hadron.py ${INPUT_NTP} emu_l0_b0.root \
    -t TupleB0/DecayTree --debug
run2-rdx-l0_hadron.py ${INPUT_NTP} emu_l0_b.root \
    -t TupleBminus/DecayTree --debug


# Plot efficiencies: Hlt1TwoTrackMVA
#   D*
plot_hlt_eff emu_hlt1_b0.root "TupleB0/DecayTree" b0 \
    "d0_hlt1_twotrackmva_tos d0_hlt1_twotrackmva_tos_emu" \
    "Hlt1TwoTrackMVA TOS"
#   D0
plot_hlt_eff emu_hlt1_b.root "TupleBminus/DecayTree" b \
    "d0_hlt1_twotrackmva_tos d0_hlt1_twotrackmva_tos_emu" \
    "Hlt1TwoTrackMVA TOS"


# Plot efficiencies: Hlt1TrackMVA
#   D*
plot_hlt_eff emu_hlt1_b0.root "TupleB0/DecayTree" b0 \
    "d0_hlt1_trackmva_tos d0_hlt1_trackmva_tos_emu" \
    "Hlt1TrackMVA TOS"
#   D0
plot_hlt_eff emu_hlt1_b.root "TupleBminus/DecayTree" b \
    "d0_hlt1_trackmva_tos d0_hlt1_trackmva_tos_emu" \
    "Hlt1TrackMVA TOS"


# Plot efficiencies: L0Hadron
#   D*
plot_l0_eff emu_l0_b0.root "TupleB0/DecayTree" b0 \
    "d0_l0_hadron_tos d0_l0_hadron_tos_emu" \
    "L0Hadron TOS"
#   D0
plot_l0_eff emu_l0_b.root "TupleBminus/DecayTree" b \
    "d0_l0_hadron_tos d0_l0_hadron_tos_emu" \
    "L0Hadron TOS"

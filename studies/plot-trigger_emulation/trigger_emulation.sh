#!/usr/bin/env bash
# Author: Yipeng Sun
# Last Change: Tue Sep 20, 2022 at 11:55 PM -0400

INPUT_NTP=../../ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root

plot_hlt1_twotrackmva() {
    NTP=$1
    TREE=$2
    OUTPUT_PREFIX=$3
    TRIGGER=$4
    TITLE=$5

    plot_trigger_efficiencies.py \
        -n "${NTP}/${TREE}" -b ${TRIGGER} -o "${OUTPUT_PREFIX}" \
        --title "${TITLE}" --default-cut d0_l0_global_dec --ratio-plot \
        -k q2 mmiss2 el \
        -D 0 11 -6 11 0 4 \
        -Y 0.61 0.91 0.6 1 0.6 1
}

plot_hlt1_trackmva() {
    NTP=$1
    TREE=$2
    OUTPUT_PREFIX=$3
    TRIGGER=$4
    TITLE=$5

    plot_trigger_efficiencies.py \
        -n "${NTP}/${TREE}" -b ${TRIGGER} -o "${OUTPUT_PREFIX}"  \
        --title "${TITLE}" --default-cut d0_l0_global_dec --ratio-plot \
        -k q2 mmiss2 el \
        -D 0 11 -6 11 0 4 \
        -Y 0.61 0.91 0.6 1 0.6 1
}

plot_l0_hadron_eff() {
    NTP=$1
    TREE=$2
    OUTPUT_PREFIX=$3
    TRIGGER=$4
    TITLE=$5

    plot_trigger_efficiencies.py \
        -n "${NTP}/${TREE}" -b ${TRIGGER} -o "${OUTPUT_PREFIX}" \
        --title "${TITLE}" --ratio-plot \
        -k d0_pt k_pt pi_pt \
           nspdhits \
           d0_p k_p pi_p \
        -D 0 50 0 25 0 25 \
           0 500 \
           0 250 0 150 0 150 \
        --xlabel "\$D^0$ \$p_T$ [GeV]" \
                 "\$K$ \$p_T$ [GeV]" \
                 "\$\\pi$ \$p_T$ [GeV]" \
                 "Number of SPD hits" \
                 "\$D^0$ \$p$ [GeV]" \
                 "\$K$ \$p$ [GeV]" \
                 "\$\\pi$ \$p$ [GeV]"
}

plot_l0_hadron_eff_all() {
    NTP=$1
    TREE=$2
    OUTPUT_PREFIX=$3
    TRIGGER=$4
    TITLE=$5

    plot_trigger_efficiencies.py \
        -n "${NTP}/${TREE}" -b ${TRIGGER} -o "${OUTPUT_PREFIX}" \
        --title "${TITLE}" \
        -k d0_pt k_pt pi_pt \
           nspd_hits \
           d0_p k_p pi_p \
        -D 0 40 0 20 0 20 \
           0 500 \
           0 250 0 150 0 150 \
        --xlabel "\$D^0$ \$p_T$ [GeV]" \
                 "\$K$ \$p_T$ [GeV]" \
                 "\$\\pi$ \$p_T$ [GeV]" \
                 "Number of SPD hits" \
                 "\$D^0$ \$p$ [GeV]" \
                 "\$K$ \$p$ [GeV]" \
                 "\$\\pi$ \$p$ [GeV]"
}

plot_l0_global_tis_eff() {
    NTP=$1
    TREE=$2
    OUTPUT_PREFIX=$3
    TRIGGER=$4
    TITLE=$5

    plot_trigger_efficiencies.py \
        -n "${NTP}/${TREE}" -b ${TRIGGER} -o "${OUTPUT_PREFIX}" \
        --title "${TITLE}" --ratio-plot \
        -k "log_${OUTPUT_PREFIX}_pz" "log_${OUTPUT_PREFIX}_pt" \
           nspd_hits \
        -D -10 10 -10 8 0 3 9 14 6 12 0 500 \
        --bins 8 \
        --xlabel "\$\\log(p_Z)$" \
                 "\$\\log(p_T)$" \
                 "Number of SPD hits"
}

# Hlt1 emulation: Hlt1TwoTrackMVA & Hlt1TrackMVA
run2-rdx-hlt1.py ${INPUT_NTP} emu_hlt1_b0.root \
    -t TupleB0/DecayTree -B b0 --debug
run2-rdx-hlt1.py ${INPUT_NTP} emu_hlt1_b.root \
    -t TupleBminus/DecayTree -B b --debug || exit 1

# L0 emulation: L0Hadron
run2-rdx-l0_hadron_tos.py ${INPUT_NTP} emu_l0_hadron_b0.root \
    -t TupleB0/DecayTree --debug
run2-rdx-l0_hadron_tos.py ${INPUT_NTP} emu_l0_hadron_b.root \
    -t TupleBminus/DecayTree --debug || exit 1

# L0 emulation: L0Global TIS
run2-rdx-l0_global_tis.py ${INPUT_NTP} emu_l0_global_tis_b0.root \
    -t TupleB0/DecayTree -B b0 --debug
run2-rdx-l0_global_tis.py ${INPUT_NTP} emu_l0_global_tis_b.root \
    -t TupleBminus/DecayTree -B b --debug || exit 1


# Plot efficiencies: Hlt1TwoTrackMVA
#   D*
plot_hlt1_twotrackmva emu_hlt1_b0.root "TupleB0/DecayTree" b0 \
    "d0_hlt1_twotrackmva_tos d0_hlt1_twotrackmva_tos_emu" \
    "Hlt1TwoTrackMVA TOS"
#   D0
plot_hlt1_twotrackmva emu_hlt1_b.root "TupleBminus/DecayTree" b \
    "d0_hlt1_twotrackmva_tos d0_hlt1_twotrackmva_tos_emu" \
    "Hlt1TwoTrackMVA TOS"


# Plot efficiencies: Hlt1TrackMVA
#   D*
plot_hlt1_trackmva emu_hlt1_b0.root "TupleB0/DecayTree" b0 \
    "d0_hlt1_trackmva_tos d0_hlt1_trackmva_tos_emu" \
    "Hlt1TrackMVA TOS"
#   D0
plot_hlt1_trackmva emu_hlt1_b.root "TupleBminus/DecayTree" b \
    "d0_hlt1_trackmva_tos d0_hlt1_trackmva_tos_emu" \
    "Hlt1TrackMVA TOS"


# Plot efficiencies: L0Hadron
#   D*
plot_l0_hadron_eff emu_l0_hadron_b0.root "TupleB0/DecayTree" b0 \
    "d0_l0_hadron_tos d0_l0_hadron_tos_emu_xgb" \
    "L0Hadron TOS"
#   D0
plot_l0_hadron_eff emu_l0_hadron_b.root "TupleBminus/DecayTree" b \
    "d0_l0_hadron_tos d0_l0_hadron_tos_emu_xgb" \
    "L0Hadron TOS"


# Plot efficiencies: L0Global TIS
#   B0
plot_l0_global_tis_eff emu_l0_global_tis_b0.root "TupleB0/DecayTree" b0 \
    "b0_l0_global_tis b0_l0_global_tis_emu" \
    "L0Global TIS"
#   B
plot_l0_global_tis_eff emu_l0_global_tis_b.root "TupleBminus/DecayTree" b \
    "b_l0_global_tis b_l0_global_tis_emu" \
    "L0Global TIS"

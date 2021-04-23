#!/usr/bin/env bash
# Author: Yipeng Sun
# Last Change: Fri Apr 23, 2021 at 03:56 AM +0200

INPUT_NTP=$1

plot_hlt1_twotrackmva() {
    NTP=$1
    TREE=$2
    OUTPUT_PREFIX=$3
    TRIGGER=$4
    TITLE=$5

    plot_trigger_efficiency_comp.py \
        -n "${NTP}" -o "${OUTPUT_PREFIX}" -T ${TRIGGER} \
        -t "${TREE}" --title "${TITLE}"
}

plot_hlt1_trackmva() {
    NTP=$1
    TREE=$2
    OUTPUT_PREFIX=$3
    TRIGGER=$4
    TITLE=$5

    plot_trigger_efficiency_comp.py \
        -n "${NTP}" -o "${OUTPUT_PREFIX}" -T ${TRIGGER} \
        -t "${TREE}" --title "${TITLE}" \
        -k q2 mmiss2 el \
           k_p k_pt pi_p pi_pt \
           k_chi2ndof k_ipchi2 k_ghost \
           pi_chi2ndof pi_ipchi2 pi_ghost \
           mu_theta k_theta pi_theta \
           mu_phi k_phi pi_phi
}

plot_l0_hadron_eff() {
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

plot_l0_global_tis_eff() {
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
           "log_${OUTPUT_PREFIX}_true_pz" "log_${OUTPUT_PREFIX}_true_pt" \
        -D -10 10 -10 8 0 3 9 14 6 12 \
        --xlabel "\$q^2$ [GeV\$^2$]" \
                 "\$m_{miss}^2$ [GeV\$^2$]" \
                 "\$E_l$ [GeV]" \
                 "\$\\log(P_Z)$" \
                 "\$\\log(P_T)$"
}


# Hlt1 emulation: Hlt1TwoTrackMVA & Hlt1TrackMVA
run2-rdx-hlt1.py ${INPUT_NTP} emu_hlt1_b0.root \
    -t TupleB0/DecayTree -B b0 --debug
run2-rdx-hlt1.py ${INPUT_NTP} emu_hlt1_b.root \
    -t TupleBminus/DecayTree -B b --debug || exit 1

# L0 emulation: L0Hadron
run2-rdx-l0_hadron.py ${INPUT_NTP} emu_l0_hadron_b0.root \
    -t TupleB0/DecayTree --debug
run2-rdx-l0_hadron.py ${INPUT_NTP} emu_l0_hadron_b.root \
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
    "d0_l0_hadron_tos d0_l0_hadron_tos_emu" \
    "L0Hadron TOS"
#   D0
plot_l0_hadron_eff emu_l0_hadron_b.root "TupleBminus/DecayTree" b \
    "d0_l0_hadron_tos d0_l0_hadron_tos_emu" \
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

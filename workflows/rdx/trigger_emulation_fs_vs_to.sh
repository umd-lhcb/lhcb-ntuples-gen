#!/usr/bin/env bash
# Author: Yipeng Sun
# Last Change: Mon May 03, 2021 at 10:45 PM +0200

INPUT_NTP1=$1
INPUT_NTP2=$2

plot_hlt1_twotrackmva() {
    NTP1=$1
    NTP2=$2
    TREE=$3
    OUTPUT_PREFIX=$4
    TRIGGER=$5
    TITLE=$6

    plot_trigger_efficiency_comp_two_ntuples.py \
        -n "${NTP1}" -N "${NTP2}" -o "${OUTPUT_PREFIX}" \
        -t "${TREE}" -T "${TREE}" \
        --title "${TITLE}" \
        --triggers ${TRIGGER} \
        --legends FS TO
}

plot_hlt1_trackmva() {
    NTP1=$1
    NTP2=$2
    TREE=$3
    OUTPUT_PREFIX=$4
    TRIGGER=$5
    TITLE=$6

    plot_trigger_efficiency_comp_two_ntuples.py \
        -n "${NTP1}" -N "${NTP2}" -o "${OUTPUT_PREFIX}" \
        -t "${TREE}" -T "${TREE}" \
        --title "${TITLE}" \
        --triggers ${TRIGGER} \
        --legends FS TO \
        -k q2 mmiss2 el \
           k_p k_pt pi_p pi_pt mu_p mu_pt \
           k_chi2ndof k_ipchi2 k_ghost \
           pi_chi2ndof pi_ipchi2 pi_ghost \
           mu_chi2ndof mu_ipchi2 mu_ghost \
           k_theta pi_theta mu_theta \
           k_phi pi_phi mu_phi \
           nspd_hits
}

plot_l0_hadron_eff() {
    NTP1=$1
    NTP2=$2
    TREE=$3
    OUTPUT_PREFIX=$4
    TRIGGER=$5
    TITLE=$6

    plot_trigger_efficiency_comp_two_ntuples.py \
        -n "${NTP1}" -N "${NTP2}" -o "${OUTPUT_PREFIX}" \
        -t "${TREE}" -T "${TREE}" \
        --title "${TITLE}" \
        --triggers ${TRIGGER} \
        --legends FS TO \
        -c \
        -k q2 mmiss2 el \
           d0_pt k_pt pi_pt \
        -D -10 10 -10 8 0 3 \
           0 100 0 50 0 50 \
        --xlabel "\$q^2$ [GeV\$^2$]" \
                 "\$m_{miss}^2$ [GeV\$^2$]" \
                 "\$E_l$ [GeV]" \
                 "\$D^0$ \$p_T$ [GeV]" \
                 "\$K$ \$p_T$ [GeV]" \
                 "\$\\pi$ \$p_T$ [GeV]"
}

plot_l0_global_tis_eff() {
    NTP1=$1
    NTP2=$2
    TREE=$3
    OUTPUT_PREFIX=$4
    TRIGGER=$5
    TITLE=$6

    plot_trigger_efficiency_comp_two_ntuples.py \
        -n "${NTP1}" -N "${NTP2}" -o "${OUTPUT_PREFIX}" \
        -t "${TREE}" -T "${TREE}" \
        --title "${TITLE}" \
        --triggers ${TRIGGER} \
        --legends FS TO \
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
run2-rdx-hlt1.py ${INPUT_NTP1} emu_hlt1_fs_b0.root \
    -t TupleB0/DecayTree -B b0 --debug
run2-rdx-hlt1.py ${INPUT_NTP2} emu_hlt1_to_b0.root \
    -t TupleB0/DecayTree -B b0 --debug || exit 1

run2-rdx-hlt1.py ${INPUT_NTP1} emu_hlt1_fs_b.root \
    -t TupleBminus/DecayTree -B b --debug
run2-rdx-hlt1.py ${INPUT_NTP2} emu_hlt1_to_b.root \
    -t TupleBminus/DecayTree -B b --debug || exit 1

# L0 emulation: L0Hadron
run2-rdx-l0_hadron.py ${INPUT_NTP1} emu_l0_hadron_fs_b0.root \
    -t TupleB0/DecayTree --debug
run2-rdx-l0_hadron.py ${INPUT_NTP2} emu_l0_hadron_to_b0.root \
    -t TupleB0/DecayTree --debug || exit 1

run2-rdx-l0_hadron.py ${INPUT_NTP1} emu_l0_hadron_fs_b.root \
    -t TupleBminus/DecayTree --debug
run2-rdx-l0_hadron.py ${INPUT_NTP2} emu_l0_hadron_to_b.root \
    -t TupleBminus/DecayTree --debug || exit 1

# L0 emulation: L0Global TIS
run2-rdx-l0_global_tis.py ${INPUT_NTP1} emu_l0_global_tis_fs_b0.root \
    -t TupleB0/DecayTree -B b0 --debug
run2-rdx-l0_global_tis.py ${INPUT_NTP2} emu_l0_global_tis_to_b0.root \
    -t TupleB0/DecayTree -B b0 --debug || exit 1

run2-rdx-l0_global_tis.py ${INPUT_NTP1} emu_l0_global_tis_fs_b.root \
    -t TupleBminus/DecayTree -B b --debug
run2-rdx-l0_global_tis.py ${INPUT_NTP2} emu_l0_global_tis_to_b.root \
    -t TupleBminus/DecayTree -B b --debug || exit 1


# Plot efficiencies: Hlt1TwoTrackMVA
#   D*
plot_hlt1_twotrackmva emu_hlt1_fs_b0.root emu_hlt1_to_b0.root \
    "TupleB0/DecayTree" b0 \
    "d0_hlt1_twotrackmva_tos_emu" \
    "Hlt1TwoTrackMVA TOS"
#   D0
plot_hlt1_twotrackmva emu_hlt1_fs_b.root emu_hlt1_to_b.root \
    "TupleBminus/DecayTree" b \
    "d0_hlt1_twotrackmva_tos_emu" \
    "Hlt1TwoTrackMVA TOS"


# Plot efficiencies: Hlt1TrackMVA
#   D*
plot_hlt1_trackmva emu_hlt1_fs_b0.root emu_hlt1_to_b0.root \
    "TupleB0/DecayTree" b0 \
    "d0_hlt1_trackmva_tos_emu" \
    "Hlt1TrackMVA TOS"
#   D0
plot_hlt1_trackmva emu_hlt1_fs_b.root emu_hlt1_to_b.root \
    "TupleBminus/DecayTree" b \
    "d0_hlt1_trackmva_tos_emu" \
    "Hlt1TrackMVA TOS"


# Plot efficiencies: L0Hadron
#   D*
plot_l0_hadron_eff emu_l0_hadron_fs_b0.root emu_l0_hadron_to_b0.root \
    "TupleB0/DecayTree" b0 \
    "d0_l0_hadron_tos_emu" \
    "L0Hadron TOS"
#   D0
plot_l0_hadron_eff emu_l0_hadron_fs_b.root emu_l0_hadron_to_b.root \
    "TupleBminus/DecayTree" b \
    "d0_l0_hadron_tos_emu" \
    "L0Hadron TOS"


# Plot efficiencies: L0Global TIS
#   B0
plot_l0_global_tis_eff \
    emu_l0_global_tis_fs_b0.root emu_l0_global_tis_to_b0.root \
    "TupleB0/DecayTree" b0 \
    "b0_l0_global_tis_emu" \
    "L0Global TIS"
#   B-
plot_l0_global_tis_eff \
    emu_l0_global_tis_fs_b.root emu_l0_global_tis_to_b.root \
    "TupleBminus/DecayTree" b \
    "b_l0_global_tis_emu" \
    "L0Global TIS"

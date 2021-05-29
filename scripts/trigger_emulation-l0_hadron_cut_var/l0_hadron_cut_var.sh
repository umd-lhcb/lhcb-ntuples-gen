#!/usr/bin/env bash

INPUT_NTP=../../ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root

# Emulate L0 Hadron
../../lib/python/TrackerOnlyEmu/scripts/run2-rdx-l0_hadron.py ${INPUT_NTP} \
    emu_l0_hadron_debug.root --debug

# Generate comparison plots
../plot_trigger_efficiency_comp.py \
    -n ./emu_l0_hadron_debug.root -o b0 -t TupleB0/DecayTree -c \
    --title "L0Hadron TOS" \
    --ext png \
    --triggers d0_l0_hadron_tos d0_l0_hadron_tos_emu_no_bdt \
    -k k_trg_et k_trg_hcal_et \
       pi_trg_et pi_trg_hcal_et \
       k_pi_trg_et_sum k_pi_trg_hcal_et_sum \
       d0_et_emu_no_bdt \
       k_pi_trg_et_cap \
    -D 3244 4244 3244 4244 \
       3244 4244 3244 4244 \
       3244 4244 3244 4244 \
       3244 4244 \
       3244 4244 \
    --xlabel "\$K$ trigger \$E_T$" \
             "\$K$ trigger HCAL \$E_T$" \
             "\$\\pi$ trigger \$E_T$" \
             "\$\\pi$ trigger HCAL \$E_T$" \
             "\$K+\\pi$ trigger \$E_T$ (capped)" \
             "\$K+\\pi$ trigger HCAL \$E_T$ (capped)" \
             "\$D^0$ emulated \$E_T$ (no BDT)" \
             "\$Max(K, \\pi)$ trigger \$E_T$ (capped)" \
    --bins 50

# Plot differences between Trigger ET variables
../plot_two_branches.py -n ./emu_l0_hadron_debug.root -t TupleB0/DecayTree \
    -b k_trg_et -B pi_trg_et \
    -l "\$K$ Trigger \$E_T$" -L "\$\\pi$ Trigger \$E_T$" \
    -o k_pi_trg_et_comparison.png \
    -XD -10 6200

#!/usr/bin/env bash

INPUT_NTP=../../ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root

# Emulate L0 Hadron
#../../lib/python/TrackerOnlyEmu/scripts/run2-rdx-l0_hadron.py ${INPUT_NTP} \
    #emu_l0_hadron_debug.root --debug
#../../lib/python/TrackerOnlyEmu/scripts/run2-rdx-l0_hadron.py ${INPUT_NTP} \
    #emu_l0_hadron_no_debug.root

# Generate comparison plots
#../plot_trigger_efficiency_comp.py \
    #-n ./emu_l0_hadron_debug.root -o b0 -t TupleB0/DecayTree -c \
    #--title "L0Hadron TOS" \
    #--ext png \
    #--triggers d0_l0_hadron_tos d0_l0_hadron_tos_emu_no_bdt \
    #-k k_trg_et k_trg_hcal_et \
       #pi_trg_et pi_trg_hcal_et \
       #k_pi_trg_et_sum k_pi_trg_hcal_et_sum \
       #d0_et_emu_no_bdt \
       #k_pi_trg_et_cap \
    #-D 744 5744 744 5744 \
       #744 5744 744 5744 \
       #744 5744 744 5744 \
       #744 5744 \
       #744 5744 \
    #--xlabel "\$K$ trigger \$E_T$" \
             #"\$K$ trigger HCAL \$E_T$" \
             #"\$\\pi$ trigger \$E_T$" \
             #"\$\\pi$ trigger HCAL \$E_T$" \
             #"\$K+\\pi$ trigger \$E_T$ (capped)" \
             #"\$K+\\pi$ trigger HCAL \$E_T$ (capped)" \
             #"\$D^0$ emulated \$E_T$ (no BDT)" \
             #"\$Max(K, \\pi)$ trigger \$E_T$ (capped)" \
    #--bins 25

# Plot differences between Trigger ET variables
plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b k_trg_et pi_trg_et \
    -l "\$K$ Trigger \$E_T$" "\$\\pi$ Trigger \$E_T$" \
    -o k_pi_trg_et_comparison.png \
    -XD -10 6200 -YD 0 5e4

# Plot the difference between realET and TriggerET
plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b k_real_et k_trg_et \
    -l "\$K$ MC true \$E_T$" "\$K$ trigger \$E_T$" \
    -o k_real_trg_et_comparison.png \
    -XD -100 8000 -YD 0 9e4 \
    --xlabel "\$K$ \$E_T$"

plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b pi_real_et pi_trg_et \
    -l "\$\\pi$ MC true \$E_T$" "\$\\pi$ trigger \$E_T$" \
    -o pi_real_trg_et_comparison.png \
    -XD -100 8000 -YD 0 9e4 \

# Plot the difference between K, pi MC True ET
plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b k_real_et pi_real_et \
    -l "\$K$ MC true \$E_T$" "\$\\pi$ MC true \$E_T$" \
    -o k_pi_real_et_comparison.png \
    -XD -10 8000 -YD 0 1e5 \
    --xlabel "\$K/\\pi$ \$E_T$"

# Plot the difference between D0 PT and ET
plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b d0_pt_raw k_pi_trg_et_cap \
    -l "\$D^0$ \$p_T$" "\$D^0$ HCAL \$E_T$" \
    -o d0_pt_et_comparison.png \
    -XD 0 8000 -YD 0 9e4 \
    --xlabel "\$D^0$ \$E_T$ or \$p_T$"

plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b d0_pt_raw d0_et_emu_no_bdt \
    -l "\$D^0$ \$p_T$" "\$D^0$ emulated HCAL \$E_T$" \
    -o d0_pt_et_emu_comparison.png \
    -XD 0 8000 -YD 0 9e4 \
    --xlabel "\$D^0$ \$E_T$ or \$p_T$"

plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b k_pi_trg_et_cap d0_et_emu_no_bdt \
    -l "\$D^0$ HCAL \$E_T$" "\$D^0$ emulated HCAL \$E_T$" \
    -o d0_et_et_emu_comparison.png \
    -XD 0 6200 -YD 0 9e4 \
    --xlabel "\$D^0$ \$E_T$"

# Plot the difference between real and emulated D0 HCAL ET, separated by low and
# high ET components
plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b d0_et_diff d0_et_diff d0_et_diff \
    -l "no cut" \
       "\$D^0$ \$E_T < 3744$" \
       "\$D^0$ \$E_T \\geq 3744$" \
    --cuts "true" \
           "k_pi_trg_et_cap < 3744" \
           "k_pi_trg_et_cap >= 3744" \
    -XD -6500 6500 \
    --xlabel "\$D^0$ \$E_T$ real-emulated" \
    -o d0_et_diff_low_high.png

# Plot the radial differences vs radial differences (wrong)
plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b rdiff_k_pi "rdiff_k_pi_wrong*10" \
    -l "\$K$ \$\\pi$ radial distance" \
       "\$K$ \$\\pi$ radial distance (wrong) \$\\times 10$" \
    --normalize \
    --ylabel "Normalized" \
    -o rdiff_k_pi_vs_rdiff_k_pi_wrong.png

# Plot the effect of nSPDhits < 450 for radial differences
plotbr \
    -n ./emu_l0_hadron_no_debug.root/TupleB0/DecayTree -b rdiff_k_pi \
    -l "no nSPDHits \$< 450$ cut" \
    -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree -b rdiff_k_pi \
    -l "with nSPDhits cut" \
    -XD 0 5000 \
    --xlabel "\$K$ \$\\pi$ radial distance" \
    -o rdiff_k_pi_nspd_cut_comp.png

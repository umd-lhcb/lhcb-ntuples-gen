#!/usr/bin/env bash

INPUT_NTP=../../ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root

# Emulate L0 Hadron
../../lib/python/TrackerOnlyEmu/scripts/run2-rdx-l0_hadron.py ${INPUT_NTP} \
    emu_l0_hadron_debug.root --debug
../../lib/python/TrackerOnlyEmu/scripts/run2-rdx-l0_hadron.py ${INPUT_NTP} \
    emu_l0_hadron_no_debug.root

# Generate trigger efficiency comparison plots, zoomed out
../../scripts/plot_trigger_efficiencies.py \
    -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree  \
    -b d0_l0_hadron_tos d0_l0_hadron_tos_emu_no_bdt \
    -k k_trg_et k_trg_hcal_et \
       pi_trg_et pi_trg_hcal_et \
       k_pi_trg_et_sum k_pi_trg_hcal_et_sum \
       d0_et_emu_no_bdt \
       k_pi_trg_et_cap \
    -D 744 5744 744 5744 \
       744 5744 744 5744 \
       744 5744 744 5744 \
       744 5744 \
       744 5744 \
    --xlabel "\$K$ trigger \$E_T$" \
             "\$K$ trigger HCAL \$E_T$" \
             "\$\\pi$ trigger \$E_T$" \
             "\$\\pi$ trigger HCAL \$E_T$" \
             "\$K+\\pi$ trigger \$E_T$ (capped)" \
             "\$K+\\pi$ trigger HCAL \$E_T$ (capped)" \
             "\$D^0$ emulated \$E_T$ (no BDT)" \
             "\$Max(K, \\pi)$ trigger \$E_T$ (capped)" \
    -o b0 --bins 25 --title "L0Hadron TOS" --ext png --ratio-plot

# Generate trigger efficiency comparison plots, with a different zoom but the
# same bin width
../../scripts/plot_trigger_efficiencies.py \
    -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree  \
    -b d0_l0_hadron_tos d0_l0_hadron_tos_emu_no_bdt d0_l0_hadron_tos_emu \
    -k d0_pt_raw  \
    -D 2500 10500 \
    --xlabel "\$D^0$ \$p_T$" \
    -o b0 --bins 40 --title "L0Hadron TOS" --ext png --ratio-plot

# Plot differences between Trigger ET variables
plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b k_trg_et pi_trg_et \
    -l "\$K$ Trigger \$E_T$" "\$\\pi$ Trigger \$E_T$" \
    -o k_pi_trg_et_comparison.png \
    -XD -10 6200 -YD 0 5e4

plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b "k_trg_et-pi_trg_et" \
    -l "\$K$ Trigger \$E_T - \\pi$ Trigger \$E_T$" \
    -o k_pi_trg_et_diff_comparison.png \
    -YD 0 5.8e5

# Plot the difference between realET, TriggerET, and TriggerHCALET
plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b k_real_et k_trg_et k_trg_hcal_et \
    -l "\$K$ real \$E_T$" "\$K$ trigger \$E_T$" "\$K$ trigger HCAL \$E_T$" \
    -o k_real_trg_trg_hcal_et_comparison.png \
    -XD -100 8000 -YD 0 9e4 \
    --xlabel "\$K$ \$E_T$"

plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b pi_real_et pi_trg_et pi_trg_hcal_et \
    -l "\$\\pi$ real \$E_T$" "\$\\pi$ trigger \$E_T$" \
       "\$\\pi$ trigger HCAL \$E_T$" \
    -o pi_real_trg_trg_hcal_et_comparison.png \
    -XD -100 8000 -YD 0 9e4 \
    --xlabel "\$\\pi$ \$E_T$"

# Plot the difference between K, pi MC True ET
plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b k_real_et pi_real_et \
    -l "\$K$ real \$E_T$" "\$\\pi$ real \$E_T$" \
    -o k_pi_real_et_comparison.png \
    -XD -10 8000 -YD 0 1e5 \
    --xlabel "\$K/\\pi$ \$E_T$"

# Plot the difference between D0 PT and ET
plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b d0_pt_raw k_pi_trg_et_cap \
    -l "\$D^0$ \$p_T$" "\$D^0$ Trigger \$E_T$" \
    -o d0_pt_et_comparison.png \
    -XD 0 8000 -YD 0 9e4 \
    --xlabel "\$D^0$ \$E_T$ or \$p_T$"

plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b d0_pt_raw d0_et_emu_no_bdt \
    -l "\$D^0$ \$p_T$" "\$D^0$ emulated \$E_T$" \
    -o d0_pt_et_emu_comparison.png \
    -XD 0 8000 -YD 0 9e4 \
    --xlabel "\$D^0$ \$E_T$ or \$p_T$"

plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b k_pi_trg_et_cap d0_et_emu_no_bdt \
    -l "\$D^0$ Trigger \$E_T$" "\$D^0$ emulated \$E_T$" \
    -o d0_et_et_emu_comparison.png \
    -XD 0 6200 -YD 0 9e4 \
    --xlabel "\$D^0$ \$E_T$"

# Plot the difference between official and emulated D0 Trigger ET, separated by
# low and high ET components
plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b d0_et_diff d0_et_diff d0_et_diff \
    -l "no cut" \
       "\$D^0$ \$E_T < 3744$" \
       "\$D^0$ \$E_T \\geq 3744$" \
    --cuts "true" \
           "k_pi_trg_et_cap < 3744" \
           "k_pi_trg_et_cap >= 3744" \
    -XD -6500 6500 \
    --xlabel "\$D^0$ trigger \$-$ emulated \$E_T$ (no BDT)" \
    -o d0_et_diff_low_high.png

plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b "k_pi_trg_et_cap-d0_et_emu" "k_pi_trg_et_cap-d0_et_emu" \
       "k_pi_trg_et_cap-d0_et_emu" \
    -l "no cut" \
       "\$D^0$ \$E_T < 3744$" \
       "\$D^0$ \$E_T \\geq 3744$" \
    --cuts "true" \
           "k_pi_trg_et_cap < 3744" \
           "k_pi_trg_et_cap >= 3744" \
    -XD -6500 6500 \
    --xlabel "\$D^0$ trigger \$-$ emulated \$E_T$ (BDT)" \
    -o d0_et_bdt_diff_low_high.png

# Plot the radial differences vs radial differences (wrong)
plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree \
    -b rdiff_k_pi "rdiff_k_pi_wrong*10" \
    -l "\$K$ \$\\pi$ radial distance" \
       "\$K$ \$\\pi$ radial distance (wrong) \$\\times 10$" \
    --normalize \
    --ylabel "Normalized" \
    -XD 0 5000 \
    -o rdiff_k_pi_vs_rdiff_k_pi_wrong.png

# Plot the effect of nSPDhits < 450 for radial differences
# plotbr -n ./emu_l0_hadron_no_debug.root/TupleB0/DecayTree -b rdiff_k_pi \
#     -l "no nSPDHits \$< 450$ cut" \
#     -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree -b rdiff_k_pi \
#     -l "with nSPDhits cut" \
#     -XD 0 5000 \
#     --xlabel "\$K$ \$\\pi$ radial distance" \
#     -o rdiff_k_pi_nspd_cut_comp.png

plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree -b d0_pt_raw d0_pt_raw d0_pt_raw -l "\$D^0$ \$p_T$ for \$E_T^{emu} \\in [-inf,3744]$" "\$D^0$ \$p_T$ for \$E_T^{emu} \\in [3744,6000)$" "\$D^0$ \$p_T$ for \$E_T^{emu} \\in [6000+]$" -o d0_pt_emubins.png --xlabel "\$D^0$ \$p_T$" -XD 1800 12000 --cuts "d0_et_emu_no_bdt<3744" "d0_et_emu_no_bdt>=3744 & d0_et_emu_no_bdt<6000" "d0_et_emu_no_bdt>=6000"

plotbr -n ./emu_l0_hadron_debug.root/TupleB0/DecayTree -b d0_et_emu_no_bdt d0_et_emu_no_bdt d0_et_emu_no_bdt -l "\$E_T^{emu}$ for \$D^0$ \$p_T \\in [-inf,5000]$" "\$E_T^{emu}$ for \$D^0$ \$p_T \\in [5000,10000)$" "\$E_T^{emu}$ for \$D^0$ \$p_T \\in [10000+]$" -o emu_et_d0ptbins.png --xlabel "\$D^0$ \$E^{emu}_T$" -XD 0 7000 --cuts "d0_pt_raw<5000" "d0_pt_raw>=5000 & d0_pt_raw<10000" "d0_pt_raw>=10000"
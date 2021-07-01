#!/usr/bin/env bash

INPUT_NTP=../ntuple-RDX_l0_hadron_tos_training_sample/rdx-bdt_train_sample.root

if [ ! -f ${INPUT_NTP} ]; then
    echo "Input ntuple: ${INPUT_NTP} doesn't exist!"
    echo "Generating required ntuple..."
    ../ntuple-RDX_l0_hadron_tos_training_sample/bdt_train_sample_from_DstMuNu.sh
fi

# Train BDT w/ different max_depth
for d in 3 4 5 6 7 8 9 10 11 12 15 20 25 40 50 80 100
do
    echo "========"
    echo "BDT max_depth is set to ${d}"

    # Generate debug ntuples w/ different BDT max_depth
    ../../lib/python/TrackerOnlyEmu/scripts/run2-rdx-l0_hadron_train_bdt.py \
        ${INPUT_NTP} None \
        --debug-ntuple "bdt_max_depth_${d}.root" --max-depth $d

    # Debug plots
    plotbr -n "./bdt_max_depth_${d}.root/TupleB0/DecayTree" \
        -b d0_et_diff d0_et_diff_pred \
        -l "\$D^0$ trigger \$-$ emulated \$E_T$ (no BDT)" \
           "BDT prediction" \
        --xlabel "Difference in \$E_T$, w/ \$depth_{BDT} = ${d}$ [MeV]" \
        -o "d0_et_diff_max_depth_${d}.png"
    plotbr -n "./bdt_max_depth_${d}.root/TupleB0/DecayTree" \
        -b d0_et_trg_pred_diff \
        -l '' \
        --xlabel "\$D^0$ \$E_T$ emulation resolution, w/ \$depth_{BDT} = ${d}$ [MeV]" \
        -o "d0_et_emu_resolution_max_depth_${d}.png"
done

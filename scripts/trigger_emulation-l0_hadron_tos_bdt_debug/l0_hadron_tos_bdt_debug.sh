#!/usr/bin/env bash

INPUT_NTP=../ntuple-RDX_l0_hadron_tos_training_sample/rdx-bdt_train_sample.root

if [ ! -f ${INPUT_NTP} ]; then
    echo "Input ntuple: ${INPUT_NTP} doesn't exist!"
    echo "Generating required ntuple..."
    ../ntuple-RDX_l0_hadron_tos_training_sample/bdt_train_sample_from_DstMuNu.sh
fi

declare -A YLIM=(
    [3]=2.8e5
    [4]=2.2e5
    [5]=2.2e5
    [6]=2.2e5
    [7]=2.2e5
    [8]=2.2e5
    [9]=2.2e5
    [10]=2.2e5
    [11]=2.2e5
    [12]=2.2e5
    [15]=2.2e5
    [20]=1.5e5
    [25]=1.2e5
    [40]=7e4
    [50]=7e4
    [80]=7e4
    [100]=7e4
)

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
        -l \
           "\$D^0$ trigger \$-$ emulated \$E_T$ (no BDT)" \
           "BDT prediction" \
        --xlabel "Difference in \$E_T$, w/ \$depth_{BDT} = ${d}$ [MeV]" \
        --bins 40 -XD -4000 6000 -YD 0 ${YLIM[$d]} \
        -o "d0_et_diff_max_depth_${d}.png"
    plotbr -n "./bdt_max_depth_${d}.root/TupleB0/DecayTree" \
        -b d0_et_trg_pred_diff \
        -l '' \
        --xlabel "\$D^0$ \$E_T$ emulation resolution, w/ \$depth_{BDT} = ${d}$ [MeV]" \
        -o "d0_et_emu_resolution_max_depth_${d}.png"
done

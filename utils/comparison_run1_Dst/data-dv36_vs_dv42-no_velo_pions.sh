#!/bin/bash

OUTPUT_DIR="../../docs/data/comparison_run1_Dst/data-dv36_vs_dv42-no_velo_pions"
NTP_REF="../../run1-b2D0MuXB2DMuNuForTauMuLine/samples/BCands_Dst-phoebe-data-2012-mag_down-dv36-subset-no_velo_pions.root"
NTP_COM="../../run1-b2D0MuXB2DMuNuForTauMuLine/samples/BCands_Dst-yipeng-data-2012-mag_down-dv42-subset-no_velo_pions.root"

BRANCHES=(
    "Y_ISOLATION_Type"
    "Y_ISOLATION_Type2"
    "Y_ISOLATION_Type3"
    "Y_ISOLATION_Type4"
)

BRANCHES_DIFF="Y_ISOLATION_BDT,Y_ISOLATION_BDT2,Y_ISOLATION_BDT3"

for branch in "${BRANCHES[@]}"; do
    ../plot_single_branch.py \
        -n "${NTP_REF}" -t "TupleY/DecayTree" -b "${branch}" \
        -o "${OUTPUT_DIR}/${branch}_dv36.png"
    ../plot_single_branch.py \
        -n "${NTP_COM}" -t "TupleB0/DecayTree" -b "${branch}" \
        -o "${OUTPUT_DIR}/${branch}_dv42.png"
done

# Comparison between track types
../plot_match_iso_track.py -n ${NTP_REF} -N ${NTP_COM} \
    -t 'TupleY/DecayTree' -T 'TupleB0/DecayTree' -s '_dv42,_dv36' \
    -o ${OUTPUT_DIR}

../plot_diff_two_ntuples.py -n "${NTP_REF}" -N "${NTP_COM}" \
    -t "TupleY/DecayTree" -T "TupleB0/DecayTree" \
    -b "${BRANCHES_DIFF}" -B "${BRANCHES_DIFF}" \
    -o "${OUTPUT_DIR}"

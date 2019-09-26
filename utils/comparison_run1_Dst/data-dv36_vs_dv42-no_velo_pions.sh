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

for branch in "${BRANCHES[@]}"; do
    ../plot_single_branch.py "${NTP_REF}" "TupleY/DecayTree" "${branch}" \
        -o "${OUTPUT_DIR}/${branch}_dv36-no_velo_pions.png"
    ../plot_single_branch.py "${NTP_COM}" "TupleB0/DecayTree" "${branch}" \
        -o "${OUTPUT_DIR}/${branch}_dv42-no_velo_pions.png"
done

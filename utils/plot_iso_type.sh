#!/bin/bash

OUTPUT_DIR="../docs/data/comparison_run1_RDst/data-2012-mag_down-dv36r1p2_vs_dv42r8p1"
NTP_DV36="../run1-b2D0MuXB2DMuNuForTauMuLine/samples/BCands_Dst-phoebe-data-2012-mag_down-davinci_v36r1p2-subset.root"
NTP_DV42="../run1-b2D0MuXB2DMuNuForTauMuLine/samples/BCands_Dst-yipeng-data-2012-mag_down-davinci_v42r8p1-subset.root"

BRANCHES=(
    "Y_ISOLATION_Type"
    "Y_ISOLATION_Type2"
    "Y_ISOLATION_Type3"
    "Y_ISOLATION_Type4"
)

for branch in "${BRANCHES[@]}"; do
    ./plot_single_branch.py "${NTP_DV36}" "TupleY/DecayTree" "${branch}" \
        -o "${OUTPUT_DIR}/${branch}_dv36r1p2.png"
    ./plot_single_branch.py "${NTP_DV42}" "TupleB0/DecayTree" "${branch}" \
        -o "${OUTPUT_DIR}/${branch}_dv42r8p1.png"
done

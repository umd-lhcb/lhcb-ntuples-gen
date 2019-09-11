#!/bin/bash

OUTPUT_DIR="../gen/"
NTP_DV36="../run1-b2D0MuXB2DMuNuForTauMuLine/samples/BCands_Dst-phoebe-data-2012-mag_down-davinci_v36r1p2-subset-no_velo_pions.root"
NTP_DV42="../run1-b2D0MuXB2DMuNuForTauMuLine/samples/BCands_Dst-yipeng-data-2012-mag_down-davinci_v42r8p1-subset-no_velo_pions.root"

BRANCHES=(
    "Y_ISOLATION_Type"
    "Y_ISOLATION_Type2"
    "Y_ISOLATION_Type3"
    "Y_ISOLATION_Type4"
)

for branch in "${BRANCHES[@]}"; do
    root -q -l 'make_histo_float.cxx(
        "'"${NTP_DV36}"'", "'"${OUTPUT_DIR}"'",
        "_dv36r1p2-no_velo_pions",
        "TupleY/DecayTree", "'"${branch}"'", 40, 0, 5)'
    root -q -l 'make_histo_float.cxx(
        "'"${NTP_DV42}"'", "'"${OUTPUT_DIR}"'",
        "_dv42r8p1-no_velo_pions",
        "TupleB0/DecayTree", "'"${branch}"'", 40, 0, 5)'
done

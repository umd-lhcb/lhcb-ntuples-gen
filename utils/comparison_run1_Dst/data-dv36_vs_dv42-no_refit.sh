#!/bin/bash

OUTPUT_DIR="../../docs/data/comparison_run1_Dst/data-dv36_vs_dv42-no_refit"
NTP_REF="../../run1-b2D0MuXB2DMuNuForTauMuLine/samples/BCands_Dst-phoebe-data-2012-mag_down-dv36-subset-no_refit.root"
NTP_COM="../../run1-b2D0MuXB2DMuNuForTauMuLine/samples/BCands_Dst-yipeng-data-2012-mag_down-dv42-subset-no_refit.root"

# Diff
BRANCHES="D0_P,Dst_2010_minus_P,"
BRANCHES+="Kplus_P,Kplus_PX,Kplus_PY,Kplus_PZ,"
BRANCHES+="muplus_P,muplus_PX,muplus_PY,muplus_PZ,"
BRANCHES+="Y_ISOLATION_BDT,Y_ISOLATION_BDT2,Y_ISOLATION_BDT3"

../plot_diff_two_ntuples.py -n "${NTP_REF}" -N "${NTP_COM}" \
    -t "TupleB0/DecayTree" -T "TupleB0/DecayTree" \
    -b "${BRANCHES}" -B ${BRANCHES} \
    -o "${OUTPUT_DIR}"

# Individual branches
BRANCHES=(
    "Y_ISOLATION_Type"
    "Y_ISOLATION_Type2"
    "Y_ISOLATION_Type3"
    "Y_ISOLATION_Type4"
)

for branch in "${BRANCHES[@]}"; do
    ../plot_single_branch.py "${NTP_REF}" "TupleB0/DecayTree" "${branch}" \
        -o "${OUTPUT_DIR}/${branch}_dv36-no_refit.png"
    ../plot_single_branch.py "${NTP_COM}" "TupleB0/DecayTree" "${branch}" \
        -o "${OUTPUT_DIR}/${branch}_dv42-no_refit.png"
done

# Comparison between track types
../plot_match_iso_track_two_ntuples.py -n ${NTP_REF} -N ${NTP_COM} \
    -t 'TupleB0/DecayTree' -T 'TupleB0/DecayTree' -s '_dv42,_dv36' \
    -o ${OUTPUT_DIR}

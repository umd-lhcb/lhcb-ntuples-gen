#!/bin/bash

OUTPUT_DIR="../../docs/data/comparison/Dst_vars_run1/data-phoebe_vs_yipeng"
NTP_REF="../../run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/run1-Dst/BCands_Dst-phoebe-data-2012-mag_down.root"
NTP_COM="../../run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/run1-Dst/BCands_Dst-yipeng-data-2012-mag_down.root"

BRANCHES="D0_P,Dst_2010_minus_P,"
BRANCHES+="Kplus_P,Kplus_PX,Kplus_PY,Kplus_PZ,"
BRANCHES+="muplus_P,muplus_PX,muplus_PY,muplus_PZ,"
BRANCHES+="Y_ISOLATION_BDT,Y_ISOLATION_BDT2,Y_ISOLATION_BDT3,"
BRANCHES+="Y_ENDVERTEX_X,Y_ENDVERTEX_Y,Y_ENDVERTEX_Z,"
BRANCHES+="Y_OWNPV_X,Y_OWNPV_Y,Y_OWNPV_Z"

BRANCHES_TWO_NTP=(
    "Y_ENDVERTEX_X"
    "Y_ENDVERTEX_Y"
    "Y_ENDVERTEX_Z"
    "Y_OWNPV_X"
    "Y_OWNPV_Y"
    "Y_OWNPV_Z"
)

for branch in "${BRANCHES_TWO_NTP[@]}"; do
    ../plot_single_branch_two_ntuples.py -n "${NTP_REF}" -N "${NTP_COM}" \
        -t "YCands/DecayTree" -T "TupleY/DecayTree" \
        -b "${branch}" -B "${branch}" -o "${OUTPUT_DIR}/${branch}_dist.png"
done

../plot_diff_two_ntuples.py -n "${NTP_REF}" -N "${NTP_COM}" \
    -t "YCands/DecayTree" -T "TupleY/DecayTree" \
    -b "${BRANCHES}" -B "${BRANCHES}" \
    -o "${OUTPUT_DIR}"

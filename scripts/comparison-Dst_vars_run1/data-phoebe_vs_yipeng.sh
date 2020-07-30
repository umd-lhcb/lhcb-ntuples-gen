#!/bin/bash

OUTPUT_DIR="../../docs/data/comparison/Dst_vars_run1/data-phoebe_vs_yipeng"
NTP_REF="../../ntuples/ref-rdx-run1/Dst-std/Dst--19_09_05--std--data--2012--md--phoebe.root"
NTP_COM="../../ntuples/pre-0.9.0/Dst-std/Dst--19_09_05--std--data--2012--md.root"

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

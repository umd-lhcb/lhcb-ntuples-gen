#!/bin/bash

OUTPUT_DIR="../../docs/data/comparison/Dst_vars_run1/mc-py6-phoebe_vs_yipeng"
NTP_REF="../../run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/mc/BCands-phoebe-mc-mag_down-py6-Bd2DstTauNu.root"
NTP_COM="../../run1-b2D0MuXB2DMuNuForTauMuLine/ntuples/mc/BCands-yipeng-mc-mag_down-py6-sim08a-Bd2DstTauNu.root"

BRANCHES="D0_P,Kplus_P,"
BRANCHES+="Y_ISOLATION_BDT,Y_ISOLATION_BDT2,Y_ISOLATION_BDT3"

../plot_diff_two_ntuples.py -n "${NTP_REF}" -N "${NTP_COM}" \
    -t "YCands/DecayTree" -T "TupleY/DecayTree" \
    -b "${BRANCHES}" -B ${BRANCHES} \
    -o "${OUTPUT_DIR}"

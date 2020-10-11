#!/usr/bin/env bash

OUTPUT_DIR="../../docs/data/comparison/RDst_vars_run1/mc-py6-phoebe_vs_yipeng"
NTP_REF="../../ntuples/ref-rdx-run1/Dst-mc/Dst--19_09_26--mc--Bd2DstTauNu--2012--md--py6-phoebe.root"
NTP_COM="../../ntuples/pre-0.9.0/Dst-mc/Dst--19_09_26--mc--Bd2DstTauNu--2012--md--py6-sim08a.root"

mkdir -p ${OUTPUT_DIR}

BRANCHES="D0_P,Kplus_P,"
BRANCHES+="Y_ISOLATION_BDT,Y_ISOLATION_BDT2,Y_ISOLATION_BDT3"

../plot_diff_two_ntuples.py -n "${NTP_REF}" -N "${NTP_COM}" \
    -t "YCands/DecayTree" -T "TupleY/DecayTree" \
    -b "${BRANCHES}" -B ${BRANCHES} \
    -o "${OUTPUT_DIR}"

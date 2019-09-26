#!/bin/bash

OUTPUT_DIR="../docs/data/comparison_run1_RDst/data-2012-mag_down-dv36r1p2_vs_dv42r8p1"
NTP_DV36="../run1-b2D0MuXB2DMuNuForTauMuLine/samples/BCands_Dst-phoebe-data-2012-mag_down-davinci_v36r1p2-subset.root"
NTP_DV42="../run1-b2D0MuXB2DMuNuForTauMuLine/samples/BCands_Dst-yipeng-data-2012-mag_down-davinci_v42r8p1-subset.root"

BRANCHES="D0_P,Dst_2010_minus_P,"
BRANCHES+="Kplus_P,Kplus_PX,Kplus_PY,Kplus_PZ,"
BRANCHES+="muplus_P,muplus_PX,muplus_PY,muplus_PZ,"
BRANCHES+="Y_ISOLATION_BDT,Y_ISOLATION_BDT2,Y_ISOLATION_BDT3"

./plot_diff_two_branches.py -n "${NTP_DV36}" -N "${NTP_DV42}" \
    -t "TupleY/DecayTree" -T "TupleB0/DecayTree" -b "${BRANCHES}" \
    -o "${OUTPUT_DIR}"

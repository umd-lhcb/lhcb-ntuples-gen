#!/usr/bin/env bash

OUTPUT_DIR="../../docs/data/comparison/RDst_vars_run1/data-dv36_vs_dv45-no_refit"
NTP_REF="../../run1-rdx/samples/Dst--19_10_04--std--data--2012--md--dv36-subset-no_refit.root"
NTP_COM="../../run1-rdx/samples/Dst--19_11_14--std--data--2012--md--dv45-subset-no_refit.root"

mkdir -p ${OUTPUT_DIR}

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
    ../plot_single_branch.py \
        -n "${NTP_REF}" -t "TupleB0/DecayTree" -b "${branch}" \
        -o "${OUTPUT_DIR}/${branch}_dv36.png"
    ../plot_single_branch.py \
        -n "${NTP_COM}" -t "TupleB0/DecayTree" -b "${branch}" \
        -o "${OUTPUT_DIR}/${branch}_dv45.png"
done

# Comparison between track types
../plot_match_iso_track.py -n ${NTP_REF} -N ${NTP_COM} \
    -t 'TupleB0/DecayTree' -T 'TupleB0/DecayTree' -s '_dv45,_dv36' \
    -o ${OUTPUT_DIR}

# Draw 2D histogram between track type difference and BDT score difference
../plot_match_iso_track_hexbin.py -n ${NTP_REF} -N ${NTP_COM} \
    -t 'TupleB0/DecayTree' -T 'TupleB0/DecayTree' -s '_dv45,_dv36' \
    -o ${OUTPUT_DIR} --bins 30

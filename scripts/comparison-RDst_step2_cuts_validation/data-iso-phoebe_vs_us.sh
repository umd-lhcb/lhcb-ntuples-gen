#!/usr/bin/env bash

OUTPUT_DIR="../../docs/data/comparison/RDst_step2_cuts_validation/data-iso_phoebe_vs_us"
NTP_REF="../../gen/run1-Dst-step2/Dst--20_07_02--mix--data--2011--md--phoebe-step2.root"
NTP_COM="../../gen/run1-Dst_D0-step2/Dst_D0--20_10_12--std--data--2011--md--step2.root"

mkdir -p ${OUTPUT_DIR}

# Diff
BRANCHES="el,mm2"

../plot_diff_two_ntuples.py -n "${NTP_REF}" -N "${NTP_COM}" \
    -t "dst_iso" -T "dst_iso" \
    -b "${BRANCHES}" -B ${BRANCHES} \
    -o "${OUTPUT_DIR}"

# Individual branches
BRANCHES_TWO_NTP=(
    "el"
    "mm2"
)

for branch in "${BRANCHES_TWO_NTP[@]}"; do
    ../plot_single_branch_two_ntuples.py -n "${NTP_REF}" -N "${NTP_COM}" \
        -t "dst_iso" -T "dst_iso" \
        -b "${branch}" -B "${branch}" -o "${OUTPUT_DIR}/${branch}_dist.png"
done

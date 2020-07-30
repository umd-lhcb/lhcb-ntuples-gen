#!/bin/bash

OUTPUT_DIR="../../docs/data/cutflows/Dst_run1_vs_run2/cutflow_mc-2011_vs_2016"
NTP_REF="../../ntuples/pre-0.9.0/Dst-cutflow_mc/Dst--20_03_18--cutflow_mc--cocktail--2011--md.root"
NTP_COM="../../ntuples/pre-0.9.0/Dst-cutflow_mc/Dst--20_03_18--cutflow_mc--cocktail--2016--md.root"

BRANCHES_TWO_NTP=(
    "Y_PT"
    "Dst_2010_minus_PT"
    "D0_PT"
    "Kplus_PT"
    "muplus_PT"
    "piminus0_PT"
    "piminus_PT"
)

for branch in "${BRANCHES_TWO_NTP[@]}"; do
    ../plot_single_branch_two_ntuples.py -n "${NTP_REF}" -N "${NTP_COM}" \
        -t "TupleB0/DecayTree" -T "TupleB0/DecayTree" \
        -b "${branch}" -B "${branch}" -o "${OUTPUT_DIR}/${branch}_dist.png"
done

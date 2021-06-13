#!/usr/bin/env bash

OUTPUT_DIR="."
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
    plotbr \
        -n "${NTP_REF}/TupleB0/DecayTree" -b "${branch}" -l 2011 \
        -n "${NTP_COM}/TupleB0/DecayTree" -b "${branch}" -l 2016 \
        --xlabel ${branch} \
         -o "${OUTPUT_DIR}/${branch}_dist.png"
done

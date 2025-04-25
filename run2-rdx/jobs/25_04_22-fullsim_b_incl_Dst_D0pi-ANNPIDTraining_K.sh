#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
export PATH=$DIR/../../ganga:$PATH
EXE=ganga_jobs-DV46r12.py

for i in 27163974; do
    for y in 2016 2017 2018; do
        for p in md mu; do
            $EXE \
                ../reco_Dst_D0-incl_b.py \
                ../conds/cond-mc-$y-$p-sim10d-incl_b.py \
                -p $p -d $i
        done
    done
done

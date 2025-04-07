#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
export PATH=$DIR/../../ganga:$PATH
#EXE=ganga_sample_jobs_parser.py
EXE=ganga_jobs.py

for y in 17 18; do
    for i in 11574021 11574011; do
        for p in md mu; do
            $EXE \
                ../reco_Dst_D0.py \
                ../conds/cond-mc-20$y-$p-sim09k.py \
                -p $p -d $i
        done
    done
done

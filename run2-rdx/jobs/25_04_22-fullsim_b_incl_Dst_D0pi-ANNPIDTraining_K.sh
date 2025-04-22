#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
export PATH=$DIR/../../ganga:$PATH
#EXE=ganga_sample_jobs_parser.py
EXE=ganga_jobs.py

for i in 27163974; do
    for p in md mu; do
        $EXE \
            ../reco_Dst_D0-incl_b.py \
            ../conds/cond-mc-2016-$p-sim10d-incl_b.py \
            -p $p -d $i
    done
done

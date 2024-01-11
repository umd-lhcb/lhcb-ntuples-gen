#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
export PATH=$DIR/../../ganga:$PATH
#EXE=ganga_sample_jobs_parser.py
EXE=ganga_jobs.py

for p in md mu; do
    $EXE \
        ../reco_Dst_D0.py \
        ../conds/cond-mc-2016-$p-sim10b-tracker_only.py \
        -p $p -d 11895400
done

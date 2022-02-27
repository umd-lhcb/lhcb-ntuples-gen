#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
export PATH=$DIR/../../ganga:$PATH
#EXE=ganga_sample_jobs_parser.py
EXE=ganga_jobs.py

for i in 12573012 11874430 11874440 12873450 12873460 12675011 11674401 12675402 11676012 12875440; do
    for p in md mu; do
        $EXE \
            ../reco_Dst_D0.py \
            ../conds/cond-mc-2016-$p-sim09k-tracker_only.py \
            -p $p -d $i
    done
done

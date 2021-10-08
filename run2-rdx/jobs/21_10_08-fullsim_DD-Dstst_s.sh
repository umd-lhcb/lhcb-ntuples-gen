#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
export PATH=$DIR/../../ganga:$PATH
#EXE=ganga_sample_jobs_parser.py
EXE=ganga_jobs.py

for i in 13874020 13674000 11894600 12893600 11894200 12893610 11894610 12895400 11894210 12895000; do
    for p in md mu; do
        $EXE \
            ../reco_Dst_D0.py \
            ../conds/cond-mc-2016-$p-sim09j.py \
            -p $p -d $i
    done
done

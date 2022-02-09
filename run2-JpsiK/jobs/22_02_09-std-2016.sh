#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
export PATH=$DIR/../../ganga:$PATH
#EXE=ganga_sample_jobs_parser.py
EXE=ganga_jobs.py

for p in md mu; do
    $EXE \
        ../reco_JpsiK.py \
        ../conds/cond-std-2016.py \
        -p $p
done

#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
export PATH=$DIR/../../ganga:$PATH

ganga_jobs.py \
    ../reco_Dst_D0.py \
    ../conds/cond-std-2016.py \
    -p md

ganga_jobs.py \
    ../reco_Dst_D0.py \
    ../conds/cond-std-2016.py \
    -p mu

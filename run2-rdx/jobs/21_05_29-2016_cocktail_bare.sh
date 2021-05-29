#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
export PATH=$DIR/../../ganga:$PATH

ganga_jobs.py \
    ../reco_Dst_D0.py \
    ../conds/cond-cutflow_mc-2016-md-sim09b-bare.py \

ganga_jobs.py \
    ../reco_Dst_D0.py \
    ../conds/cond-cutflow_mc-2016-mu-sim09b-bare.py \

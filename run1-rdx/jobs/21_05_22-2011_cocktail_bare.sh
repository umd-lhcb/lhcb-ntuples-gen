#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
export PATH=$DIR/../../ganga:$PATH

ganga_jobs.py \
    ../reco_Dst_D0.py \
    ../conds/cond-cutflow_mc-2011-md-sim08h-bare.py \

ganga_jobs.py \
    ../reco_Dst_D0.py \
    ../conds/cond-cutflow_mc-2011-mu-sim08h-bare.py \

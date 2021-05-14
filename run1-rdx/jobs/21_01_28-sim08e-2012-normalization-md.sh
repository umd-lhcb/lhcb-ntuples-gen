#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
export PATH=$DIR/../../ganga:$PATH

ganga_jobs.py \
    ../reco_Dst_D0.py \
    ../conds/cond-mc-2012-sim08e.py \
    -p md -d Bd2DstMuNu

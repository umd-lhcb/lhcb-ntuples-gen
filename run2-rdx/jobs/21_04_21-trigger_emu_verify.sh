#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
export PATH=$DIR/../../ganga:$PATH

ganga_jobs.py \
    ../reco_Dst_D0.py \
    ../conds/cond-mc-2016-sim09j.py \
    -p md -d 11574021

ganga_jobs.py \
    ../reco_Dst_D0.py \
    ../conds/cond-mc-2016-sim09j-tracker_only.py \
    -p md -d 11574021

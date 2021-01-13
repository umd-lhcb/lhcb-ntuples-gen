#!/usr/bin/env bash
#
# Last Change: Tue Jan 12, 2021 at 12:13 PM +0100

../../scripts/ganga/ganga_jobs.py \
    ../reco_Dst_D0.py \
    ../conds/cond-std-2016.py \
    -p md
../../scripts/ganga/ganga_jobs.py \
    ../reco_Dst_D0.py \
    ../conds/cond-std-2016.py \
    -p mu

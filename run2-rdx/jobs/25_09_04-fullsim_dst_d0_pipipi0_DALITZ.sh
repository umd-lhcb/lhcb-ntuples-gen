#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
export PATH=$DIR/../../ganga:$PATH
EXE=ganga_jobs-DV46r12.py

MCID=27163404
for p in md mu; do
    # 2016 Sim09c sample #1
    $EXE \
        ../reco_Dst_D0-incl_b.py \
        ../conds/cond-mc_s28-2016-$p-sim09c-pipipi0.py \
        -p $p -d $MCID
    # 2016 Sim09c sample #2
    $EXE \
        ../reco_Dst_D0-incl_b.py \
        ../conds/cond-mc_s28r1-2016-$p-sim09c-pipipi0.py \
        -p $p -d $MCID
    # 2016 Sim09l sample
    $EXE \
        ../reco_Dst_D0-incl_b.py \
        ../conds/cond-mc_s28r2-2016-$p-sim09l-pipipi0.py \
        -p $p -d $MCID
done
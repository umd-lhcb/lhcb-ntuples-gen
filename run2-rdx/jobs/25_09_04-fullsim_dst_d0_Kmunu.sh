#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
export PATH=$DIR/../../ganga:$PATH
EXE=ganga_jobs-DV46r12.py

MCID=27173001
for p in md mu; do
    # 2016 Sim09b sample
    $EXE \
        ../reco_Dst_D0-incl_b.py \
        ../conds/cond-mc_s28-2016-$p-sim09b-kmunu.py \
        -p $p -d $MCID
    # 2016 Sim09c sample
    $EXE \
        ../reco_Dst_D0-incl_b.py \
        ../conds/cond-mc_s28r1-2016-$p-sim09c-kmunu.py \
        -p $p -d $MCID
    # 2017
    $EXE \
        ../reco_Dst_D0-incl_b.py \
        ../conds/cond-mc_s29r2-2017-$p-sim09e-kmunu.py \
        -p $p -d $MCID
    # 2018
    $EXE \
        ../reco_Dst_D0-incl_b.py \
        ../conds/cond-mc_s34-2018-$p-sim10c-kmunu.py \
        -p $p -d $MCID
done

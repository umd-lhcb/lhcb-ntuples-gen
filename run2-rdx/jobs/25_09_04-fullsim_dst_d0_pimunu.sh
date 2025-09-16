#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
export PATH=$DIR/../../ganga:$PATH
EXE=ganga_jobs-DV46r12.py

MCID=27573001
for p in md mu; do
    # 2016 Sim09b sample
    $EXE \
        ../reco_Dst_D0-incl_b.py \
        ../conds/cond-mc_s28-2016-$p-sim09b-pimunu.py \
        -p $p -d $MCID
    # 2016 Sim09c sample
    $EXE \
        ../reco_Dst_D0-incl_b.py \
        ../conds/cond-mc_s28r1-2016-$p-sim09c-pimunu.py \
        -p $p -d $MCID
    # # 2016 Sim09h sample
    # $EXE \
    #     ../reco_Dst_D0-incl_b.py \
    #     ../conds/cond-mc_s28r1_turbo3a-2016-$p-sim09h-pimunu.py \
    #     -p $p -d $MCID
    # # 2017
    # $EXE \
    #     ../reco_Dst_D0-incl_b.py \
    #     ../conds/cond-mc_s29r2_mdst-2017-$p-sim09h-pimunu.py \
    #     -p $p -d $MCID
    # # 2018
    # $EXE \
    #     ../reco_Dst_D0-incl_b.py \
    #     ../conds/cond-mc_s34_mdst-2018-$p-sim09h-pimunu.py \
    #     -p $p -d $MCID
done

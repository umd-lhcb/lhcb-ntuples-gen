#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
export PATH=$DIR/../../ganga:$PATH
EXE=ganga_jobs-DV46r12.py

MCID=27163001
for p in md mu; do
    # 2016 Sim09c sample
    $EXE \
        ../reco_Dst_D0-incl_b.py \
        ../conds/cond-mc_s28r1_tck2-2016-$p-sim09c-pipi.py \
        -p $p -d $MCID
    # 2016 Sim09d sample
    $EXE \
        ../reco_Dst_D0-incl_b.py \
        ../conds/cond-mc_s28r1_mdst-2016-$p-sim09d-pipi.py \
        -p $p -d $MCID
    # 2017 Sim09e sample
    $EXE \
        ../reco_Dst_D0-incl_b.py \
        ../conds/cond-mc_s29r2-2017-$p-sim09e-pipi.py \
        -p $p -d $MCID
    # 2017 Sim09f sample
    $EXE \
        ../reco_Dst_D0-incl_b.py \
        ../conds/cond-mc_s29r2_mdst-2017-$p-sim09f-pipi.py \
        -p $p -d $MCID
    # 2018 DST sample
    $EXE \
        ../reco_Dst_D0-incl_b.py \
        ../conds/cond-mc_s34-2018-$p-sim09f-pipi.py \
        -p $p -d $MCID
    # 2018 MDST sample
    $EXE \
        ../reco_Dst_D0-incl_b.py \
        ../conds/cond-mc_s34_mdst-2018-$p-sim09f-pipi.py \
        -p $p -d $MCID
done

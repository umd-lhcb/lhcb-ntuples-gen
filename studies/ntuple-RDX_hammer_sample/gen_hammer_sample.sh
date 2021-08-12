#!/usr/bin/env bash

PROG=../../scripts/haddcut.py

declare -A NTPS=(
    ["rdx-run1-Bd2DstTauNu.root"]="../../run1-rdx/samples/Dst_D0--21_08_05--mc--Bd2DstTauNu--2012--md--py8-sim08a-dv45-subset.root"
    ["rdx-run1-Bd2DstMuNu.root"]="../../run1-rdx/samples/Dst_D0--21_08_11--mc--Bd2DstMuNu--2012--md--py8-sim08e-dv45-subset.root"
    ["rdx-run2-Bd2DstTauNu.root"]="../../run2-rdx/samples/Dst_D0--21_07_30--mc--Bd2DstTauNu--2016--md--py8-sim09j-dv45-subset.root"
    ["rdx-run2-Bd2DstMuNu.root"]="../../run2-rdx/samples/Dst_D0--21_07_30--mc--Bd2DstMuNu--2016--md--py8-sim09j-dv45-subset.root"
    ["rdx-run2-Bd2DststTauNu.root"]="../../run2-rdx/samples/Dst_D0--21_07_30--mc--Bd2DststTauNu--2016--md--py8-sim09j-dv45-subset.root"
)

for key in "${!NTPS[@]}"; do
    ${PROG} $key ${NTPS[$key]} -c ./hammer_sample.yml
done

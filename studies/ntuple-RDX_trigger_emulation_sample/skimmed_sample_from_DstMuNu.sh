#!/usr/bin/env bash

# Generate the base ntuple
../../tools/haddcut.py \
    rdx-tracker_only.root \
    ../../run2-rdx/samples/Dst_D0--21_04_12--mc--Bd2DstMuNu--2016--md--py8-sim09j-dv45-subset.root \
    -c ./trigger_emulation_sample.yml

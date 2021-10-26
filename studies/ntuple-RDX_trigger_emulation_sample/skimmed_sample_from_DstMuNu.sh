#!/usr/bin/env bash

NTP=../../run2-rdx/samples/Dst_D0--21_04_12--mc--Bd2DstMuNu--2016--md--py8-sim09j-dv45-subset.root

# Generate the base ntuple
../../scripts/haddcut.py \
    rdx-fullsim.root $NTP \
    -c ./trigger_emulation_sample.yml

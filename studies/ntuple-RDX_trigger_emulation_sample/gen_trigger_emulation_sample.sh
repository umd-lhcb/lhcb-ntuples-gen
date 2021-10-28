#!/usr/bin/env bash

NTP=../../run2-rdx/samples/Dst_D0--21_07_30--mc--Bd2DstMuNu--2016--md--py8-sim09j-dv45-subset.root

# Generate the base ntuple
../../scripts/haddcut.py \
    run2-rdx-sample.root $NTP \
    -c ./trigger_emulation_sample.yml

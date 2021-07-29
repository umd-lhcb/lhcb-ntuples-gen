#!/usr/bin/env bash

INPUT_NTP=../ntuple-RDX_l0_hadron_tos_training_sample/rdx-bdt_train_sample.root

../../lib/python/TrackerOnlyEmu/scripts/run2-rdx-l0_hadron_train_bdt.py \
    ${INPUT_NTP} None \
    --max-depth 40 \
    --debug-ntuple bdt_train_sample.root \
    --test-ntuple bdt_test_sample.root

plotbr \
    -n bdt_train_sample.root/TupleB0/DecayTree -b d0_et_trg_pred_diff \
    -n bdt_test_sample.root/TupleB0/DecayTree -b d0_et_trg_pred_diff \
    --normalize \
    -XD -2000 2000 \
    -l "Train sample" -l "Test sample" \
    -XL "Emulation resolution" -YL "Normalized" \
    -o d0_et_emu_resolution_over_train.png

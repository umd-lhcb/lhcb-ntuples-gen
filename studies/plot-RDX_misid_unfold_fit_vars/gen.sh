#!/usr/bin/env bash

echo "Run 'make rdx-ntuple-run2-mu_misid' first to generate required files."

shopt -s nullglob
NTP_D0=(../../gen/rdx-ntuple-run2-mu_misid/ntuple_merged/D0--*.root)

./plot_fit_vars.py -o . -i "${list[@]}"

#!/usr/bin/env bash
#
# Note: Run this on lxplus!

declare -A SAMPLES
SAMPLES[K]="DLLK > 4"
SAMPLES[Pi]="DLLK < 2"
SAMPLES[Mu]="DLLmu > -200"

for part in "${!SAMPLES[@]}"; do
    lb-conda pidcalib pidcalib2.make_eff_hists \
        --output-dir pidcalib_output \
        --sample Turbo16 --magnet down \
        --particle ${part} --pid-cut ${SAMPLES[${part}]} \
        --bin-var P --bin-var ETA

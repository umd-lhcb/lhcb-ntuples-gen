#!/usr/bin/env bash
#
# Note: Run this on lxplus!

lb-conda pidcalib pidcalib2.make_eff_hists \
    --output-dir pidcalib_output \
    --sample Turbo16 --magnet down \
    --particle K --pid-cut "DLLK > 4.0" \
    --bin-var P --bin-var ETA \
    --max-files 3  # debug only

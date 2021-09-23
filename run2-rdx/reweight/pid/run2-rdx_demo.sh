#!/usr/bin/env bash
#
# Note: Run this on lxplus!

PARTICLE="K"
CUTS="DLLK > 4.0 & IsMuon == 0.0"


lb-conda pidcalib pidcalib2.make_eff_hists \
    --output-dir pidcalib_output \
    --sample Turbo16 --magnet down \
    --particle ${PARTICLE} --pid-cut "${CUTS}" \
    --bin-var P --bin-var ETA
    #--max-files 3  # debug only

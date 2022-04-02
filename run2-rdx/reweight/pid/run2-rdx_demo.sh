#!/usr/bin/env bash
#
# Note: Run this on lxplus!

#PARTICLE="K"
#CUTS="DLLK > 4.0 & IsMuon == 0.0"

#PARTICLE="Pi"
#CUTS="DLLK < 2.0 & IsMuon == 0.0"

PARTICLE="Mu"
#PARTICLE="Mu_nopt"
CUTS="DLLmu > 2.0 & DLLe < 1.0 & IsMuon == 1.0"

lb-conda pidcalib pidcalib2.make_eff_hists \
    --output-dir pidcalib_output \
    --sample Turbo16 --magnet down \
    --particle ${PARTICLE} --pid-cut "${CUTS}" \
    --cut "IPCHI2 > 45.0 & Brunel_TRACK_GHOSTPROB < 0.5" \
    --verbose \
    --bin-var Brunel_P --bin-var Brunel_ETA --bin-var nTracks_Brunel \
    --max-files 3  # debug only

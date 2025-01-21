#!/usr/bin/env bash
#
# Note: Run this on lxplus!

PARTICLE="Mu_nopt"
CUT="IPCHI2 > 45.0 & Brunel_TRACK_GHOSTPROB < 0.5"
PID_CUT="DLLmu > 2.0 & DLLe < 1.0 & IsMuon == 1.0"

lb-conda pidcalib pidcalib2.make_eff_hists \
    --output-dir pidcalib_output \
    --sample Turbo16 --magnet down \
    --particle ${PARTICLE} --cut "${CUT}" --pid-cut "${PID_CUT}" \
    --verbose \
    --bin-var Brunel_P --bin-var Brunel_ETA --bin-var nTracks_Brunel \
    --max-files 3  # debug only

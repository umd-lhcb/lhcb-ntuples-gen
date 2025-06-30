#!/usr/bin/env bash
#
# Note: Run this on lxplus!

declare -A PIDCUTS
# PIDCUTS[K]="DLLK > 4.0"
PIDCUTS[Mu_nopt]="DLLmu > 2.0"
declare -A CUTS
# CUTS[K]="true"
CUTS[Mu_nopt]="IsMuon==1"

for year in 16 17 18; do
    for polarity in "up" "down"; do
        for part in "${!PIDCUTS[@]}"; do
            lb-conda pidcalib pidcalib2.make_eff_hists \
                --output-dir pidcalib_output \
                --sample "Turbo${year}" --magnet ${polarity} \
                --particle ${part} --pid-cut "${PIDCUTS[${part}]}" --cut "${CUTS[${part}]}" \
                --binning-file ./binning.json \
                --bin-var Brunel_P --bin-var Brunel_ETA --bin-var nTracks_Brunel
        done
    done
done

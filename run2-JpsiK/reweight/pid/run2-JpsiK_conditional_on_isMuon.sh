#!/usr/bin/env bash
#
# Note: Run this on lxplus!

declare -A SAMPLES
SAMPLES[Mu_nopt]="DLLmu > 2.0"
declare -A CONDITIONALS
CONDITIONALS[Mu_nopt]="isMuon == 1"

for year in 16 17 18; do
    for polarity in "up" "down"; do
        for part in "${!SAMPLES[@]}"; do
            lb-conda pidcalib pidcalib2.make_eff_hists \
                --output-dir pidcalib_output \
                --sample "Turbo${year}" --magnet ${polarity} \
                --particle ${part} --pid-cut "${SAMPLES[${part}]}" --cut "${CONDITIONALS[${part}]}" \
                --binning-file ./binning.json \
                --bin-var Brunel_P --bin-var Brunel_ETA --bin-var nTracks_Brunel
        done
    done
done

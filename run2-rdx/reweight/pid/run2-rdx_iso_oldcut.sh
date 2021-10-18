#!/usr/bin/env bash
#
# Note: Run this on lxplus!

declare -a K_CUTS=(
    "ProbNNk > 0.2"
    "ProbNNk < 0.2"
)

for year in 15 16 17 18; do
    for polarity in "up" "down"; do
        for cut in "${K_CUTS[@]}"; do
            lb-conda pidcalib pidcalib2.make_eff_hists \
                --output-dir pidcalib_output \
                --sample "Turbo${year}" --magnet ${polarity} \
                --particle K --pid-cut ${cut} \
                --bin-var Brunel_P --bin-var Brunel_ETA --bin-var nTracks_Brunel
        done
    done
done

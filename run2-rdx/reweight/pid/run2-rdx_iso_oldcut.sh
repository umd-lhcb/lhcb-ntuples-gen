#!/usr/bin/env bash
#
# Note: Run this on lxplus!

SAMPLES=("K" "Pi" "P" "Mu_nopt" "e_B_Jpsi")

declare -A CUTS
CUTS[nnk_gt]="Brunel_MC15TuneV1_ProbNNk > 0.2"

declare -A POLARITY
POLARITY[up]="mu"
POLARITY[down]="md"

for year in 16; do
    for polarity in "up" "down"; do
        for part in "${SAMPLES[@]}"; do
            for name in "${!CUTS[@]}"; do
                folder_name="run2-rdx-20${year}-${POLARITY[${polarity}]}-${part}_${name}-p_eta_ntracks_all_offline"
                echo "Output folder: ${folder_name}"
                lb-conda pidcalib pidcalib2.make_eff_hists \
                    --output-dir ${folder_name} \
                    --sample "Turbo${year}" --magnet ${polarity} \
                    --particle ${part} --pid-cut "${CUTS[${name}]}" \
                    --bin-var Brunel_P --bin-var Brunel_ETA --bin-var nTracks_Brunel \
                    --max-files 3
            done
        done
    done
done

# now rename the pkls
rm -rf pkl-run2-rdx_iso_oldcut
mkdir -p pkl-run2-rdx_iso_oldcut

for pkl in ./*/*.pkl; do
    new_name="$(basename $(dirname $pkl)).pkl"
    echo "Renaming $pkl to pkl-run2-rdx_iso_oldcut/${new_name}..."
    cp $pkl pkl-run2-rdx_iso_oldcut/${new_name}

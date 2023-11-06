#!/usr/bin/env bash
#
# Note: Run this on lxplus!

SAMPLES=("K" "Pi" "P" "Mu_nopt" "e_B_Jpsi")

declare -A CUTS
CUTS[nnk_gt]="Brunel_MC15TuneV1_ProbNNk > 0.2 & Brunel_MC15TuneV1_ProbNNghost < 0.3"

declare -A POLARITY
POLARITY[up]="mu"
POLARITY[down]="md"

declare -A PREFIX
PREFIX[K]="Turbo"
PREFIX[Pi]="Turbo"
PREFIX[P]="Turbo"
PREFIX[Mu_nopt]="Turbo"
PREFIX[e_B_Jpsi]="Electron"

declare -A NTRACKS_ALIAS
NTRACKS_ALIAS[K]="nTracks_Brunel"
NTRACKS_ALIAS[Pi]="nTracks_Brunel"
NTRACKS_ALIAS[P]="nTracks_Brunel"
NTRACKS_ALIAS[Mu_nopt]="nTracks_Brunel"
NTRACKS_ALIAS[e_B_Jpsi]="nTracks"

rm -rf pidcalib_iso_oldcut

for year in 16; do
    for polarity in "up" "down"; do
        for part in "${SAMPLES[@]}"; do
            for name in "${!CUTS[@]}"; do
                folder_name="pidcalib_iso_oldcut/run2-rdx-20${year}-${POLARITY[${polarity}]}-${part}_${name}-p_eta_ntracks"
                echo "Output folder: ${folder_name}"
                lb-conda pidcalib pidcalib2.make_eff_hists \
                    --output-dir ${folder_name} \
                    --sample "${PREFIX[${part}]}${year}" --magnet ${polarity} \
                    --particle ${part} --pid-cut "${CUTS[${name}]}" \
                    --bin-var Brunel_P --bin-var Brunel_ETA --bin-var "${NTRACKS_ALIAS[${part}]}" \
                    --binning-file ./binning.json
            done
        done
    done
done

# now rename the pkls
rm -rf pkl-run2-rdx_iso_oldcut
mkdir -p pkl-run2-rdx_iso_oldcut

for pkl in ./pidcalib_iso_oldcut/*/*.pkl; do
    new_name="$(basename $(dirname ${pkl})).pkl"
    echo "Renaming $pkl to pkl-run2-rdx_iso_oldcut/${new_name}..."
    cp ${pkl} pkl-run2-rdx_iso_oldcut/${new_name}
done

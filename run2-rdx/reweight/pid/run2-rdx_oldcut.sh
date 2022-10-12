#!/usr/bin/env bash
#
# Note: Run this on lxplus!

declare -A SAMPLES
SAMPLES[K]="DLLK > 4.0 & IsMuon == 0.0"
SAMPLES[Pi]="DLLK < 2.0 & IsMuon == 0.0"
# SAMPLES[Mu]="DLLmu > 2.0 & DLLe < 1.0 & IsMuon == 1.0"
# SAMPLES[Mu_nopt]="DLLmu > 2.0 & DLLe < 1.0 & IsMuon == 1.0"

rm -rf pidcalib_oldcut

for year in 16; do
    for polarity in "up" "down"; do
        for part in "${!SAMPLES[@]}"; do
            folder_name="pidcalib_oldcut/run2-rdx-20${year}-${POLARITY[${polarity}]}-${part}-p_eta_ntracks"
            echo "Output folder: ${folder_name}"
            lb-conda pidcalib pidcalib2.make_eff_hists \
                --output-dir ${folder_name} \
                --sample "Turbo${year}" --magnet ${polarity} \
                --particle ${part} --pid-cut "${SAMPLES[${part}]}" \
                --bin-var Brunel_P --bin-var Brunel_ETA --bin-var nTracks_Brunel \
                --binning-file ./binning.json
        done
    done
done


# now rename the pkls
rm -rf pkl-run2-rdx_oldcut
mkdir -p pkl-run2-rdx_oldcut

for pkl in ./pidcalib_oldcut/*/*.pkl; do
    new_name="$(basename $(dirname ${pkl})).pkl"
    echo "Renaming $pkl to pkl-run2-rdx_oldcut/${new_name}..."
    cp ${pkl} pkl-run2-rdx_oldcut/${new_name}
done

#!/usr/bin/env bash
#
# Note: Run this on lxplus!

declare -A SAMPLES
SAMPLES[K]="DLLK > 4.0"
SAMPLES[Mu_nopt]="DLLmu > 2.0 & IsMuon == 1"

declare -A POLARITY
POLARITY[up]="mu"
POLARITY[down]="md"

if [ -d "pidcalib_withIsMuon" ]; then
    rm -r pidcalib_withIsMuon
fi

for year in 16 17 18; do
    for polarity in "up" "down"; do
        for part in "${!SAMPLES[@]}"; do
            folder_name="pidcalib_withIsMuon/run2-JpsiK-20${year}-${POLARITY[${polarity}]}-${part}-p_eta_ntracks"
            echo "Output folder: ${folder_name}"
            lb-conda pidcalib pidcalib2.make_eff_hists \
                --output-dir ${folder_name} \
                --sample "Turbo${year}" --magnet ${polarity} \
                --particle ${part} --pid-cut "${SAMPLES[${part}]}" \
                --binning-file ./binning.json \
                --bin-var Brunel_P --bin-var Brunel_ETA --bin-var nTracks_Brunel
        done
    done
done

# now rename the pkls
if [ -d "pkl-run2-JpsiK_withIsMuon" ]; then
    rm -r pkl-run2-JpsiK_withIsMuon
fi
mkdir -p pkl-run2-JpsiK_withIsMuon

for pkl in ./pidcalib_withIsMuon/*/*.pkl; do
    new_name="$(basename $(dirname ${pkl})).pkl"
    echo "Renaming $pkl to pkl-run2-JpsiK_withIsMuon/${new_name}..."
    cp ${pkl} pkl-run2-JpsiK_withIsMuon/${new_name}
done

rm -r pidcalib_withIsMuon

# Convert pkls to root
for pkl in ./pkl-run2-JpsiK_withIsMuon/*.pkl; do
    echo "Converting $pkl to root..."
    lb-conda pidcalib pidcalib2.pklhisto2root "${pkl}"
done

# Move root files to separate directory
if [ -d "root-run2-JpsiK_withIsMuon-tmp" ]; then
    rm -r root-run2-JpsiK_withIsMuon-tmp
fi
mkdir -p root-run2-JpsiK_withIsMuon-tmp

mv ./pkl-run2-JpsiK_withIsMuon/*.root ./root-run2-JpsiK_withIsMuon-tmp/

# Shift efficiencies
if [ -d "root-run2-JpsiK_withIsMuon-shifted-tmp" ]; then
    rm -r root-run2-JpsiK_withIsMuon-shifted-tmp
fi
mkdir -p root-run2-JpsiK_withIsMuon-shifted-tmp

lb-conda pidcalib ../../../scripts/shift_histo_efficiencies.py ./root-run2-JpsiK_withIsMuon-tmp ./root-run2-JpsiK_withIsMuon-shifted-tmp

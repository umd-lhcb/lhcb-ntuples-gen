#!/usr/bin/env bash
#
# Note: Run this on lxplus!

declare -A SAMPLES
SAMPLES[K]="DLLK > 4.0 & IsMuon == 0.0"
SAMPLES[Pi]="DLLK < 2.0 & IsMuon == 0.0"

declare -A POLARITY
POLARITY[up]="mu"
POLARITY[down]="md"

if [ -d "pidcalib_oldcut" ]; then
    rm -r pidcalib_oldcut
fi

for year in 16; do
    for polarity in "up" "down"; do
        for part in "${!SAMPLES[@]}"; do
            folder_name="pidcalib_oldcut/run2-rdx-20${year}-${POLARITY[${polarity}]}-${part}-p_eta_ntracks"
            echo "Output folder: ${folder_name}"
            lb-conda pidcalib pidcalib2.make_eff_hists \
                --output-dir ${folder_name} \
                --sample "Turbo${year}" --magnet ${polarity} \
                --particle ${part} --pid-cut "${SAMPLES[${part}]}" --cut "InMuonAcc == 1.0"\
                --bin-var Brunel_P --bin-var Brunel_ETA --bin-var nTracks_Brunel \
                --binning-file ./binning.json
        done
    done
done

# now rename the pkls
if [ -d "pkl-run2-rdx_oldcut" ]; then
    rm -r pkl-run2-rdx_oldcut
fi
mkdir -p pkl-run2-rdx_oldcut

for pkl in ./pidcalib_oldcut/*/*.pkl; do
    new_name="$(basename $(dirname ${pkl})).pkl"
    echo "Renaming $pkl to pkl-run2-rdx_oldcut/${new_name}..."
    cp ${pkl} pkl-run2-rdx_oldcut/${new_name}
done

rm -r pidcalib_oldcut

# Convert pkls to root
for pkl in ./pkl-run2-rdx_oldcut/*.pkl; do
    echo "Converting $pkl to root..."
    lb-conda pidcalib pidcalib2.pklhisto2root "${pkl}"
done

# Move root files to separate directory
if [ -d "root-run2-rdx_oldcut-tmp" ]; then
    rm -r root-run2-rdx_oldcut-tmp
fi
mkdir -p root-run2-rdx_oldcut-tmp

mv ./pkl-run2-rdx_oldcut/*.root ./root-run2-rdx_oldcut-tmp/

# Shift efficiencies
if [ -d "root-run2-rdx_oldcut-shifted-tmp" ]; then
    rm -r root-run2-rdx_oldcut-shifted-tmp
fi
mkdir -p root-run2-rdx_oldcut-shifted-tmp

lb-conda pidcalib ../../../scripts/shift_histo_efficiencies.py ./root-run2-rdx_oldcut-tmp ./root-run2-rdx_oldcut-shifted-tmp

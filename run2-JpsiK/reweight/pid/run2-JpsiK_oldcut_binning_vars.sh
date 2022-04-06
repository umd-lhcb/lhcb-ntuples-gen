#!/usr/bin/env bash

lb-conda pidcalib pidcalib2.plot_calib_distributions \
    --sample Turbo16 --magnet down --particle K \
    --bin-var Brunel_P --binning ./binning.json
lb-conda pidcalib pidcalib2.plot_calib_distributions \
    --sample Turbo16 --magnet down --particle Mu_nopt \
    --bin-var Brunel_P --binning ./binning.json

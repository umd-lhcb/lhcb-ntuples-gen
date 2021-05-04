#!/usr/bin/env bash

./selection_efficiency.py \
    ../../ntuples/0.9.3-production_for_validation/Dst_D0-mc/*.root \
    -r ../../archive/21_04_30/scripts/comparison-RDX_selection_efficiency/mc_on_dirac.csv \
    -O 12573012 11574021 12773410 12573001 11574011 12773400 11874430 11874440 \
       12873450 12873460 12675011 11674401 12675402 11676012 12875440 13874020 \
       13674000 11894600 11894200 12893600 12893610 11894610 11894210 12895400 \
       12895000

#!/usr/bin/env bash

# 2016
plotbr -o 2016_md_ws_pi.png -n \
    ../../ntuples/0.9.6-2016_production/Dst_D0-std/Dst_D0--22_02_07--std--LHCb_Collision16_Beam6500GeV-VeloClosed-MagDown_Real_Data_Reco16_Stripping28r2_90000000_SEMILEPTONIC.DST/*dv.root/TupleB0WSPi/DecayTree \
    -b "dst_M - d0_M" -XL "deltaM [MeV]" --title "2016 MagDown, WS Pi" \
    -l deltaM -XD 138 164

#!/usr/bin/env bash

# 2016, std
plotbr -o 2016_std_md_ws_pi.png -n \
    ../../ntuples/0.9.6-2016_production/Dst_D0-std/Dst_D0--22_02_07--std--LHCb_Collision16_Beam6500GeV-VeloClosed-MagDown_Real_Data_Reco16_Stripping28r2_90000000_SEMILEPTONIC.DST/*dv.root/TupleB0WSPi/DecayTree \
    -b "dst_M - d0_M" -XL "deltaM [MeV]" --title "2016 std, MD, WS Pi" \
    -l deltaM -XD 139 159.5

plotbr -o 2016_std_md_rs.png -n \
    ../../ntuples/0.9.6-2016_production/Dst_D0-std/Dst_D0--22_02_07--std--LHCb_Collision16_Beam6500GeV-VeloClosed-MagDown_Real_Data_Reco16_Stripping28r2_90000000_SEMILEPTONIC.DST/*dv.root/TupleB0/DecayTree \
    -b "dst_M - d0_M" -XL "deltaM [MeV]" --title "2016 std, MD, RS" \
    -l deltaM -XD 139 159.5

# 2016, misID
plotbr -o 2016_mu_misid_md_ws_pi.png -n \
    ../../ntuples/0.9.6-2016_production/Dst_D0-mu_misid/Dst_D0--22_03_01--mu_misid--LHCb_Collision16_Beam6500GeV-VeloClosed-MagDown_Real_Data_Reco16_Stripping28r2_90000000_SEMILEPTONIC.DST/*dv.root/TupleB0WSPi/DecayTree \
    -b "dst_M - d0_M" -XL "deltaM [MeV]" --title "2016 misID, MD, WS Pi" \
    -l deltaM -XD 139 159.5

plotbr -o 2016_mu_misid_md_rs.png -n \
    ../../ntuples/0.9.6-2016_production/Dst_D0-mu_misid/Dst_D0--22_03_01--mu_misid--LHCb_Collision16_Beam6500GeV-VeloClosed-MagDown_Real_Data_Reco16_Stripping28r2_90000000_SEMILEPTONIC.DST/*dv.root/TupleB0/DecayTree \
    -b "dst_M - d0_M" -XL "deltaM [MeV]" --title "2016 misID, MD, RS" \
    -l deltaM -XD 139 159.5

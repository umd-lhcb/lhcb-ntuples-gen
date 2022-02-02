#!/usr/bin/env python
#
# Description: Plot the P-ETA histograms for tracks that have tracking weights

import sys
import os

from os.path import isdir
from glob import glob


###########
# Helpers #
###########

def checkFolderExist(folder, cmd):
    if not isdir(folder):
        print(f'The ntuple folder {ntpInFolder} does not exist!')
        print(f'Run "{cmd}" in project root to generate the ntuples first!')
        sys.exit(1)


checkFolderExist('../../gen/ref-rdx-ntuple-run1-data-Dst-comp',
                 'ref-rdx-ntuple-run1-data-Dst-comp')
checkFolderExist('../../gen/rdx-ntuple-run1-data-Dst-comp',
                 'ref-rdx-ntuple-run1-data-Dst-comp')


ntpPhoebe = glob('../../gen/ref-rdx-ntuple-run1-data-Dst-comp/ntuple/Dst_data_2011_md--*.root')[0]
ntpUs = glob('../../gen/rdx-ntuple-run1-data-Dst-comp/ntuple/Dst_us--*.root')[0]

ntpPhoebeStep1 = '../../ntuples/ref-rdx-run1/Dst-std/Dst--20_09_16--std--data--2011--md--phoebe.root'
ntpUsStep1 = '../../ntuples/0.9.5-bugfix/Dst_D0-std/Dst_D0--21_10_07--std--LHCb_Collision11_Beam3500GeV-VeloClosed-MagDown_Real_Data_Reco14_Stripping21r1_90000000_SEMILEPTONIC.DST.root'


#########
# Plots #
#########

def runCmd(cmd):
    print('  \033[92m'+cmd+'\033[0m')
    os.system(cmd)


runCmd(fr'''
    plotbr -n {ntpPhoebe}/tree -b d0_m -n {ntpUs}/tree -b d0_m \
        -l Phoebe -l Us -o d0_m.png \
        --bins 80 -XD 1780 1940 \
        --title "\$D^0$ mass window: [1842.09, 1888.89]" \
        -XL "\$D^0$ mass [MeV]" \
        --vlines "1842.09,0,40000,crimson" "1888.89,0,40000,crimson"
    ''')

runCmd(fr'''
    plotbr -n {ntpPhoebe}/tree -b dst_m -n {ntpUs}/tree -b dst_m \
        -l Phoebe -l Us -o dst_m.png \
        --bins 80 -XD 1920 2080 \
        --title "\$m_{{D^*}} -m_{{D^0}} - 145.454 < 2$: ~ [1985, 2037]" \
        -XL "\$D^*$ mass [MeV]" \
        --vlines "1985,0,40000,crimson" "2037,0,40000,crimson"
    ''')

runCmd(fr'''
    plotbr -n {ntpPhoebe}/tree -b="dst_m-d0_m" -n {ntpUs}/tree -b "dst_m-d0_m" \
        -l Phoebe -l Us -o dst_d0_delta_m.png \
        --bins 60 -XD 139 161 \
        --title "\$m_{{D^*}} -m_{{D^0}} - 145.454 < 2$: [-143.454, 147.454]" \
        -XL "\$m_{{D^*}} -m_{{D^0}}$ [MeV]" \
        --vlines "143.454,0,40000,crimson" "147.454,0,40000,crimson"
    ''')

runCmd(fr'''
    plotbr -n {ntpPhoebeStep1}/YCandsWS/DecayTree -b="muplus_PIDmu" \
        -n {ntpUsStep1}/TupleB0WSMu/DecayTree -b "mu_PIDmu" \
        -l Phoebe -l Us -o mu_pidmu_ws.png \
        --bins 60 \
        --title "\$\\mu$ PID\$\\mu$, WS \$\\mu$"
    ''')

runCmd(fr'''
    plotbr -n {ntpPhoebeStep1}/YCandsWS/DecayTree -b="Dst_2010_minus_ENDVERTEX_CHI2/Dst_2010_minus_ENDVERTEX_NDOF" \
        -n {ntpUsStep1}/TupleB0WSMu/DecayTree -b "dst_ENDVERTEX_CHI2/dst_ENDVERTEX_NDOF" \
        -l Phoebe -l Us -o dst_chi2ndof_ws.png \
        --bins 60 \
        --title "\$D^*$ \$\\chi^2/dof$, WS \$\\mu$" \
        --vlines "6,0,40000,crimson"
    ''')

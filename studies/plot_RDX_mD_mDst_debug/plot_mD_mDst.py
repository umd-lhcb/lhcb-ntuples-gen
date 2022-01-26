#!/usr/bin/env python
#
# Description: Plot the P-ETA histograms for tracks that have tracking weights

import sys
import os

from os.path import isdir


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


ntpPhoebe = '../../gen/ref-rdx-ntuple-run1-data-Dst-comp/ntuple/Dst_data_2011_md--22_01_25--mix--all--2011-2012--md-mu--phoebe.root'
ntpUs = '../../gen/rdx-ntuple-run1-data-Dst-comp/ntuple/Dst_us--22_01_25--std--data--2011--md.root'


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
        --title "\$m_{{D^*}} -m_{{D^0}} - 145.454 < 2$, ~ [1985, 2037]" \
        -XL "\$D^*$ mass [MeV]" \
        --vlines "1985,0,40000,crimson" "2037,0,40000,crimson"
    ''')

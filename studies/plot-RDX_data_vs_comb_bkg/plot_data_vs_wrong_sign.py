#!/usr/bin/env python
#
# Description: Plot D meson mass w/o mass window cuts

import os
import sys

from os.path import isdir
from glob import glob
from matplotlib.patches import Rectangle

from pyTuplingUtils.io import read_branches
from pyTuplingUtils.plot import plot_top


###########
# Helpers #
###########

def runCmd(cmd):
    print('  \033[92m'+cmd+'\033[0m')
    os.system(cmd)


def testIfFolderExists(makeRule):
    folder = f'../../gen/{makeRule}'
    if not isdir(folder):
        print(f'The ntuple folder {folder} does not exist!')
        print(f'Run "make {makeRule}" in project root to generate the ntuples first!')
        sys.exit(1)
    return folder


ntpD0InFolder = testIfFolderExists('ref-rdx-ntuple-run1-data-D0')
ntpDstInFolder = testIfFolderExists('ref-rdx-ntuple-run1-data-Dst')

ntpD0InData = glob(f'{ntpD0InFolder}/ntuple/D0_data--*.root')[0]
ntpD0InComb = glob(f'{ntpD0InFolder}/ntuple/D0_comb--*.root')[0]

ntpDstInData = glob(f'{ntpDstInFolder}/ntuple/Dst_data--*.root')[0]
ntpDstInComb = glob(f'{ntpDstInFolder}/ntuple/Dst_comb--*.root')[0]


#########
# Plots #
#########

def plotBMass(ntpData, ntpComb, output, br='b_m',
              title=r'\$D^0$ tree', xlabel=r'\$m_{B}$ [MeV]',
              xRange='2000 10000', yscale='linear'):
    cmd = fr'''plotbr -o {output} --title "{title}" -XL "{xlabel}" -XD {xRange} --yscale {yscale} \
    -n {ntpData}/tree -b "{br}" --cuts "mu_ubdt_ok & d_mass_window_ok & is_iso" \
    -l "right-sign, all" \
    -n {ntpComb}/tree -b "{br}" "{br}" "{br}" \
    --cuts "mu_ubdt_ok & d_mass_window_ok & is_iso" "mu_ubdt_ok & is_normal & d_mass_window_ok & is_iso" "mu_ubdt_ok & is_sb & d_mass_window_ok & is_iso" \
    -l "wrong-sign, all" "wrong-sign, normal" "wrong-sign, SB" \
    --bins 60
'''
    runCmd(cmd)


plotBMass(ntpD0InData, ntpD0InComb, 'D0_B_mass_data_vs_comb.png')
plotBMass(ntpD0InData, ntpD0InComb, 'D0_B_mass_data_vs_comb_log.png',
          yscale='log')

plotBMass(ntpDstInData, ntpDstInComb, 'Dst_B_mass_data_vs_comb.png',
          'b0_m', r'\$D^*$ tree', r'\$m_{B^0}$ [MeV]')
plotBMass(ntpDstInData, ntpDstInComb, 'Dst_B_mass_data_vs_comb_log.png',
          'b0_m', r'\$D^*$ tree', r'\$m_{B^0}$ [MeV]', yscale='log')

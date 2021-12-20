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

ntpD0In = glob(f'{ntpD0InFolder}/ntuple/D0_data--*.root')[0]
ntpDstIn = glob(f'{ntpDstInFolder}/ntuple/Dst_data--*.root')[0]


#########
# Plots #
#########

def plotDMass(ntpIn, output, br='d0_m',
              cuts=['is_normal', 'is_normal & d_mass_window_ok'],
              labels=['w/o', 'w/ mass window cut'],
              xlabel=r'\$m_{K \\pi}$ [MeV]',
              xRange='1780 1940', yRange='0 1000000'):
    cuts = ' '.join(f'"{i}"' for i in cuts)
    labels = ' '.join(f'"{i}"' for i in labels)

    cmd = f'plotbr -n {ntpIn}/tree -b "{br}" "{br}" -o {output} --labels {labels} -XL "{xlabel}" --cuts {cuts} -XD {xRange} -YD {yRange}'
    runCmd(cmd)


plotDMass(ntpD0In, 'D0_KPi_mass_no_mass_window_cut.png')
plotDMass(ntpDstIn, 'Dst_KPi_mass_no_mass_window_cut.png', 'd0_m',
          yRange='0 280000')
plotDMass(ntpDstIn, 'Dst_KPiPislow_mass_no_mass_window_cut.png', 'dst_m - d0_m',
          xlabel=r'\$m_{K \\pi \\pi_{slow}} -m_{K \\pi}$ [MeV]',
          xRange='140 190', yRange='0 540000')

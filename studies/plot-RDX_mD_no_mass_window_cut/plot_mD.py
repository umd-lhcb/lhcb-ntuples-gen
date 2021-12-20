#!/usr/bin/env python
#
# Description: Plot D meson mass w/o mass window cuts

import sys
import uproot

from os.path import isdir
from glob import glob
from matplotlib.patches import Rectangle

from pyTuplingUtils.io import read_branches
from pyTuplingUtils.plot import plot_top


###########
# Helpers #
###########

ntpD0InFolder = '../../gen/ref-rdx-ntuple-run1-data-D0-comp'
ntpDstInFolder = '../../gen/ref-rdx-ntuple-run1-data-Dst-comp'


def testIfFolderExists(folder, makeRule):
    if not isdir(folder):
        print(f'The ntuple folder {folder} does not exist!')
        print(f'Run "{makeRule}" in project root to generate the ntuples first!')
        sys.exit(1)


testIfFolderExists(ntpD0InFolder, 'ref-rdx-ntuple-run1-data-D0-comp')
testIfFolderExists(ntpDstInFolder, 'ref-rdx-ntuple-run1-data-Dst-comp')


ntpD0In = glob(f'{ntpD0InFolder}/ntuple/D0_data--*.root')[0]
ntpDstIn = glob(f'{ntpDstInFolder}/ntuple/Dst_data--*.root')[0]

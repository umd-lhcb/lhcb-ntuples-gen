#!/usr/bin/env python
#
# Description: Plot the P-ETA histograms for tracks that have tracking weights

import os
import sys
import uproot
import numpy as np
import mplhep as hep

from os.path import isdir
from glob import glob

from pyTuplingUtils.io import read_branches

from pyTuplingUtils.plot import (
    plot_top, plot_hist2d,
    ax_add_args_hist2d
)


###########
# Helpers #
###########

def runCmd(cmd):
    print('  \033[92m'+cmd+'\033[0m')
    os.system(cmd)


ntpInFolder = '../../gen/rdx-ntuple-run2-mc-demo'

if not isdir(ntpInFolder):
    print(f'The ntuple folder {ntpInFolder} does not exist!')
    print('Run "make rdx-ntuple-run2-mc-demo" in project root to generate the ntuples first!')
    sys.exit(1)

ntpsIn = glob(f'{ntpInFolder}/ntuple/*.root')


#########
# Plots #
#########

def plotPEta(brP, brEta, output, title, binning=None,
             xlabel=r'$p$', ylabel=r'$\eta$'):
    top_plotters = []

    # The main histo plot
    histoArgs = ax_add_args_hist2d(binning)
    top_plotters.append(
        lambda fig, ax, x=brP, y=brEta, add=histoArgs:
        plot_hist2d(x, y, add, figure=fig, axis=ax, show_legend=False)
    )

    # Plot
    fig, *_ = plot_top(top_plotters, title=title, xlabel=xlabel, ylabel=ylabel)
    fig.savefig(output)


plotRange = [
    [0, 5e3, 10e3, 20e3, 40e3, 100e3, 200e3],  # P
    [0, 1.9, 3.2, 4.9, 5.5],  # ETA
]

plotScheme = {
    'Dst': {
        'spi': {
            'title': r'slow $\pi$ - $p$ vs. $\eta$'
        }
    },
}


for ntpName in ntpsIn:
    hep.style.use('LHCb2')
    ntp = uproot.open(ntpName)

    for treeId, scheme in plotScheme.items():
        if treeId in ntpName:
            for part in scheme:
                brP, brEta = read_branches(
                    ntp, 'tree', [f'{part}_p', f'{part}_eta'])

                plotPEta(brP, brEta, f'{treeId}_{part}_p_eta.png',
                         binning=plotRange, **scheme[part])
            break

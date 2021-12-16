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
from matplotlib.patches import Rectangle

from pyTuplingUtils.io import read_branches
from pyTuplingUtils.plot import plot_top


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

def genHist2D(x, y, bins):
    counts, *_ = np.histogram2d(x, y, bins=bins)
    return counts


def plotColorMesh(fig, ax, x, y, bins, colorbarLabel='Number of events'):
    histo = genHist2D(x, y, bins)
    mesh = ax.pcolormesh(bins[0], bins[1], histo.T, cmap='YlOrRd')
    cb = fig.colorbar(mesh, ax=ax)
    cb.set_label(colorbarLabel)


def plotPEta(brP, brEta, output, title, binning=None,
             xlabel=r'$p$ [GeV]', ylabel=r'$\eta$',
             rectAnchor=(5, 1.9), rectWidth=195, rectHeight=3):
    top_plotters = []

    # The main histo plot
    top_plotters.append(
        lambda fig, ax: plotColorMesh(fig, ax, brP, brEta, binning)
    )

    # Draw a rectangle indicating the region the efficiency covers
    top_plotters.append(
        lambda fig, ax: ax.add_patch(
            Rectangle(rectAnchor, rectWidth, rectHeight,
                      fc='none', color='black', linewidth=4, linestyle='dashed')
        )
    )

    # Plot
    fig, ax = plot_top(top_plotters, title=title, xlabel=xlabel, ylabel=ylabel)
    ax.set_xscale('log')
    fig.savefig(output)


plotRange = [
    [0, 5, 10, 20, 40, 100, 200],  # P, GeV
    [1.5, 1.9, 3.2, 4.9, 5.5],  # ETA
]

plotScheme = {
    'Dst': {
        'k': {'title': r'$K$'},
        'pi': {'title': r'$\pi$'},
        'mu': {'title': r'$\mu$'},
        'spi': {'title': r'slow $\pi$'},
    },
    'D0': {
        'k': {'title': r'$K$'},
        'pi': {'title': r'$\pi$'},
        'mu': {'title': r'$\mu$'},
    },
}

plotTitleAddOn = {
    'Dst': r'$D^{*}$ tree',
    'D0': r'$D^{0}$ tree',
}


for ntpName in ntpsIn:
    hep.style.use('LHCb2')
    ntp = uproot.open(ntpName)

    for treeId, scheme in plotScheme.items():
        if treeId in ntpName:
            for part in scheme:
                brP, brEta, brWt = read_branches(
                    ntp, 'tree', [f'{part}_p', f'{part}_eta', f'wtrk_{part}'])

                effRatio = f', {plotTitleAddOn[treeId]}, tracking eff: {brWt.sum() / brWt.size:.2f}'

                plotPEta(brP, brEta, f'{treeId}_{part}_p_eta.png',
                         binning=plotRange,
                         title=scheme[part]['title']+effRatio)
            break

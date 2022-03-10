#!/usr/bin/env python
#
# Description: Plot J/psi K variables before/after reweighting

import numpy as np
import mplhep as hep
import uproot

from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.plot import (
    plot_step, plot_histo,
    ax_add_args_step, ax_add_args_histo
)


#################
# Configurables #
#################

mcNtps = [
    '../../ntuples/0.9.6-2016_production/JpsiK-mc-step2/JpsiK--22_03_10--mc--12143001--2016--md.root:tree',
    '../../ntuples/0.9.6-2016_production/JpsiK-mc-step2/JpsiK--22_03_10--mc--12143001--2016--mu.root:tree',
]

dataNtps = '../../run2-JpsiK/fit/fit_results/JpsiK-22_02_26_23_52-std-fit-2016/fit.root:tree'

#########
# Plots #
#########

varsToComp = ['b_ownpv_ndof', 'ntracks', 'b_pt', 'b_eta']
weightBrs = ['wpid', 'wtrk', 'w', 'wjk_kin', 'wjk_occ']
sweightBrs = ['sw_sig']

varsLabels = [r'$B$ PV NDOF', r'nTracks', r'$B$ $p_T$ [MeV]', r'$B$ $\eta$']
dataRanges = [[1, 200], [0, 450], [0, 25e3], [2, 5]]
binnings = [20, 20, 20, 9]

dataBrs = uproot.concatenate(dataNtps, varsToComp + sweightBrs, library='np')
mcBrs = uproot.concatenate(mcNtps, varsToComp + weightBrs, library='np')

# Make numpy histogram consistent w/ ROOT's
globalCut = lambda brs: (brs['ntracks'] < 450) & (brs['b_ownpv_ndof'] < 200) & \
    (brs['b_pt'] < 25e3) & (brs['b_eta'] < 5)
dataCut = globalCut(dataBrs)
mcCut = globalCut(mcBrs)


def plot(output, br, xLabel, dataRange, bins):
    suf = ' MeV' if br == 'b_pt' else ''
    yLabel = f'Normalized / {(dataRange[1]-dataRange[0])/bins:.1f}{suf}'

    hData, hBins = gen_histo(
        dataBrs[br][dataCut], bins, data_range=dataRange,
        weights=dataBrs['sw_sig'][dataCut], density=True)
    dataStyle = ax_add_args_histo('data (sweighted)', 'cornflowerblue')
    fig, ax = plot_histo(
        hBins, hData, dataStyle, title=r'$J/\psi K$ samples',
        xlabel=xLabel, ylabel=yLabel, show_legend=False)

    wMcBefore = mcBrs['wpid']*mcBrs['wtrk']
    hMcBefore, _ = gen_histo(
        mcBrs[br][mcCut], bins, data_range=dataRange,
        weights=wMcBefore[mcCut], density=True)
    mcBeforeStyle = ax_add_args_step('MC (before)', 'black')
    plot_step(
        hBins, hMcBefore, mcBeforeStyle, show_legend=False,
        figure=fig, axis=ax)

    # w_mc_after = w_mc_before*mcBrs['wjk_occ']
    wMcAfter = mcBrs['w']
    hMcAfter, _ = gen_histo(
        mcBrs[br][mcCut], bins, data_range=dataRange,
        weights=wMcAfter[mcCut], density=True)
    mcAfterStyle = ax_add_args_step('MC (after)', 'crimson')
    plot_step(
        hBins, hMcAfter, mcAfterStyle, show_legend=False,
        figure=fig, axis=ax)

    ax.legend(numpoints=1, loc='best', frameon=True)

    fig.set_tight_layout({'pad': 0.0})
    fig.savefig(output, transparent=True)


if __name__ == '__main__':
    hep.style.use('LHCb2')

    for br, lbl, dr, bins in zip(varsToComp, varsLabels, dataRanges, binnings):
        print(f'Plotting {br}...')
        plot(br+'.pdf', br, lbl, dr, bins)
        plot(br+'.png', br, lbl, dr, bins)

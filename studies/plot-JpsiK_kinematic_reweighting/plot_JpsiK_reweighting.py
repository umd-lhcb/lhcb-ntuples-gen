#!/usr/bin/env python
#
# Description: Plot J/psi K variables before/after reweighting

import mplhep as hep
import uproot

from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.plot import (
    plot_step, plot_histo, plot_top_bot, plot_top,
    ensure_no_majortick_on_topmost,
    ax_add_args_step, ax_add_args_histo
)


#################
# Configurables #
#################

mcNtps = [
    '../../ntuples/0.9.6-2016_production/JpsiK-mc-step2/JpsiK--22_10_24--mc--12143001--2016--md.root:tree',
    '../../ntuples/0.9.6-2016_production/JpsiK-mc-step2/JpsiK--22_10_24--mc--12143001--2016--mu.root:tree',
]

dataNtps = '../../run2-JpsiK/fit/fit_results/JpsiK-22_02_26_23_52-std-fit-2016/fit.root:tree'


#########
# Plots #
#########

varsToComp = ['b_ownpv_ndof', 'ntracks', 'b_pt', 'b_eta']
weightBrs = ['wpid', 'wtrk', 'w', 'wjk_kin', 'wjk_occ']
sweightBrs = ['sw_sig']

varsLabels = [r'$B$ PV NDOF', r'nTracks', r'$B$ $p_T$ [MeV]', r'$B$ $\eta$']
dataRanges = [[1, 250], [0, 450], [0, 30e3], [2, 6]]
binnings = [20, 20, 20, 9]

dataBrs = uproot.concatenate(dataNtps, varsToComp + sweightBrs, library='np')
mcBrs = uproot.concatenate(mcNtps, varsToComp + weightBrs, library='np')

# Make numpy histogram consistent w/ ROOT's
#  globalCut = lambda brs: (brs['ntracks'] < 550) & (brs['b_ownpv_ndof'] < 200) & \
#      (brs['b_pt'] < 25e3) & (brs['b_eta'] < 5)
dataCut = True
#  mcCut = globalCut(mcBrs)
mcCut = True


def plot(output, br, xLabel, dataRange, bins, ratios=False):
    suf = ' MeV' if br == 'b_pt' else ''
    yLabel = f'Norm. / {(dataRange[1]-dataRange[0])/bins:.1f}{suf}'

    topPlotters = []
    botPlotters = []

    hData, hBins = gen_histo(
        dataBrs[br][dataCut], bins, data_range=dataRange,
        weights=dataBrs['sw_sig'][dataCut], density=True)
    dataStyle = ax_add_args_histo('data (sweighted)', 'cornflowerblue')
    topPlotters.append(
        lambda fig, ax, b=hBins, h=hData, add=dataStyle:
        plot_histo(b, h, add, figure=fig, axis=ax, show_legend=False)
    )

    wMcBefore = mcBrs['wpid']*mcBrs['wtrk']
    hMcBefore, _ = gen_histo(
        mcBrs[br][mcCut], bins, data_range=dataRange,
        weights=wMcBefore[mcCut], density=True)
    mcBeforeStyle = ax_add_args_step('MC (before)', 'black')
    topPlotters.append(
        lambda fig, ax, b=hBins, h=hMcBefore, add=mcBeforeStyle:
        plot_step(b, h, add, figure=fig, axis=ax, show_legend=False)
    )

    # w_mc_after = w_mc_before*mcBrs['wjk_occ']
    wMcAfter = mcBrs['w']
    hMcAfter, _ = gen_histo(
        mcBrs[br][mcCut], bins, data_range=dataRange,
        weights=wMcAfter[mcCut], density=True)
    mcAfterStyle = ax_add_args_step('MC (after)', 'crimson')
    topPlotters.append(
        lambda fig, ax, b=hBins, h=hMcAfter, add=mcAfterStyle:
        plot_step(b, h, add, figure=fig, axis=ax, show_legend=False)
    )

    # Compute ratio
    botPlotters.append(
        lambda fig, ax, b=hBins, h=hMcBefore / hData, add=mcBeforeStyle:
        plot_step(b, h, add, figure=fig, axis=ax, show_legend=False)
    )

    title = r'$J/\psi K$ samples'
    if ratios:
        fig, _, ax2 = plot_top_bot(
            topPlotters, botPlotters, title=title,
            xlabel=xLabel, ax1_ylabel=yLabel, ax2_ylabel='MC / data',
            legend_add_args={'numpoints': 1, 'loc': 'best', 'frameon': True}
        )
        ensure_no_majortick_on_topmost(ax2, 'linear', 0.6, 0.58, verbose=True)

    else:
        fig, *_ = plot_top(
            topPlotters, title=title,
            xlabel=xLabel, ylabel=yLabel,
            legend_add_args={'numpoints': 1, 'loc': 'best', 'frameon': True}
        )

    fig.savefig(output, transparent=False)


if __name__ == '__main__':
    hep.style.use('LHCb2')

    for br, lbl, dr, bins in zip(varsToComp, varsLabels, dataRanges, binnings):
        print(f'Plotting {br}...')
        plot(br+'.pdf', br, lbl, dr, bins)
        plot(br+'.png', br, lbl, dr, bins)

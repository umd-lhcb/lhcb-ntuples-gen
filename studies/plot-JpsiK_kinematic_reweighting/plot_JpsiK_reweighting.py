#!/usr/bin/env python
#
# Description: Plot J/psi K variables before/after reweighting

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
    '../../ntuples/0.9.6-2016_production/JpsiK-mc-step2/JpsiK--22_03_02--mc--12143001--2016--md/*.root:tree',
    '../../ntuples/0.9.6-2016_production/JpsiK-mc-step2/JpsiK--22_03_02--mc--12143001--2016--mu/*.root:tree',
]

dataNtps = '../../run2-JpsiK/fit/fit_results/JpsiK-22_02_26_23_52-std-fit/fit.root:tree'

#########
# Plots #
#########

defaultBinning = 60

varsToComp = ['b_ownpv_ndof', 'ntracks', 'b_pt', 'b_eta']
weightBrs = ['wpid', 'wtrk', 'w', 'wjk_kin']
sweightBrs = ['sw_sig']

varsLabels = [r'$B$ PV NDOF', r'nTracks', r'$B$ $p_T$ [MeV]', r'$B$ $\eta$']
dataRanges = [[1, 200], [0, 450], [0, 25e3], [2, 5]]
binnings = [20, 20, 20, 9]

dataBrs = uproot.concatenate(dataNtps, varsToComp + sweightBrs, library='np')
mcBrs = uproot.concatenate(mcNtps, varsToComp + weightBrs, library='np')

global_cut = dataBrs['ntracks'] <= 450
# global_cut = np.full(dataBrs['ntracks'].size, True, dtype=bool)


def plot(output, br, xLabel, dataRange, defaultBinning):
    suf = ' MeV' if br == 'b_pt' else ''
    yLabel = f'Normalized / {(dataRange[1]-dataRange[0])/defaultBinning:.1f}{suf}'

    h_data, h_bins = gen_histo(
        dataBrs[br][global_cut], defaultBinning, data_range=dataRange,
        weights=dataBrs['sw_sig'][global_cut], density=True)
    data_style = ax_add_args_histo('data (sweighted)', 'cornflowerblue')
    fig, ax = plot_histo(
        h_bins, h_data, data_style, title=r'$J/\psi K$ samples',
        xlabel=xLabel, ylabel=yLabel, show_legend=False
    )

    h_mc_before, _ = gen_histo(
        mcBrs[br], defaultBinning, data_range=dataRange,
        weights=mcBrs['wpid']*mcBrs['wtrk'], density=True)
    mc_before_style = ax_add_args_step('MC (before)', 'black')
    plot_step(
        h_bins, h_mc_before, mc_before_style, show_legend=False,
        figure=fig, axis=ax)

    w_mc_after = mcBrs['w']
    h_mc_after, _ = gen_histo(
        mcBrs[br], defaultBinning, data_range=dataRange, weights=w_mc_after,
        density=True)
    mc_after_style = ax_add_args_step('MC (after)', 'crimson')
    plot_step(
        h_bins, h_mc_after, mc_after_style, show_legend=False,
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

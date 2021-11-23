#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Tue Nov 23, 2021 at 03:50 AM +0100

import sys
import uproot
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  # Don't hijack argparse!

from argparse import ArgumentParser
from pyTuplingUtils.plot import (
    plot_hlines, plot_vlines, plot_top,
    ax_add_args_hlines, ax_add_args_vlines
)


#################################
# Command line arguments parser #
#################################

def parse_input(descr='plot TEfficiencies.'):
    parser = ArgumentParser(description=descr)

    parser.add_argument('ntp', help='specify input ntuple.')

    parser.add_argument('-H', '--histos',
                        nargs='+',
                        required=True,
                        help='specify histograms to plot.')

    parser.add_argument('-o', '--output',
                        required=True,
                        help='specify name of the output file.')

    parser.add_argument('--xlabel',
                        default=r'$\log(p_Z)$',
                        help='specify the x-axis label.')

    parser.add_argument('--ylabel',
                        default='Efficiency',
                        help='specify y-axis label for the top plot.')

    parser.add_argument('--yscale',
                        default='linear',
                        choices=['linear', 'log'],
                        help='specify y-axis scale for the top plot.')

    parser.add_argument('--title',
                        default=None,
                        help='specify title of the plot.')

    parser.add_argument('--ext',
                        nargs='+',
                        default=['pdf', 'png'],
                        help='specify output filetypes.')

    parser.add_argument('-l', '--legends',
                        nargs='+',
                        default=[
                            r'$B \rightarrow D* \mu \nu$',
                            r'$B \rightarrow D* \tau \nu$'
                        ],
                        help='specify legend labels.')

    parser.add_argument('--legend-loc',
                        default='best',
                        help='specify legend location.')

    parser.add_argument('--colors',
                        nargs='+',
                        default=[
                            'black', 'crimson', 'mediumblue', 'darkgoldenrod'
                        ],
                        help='specify plot colors.')

    return parser.parse_args()


###########
# Helpers #
###########

def find_binning(histo, binLbls=['x']):
    result = []

    for lbl in binLbls:
        axis = getattr(histo, f'Get{lbl.upper()}axis')()
        nbins = axis.GetNbins()
        bin_bdy = []

        for idx in range(1, nbins+1):
            bin_ctr = axis.GetBinCenter(idx)
            bin_width = axis.GetBinWidth(idx)
            bin_bdy.append(bin_ctr-bin_width/2)

        bin_bdy.append(bin_ctr+bin_width/2)
        result.append(bin_bdy)

    return result


def tefficiency_to_np_histo(histo):  # 1D TEfficiency only
    freq, intv = [], []

    ref_histo = histo.GetTotalHistogram()
    binning = np.array(find_binning(ref_histo)[0])

    for idx in range(1, binning.size):
        val = histo.GetEfficiency(idx)
        freq.append(val)
        intv.append([
            val-histo.GetEfficiencyErrorLow(idx),
            val+histo.GetEfficiencyErrorUp(idx)
        ])

    return binning, np.array(freq), np.array(list(zip(*intv)))


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()
    hep.style.use('LHCb2')

    top_plotters = []

    # Build histograms
    h_bin, h_val, h_intv = [], [], []
    ntp = ROOT.TFile.Open(args.ntp, 'READ')
    for h in args.histos:
        histo = ntp.Get(h)
        _h_bin, _h_val, _h_intv = tefficiency_to_np_histo(histo)
        h_bin.append(_h_bin)
        h_val.append(_h_val)
        h_intv.append(_h_intv)

    for bins, val, intv, clr, lbl in zip(
            h_bin, h_val, h_intv, args.colors, args.legends):
        # Horizontal lines
        hline_args = ax_add_args_hlines(lbl, clr)
        top_plotters.append(
            lambda fig, ax, b=bins, h=val, add=hline_args:
            plot_hlines(b, h, add, figure=fig, axis=ax, show_legend=False))

        # Error bar
        vline_args = ax_add_args_vlines(None, clr)
        top_plotters.append(
            lambda fig, ax, b=bins, y=intv, add=vline_args:
            plot_vlines(b, y, add, figure=fig, axis=ax, show_legend=False))

    # Now do the actual plot
    fig, *_ = plot_top(
        top_plotters,
        title=args.title,
        xlabel=args.xlabel, ylabel=args.ylabel,
        yscale=args.yscale, legend_add_args={'loc': args.legend_loc})

    for ext in args.ext:
        fig.savefig(args.output + '.' + ext)

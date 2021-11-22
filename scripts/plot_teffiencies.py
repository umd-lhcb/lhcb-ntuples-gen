#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Mon Nov 22, 2021 at 05:03 PM +0100

import sys
import uproot
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  # Don't hijack argparse!

from argparse import ArgumentParser
from pyTuplingUtils.plot import (
    plot_step, plot_fill, plot_top,
    ax_add_args_step, ax_add_args_fill
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
        result.append(list(axis.GetXbins()))

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
        step_args = ax_add_args_step(lbl, clr)
        top_plotters.append(
            lambda fig, ax, b=bins, h=val, add=step_args:
            plot_step(b, h, add, figure=fig, axis=ax, show_legend=False))

        # Error bar
        fill_args = ax_add_args_fill(clr, alpha=0.4)
        top_plotters.append(
            lambda fig, ax, b=bins, y=intv, add=fill_args:
            plot_fill(b, y, add, figure=fig, axis=ax, show_legend=False))

    # Now do the actual plot
    fig, *_ = plot_top(
        top_plotters,
        title=args.title,
        xlabel=args.xlabel, ylabel=args.ylabel,
        yscale=args.yscale)

    for ext in args.ext:
        fig.savefig(args.output + '.' + ext)

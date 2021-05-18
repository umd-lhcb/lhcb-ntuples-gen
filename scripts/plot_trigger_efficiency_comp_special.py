#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Tue May 18, 2021 at 07:07 PM +0200

import uproot
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from numpy import logical_and as AND
from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.io import read_branches, read_branch
from pyTuplingUtils.plot import plot_errorbar, plot_step
from pyTuplingUtils.plot import ax_add_args_errorbar as errorbar_style
from pyTuplingUtils.plot import ax_add_args_step as step_style

from plot_trigger_efficiency_comp import parse_input as parent_parse_input
from plot_trigger_efficiency_comp import div_with_confint


#################################
# Command line arguments parser #
#################################

DESCR = '''
generate trigger efficiency comparison plots with step plots and no ratio.
'''


def parse_input(descr=DESCR):
    parser = parent_parse_input(descr)

    parser.add_argument('--output-suffix', default='step', help='''
specify output filename suffix.''')

    return parser


########
# Main #
########

if __name__ == '__main__':
    args = parse_input().parse_args()
    hep.set_style('LHCb2')

    ntp = uproot.open(args.ref)

    # Load trigger branches that we cut on
    if args.cuts:
        cut = read_branches(ntp, args.ref_tree, args.cuts)
        if len(cut) > 1:
            cut = AND(cut)
        else:
            cut = cut[0]
    else:
        evt_num = read_branch(ntp, args.ref_tree, 'runNumber')
        cut = np.array([True]*evt_num.size)

    # Load trigger branches that will be used for efficiency comparison
    eff_branches = []
    for br in args.triggers:
        raw = read_branch(ntp, args.ref_tree, br)
        filtered = raw[cut]
        eff_branches.append(filtered)

    # Now generate efficiency plots regarding some kinematic variables
    for br, data_range, xlabel in zip(
            args.kinematic_vars, args.data_range, args.xlabel):
        raw = read_branch(ntp, args.ref_tree, br)
        filtered = raw[cut]
        histos = []
        styles = []
        first = True

        for tr_br, color, legend in zip(
                eff_branches, args.colors, args.legends):
            histo_orig, bins = gen_histo(
                filtered, bins=args.bins, data_range=data_range)
            histo_weighted, bins = gen_histo(
                filtered, bins=args.bins, data_range=data_range,
                weights=tr_br.astype(np.double))

            histo, error = div_with_confint(histo_weighted, histo_orig)
            histos.append(histo)

            if first:
                styles.append(errorbar_style(legend, color, yerr=error))
                first = False
            else:
                styles.append(step_style(legend, color))

        for ext in args.ext:
            filename = '_'.join([
                args.output_prefix, args.title.replace(' ', '_'), br,
                args.output_suffix]) + \
                '.' + ext

            # The first trigger is plotted as error bars
            fig, ax = plot_errorbar(bins, histos[0], styles[0],
                                    show_legend=False)

            for is_final, hist, style in zip([False]*len(histos[1:-1])+[True],
                                   histos[1:], styles[1:]):
                if not is_final:
                    fig, ax = plot_step(bins, hist, style,
                                        figure=fig, axis=ax, show_legend=False)
                else:
                    plot_step(bins, hist, style,
                              figure=fig, axis=ax, show_legend=True,
                              output=filename, xlabel=xlabel,
                              ylabel='Efficiency')

            # Clear plot in memory
            plt.close('all')

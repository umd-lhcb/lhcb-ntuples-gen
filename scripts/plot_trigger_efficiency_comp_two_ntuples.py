#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Thu Apr 29, 2021 at 01:52 AM +0200

import uproot
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from argparse import Action
from numpy import logical_and as AND
from numpy import nan_to_num
from statsmodels.stats.proportion import proportion_confint

from pyTuplingUtils.parse import double_ntuple_parser_no_output
from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.io import read_branches, read_branch
from pyTuplingUtils.plot import plot_style, plot_top_errorbar_bot_errorbar
from pyTuplingUtils.plot import ax_add_args_errorbar as errorbar_style

from plot_trigger_efficiency_comp import parse_input as parent_parse_input
from plot_trigger_efficiency_comp import div_with_confint


#################################
# Command line arguments parser #
#################################

DESCR = '''
generate trigger efficiency comparison plots in two different ntuples.
'''


def modify_action(parser, dest, default):
    for action in parser._actions:
        if action.dest == dest:
            action.default = default


def parse_input(descr=DESCR):
    parser = parent_parse_input(descr)
    modify_action(parser, 'ax2_ylabel', 'TO / FS')
    return parser


########
# Main #
########

if __name__ == '__main__':
    args = parse_input().parse_args()

    plot_style(text_usetex=True)

    ntp1 = uproot.open(args.ref)
    ntp2 = uproot.open(args.comp)

    # Load trigger branches that will be used for efficiency comparison
    eff_branches = []
    eff_branches.append(read_branch(ntp1, args.ref_tree, args.triggers[0]))
    eff_branches.append(read_branch(ntp2, args.comp_tree, args.triggers[1]))

    # Now generate efficiency plots regarding some kinematic variables
    for br, data_range, xlabel in zip(
            args.kinematic_vars, args.data_range, args.xlabel):
        raw = []
        raw.append(read_branch(ntp1, args.ref_tree, br))
        raw.append(read_branch(ntp2, args.comp_tree, br))

        histos = []
        styles = []

        for raw_br, tr_br, color, legend in zip(
                raw, eff_branches, args.colors, args.legends):
            histo_orig, bins = gen_histo(
                raw_br, bins=25, data_range=data_range)
            histo_weighted, bins = gen_histo(
                raw_br, bins=25, data_range=data_range,
                weights=tr_br.astype(np.double))

            histo, error = div_with_confint(histo_weighted, histo_orig)
            histos.append(histo)
            styles.append(errorbar_style(legend, color, yerr=error))

        # Compute the ratio
        ratio = histos[1] / histos[0]

        for ext in args.ext:
            filename = '_'.join([
                args.output_prefix, args.title.replace(' ', '_'), br]) + \
                '.' + ext

            plot_top_errorbar_bot_errorbar(
                bins, histos[0], bins, histos[1], bins, ratio,
                styles[0], styles[1],
                output=filename,
                title=args.title,
                xlabel=xlabel,
                ax1_ylabel='Efficiency', ax2_ylabel=args.ax2_ylabel
            )

            # Clear plot in memory
            plt.close('all')

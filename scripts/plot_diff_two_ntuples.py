#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Wed Oct 23, 2019 at 02:52 AM -0400

import sys
import os
import uproot
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from pyTuplingUtils.parse import double_ntuple_parser
from pyTuplingUtils.utils import find_common_uid
from pyTuplingUtils.io import read_branch
from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.plot import plot_style, plot_histo, ax_add_args_default

from plot_single_branch_two_ntuples import parse_input


#################################
# Command line arguments parser #
#################################

DESCR = '''
generate two plots (diff, norm) comparing a branch in trees contained in two
n-tuples.
'''


########
# Main #
########

if __name__ == '__main__':
    args = parse_input(DESCR).parse_args()

    plot_style()

    ref_ntp, comp_ntp = map(uproot.open, (args.ref, args.comp))
    _, ref_idx, comp_idx = find_common_uid(
        ref_ntp, comp_ntp, args.ref_tree, args.comp_tree)

    for b, B in zip(args.ref_branch.split(','), args.comp_branch.split(',')):
        ref_branch = read_branch(ref_ntp, args.ref_tree, b)
        comp_branch = read_branch(comp_ntp, args.comp_tree, B)

        # Keep the intersection between the two branches, also only keep events
        # that are unique
        ref_branch = ref_branch[ref_idx]
        comp_branch = comp_branch[comp_idx]

        diff_filename = os.path.join(args.output, b+'_diff.png')
        diff_norm_filename = os.path.join(args.output, b+'_diff_norm.png')

        # Plot the difference
        diff = comp_branch - ref_branch
        histo, bins = gen_histo(diff)

        plot_add_args = ax_add_args_default(diff.size, diff.mean(), diff.std())
        plot_histo(histo, bins, plot_add_args, diff_filename,
                   title=b+' (diff)', yscale=args.y_axis_scale)

        # Plot the normalized difference
        diff_norm = diff / ref_branch
        diff_norm[np.isinf(diff_norm)] = 0  # Remove infinities
        diff_norm[np.isnan(diff_norm)] = 0  # Remove nan
        histo, bins = gen_histo(diff_norm)

        plot_add_args = ax_add_args_default(diff_norm.size, diff_norm.mean(),
                                            diff_norm.std())
        plot_histo(histo, bins, plot_add_args, diff_norm_filename,
                   title=b+' (diff norm)', yscale=args.y_axis_scale)

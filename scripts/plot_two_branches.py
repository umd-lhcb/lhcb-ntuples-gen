#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Sun May 30, 2021 at 12:20 AM +0200

import uproot
import mplhep as hep
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from pyTuplingUtils.parse import single_ntuple_parser
from pyTuplingUtils.io import read_branches
from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.plot import plot_histo, plot_errorbar
from pyTuplingUtils.plot import ax_add_args_histo

from plot_trigger_efficiency_comp import DataRangeAction


#################################
# Command line arguments parser #
#################################

DESCR = '''
generate a plot from a branch of tree contained in a n-tuple.
'''


def parse_input(descr=DESCR):
    parser = single_ntuple_parser(descr)

    parser.add_argument('--y-axis-scale',
                        nargs='?',
                        default='linear',
                        help='''
y axis scale (linear or log).''')

    parser.add_argument('-B', '--comp-branch',
                        help='''
comparison branch name.''')

    parser.add_argument('-l', '--ref-label',
                        help='''
specify label for reference branch.''')

    parser.add_argument('-L', '--comp-label',
                        help='''
specify label for comparison branch.''')

    parser.add_argument('--bins', type=int, default=25,
                        help='''
specify binning.''')

    parser.add_argument('-D', '--data-range',
                        nargs='+',
                        default=[(0, 4e4)],
                        help='''
specify plotting range for the kinematic variable multiplicities.''')

    return parser


########
# Main #
########

if __name__ == '__main__':
    args = parse_input().parse_args()
    hep.style.use('LHCb2')

    ntp = uproot.open(args.ref)
    branch1, branch2 = read_branches(ntp, args.ref_tree,
                                     [args.ref_branch, args.comp_branch])
    histo1, bins = gen_histo(branch1, args.bins)
    histo2, _ = gen_histo(branch2, args.bins)

    histo_args = ax_add_args_histo(args.ref_label, '#87CEFA')  # light blue
    pts_args = {'label': args.comp_label, 'color': 'black', 'marker': '_',
                'ls': 'none'}
    fig, ax = plot_histo(histo1, bins, histo_args,
                         output=None, yscale=args.y_axis_scale,
                         show_legend=False, ylim=args.data_range[0])
    plot_errorbar(bins, histo2, pts_args,
                  output=args.output,
                  figure=fig, axis=ax, yscale=args.y_axis_scale,
                  ylim=args.data_range[0])

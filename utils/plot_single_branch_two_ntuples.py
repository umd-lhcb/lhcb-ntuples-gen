#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Wed Oct 23, 2019 at 02:22 AM -0400

import uproot
import numpy as np
import matplotlib as mp

from pyTuplingUtils.parse import double_ntuple_parser
from pyTuplingUtils.io import read_branch
from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.plot import plot_style, plot_histo, ax_add_args_default


#################################
# Command line arguments parser #
#################################

DESCR = '''
generate a plot from the same branch of tree contained in two n-tuples.
'''


def parse_input(descr=DESCR):
    parser = double_ntuple_parser(descr)

    parser.add_argument('--y-axis-scale',
                        nargs='?',
                        default='linear',
                        help='''
y axis scale (linear or log).''')

    return parser


########
# Main #
########

if __name__ == '__main__':
    args = parse_input().parse_args()

    plot_style()

    ntps = map(uproot.open, (args.ref, args.comp))
    branch1, branch2 = map(lambda x, y, z: read_branch(x, y, z),
                           ntps,
                           (args.ref_tree, args.comp_tree),
                           (args.ref_branch, args.comp_branch))
    (histo1, bins1), (histo2, bins2) = map(gen_histo, (branch1, branch2))

    plot1_add_args = ax_add_args_default(
        branch1.size, branch1.mean(), branch1.std(),
        color=(0, 0, 1, .5), edgecolor=(0, 0, 0, 0)
    )
    plot2_add_args = ax_add_args_default(
        branch2.size, branch2.mean(), branch2.std(),
        color=(1, 0, 0, .5), edgecolor=(0, 0, 0, 0)
    )

    fig, ax = plot_histo(histo1, bins1, plot1_add_args, None)
    plot_histo(histo2, bins2, plot2_add_args,
               output=args.output, figure=fig, axis=ax,
               title=args.ref_branch, yscale=args.y_axis_scale)

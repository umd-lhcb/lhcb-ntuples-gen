#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Tue Jun 01, 2021 at 08:49 PM +0200

import uproot
import mplhep as hep

from pyTuplingUtils.parse import single_ntuple_parser
from pyTuplingUtils.io import read_branch
from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.plot import plot_histo, ax_add_args_default


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

    return parser


########
# Main #
########

if __name__ == '__main__':
    args = parse_input().parse_args()
    hep.style.use('LHCb2')

    ntp = uproot.open(args.ref)
    branch = read_branch(ntp, args.ref_tree, args.ref_branch)
    histo, bins = gen_histo(branch)

    plot_add_args = ax_add_args_default(
        branch.size, branch.mean(), branch.std())
    plot_histo(histo, bins, plot_add_args, args.output,
               title=args.ref_branch, yscale=args.y_axis_scale)

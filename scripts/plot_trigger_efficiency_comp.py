#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Tue Apr 13, 2021 at 06:30 PM +0200

import uproot

from numpy import logical_and as AND

from pyTuplingUtils.parse import single_ntuple_parser_no_output
from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.io import read_branches, read_branch
from pyTuplingUtils.plot import plot_style, plot_histo, ax_add_args_simple


#################################
# Command line arguments parser #
#################################

DESCR = '''
generate trigger efficiency comparison plots
'''


def parse_input(descr=DESCR):
    parser = single_ntuple_parser_no_output(descr)

    parser.add_argument('-o', '--output-prefix',
                        required=True,
                        help='''
specify prefix to all output files.
''')

    parser.add_argument('-k', '--kinematic-vars',
                        nargs='+',
                        default=['q2', 'mmiss2', 'el'],
                        help='''
specify efficiency regarding which kinematic variables.
''')

    parser.add_argument('-T', '--triggers',
                        nargs='+',
                        required=True,
                        help='''
specify trigger branches that will be used for efficiency comparison.
''')

    parser.add_argument('-c', '--cuts',
                        nargs='+',
                        default=['d0_l0_global_dec'],
                        help='''
specify triggers to be required True before evaluating efficiency.
''')

    return parser


########
# Main #
########

if __name__ == '__main__':
    args = parse_input().parse_args()

    plot_style()

    ntp = uproot.open(args.ref)

    # Load trigger branches that we cut on
    cut = read_branches(ntp, args.ref_tree, args.cuts)
    if len(cut) > 1:
        cut = AND(cut)
    else:
        cut = cut[0]

    # Load trigger branches that will be used for efficiency comparison
    eff_branches = []
    for br in args.triggers:
        raw = read_branch(ntp, args.ref_tree, br)
        filtered = raw[cut]
        eff_branches.append(filtered)

    # Now generate efficiency plots regarding some kinematic variables
    for br in args.kinematic_vars:
        raw = read_branch(ntp, args.ref_tree, br)
        filtered = raw[cut]

        for tr_br in eff_branches:
            data_range = (-1e7, 1e7)
            histo_orig, bins = gen_histo(
                filtered, bins=25, data_range=data_range)
            histo_weighted, bins = gen_histo(
                filtered, bins=25, data_range=data_range,
                weights=tr_br.astype(int))
            histo = histo_weighted / histo_orig

            plot_add_args = ax_add_args_simple('test')
            plot_histo(histo, bins, plot_add_args, 'test.png')
                       # title=args.ref_branch, yscale=args.y_axis_scale)
            break  # Let's stop immediately.

        break

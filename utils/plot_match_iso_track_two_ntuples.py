#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Sat Sep 28, 2019 at 04:22 PM -0400

import sys
import os
import uproot
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from argparse import ArgumentParser
from find_common_uid import find_common_uid
from plot_single_branch import BINS
from plot_single_branch import read_branch, gen_histo, plot


################
# Configurable #
################

DELTA = 1E-5
BRANCHS = {
    'ISOLATION_TRACK1': ['Y_ISOLATION_PE', 'Y_ISOLATION_PX', 'Y_ISOLATION_PY',
                         'Y_ISOLATION_PZ'],
    'ISOLATION_TRACK2': ['Y_ISOLATION_PE2', 'Y_ISOLATION_PX2',
                         'Y_ISOLATION_PY2', 'Y_ISOLATION_PZ2'],
    'ISOLATION_TRACK3': ['Y_ISOLATION_PE3', 'Y_ISOLATION_PX3',
                         'Y_ISOLATION_PY3', 'Y_ISOLATION_PZ3'],
}


#################################
# Command line arguments parser #
#################################

def parse_input():
    parser = ArgumentParser(description='''
generate two plots with the momentum matching results from two n-tuples.''')

    parser.add_argument('-n', '--ref',
                        nargs='?',
                        required=True,
                        help='''
path to reference n-tuple.''')

    parser.add_argument('-N', '--comp',
                        nargs='?',
                        required=True,
                        help='''
path to comparison n-tuple.''')

    parser.add_argument('-t', '--refTree',
                        nargs='?',
                        required=True,
                        help='''
supply tree name in the reference n-tuple.''')

    parser.add_argument('-T', '--compTree',
                        nargs='?',
                        required=True,
                        help='''
supply tree name in the comparison n-tuple.''')

    parser.add_argument('-s', '--suffix',
                        nargs='?',
                        required=True,
                        help='''
output filename suffix, separated by ",".''')

    parser.add_argument('-o', '--output',
                        nargs='?',
                        required=True,
                        help='''
path to output directory.''')

    parser.add_argument('--bins',
                        nargs='?',
                        type=int,
                        default=BINS,
                        help='''
number of bins. default to {}.'''.format(BINS))

    return parser.parse_args()


#########
# Match #
#########

# NOTE: 'val' and 'ref_val' are four momenta
def match(val, ref_dict):
    for ref_key, ref_val in ref_dict.items():
        if abs(val[0]-ref_val[0]) <= DELTA and \
                np.linalg.norm(ref_val[1:] - val[1:]) <= DELTA:
            return ref_key
    return 0


def four_momenta(tree, brach_dict=BRANCHS):
    momenta = {}
    for k, v in brach_dict.items():
        p = tree.arrays(v).values()
        momenta[k] = np.column_stack(list(p))
    return momenta


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    _, ref_idx, comp_idx = find_common_uid(args.ref, args.comp, args.refTree,
                                           args.compTree)

    ref_ntp, comp_ntp = map(uproot.open, [args.ref, args.comp])
    ref_mom, comp_mom = map(four_momenta, [ref_ntp[args.refTree],
                                           comp_ntp[args.compTree]])

    # for suffix in args.suffix.split(','):


        # ref_branch = read_branch(args.ref, args.refTree, b)
        # comp_branch = read_branch(args.comp, args.compTree, B)

        # # Keep the intersection between the two branches, also only keep events
        # # that are unique
        # ref_branch = ref_branch[ref_idx]
        # comp_branch = comp_branch[comp_idx]

        # diff_filename = b + '_diff.png'
        # diff_norm_filename = b + '_diff_norm.png'

        # # Plot the difference
        # diff = comp_branch - ref_branch
        # mean = diff.mean()
        # std = diff.std()
        # histo, bins = gen_histo(diff, args.bins)
        # num = ref_branch.size

        # plot(histo, bins, os.path.join(args.output, diff_filename),
             # b+' (diff)', num, mean, std, args.yAxisScale)

        # # Plot the normalized difference
        # diff_norm = diff / ref_branch
        # diff_norm[np.isinf(diff_norm)] = 1  # Remove infinities
        # mean = diff_norm.mean()
        # std = diff_norm.std()
        # histo, bins = gen_histo(diff_norm, args.bins)

        # plot(histo, bins, os.path.join(args.output, diff_norm_filename),
             # b+' (diff norm)', num, mean, std, args.yAxisScale)

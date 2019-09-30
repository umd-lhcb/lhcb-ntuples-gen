#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Sun Sep 29, 2019 at 10:14 PM -0400

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
BRANCH_NAMES = list(BRANCHS.keys())


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
    for ref_key, ref_vals in ref_dict.items():
        for ref_val in ref_vals:
            if abs(val[0]-ref_val[0]) <= DELTA and \
                    np.linalg.norm(ref_val[1:] - val[1:]) <= DELTA:
                return ref_key
    return 0


def four_momenta(tree, idx, brach_dict=BRANCHS):
    momenta = {}
    for k, v in enumerate(brach_dict.values(), start=1):
        raw_events = tree.arrays(v).values()
        # Keep events with indices specified in 'idx' only
        events = []
        for e in raw_events:
            events.append(e[idx])
        momenta[k] = np.column_stack(events)
    return momenta


########
# Plot #
########

def plot_comparison(ref_mom, comp_mom, titlenames, filename_suffix):
    for key, val in comp_mom.items():
        title = titlenames[key-1]
        filename = title + filename_suffix

        result = np.fromiter((match(v, ref_mom) for v in val), val.dtype)
        mean = result.mean()
        std = result.std()

        histo, bins = gen_histo(result, bins=args.bins)
        plot(histo, bins, filename, title, result.size, mean, std)


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    _, ref_idx, comp_idx = find_common_uid(args.ref, args.comp, args.refTree,
                                           args.compTree)

    ref_ntp, comp_ntp = map(uproot.open, [args.ref, args.comp])
    ref_mom = four_momenta(ref_ntp[args.refTree], ref_idx)
    comp_mom = four_momenta(comp_ntp[args.compTree], comp_idx)
    suffix_names = args.suffix.split(',')

    plot_comparison(ref_mom, comp_mom, BRANCH_NAMES, suffix_names[0])
    plot_comparison(comp_mom, ref_mom, BRANCH_NAMES, suffix_names[1])

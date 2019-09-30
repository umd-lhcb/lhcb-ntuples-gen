#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Mon Sep 30, 2019 at 12:10 AM -0400

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
def match(mom, ref_mom_list):
    for track_idx, ref_val in enumerate(ref_mom_list, start=1):
        if abs(mom[0]-ref_val[0]) <= DELTA and \
                np.linalg.norm(ref_val[1:] - mom[1:]) <= DELTA:
            return track_idx
    return 0


def four_momenta(tree, idx, branch_dict=BRANCHS):
    momenta = []
    for b in branch_dict.values():
        raw_event_array = tree.arrays(b).values()
        # Keep events with indices specified in 'idx' only
        # NOTE: 'event_array' looks like:
        #       [[E1, E2, E3, ...], [PX1, PX2, PX3, ...], [PY1, PY2, PY3, ...],
        #        ...]
        event_array = [e[idx] for e in raw_event_array]
        momenta.append(np.column_stack(event_array))
    return momenta


def find_ref_mom_with_the_same_idx(ref_mom, idx):
    return [t[idx] for t in ref_mom]


########
# Plot #
########

def plot_comparison(ref_mom, comp_mom, titlenames, filename_suffix):
    for track_idx in range(0, len(comp_mom)):
        title = titlenames[track_idx]
        filename = os.path.join(args.output, title + filename_suffix)

        result = np.fromiter(
            (match(comp_mom[track_idx][i],
                   find_ref_mom_with_the_same_idx(ref_mom, i))
             for i in range(0, comp_mom[track_idx].shape[0])), int)
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

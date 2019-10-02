#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Tue Oct 01, 2019 at 09:29 PM -0400

import sys
import os
import uproot
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from argparse import ArgumentParser
from find_common_uid import find_common_uid
from plot_single_branch import BINS
from plot_single_branch import read_branch, gen_histo
from plot_single_branch import plot_single_branch as plot


################
# Configurable #
################

DELTA = 1E-5

BRANCHS_MOMENTA = {
    'ISOLATION_TRACK1': ['Y_ISOLATION_PE', 'Y_ISOLATION_PX', 'Y_ISOLATION_PY',
                         'Y_ISOLATION_PZ'],
    'ISOLATION_TRACK2': ['Y_ISOLATION_PE2', 'Y_ISOLATION_PX2',
                         'Y_ISOLATION_PY2', 'Y_ISOLATION_PZ2'],
    'ISOLATION_TRACK3': ['Y_ISOLATION_PE3', 'Y_ISOLATION_PX3',
                         'Y_ISOLATION_PY3', 'Y_ISOLATION_PZ3'],
}
BRANCHES_TYPES = {
    'ISOLATION_TRACK1': ['Y_ISOLATION_Type'],
    'ISOLATION_TRACK2': ['Y_ISOLATION_Type2'],
    'ISOLATION_TRACK3': ['Y_ISOLATION_Type3'],
}

MOMENTA_NAMES = list(BRANCHS_MOMENTA.keys())
TYPE_NAMES = [i[0] for i in BRANCHES_TYPES.values()]


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


def get_branches(tree, idx, branch_dict=BRANCHS_MOMENTA):
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

def plot_comparison(ref_mom, comp_mom, ref_type, comp_type, title_names,
                    type_names, filename_suffix):
    for track_idx in range(0, len(comp_mom)):
        track_title = title_names[track_idx]
        type_title = type_names[track_idx]

        track_match_result = np.array([], int)
        type_self = np.array([])
        type_match = np.array([])

        for i in range(0, comp_mom[track_idx].shape[0]):
            matched_track_idx = match(
                comp_mom[track_idx][i],
                find_ref_mom_with_the_same_idx(ref_mom, i)
            )
            track_match_result = np.append(track_match_result,
                                           matched_track_idx)

            if matched_track_idx:
                type_self = np.append(type_self, ref_type[track_idx][i])
                type_match = np.append(type_match,
                                       comp_type[matched_track_idx-1][i][0])

        # Plot track matching results
        filename = os.path.join(args.output, track_title + filename_suffix)
        mean = track_match_result.mean()
        std = track_match_result.std()

        histo, bins = gen_histo(track_match_result, bins=args.bins)
        plot(histo, bins, filename, track_title, track_match_result.size, mean,
             std)

        # Plot matched track type differences
        filename = os.path.join(args.output, type_title + '_matched_diff' +
                                filename_suffix)
        result = type_match - type_self
        mean = result.mean()
        std = result.std()

        histo, bins = gen_histo(result, bins=args.bins)
        plot(histo, bins, filename, type_title + ' (matched diff)',
             track_match_result.size, mean, std)


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    _, ref_idx, comp_idx = find_common_uid(args.ref, args.comp, args.refTree,
                                           args.compTree)

    ref_ntp, comp_ntp = map(uproot.open, [args.ref, args.comp])
    ref_mom = get_branches(ref_ntp[args.refTree], ref_idx)
    comp_mom = get_branches(comp_ntp[args.compTree], comp_idx)
    ref_type = get_branches(ref_ntp[args.refTree], ref_idx, BRANCHES_TYPES)
    comp_type = get_branches(comp_ntp[args.compTree], comp_idx, BRANCHES_TYPES)
    suffix_names = args.suffix.split(',')

    plot_comparison(ref_mom, comp_mom, ref_type, comp_type,
                    MOMENTA_NAMES, TYPE_NAMES, suffix_names[0])
    plot_comparison(comp_mom, ref_mom, comp_type, ref_type,
                    MOMENTA_NAMES, TYPE_NAMES, suffix_names[1])

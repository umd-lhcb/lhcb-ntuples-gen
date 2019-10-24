#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Thu Oct 24, 2019 at 04:12 AM -0400

import sys
import os
import uproot
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from pyTuplingUtils.utils import find_common_uid
from pyTuplingUtils.plot import plot_style, plot_hexbin

from plot_match_iso_track import BRANCHES_DICT
from plot_match_iso_track import parse_input as parse_input_base
from plot_match_iso_track import match, find_ref_val_list
from plot_match_iso_track import read_branch_dict


################
# Configurable #
################

ISO_VARS_LEN = len(list(BRANCHES_DICT.values())[0])

AUX_BRANCHES = ['totCandidates',
                'Y_P',
                'Y_PT',
                'Y_ENDVERTEX_Y',
                'Y_ENDVERTEX_Z'
                ]
for k in BRANCHES_DICT.keys():
    BRANCHES_DICT[k] += AUX_BRANCHES

CSV_HEADERS = 'comp_TrackType,ref_TrackType,comp_BDT,ref_BDT'
for b in AUX_BRANCHES:
    CSV_HEADERS += ',comp_{},ref_{}'.format(b, b)


#################################
# Command line arguments parser #
#################################

DESCR = '''
generate two hexbin plots of track type difference vs. BDT score difference from
two n-tuples.
'''


def parse_input(descr=DESCR):
    parser = parse_input_base(descr)

    parser.add_argument('--bins',
                        nargs='?',
                        default=30,
                        help='''
number of bins along each axis.''')

    return parser


########
# Plot #
########

def plot_match_iso_track_hexbin(
    ref_val, comp_val, gridsize, output_dir, filename,
        bdt_score_idx=4, track_type_idx=6,
        debug=True, **kwargs):
    track_type_diff_arr, bdt_score_diff_arr = ([] for l in range(2))
    if debug:
        print(CSV_HEADERS)

    for track_idx in range(0, len(comp_val)):
        for i in range(0, comp_val[track_idx].shape[0]):
            matched_track_idx = comp_bdt_score = \
                comp_val[track_idx][i][bdt_score_idx]

            if comp_bdt_score != -2:
                matched_track_idx = match(comp_val[track_idx][i],
                                          find_ref_val_list(ref_val, i))

            if matched_track_idx > 0:
                comp_type = comp_val[track_idx][i][track_type_idx]
                ref_type = ref_val[matched_track_idx-1][i][track_type_idx]
                ref_bdt_score = ref_val[matched_track_idx-1][i][bdt_score_idx]

                track_type_diff = ref_type - comp_type
                bdt_score_diff = ref_bdt_score - comp_bdt_score

                track_type_diff_arr.append(track_type_diff)
                bdt_score_diff_arr.append(bdt_score_diff)

                if debug and abs(bdt_score_diff) > 0.1:
                    data = [comp_type, ref_type, comp_bdt_score, ref_bdt_score]
                    for idx in range(ISO_VARS_LEN,
                                     ISO_VARS_LEN+len(AUX_BRANCHES)):
                        data += [comp_val[track_idx][i][idx],
                                 ref_val[matched_track_idx-1][i][idx]]
                    print(','.join(map(str, data)))

    track_type_diff_arr, bdt_score_diff_arr = \
        map(np.array, (track_type_diff_arr, bdt_score_diff_arr))

    plot_hexbin(track_type_diff_arr, bdt_score_diff_arr,
                gridsize, {},
                output=os.path.join(output_dir, filename),
                xlabel='Track type diff', ylabel='BDT score diff',
                colorbar_label='tot: {}'.format(track_type_diff_arr.size))


########
# Main #
########

if __name__ == '__main__':
    args = parse_input().parse_args()

    plot_style()

    ref_ntp, comp_ntp = map(uproot.open, [args.ref, args.comp])
    _, ref_idx, comp_idx = find_common_uid(
        ref_ntp, comp_ntp, args.ref_tree, args.comp_tree)

    ref_val = read_branch_dict(ref_ntp, args.ref_tree, ref_idx)
    comp_val = read_branch_dict(comp_ntp, args.comp_tree, comp_idx)
    suffix_names = args.suffix.split(',')

    # Typically for v42
    plot_match_iso_track_hexbin(
        ref_val, comp_val, args.bins,
        args.output, 'ISOLATION_TRACK_vs_BDT'+suffix_names[0])

    # Typically for v36
    plot_match_iso_track_hexbin(
        comp_val, ref_val, args.bins,
        args.output, 'ISOLATION_TRACK_vs_BDT'+suffix_names[1])

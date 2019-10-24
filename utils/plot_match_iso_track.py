#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Thu Oct 24, 2019 at 02:40 AM -0400

import uproot
import numpy as np
import os

from pyTuplingUtils.parse import double_ntuple_parser
from pyTuplingUtils.utils import find_common_uid
from pyTuplingUtils.io import read_branches
from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.plot import plot_style, plot_histo, ax_add_args_default


################
# Configurable #
################

FILE_EXTENSION = '.png'
DELTA = 1E-5

ISOLATION_BRANCHS = ['Y_ISOLATION_PX',
                     'Y_ISOLATION_PY',
                     'Y_ISOLATION_PZ',
                     'Y_ISOLATION_ANGLE',
                     'Y_ISOLATION_BDT',
                     'Y_ISOLATION_CHI2',
                     'Y_ISOLATION_Type'
                     ]

BRANCHES_DICT = {k: [b+str(idx) if idx > 1 else b for b in ISOLATION_BRANCHS]
                 for idx, k in enumerate(
                     ('ISOLATION_TRACK1',
                      'ISOLATION_TRACK2',
                      'ISOLATION_TRACK3'), start=1)}

ISOLATION_TRACK_NAMES = list(BRANCHES_DICT.keys())
ISOLATION_TYPE_NAMES = ['Y_ISOLATION_Type',
                        'Y_ISOLATION_Type2',
                        'Y_ISOLATION_Type3']


#################################
# Command line arguments parser #
#################################

DESCR = '''
generate two plots with the momentum matching results from two n-tuples.
'''


def remove_args(parser, dest):
    for action in parser._actions:
        if action.dest == dest:
            parser._remove_action(action)


def parse_input(descr=DESCR):
    parser = double_ntuple_parser(descr)

    parser.add_argument('-s', '--suffix',
                        nargs='?',
                        required=True,
                        help='''
output filename suffix, separated by ",".''')

    remove_args(parser, 'ref_branch')
    remove_args(parser, 'comp_branch')

    return parser


######
# IO #
######

def read_branch_dict(ntp, tree, idx, branch_dict=BRANCHES_DICT):
    value = []
    for b in branch_dict.values():
        data = read_branches(ntp, tree, b, idx, transpose=True)
        value.append(data)
    return value


#########
# Match #
#########

def TAN(val, i, j):
    return val[i] / val[j] if val[j] != 0 else 0


def PXPZ(val, px_idx=0, pz_idx=2):
    return TAN(val, px_idx, pz_idx)


def PYPZ(val, py_idx=1, pz_idx=2):
    return TAN(val, py_idx, pz_idx)


def match(val, ref_val_list, angle_idx=3):
    for track_idx, ref_val in enumerate(ref_val_list, start=1):
        pxpz = PXPZ(val)
        pypz = PYPZ(val)
        angle = val[angle_idx]

        ref_pxpz = PXPZ(ref_val)
        ref_pypz = PYPZ(ref_val)
        ref_angle = ref_val[angle_idx]

        if pxpz != 0 and pypz != 0 and \
                abs(pxpz-ref_pxpz) <= DELTA and \
                abs(pypz-ref_pypz) <= DELTA and \
                abs(angle-ref_angle) <= DELTA:
            return track_idx
    return 0


def find_ref_val_list(ref_val, idx):
    return [t[idx] for t in ref_val]


########
# Plot #
########

def plot_histo_wrapper(data, title, output_dir, filename,
                       extension=FILE_EXTENSION):
    output_path = os.path.join(output_dir, filename+extension)
    histo, bins = gen_histo(data)

    plot_add_args = ax_add_args_default(data.size, data.mean(), data.std())
    plot_histo(histo, bins, plot_add_args, title=title, output=output_path)


def plot_track_idx_and_type(
    ref_val, comp_val, output_dir, filename_suffix,
        chi2_types,
        track_names=ISOLATION_TRACK_NAMES, type_names=ISOLATION_TYPE_NAMES,
        bdt_score_idx=4, track_type_idx=6, chi2_idx=5,
        counter=None):
    for track_idx in range(len(comp_val)):
        track_name, type_name = \
            map(lambda x: x[track_idx], (track_names, type_names))
        matched_track_idx_arr, comp_type_arr, ref_type_arr = \
            ([] for l in range(3))

        for i in range(comp_val[track_idx].shape[0]):
            matched_track_idx = comp_bdt_score = \
                comp_val[track_idx][i][bdt_score_idx]

            if comp_bdt_score != -2:  # Ignore events without iso tracks.
                matched_track_idx = match(comp_val[track_idx][i],
                                          find_ref_val_list(ref_val, i))

            matched_track_idx_arr.append(matched_track_idx)

            if matched_track_idx > 0:
                comp_type = comp_val[track_idx][i][track_type_idx]
                ref_type = ref_val[matched_track_idx-1][i][track_type_idx]
                chi_square = comp_val[track_idx][i][chi2_idx]

                comp_type_arr.append(comp_type)
                ref_type_arr.append(ref_type)
                chi2_types[comp_type].append(chi_square)

                if counter:
                    counter[matched_track_idx-1] += 1

        matched_track_idx_arr, ref_type_arr, comp_type_arr = \
            map(np.array, (matched_track_idx_arr, ref_type_arr, comp_type_arr))

        # Plot track indices matching results
        plot_histo_wrapper(matched_track_idx_arr, track_name,
                           output_dir, track_name+filename_suffix)

        # Plot matched track type differences
        track_type_diff = ref_type_arr - comp_type_arr
        plot_histo_wrapper(track_type_diff, type_name+' (matched diff)',
                           output_dir,
                           type_name+'_matched_diff'+filename_suffix)


def plot_match_iso_track(ref_val, comp_val, output_dir, filename_suffix,
                         **kwargs):
    chi2_types = {1: [], 3: [], 4: []}
    plot_track_idx_and_type(ref_val, comp_val, output_dir, filename_suffix,
                            chi2_types, **kwargs)

    # Plot chi^2 of each track type
    for data, title in zip(
        map(np.array, chi2_types.values()),
        ['TRACK_TYPE1_CHI2', 'TRACK_TYPE3_CHI2', 'TRACK_TYPE4_CHI2']
    ):
        plot_histo_wrapper(data, title, output_dir, title+filename_suffix)


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
    plot_match_iso_track(
        ref_val, comp_val, args.output, suffix_names[0])

    # Typically for v36
    counter = [0, 0, 0]
    plot_match_iso_track(comp_val, ref_val, args.output, suffix_names[1],
                         counter=counter)
    print('Matched track types: {} {} {}'.format(*counter))

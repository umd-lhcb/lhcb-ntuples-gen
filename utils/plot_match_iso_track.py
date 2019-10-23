#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Wed Oct 23, 2019 at 04:39 AM -0400

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

DELTA = 1E-5

BRANCHES_MATCH = {
    'ISOLATION_TRACK1': ['Y_ISOLATION_PX', 'Y_ISOLATION_PY', 'Y_ISOLATION_PZ',
                         'Y_ISOLATION_ANGLE',
                         'Y_ISOLATION_BDT', 'Y_ISOLATION_CHI2'],
    'ISOLATION_TRACK2': ['Y_ISOLATION_PX2', 'Y_ISOLATION_PY2',
                         'Y_ISOLATION_PZ2', 'Y_ISOLATION_ANGLE2',
                         'Y_ISOLATION_BDT2', 'Y_ISOLATION_CHI22'],
    'ISOLATION_TRACK3': ['Y_ISOLATION_PX3', 'Y_ISOLATION_PY3',
                         'Y_ISOLATION_PZ3', 'Y_ISOLATION_ANGLE3',
                         'Y_ISOLATION_BDT3', 'Y_ISOLATION_CHI23'],
}

BRANCHES_AUX = {
    'ISOLATION_TRACK1': ['Y_ISOLATION_Type', 'Y_ISOLATION_BDT'],
    'ISOLATION_TRACK2': ['Y_ISOLATION_Type2', 'Y_ISOLATION_BDT2'],
    'ISOLATION_TRACK3': ['Y_ISOLATION_Type3', 'Y_ISOLATION_BDT3'],
}
AUX_VAL_ADDONS = [
    'totCandidates',
    'Y_P',
    'Y_PT',
    'Y_ENDVERTEX_Y',
    'Y_ENDVERTEX_Z'
]

for k in BRANCHES_AUX.keys():
    BRANCHES_AUX[k] = BRANCHES_AUX[k] + AUX_VAL_ADDONS

ISOLATION_TRACK_NAMES = list(BRANCHES_MATCH.keys())
ISOLATION_TYPE_NAMES = [i[0] for i in BRANCHES_AUX.values()]


#################################
# Command line arguments parser #
#################################

DESCR = '''
generate two plots with the momentum matching results from two n-tuples.
'''


def parse_input():
    parser = double_ntuple_parser(DESCR)

    parser.add_argument('-s', '--suffix',
                        nargs='?',
                        required=True,
                        help='''
output filename suffix, separated by ",".''')

    return parser


#########
# Match #
#########

def TAN(val, i, j):
    if val[j] != 0:
        return val[i] / val[j]
    else:
        return 0


def PXPZ(val):
    return TAN(val, 0, 2)


def PYPZ(val):
    return TAN(val, 1, 2)


# NOTE: 'val' and 'ref_val' are four momenta
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


def read_branch_dict(ntp, tree, idx, branch_dict=BRANCHES_MATCH):
    value = []
    for b in branch_dict.values():
        data = read_branches(ntp, tree, b, idx, transpose=True)
        value.append(data)
    return value


def find_ref_val_list(ref_mom, idx):
    return [t[idx] for t in ref_mom]


########
# Plot #
########

def plot_track_type_diff(
    ref_val, comp_val, chi2_type_1, chi2_type_3, chi2_type_4, filename_suffix,
        track_names=ISOLATION_TRACK_NAMES, type_names=ISOLATION_TYPE_NAMES,
        counter=None):
    for track_idx in range(0, len(comp_val)):
        track_name = track_names[track_idx]
        type_name = type_names[track_idx]

        track_match_result = np.array([], int)
        comp_type_arr = []
        ref_type_arr = []

        for i in range(0, comp_val[track_idx].shape[0]):
            comp_bdt_score = int(comp_val[track_idx][i][5])

            if comp_bdt_score != -2:
                matched_track_idx = match(comp_val[track_idx][i],
                                          find_ref_val_list(ref_val, i))
            else:
                matched_track_idx = -2

            track_match_result = np.append(track_match_result,
                                           matched_track_idx)

            if matched_track_idx > 0:
                comp_type = comp_aux[track_idx][i][0]
                ref_type = ref_aux[matched_track_idx-1][i][0]

                comp_type_arr.append(comp_type)
                ref_type_arr.append(ref_type)

                chi_square = comp_val[track_idx][i][-1]

                if comp_type == 1:
                    chi2_type_1.append(chi_square)
                elif comp_type == 3:
                    chi2_type_3.append(chi_square)
                elif comp_type == 4:
                    chi2_type_4.append(chi_square)

                # Counter
                if counter is not None:
                    counter[matched_track_idx-1] += 1

        # Convert difference lists to numpy arrays
        ref_type_arr = np.array(ref_type_arr)
        comp_type_arr = np.array(comp_type_arr)

        # Plot track matching results
        filename = os.path.join(args.output, track_name+filename_suffix)
        histo, bins = gen_histo(track_match_result)

        plot_add_args = ax_add_args_default(
            track_match_result.size, track_match_result.mean(),
            track_match_result.std())
        plot_histo(histo, bins, filename, track_name, plot_add_args)

        # Plot matched track type differences
        filename = os.path.join(
            args.output, type_name+'_matched_diff'+filename_suffix)
        result = ref_type_arr - comp_type_arr
        histo, bins = gen_histo(result, bins=args.bins)

        plot_add_args = ax_add_args_default(result.size, result.mean(),
                                            result.std())
        plot_histo(histo, bins, filename, type_name+' (matched diff)',
                   plot_add_args)


def plot_match_iso_track(ref_val, comp_val, ref_aux, comp_aux,
                         track_names, type_names, filename_suffix, args,
                         **kwargs):
    chi2_type_1 = []
    chi2_type_3 = []
    chi2_type_4 = []

    plot_track_type_diff(ref_val, comp_val,
                         chi2_type_1, chi2_type_3, chi2_type_4, **kwargs)

    # Plot chi^2 of each track type
    chi2_type_1 = np.array(chi2_type_1)
    chi2_type_3 = np.array(chi2_type_3)
    chi2_type_4 = np.array(chi2_type_4)

    for data, title in zip(
        [chi2_type_1, chi2_type_3, chi2_type_4],
        ['TRACK_TYPE1_CHI2', 'TRACK_TYPE3_CHI2', 'TRACK_TYPE4_CHI2']
    ):
        filename = os.path.join(args.output, title+filename_suffix)
        histo, bins = gen_histo(data)

        plot(histo, bins, filename, title,
             data.size, mean, std)


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    plot_style()

    _, ref_idx, comp_idx = find_common_uid(args.ref, args.comp, args.refTree,
                                           args.compTree)

    ref_ntp, comp_ntp = map(uproot.open, [args.ref, args.comp])
    ref_val = get_branches(ref_ntp[args.refTree], ref_idx)
    comp_val = get_branches(comp_ntp[args.compTree], comp_idx)
    ref_aux = get_branches(ref_ntp[args.refTree], ref_idx, BRANCHES_AUX)
    comp_aux = get_branches(comp_ntp[args.compTree], comp_idx, BRANCHES_AUX)
    suffix_names = args.suffix.split(',')

    # Typically for v42
    plot_match_iso_track(
        ref_val, comp_val, ref_aux, comp_aux, MOMENTA_NAMES, TYPE_NAMES,
        suffix_names[0], args)

    # Typically for v36
    counter = [0, 0, 0]
    plot_match_iso_track(
        comp_val, ref_val, comp_aux, ref_aux, MOMENTA_NAMES, TYPE_NAMES,
        suffix_names[1], args, counter)
    print('Matched track types: {} {} {}'.format(*counter))

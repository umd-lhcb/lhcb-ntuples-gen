#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Oct 24, 2019 at 01:39 AM -0400

import sys
import os
import uproot
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from argparse import ArgumentParser
from matplotlib import pyplot as plt
from find_common_uid import find_common_uid
from plot_single_branch import FONT_FAMILY, FONT_SIZE
from plot_match_iso_track import parse_input
from plot_match_iso_track import match, get_branches
from plot_match_iso_track import find_ref_val_list
from plot_match_iso_track import BRANCHES_MATCH, BRANCHES_AUX


################
# Configurable #
################

HB_STYLE = 'inferno'
BIN_SCALE = 'log'

AUX_VAL_ADDONS = [
    'totCandidates',
    'Y_P',
    'Y_PT',
    'Y_ENDVERTEX_Y',
    'Y_ENDVERTEX_Z'
]



########
# Plot #
########

def plot_hexbin(x, y, gridsize, output, xlabel, ylabel):
    plt.rcParams.update({'font.family': FONT_FAMILY})
    plt.rcParams.update({'font.size': FONT_SIZE})

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    hb = ax.hexbin(x, y, gridsize=gridsize, cmap=HB_STYLE, bins=BIN_SCALE)
    cb = fig.colorbar(hb, ax=ax)
    cb.set_label('tot: {}'.format(x.size))

    plt.tight_layout(pad=0.1)
    fig.savefig(output)

    fig.clf()
    plt.close(fig)


def plot_match_iso_track_hexbin(ref_val, comp_val, ref_aux, comp_aux, filename,
                                args):
    track_type_diff_arr = []
    bdt_score_diff_arr = []

    print('comp_TrackType,ref_TrackType,comp_BDT,ref_BDT,comp_totCandidates,ref_totCandidates,comp_Y_P,ref_Y_P,comp_Y_PT,ref_Y_PT,comp_Y_ENDVERTEX_Y,ref_Y_ENDVERTEX_Y,comp_Y_ENDVERTEX_Z,ref_Y_ENDVERTEX_Z')
    for track_idx in range(0, len(comp_val)):
        for i in range(0, comp_val[track_idx].shape[0]):
            comp_bdt_score = comp_val[track_idx][i][5]
            if int(comp_bdt_score) != -2:
                matched_track_idx = match(
                    comp_val[track_idx][i],
                    find_ref_val_list(ref_val, i)
                )
            elif comp_aux[track_idx][i][2] != 1:
                matched_track_idx = -2
            else:
                matched_track_idx = -2

            if matched_track_idx > 0:
                comp_type = comp_aux[track_idx][i][0]
                ref_type = ref_aux[matched_track_idx-1][i][0]
                ref_bdt_score = ref_aux[matched_track_idx-1][i][1]

                track_type_diff = ref_type - comp_type
                bdt_score_diff = ref_bdt_score - comp_bdt_score

                track_type_diff_arr.append(track_type_diff)
                bdt_score_diff_arr.append(bdt_score_diff)

                # NOTE: For debugging purpose
                if abs(bdt_score_diff) > 0.1:
                    print('{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(
                        comp_type, ref_type,
                        comp_bdt_score, ref_bdt_score,
                        comp_aux[track_idx][i][2],
                        ref_aux[matched_track_idx-1][i][2],
                        comp_aux[track_idx][i][3],
                        ref_aux[matched_track_idx-1][i][3],
                        comp_aux[track_idx][i][4],
                        ref_aux[matched_track_idx-1][i][4],
                        comp_aux[track_idx][i][5],
                        ref_aux[matched_track_idx-1][i][5],
                        comp_aux[track_idx][i][6],
                        ref_aux[matched_track_idx-1][i][6],
                    ))

    track_type_diff_arr = np.array(track_type_diff_arr)
    bdt_score_diff_arr = np.array(bdt_score_diff_arr)
    filename = os.path.join(args.output, filename)

    plot_hexbin(track_type_diff_arr, bdt_score_diff_arr, args.bins, filename,
                'Track type diff', 'BDT score diff')


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    _, ref_idx, comp_idx = find_common_uid(args.ref, args.comp, args.refTree,
                                           args.compTree)

    ref_ntp, comp_ntp = map(uproot.open, [args.ref, args.comp])
    ref_val = get_branches(ref_ntp[args.refTree], ref_idx)
    comp_val = get_branches(comp_ntp[args.compTree], comp_idx)
    ref_aux = get_branches(ref_ntp[args.refTree], ref_idx, BRANCHES_AUX)
    comp_aux = get_branches(comp_ntp[args.compTree], comp_idx, BRANCHES_AUX)
    suffix_names = args.suffix.split(',')

    # Typically for v42
    plot_match_iso_track_hexbin(
        ref_val, comp_val, ref_aux, comp_aux,
        'ISOLATION_TRACK_vs_BDT' + suffix_names[0] + '.png', args)

    # Typically for v36
    plot_match_iso_track_hexbin(
        comp_val, ref_val, comp_aux, ref_aux,
        'ISOLATION_TRACK_vs_BDT' + suffix_names[1] + '.png', args)

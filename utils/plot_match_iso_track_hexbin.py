#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Oct 08, 2019 at 01:56 AM -0400

import sys
import os
import uproot
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from argparse import ArgumentParser
from matplotlib import pyplot as plt
from find_common_uid import find_common_uid
from plot_single_branch import PLT_STYLE, FONT_FAMILY, FONT_SIZE
from plot_match_iso_track_two_ntuples import parse_input
from plot_match_iso_track_two_ntuples import match, get_branches
from plot_match_iso_track_two_ntuples import find_ref_val_list
from plot_match_iso_track_two_ntuples import BRANCHES_MATCH, BRANCHES_AUX


########
# Plot #
########

def plot_hexbin(x, y, gridsize, output, title, xlabel, ylabel):
    plt.style.use(PLT_STYLE)
    plt.rcParams.update({'font.family': FONT_FAMILY})
    plt.rcParams.update({'font.size': FONT_SIZE})

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.hexbin(x, y, gridsize=gridsize)

    plt.tight_layout(pad=0.1)
    fig.savefig(output)

    fig.clf()
    plt.close(fig)


def plot_comparison_2d(ref_val, comp_val, ref_aux, comp_aux, filename, args):
    for track_idx in range(0, len(comp_val)):
        track_type_diff = np.array([])
        iso_score_diff = np.array([])

        for i in range(0, comp_val[track_idx].shape[0]):
            bdt_score = int(comp_val[track_idx][i][5])
            if bdt_score != -2:
                matched_track_idx = match(
                    comp_val[track_idx][i],
                    find_ref_val_list(ref_val, i)
                )
            else:
                matched_track_idx = bdt_score

            if matched_track_idx > 0:
                type_diff = ref_aux[track_idx][i][0] - \
                    comp_aux[matched_track_idx-1][i][0]
                score_diff = ref_aux[track_idx][i][1] - \
                    comp_aux[matched_track_idx-1][i][1]

                track_type_diff = np.append(track_type_diff, type_diff)
                iso_score_diff = np.append(iso_score_diff, score_diff)

        filename = os.path.join(args.output, filename)
        plot_hexbin(track_type_diff, iso_score_diff, args.bins, filename,
                    'Track type diff vs. BDT score diff',
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

    # Typically for v42
    plot_comparison_2d(
        ref_val, comp_val, ref_aux, comp_aux,
        'ISOLATION_TRACK_vs_BDT_' + args.suffix_names[0] + '.png', args)

    # Typically for v36
    plot_comparison_2d(
        comp_val, ref_val, comp_aux, ref_aux,
        'ISOLATION_TRACK_vs_BDT_' + args.suffix_names[1] + '.png', args)

#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Feb 28, 2022 at 10:52 PM -0500

import numpy as np

from argparse import ArgumentParser
from dataclasses import dataclass
from uproot import concatenate, recreate

from typing import List, Union
from numpy.typing import ArrayLike


#################
# Configuration #
#################

@dataclass
class RwtRule:
    vars: List[str]
    bins: Union[ArrayLike, List[int], int]
    range: Union[ArrayLike, List[List[float]]]

REWEIGHT_PROCEDURE = {
    'h_occupancy': RwtRule(['b_ownpv_ndof', 'ntracks'], [20, 20], [[1, 200], [0, 450]]),
    'h_kinematic': RwtRule(['b_pt', 'b_eta'], [20, 9], [[0, 25e3], [2, 5]]),
}


#######################
# Command line parser #
#######################

def parse_input():
    parser = ArgumentParser(description='generate weights for sequential 2D reweighting.')

    parser.add_argument('-d', '--dataNtp', required=True,
                        help='specify data input ntuples, which must contains sWeight branches.')

    parser.add_argument('-m', '--mcNtp', required=True, nargs='+',
                        help='specify MC input ntuples.')

    parser.add_argument('-o', '--output', required=True,
                        help='specify output ntuple, which contains histograms.')

    parser.add_argument('-t', '--tree', default='tree',
                        help='specify the tree name in the input ntuple.')

    parser.add_argument('-s', '--sweight', default='sw_sig',
                        help='specify the name of the sweight branch.')

    return parser.parse_args()


###########
# Helpers #
###########

def get_weights(histo, branches, bin_specs):
    bin_idx = []

    for br, spec in zip(branches, bin_specs):
        tmp_idx = np.digitize(br, spec) - 1
        # handle over/underflow
        tmp_idx = np.where(tmp_idx == -1, 0, tmp_idx)
        tmp_idx = np.where(tmp_idx >= spec.size-1, spec.size-2, tmp_idx)
        bin_idx.append(tmp_idx)

    return histo[tuple(bin_idx)]



if __name__ == '__main__':
    args = parse_input()
    ntp = recreate(args.output)

    histos = dict()
    brs_mc_stash = dict()

    # Additional global cuts
    ntracks = list(concatenate(
        f'{args.dataNtp}:{args.tree}', ['ntracks'], library='np'
    ).values())[0]
    global_cut = ntracks <= 450  # additional global cut
    #  global_cut = np.full(ntracks.size, True, dtype=bool)

    br_sw = list(concatenate(
        f'{args.dataNtp}:{args.tree}', [args.sweight], library='np'
    ).values())[0][global_cut]

    brs_w_mc_tmp = list(concatenate(
        [f'{i}:{args.tree}' for i in args.mcNtp], ['wpid', 'wtrk'], library='np'
    ).values())
    br_w_mc = brs_w_mc_tmp[0] * brs_w_mc_tmp[1]  # PID & tracking weights for MC

    for idx, (name, r) in enumerate(REWEIGHT_PROCEDURE.items()):
        brs_data = list(concatenate(
            f'{args.dataNtp}:{args.tree}', r.vars, library='np').values())
        brs_data = [d[global_cut] for d in brs_data]  # apply data global cut

        brs_mc = list(concatenate(
            [f'{i}:{args.tree}' for i in args.mcNtp],
            r.vars, library='np'
        ).values())
        brs_mc_stash[idx] = brs_mc

        h_data_raw = np.histogram2d(*brs_data, r.bins, r.range, weights=br_sw)

        if idx == 0:
            h_mc_raw = np.histogram2d(
                *brs_mc, r.bins, r.range, weights=br_w_mc)
        else:
            brs_mc_prev = brs_mc_stash[idx-1]
            mc_wt = get_weights(
                histos[idx-1][0], brs_mc_prev, histos[idx-1][1:])
            h_mc_raw = np.histogram2d(
                *brs_mc, r.bins, r.range, weights=br_w_mc*mc_wt)

        h_ratio_histo = h_data_raw[0] / h_mc_raw[0]
        h_ratio_histo = h_ratio_histo * (brs_mc[0].size / brs_data[0].size)
        h_ratio_histo = np.nan_to_num(
            h_ratio_histo, nan=0.0, posinf=0.0, neginf=0.0)
        h_ratio = (h_ratio_histo, h_data_raw[1], h_data_raw[2])

        ntp[f'{name}_data_raw'] = h_data_raw
        ntp[f'{name}_mc_raw'] = h_mc_raw
        ntp[name] = h_ratio
        histos[idx] = h_ratio

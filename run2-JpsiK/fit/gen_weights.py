#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Feb 24, 2022 at 02:03 AM -0500

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
    scale: Union[None, List[float]] = None

REWEIGHT_PROCEDURE = {
    'h_occupancy': RwtRule(['b_ownpv_ndof', 'ntracks'], [20, 20], [[1, 200], [0, 450]]),
    'h_kinematic': RwtRule(['b_pt', 'b_eta'], [20, 9], [[0, 25e3], [2, 5]], [1e3, 1.]),
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

    br_sw = list(concatenate(
        f'{args.dataNtp}:{args.tree}', [args.sweight], library='np'
    ).values())[0]

    for idx, (name, r) in enumerate(REWEIGHT_PROCEDURE.items()):
        brs_data = list(
            concatenate(f'{args.dataNtp}:{args.tree}', r.vars, library='np').values())
        brs_mc = list(concatenate(
            [f'{i}:{args.tree}' for i in args.mcNtp],
            r.vars, library='np'
        ).values())
        brs_mc_stash[idx] = brs_mc

        scales = [1.0]*len(brs_data) if not r.scale else r.scale
        for i, _ in enumerate(scales):
            brs_data[i] = scales[i]*brs_data[i]
            brs_mc[i] = scales[i]*brs_mc[i]

        h_data_raw = np.histogram2d(*brs_data, r.bins, r.range, weights=br_sw)

        if idx == 0:
            h_mc_raw = np.histogram2d(*brs_mc, r.bins, r.range)
        else:
            brs_mc_prev = brs_mc_stash[idx]
            mc_wt = get_weights(
                histos[idx-1][0], brs_mc_prev, histos[idx-1][1:])
            h_mc_raw = np.histogram2d(*brs_mc, r.bins, r.range)

        h_ratio_histo = h_data_raw[0] / h_mc_raw[0]
        h_ratio_histo = h_ratio_histo * (brs_mc[0].size / brs_data[0].size)
        h_ratio_histo = np.nan_to_num(
            h_ratio_histo, nan=0.0, posinf=0.0, neginf=0.0)
        h_ratio = (h_ratio_histo, h_data_raw[1], h_data_raw[2])

        ntp[f'{name}_data_raw'] = h_data_raw
        ntp[f'{name}_mc_raw'] = h_mc_raw
        ntp[name] = h_ratio
        histos[idx] = h_ratio
        old_key = name
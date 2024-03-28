#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri Mar 24, 2023 at 12:12 PM -0400

import numpy as np

from argparse import ArgumentParser
from dataclasses import dataclass
from uproot import concatenate, recreate

from typing import List, Union
from copy import deepcopy
from numpy.typing import ArrayLike


#################
# Configuration #
#################

@dataclass
class RwtRule:
    vars: List[str]
    bins: Union[ArrayLike, List[int], int]
    range: List[List[float]]


REWEIGHT_PROCEDURE = {
    'h_occupancy': RwtRule(['b_ownpv_ndof', 'ntracks'], [20, 20], [[1, 250], [0, 450]]),
    'h_kinematic': RwtRule(['b_pt', 'b_eta'], [20, 9], [[0, 30e3], [2, 6]]),
}

DATA_WTS = ['sw_sig']
MC_WTS = ['wtrk']
MC_CUTS = {'k_pid_k': 4, 'mu_pid_mu': 2, 'amu_pid_mu': 2}

#######################
# Command line parser #
#######################

def parse_input():
    parser = ArgumentParser(description='generate weights for sequential 2D reweighting.')

    parser.add_argument('-d', '--dataNtp', required=True, nargs='+',
                        help='specify data input ntuples, which must contains sWeight branches.')

    parser.add_argument('-m', '--mcNtp', required=True, nargs='+',
                        help='specify MC input ntuples.')

    parser.add_argument('-o', '--output', required=True,
                        help='specify output ntuple, which contains histograms.')

    parser.add_argument('-t', '--tree', default='tree',
                        help='specify the tree name in the input ntuple.')

    return parser.parse_args()


###########
# Helpers #
###########

def load_brs(ntp, tree, add_brs=None, extra_brs=None):
    br_names = [] if not add_brs else deepcopy(add_brs)
    for r in REWEIGHT_PROCEDURE.values():
        br_names += r.vars
    if extra_brs:
        for var in extra_brs:
            br_names += [var]
    return concatenate([f'{i}:{tree}' for i in ntp], br_names, library='np')


def gen_cut(brs, rule, extraCuts=None):
    cuts = []
    for idx, _ in enumerate(rule.vars):
        cuts.append(brs[rule.vars[idx]] < rule.range[idx][1])  # Cut out the maximum for ROOT compatibility
    if extraCuts:
        for var, val in extraCuts.items():
            cuts.append(brs[var] > val)
    return np.logical_and.reduce(cuts)


def apply_cut(brs, rule, extraCuts=None):
    cut = gen_cut(brs, rule, extraCuts)
    return {k: v[cut] for k, v in brs.items()}


def get_weights(brs_dict, histo_raw, rule_prev):
    histo, *bin_specs = histo_raw
    brs = [brs_dict[i] for i in rule_prev.vars]
    histo_padded = np.pad(histo, tuple((1, 1) for _ in range(histo.ndim)))
    bin_idx = tuple(np.digitize(br, spec)
                   for br, spec in zip(brs, bin_specs))

    # NOTE: Need to remove right edges in the prev histogram
    cut_prev = gen_cut(brs_dict, rule_prev)
    return histo_padded[bin_idx] * cut_prev


if __name__ == '__main__':
    args = parse_input()
    ntp = recreate(args.output)
    rules = dict()
    histos = dict()

    # Load branches
    brs_data_raw = load_brs(args.dataNtp, args.tree, add_brs=DATA_WTS)
    brs_mc_raw = load_brs(args.mcNtp, args.tree, add_brs=MC_WTS, extra_brs=MC_CUTS)

    for idx, (name, r) in enumerate(REWEIGHT_PROCEDURE.items()):
        rules[idx] = r

        # Remove rightmost edges in histogram to be compatible w/ ROOT
        brs_data = apply_cut(brs_data_raw, r)
        brs_mc = apply_cut(brs_mc_raw, r, MC_CUTS)
        rwt_brs_data = [brs_data[i] for i in r.vars]
        rwt_brs_mc = [brs_mc[i] for i in r.vars]

        # Build data histogram, sWeighted
        br_sw = brs_data[DATA_WTS[0]]
        h_data_raw = np.histogram2d(
            *rwt_brs_data, r.bins, r.range, weights=br_sw)
        h_data_raw_histo = h_data_raw[0]
        h_data_raw_histo[h_data_raw_histo < 0] = 0  # after sWeight, some bins may be negative

        # Build MC histogram, with global weights and weights from previous step
        br_w_mc = np.prod([brs_mc[i] for i in MC_WTS], axis=0)
        if idx == 0:
            mc_wt_final = br_w_mc
        else:
            # NOTE: here I'm being lazy. In principle we need to apply ALL
            # weights from ALL previous steps. J/psi K reweighting only has 2
            # steps though.
            mc_wt_prev = get_weights(brs_mc, histos[idx-1], rules[idx-1])
            mc_wt_final = br_w_mc * mc_wt_prev

        h_mc_no_wt = np.histogram2d(*rwt_brs_mc, r.bins, r.range)
        h_mc_raw = np.histogram2d(
            *rwt_brs_mc, r.bins, r.range, weights=mc_wt_final)

        # Normalize the histograms because we only care about shapes
        h_tmp = (h_data_raw[0] / h_mc_raw[0]) * (
            np.sum(h_mc_raw[0]) / np.sum(h_data_raw[0]))
        h_tmp_histo = (h_tmp, *h_data_raw[1:])
        h_ratio_histo = np.nan_to_num(h_tmp, nan=0.0, posinf=1.0, neginf=1.0)
        h_ratio = (h_ratio_histo, *h_data_raw[1:])
        histos[idx] = h_ratio

        # Save histograms
        ntp[f'{name}_data_raw'] = h_data_raw
        ntp[f'{name}_mc_raw'] = h_mc_raw
        ntp[f'{name}_mc_no_wt'] = h_mc_no_wt
        ntp[f'{name}_nan_kept'] = h_tmp_histo
        ntp[name] = h_ratio

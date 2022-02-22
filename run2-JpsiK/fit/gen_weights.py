#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Feb 22, 2022 at 11:52 AM -0500

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

    parser.add_argument('-m', '--mcNtp', required=True,
                        help='specify MC input ntuples.')

    parser.add_argument('-o', '--output', required=True,
                        help='specify output ntuple, which contains histograms.')

    parser.add_argument('-t', '--tree', default='tree',
                        help='specify the tree name in the input ntuple.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_input()
    ntp = recreate(args.output)

    for name, r in REWEIGHT_PROCEDURE.items():
        brs_data = list(
            concatenate(args.dataNtp, r.vars, library='np').values())
        brs_mc = list(
            concatenate(args.mcNtp, r.vars, library='np').values())

        scales = [1.0]*len(brs_data) if not r.scale else r.scale
        for i in range(0, len(scales)):
            brs_data[i] = scales[i]*brs_data[i]
            brs_mc[i] = scales[i]*brs_mc[i]

        h_data_raw = np.histogram2d(*brs_data, r.bins, r.range)
        h_mc_raw = np.histogram2d(*brs_mc, r.bins, r.range)

        h_ratio = (h_mc_raw[0]/h_data_raw[0], h_data_raw[1], h_data_raw[2])

        ntp[f'{name}_data_raw'] = h_data_raw
        ntp[f'{name}_mc_raw'] = h_mc_raw
        ntp[name] = h_ratio

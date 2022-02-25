#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Feb 24, 2022 at 10:56 PM -0500

import numpy as np

from argparse import ArgumentParser
from pyTuplingUtils.io import read_branches


def parse_input():
    parser = ArgumentParser(
        description='Print RDX skim (e.g. ISO) sizes in step-2 ntuples.')

    parser.add_argument('ntp', help='specify input ntuple.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_input()
    print('From ntuple: {}'.format(args.ntp))

    skims = ['ISO', '1OS', '2OS', 'DD']
    # skim_branches = read_branches(args.ntp, 'tree', ['is_normal & d_mass_window_ok & ' + 'is_'+i.lower() for i in skims])
    skim_branches = read_branches(args.ntp, 'tree', ['is_'+i.lower() for i in skims])

    for name, arr in zip(skims, skim_branches):
        cut = np.logical_and.reduce([arr])
        print('{:>6}: {:>12,}'.format(name, arr[cut].size))

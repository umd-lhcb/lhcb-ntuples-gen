#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sat Dec 18, 2021 at 03:29 AM +0100

import uproot
import numpy as np

from argparse import ArgumentParser
from pyTuplingUtils.io import read_branches, read_branch


def parse_input():
    parser = ArgumentParser(
        description='Print RDX skim (e.g. ISO) sizes in step-2 ntuples.')

    parser.add_argument('ntp', help='specify input ntuple.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_input()
    ntp = uproot.open(args.ntp)
    print('From ntuple: {}'.format(args.ntp))

    # By default apply the following cuts if they exist
    global_cuts = []
    if 'd_mass_window_ok' in ntp['tree']:
        global_cuts.append(read_branch(ntp, 'tree', 'd_mass_window_ok'))

    skims = ['ISO', '1OS', '2OS', 'DD']
    skim_branches = read_branches(ntp, 'tree', ['is_'+i.lower() for i in skims])

    for name, arr in zip(skims, skim_branches):
        cut = np.logical_and.reduce(global_cuts+[arr])
        print('{:>6}: {:>12,}'.format(name, arr[cut].size))

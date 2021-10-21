#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Oct 21, 2021 at 03:07 AM +0200

import uproot

from argparse import ArgumentParser
from pyTuplingUtils.io import read_branches


def parse_input():
    parser = ArgumentParser(
        description='Print RDX skim (e.g. ISO) sizes in step-2 ntuples.')

    parser.add_argument('ntp', help='specify input ntuple.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_input()
    ntp = uproot.open(args.ntp)
    print('From ntuple: {}'.format(args.ntp))

    skims = ['ISO', '1OS', '2OS', 'DD']
    skim_branches = read_branches(ntp, 'tree', ['is_'+i.lower() for i in skims])

    for name, arr in zip(skims, skim_branches):
        print('{:>6}: {:>12,}'.format(name, arr[arr].size))

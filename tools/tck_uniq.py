#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sun Jun 13, 2021 at 05:48 PM +0200
# NOTE: For tracker-only, the TCK branches are identically 0!

import uproot
import numpy as np

from argparse import ArgumentParser
from pyTuplingUtils.io import read_branches


################################
# Command line argument parser #
################################

def parse_input():
    parser = ArgumentParser(
        description='Find all unique L0-HLT1-HLT2 TCK combo in a given tree.')

    parser.add_argument('ntp', help='specify input ntuple.')

    parser.add_argument('tree', help='specify ntuple tree.')

    parser.add_argument('--l0', default='L0DUTCK',
                        help='specify L0 TCK branch.')

    parser.add_argument('--hlt1', default='HLT1TCK',
                        help='specify HLT1 TCK branch.')

    parser.add_argument('--hlt2', default='HLT2TCK',
                        help='specify HLT2 TCK branch.')

    return parser.parse_args()


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()
    ntp = uproot.open(args.ntp)

    tck_raw = read_branches(ntp, args.tree, (args.l0, args.hlt1, args.hlt2),
                            transpose=True)
    tck = list(map(lambda x: '-'.join([hex(i) for i in x]), tck_raw))
    tck_uniq = np.unique(tck)

    print('Unique TCKs (L0-HLT1-HLT2):')
    for t in tck_uniq:
        print(t)

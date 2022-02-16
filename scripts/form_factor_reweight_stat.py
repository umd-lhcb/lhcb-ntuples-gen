#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Feb 16, 2022 at 04:20 PM -0500
# NOTE: This is for checking on the

import sys
import re

from glob import glob
from pyTuplingUtils.io import read_branches

DDX_IDS = [
    11894600,
    12893600,
    11894200,
    12893610,
    11894610,
    12895400,
    11894210,
    12895000,
]


def get_mc_id(ntp_name):
    try:
        return int(re.search(r'_(\d\d\d\d\d\d\d\d)_', ntp_name).group(1))
    except Exception:
        return f'Unknown MC ID for file: {ntp_name}'


def get_ff_stat(ntp, tree):
    ham_ok, wff = read_branches(ntp, tree, ['ham_ok', 'wff'])
    print(f'    Reweight success rate: {ham_ok.sum()/ham_ok.size:.2f}')
    wff_ok = wff[ham_ok]
    details = f'    FF avg wt: {wff_ok.mean():.3f}, max wt: {wff_ok.max():.3f}'
    details += f', wt > 1 ratio: {wff_ok[wff_ok > 1].size / wff_ok.size:.2f}'
    print(details)


if __name__ == '__main__':
    ntps = glob(sys.argv[1])

    for n in ntps:
        mc_id = get_mc_id(n)
        print(f'MC ID: {mc_id}')

        if mc_id in DDX_IDS:
            print('  This is a DDX MC, skipping...')
            continue

        for t in ['TupleB0/DecayTree', 'TupleBminus/DecayTree']:
            print(f'  Tree: {t}')
            get_ff_stat(n, t)

#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Nov 01, 2021 at 04:06 AM +0100
# NOTE: This is for checking on the

import sys
import uproot
import re

from glob import glob
from pyTuplingUtils.io import read_branches


def get_mc_id(ntp_name):
    return re.search(r'_(\d\d\d\d\d\d\d\d)_', ntp_name).group(1)


def get_ff_stat(ntp, tree):
    ham_ok, wff = read_branches(ntp, tree, ['ham_ok', 'wff'])
    print(f'    HAMMER reweight success rate: {ham_ok.sum()/ham_ok.size:.2f}')
    wff_ok = wff[ham_ok]
    print(f'    FF avg wt: {wff_ok.mean():.3f}, max wt: {wff_ok.max():.3f}')
    print(f'    FF wt > 1 ratio: {wff_ok[wff_ok > 1].size / wff_ok.size:.2f}')


if __name__ == '__main__':
    ntps = glob(sys.argv[1])

    for n in ntps:
        mc_id = get_mc_id(n)

        if not mc_id:
            print(f'Cannot figure out MC ID for file: {n}')
        else:
            print(f'MC ID: {mc_id}')

        ntp = uproot.open(n)

        for t in ['TupleB0/DecayTree', 'TupleBminus/DecayTree']:
            print(f'  Tree: {t}')
            get_ff_stat(ntp, t)

#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Dec 29, 2021 at 04:36 AM +0100

import sys
import os.path as op

from glob import glob
from pyBabyMaker.base import TermColor as TC

sys.path.insert(0, op.dirname(op.abspath(__file__)))

from utils import (
    abs_path,
    check_ntp_name
)


###########
# Helpers #
###########

def validate_ntp(paths):
    error_counter = 0

    for p in paths:
        ntuples = glob(f'{abs_path(p)}/**/*.root', recursive=True)
        for ntp in ntuples:
            print(f'  Validating ntuple {ntp}...')
            _, _, errors = check_ntp_name(op.basename(ntp))
            if len(errors):
                print(f'{TC.BOLD+TC.RED}  ntuple {ntp} has an illegal name!{TC.END}')
                for name, value in errors.items():
                    print(f'    Field "{name}" has an illegal value "{value}"')

            error_counter += len(errors)

    return error_counter


#####################
# Validation config #
#####################

JOBS = {
    'ntuple': lambda: validate_ntp([
        '../ntuples',
        '../run1-rdx/samples',
        '../run2-rdx/samples',
    ])
}

tot_err = 0
for checker in JOBS.values():
    tot_err += checker()

if tot_err:
    print(f'{TC.BOLD+TC.RED}Total error(s): {tot_err}{TC.END}')

sys.exit(tot_err)

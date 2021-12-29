#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Dec 29, 2021 at 07:39 PM +0100

import sys
import os.path as op

from glob import glob
from pathlib import Path

sys.path.insert(0, op.dirname(op.abspath(__file__)))

from utils import TermColor as TC
from utils import (
    abs_path,
    check_ntp_name, check_rules
)


#########################
# Validation procedures #
#########################

RECO_MODES = ['std', 'mc', 'cutflow_data', 'cutflow_mc', 'mix', 'mu_misid']

NTP_FOLDER_FIELDS = [
    ('particles', False, lambda x: True),
    ('reco_mode', False, lambda x: x in RECO_MODES),
    ('additional_flags', True, lambda x: True)
]


def check_ntp_folder_name(foldername):
    return check_rules(foldername.split('-'), NTP_FOLDER_FIELDS)


############
# Wrappers #
############

def print_err(errors, msg_type, msg_obj):
    if len(errors):
        print(f'{TC.BOLD+TC.RED}  {msg_type} {msg_obj} has an illegal name!{TC.END}')
        for name, value in errors.items():
            print(f'    Field "{name}" has an illegal value "{value}"')


def validate_ntp(paths):
    tot_counter = 0
    err_counter = 0
    print('Validating ntuple filenames...')

    for p in paths:
        for ntp in glob(f'{abs_path(p)}/**/*.root', recursive=True):
            tot_counter += 1
            _, _, errors = check_ntp_name(op.basename(ntp))
            print_err(errors, 'ntuple', ntp)
            err_counter += len(errors)

    print(f'Validated {tot_counter} ntuples. Found {err_counter} error(s).')
    return err_counter


def validate_ntp_folder(paths):
    tot_counter = 0
    err_counter = 0
    print('Validating ntuple folder names...')

    folders = []
    for p in paths:
        for ntp in glob(f'{abs_path(p)}/**/*.root', recursive=True):
            # Always find the parent folder first
            parent_folder = Path(ntp).parent
            if parent_folder not in folders:
                folders.append(parent_folder)

    for f in folders:
        tot_counter += 1
        parent_folder = f.name

        if '.DST' in parent_folder:
            # Also need to check grandparent
            tot_counter += 1  # 2 folders to check
            _, gp_errors = check_ntp_folder_name(f.parent.name)
            print_err(gp_errors, 'ntuple folder', f.parent)
            err_counter += len(gp_errors)

            _, _, errors = check_ntp_name(parent_folder+'.root')  # Treat parent folder as a ntuple name

        else:
            _, errors = check_ntp_folder_name(parent_folder)

        print_err(errors, 'ntuple folder', f)
        err_counter += len(errors)

    print(f'Validated {tot_counter} ntuple folders. Found {err_counter} error(s).')
    return err_counter


#####################
# Validation config #
#####################

JOBS = {
    'ntuple': lambda: validate_ntp([
        '../ntuples',
        '../run1-rdx/samples',
        '../run2-rdx/samples',
    ]),
    'ntuple_folder': lambda: validate_ntp_folder(['../ntuples']),
}

tot_err = 0
for checker in JOBS.values():
    tot_err += checker()

if tot_err:
    print(f'{TC.BOLD+TC.RED}Total error(s): {tot_err}{TC.END}')

sys.exit(tot_err)

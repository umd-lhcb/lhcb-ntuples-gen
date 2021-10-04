#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Oct 04, 2021 at 05:23 PM +0200

import re
import yaml
import os
import os.path as os_path

from os import makedirs, chdir, symlink, getcwd, environ, pathsep
from datetime import datetime
from subprocess import check_output
from shutil import rmtree
from glob import glob

from pyBabyMaker.base import TermColor as TC


###################
# Generic helpers #
###################

def gen_date(fmt='%y_%m_%d'):
    return datetime.now().strftime(fmt)


def load_yaml_db(yaml_db=[
        'rdx/rdx-run2.yml',
        'rdx/rdx-run1.yml',
]):
    result = dict()
    base_path = os_path.abspath(os_path.dirname(__file__))

    for db in yaml_db:
        with open(os_path.join(base_path, db)) as f:
            result.update(yaml.safe_load(f))

    return result


def run_cmd_wrapper(only_print=False):
    def inner(cmd):
        print('  {}'.format(cmd))

        if not only_print:
            os.system(cmd)
    return inner


###############
# I/O helpers #
###############

def abs_path(path, base_path=__file__):
    return os_path.abspath(
        os_path.join(os_path.dirname(os_path.abspath(base_path)), path))


def ensure_dir(path, delete_if_exist=True, **kwargs):
    path = abs_path(path, **kwargs)

    if os_path.isdir(path):
        if delete_if_exist:
            rmtree(path)
            makedirs(path)

    else:
        makedirs(path)

    return path


def find_all_input(inputs, patterns=['*.root']):
    result = []
    for f in inputs:
        if os_path.isfile(f):
            result.append(os_path.abspath(f))
        elif os_path.isdir(f):
            for p in patterns:
                result += [os_path.abspath(g) for g in glob(os_path.join(f, p))]
    return result


#####################
# Execution helpers #
#####################

def aggragate_output(workdir, output_dir, keep):
    # Symbolic link generated files that match 'keep' patterns in separate
    # folders so that it's easier to find them.

    # NOTE: 'workdir' is usually the main workdir of the fulljob,
    #       'output_dir' the workdir of a subjob
    workdir = os_path.abspath(workdir)
    chdir(os_path.abspath(workdir))
    output_dir = os_path.abspath(output_dir)

    for d, patterns in keep.items():
        chdir(workdir)
        ensure_dir(d, False)
        chdir(d)
        relpath = os_path.relpath(output_dir, os_path.abspath('.'))

        for p in patterns:
            for f in glob(os_path.join(relpath, p)):
                symlink(f, os_path.join('.', os_path.basename(f)))


################################
# Ntuple filename manipulation #
################################

def generate_step2_name(ntp_name):
    try:
        _, _, reco_mode, add_flag, lfn = ntp_name.split('--')
    except ValueError:
        _, _, reco_mode, lfn = ntp_name.split('--')
        add_flag = None

    date = gen_date()
    db = load_yaml_db()

    polarity_trans = {'Up': 'u', 'Down': 'd'}
    polarity = 'm'+polarity_trans[re.search(r'Mag(Up|Down)', lfn).group(1)]

    if 'Real_Data' in lfn:
        year = '20' + re.search(r'_Collision(\d\d)_', lfn).group(1)
        decay_mode = 'data'
    else:
        year = re.search(r'_(\d\d\d\d)_', lfn).group(1)
        decay_mode = re.search(r'_(\d\d\d\d\d\d\d\d)_', lfn).group(1)

        if db.get(decay_mode):
            decay_mode = db[decay_mode]['Filename']
            # NOTE: Remember to remove useless strings in the 'Filename' key and
            # replace ',' with '__'

    fields = [date, reco_mode, decay_mode, year, polarity]
    if add_flag is not None:
        fields.append(add_flag)
    return '--'.join(fields)


def parse_step2_name(ntp_name):
    _, _, reco_mode, decay_mode, year, polarity, *add_flag = \
        ntp_name.split('--')

    date = gen_date()
    fields = [date, reco_mode, decay_mode, year, polarity]
    if add_flag:
        fields.append(add_flag[0])
    return '--'.join(fields)


#####################
# Generic workflows #
#####################

#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Oct 05, 2021 at 12:36 AM +0200

import re
import yaml
import shlex
import os.path as op  # Note: Can't use pathlib because that doesn't handle symbolic link well

from os import makedirs, chdir, symlink, system, pathsep, environ
from datetime import datetime
from subprocess import check_output
from shutil import rmtree
from glob import glob


################
# Path helpers #
################

def abs_path(path, base_path=op.abspath(op.dirname(__file__))):
    return op.abspath(op.join(base_path, path))


def append_path(paths):
    for p in paths:
        environ['PATH'] = pathsep.join([abs_path(p), environ['PATH']])


def with_suffix(path, ext):
    return op.splitext(path)[0] + ext


def ensure_dir(path, delete_if_exist=True, make_absolute=True, **kwargs):
    path = abs_path(path, **kwargs) if make_absolute else path

    if delete_if_exist and op.isdir(path):
        rmtree(path)

    makedirs(path)
    return path


def find_all_input(inputs, patterns=['*.root'], blocked_patterns=['__aux']):
    result = []
    if not isinstance(inputs, list):
        inputs = [inputs]

    for f in inputs:
        if op.isfile(f):
            result.append(op.abspath(f))
        elif op.isdir(f):
            for p in patterns:
                result += [op.abspath(g) for g in glob(op.join(f, p))]

    # Remove files that contains blocked patterns
    return [f for f in result if True not in [p in f for p in blocked_patterns]]


def aggragate_output(workdir, output_dir, keep):
    # Symbolic link generated files that match 'keep' patterns in separate
    # folders so that it's easier to find them.

    # NOTE: 'workdir' is usually the main workdir of the fulljob,
    #       'output_dir' the workdir of a subjob
    workdir = op.abspath(workdir)
    chdir(op.abspath(workdir))
    output_dir = op.abspath(output_dir)

    for d, patterns in keep.items():
        chdir(workdir)
        ensure_dir(d, False, False)
        chdir(d)
        relpath = op.relpath(output_dir, op.abspath('.'))

        for p in patterns:
            for f in glob(op.join(relpath, p)):
                symlink(f, op.join('.', op.basename(f)))


################
# MISC helpers #
################

def gen_date(fmt='%y_%m_%d'):
    return datetime.now().strftime(fmt)


def load_yaml_db(yaml_db=[
        'rdx/rdx-run1.yml',
        'rdx/rdx-run2.yml',
], base_path=abs_path('.')):
    result = dict()

    for db in yaml_db:
        with open(op.join(base_path, db)) as f:
            result.update(yaml.safe_load(f))

    return result


#####################
# Execution helpers #
#####################

def run_cmd_wrapper(only_print=False):
    def inner(cmd):
        print('  {}'.format(cmd))

        if not only_print:
            system(cmd)
    return inner


def run_cmd_with_output(cmd):
    cmd_splitted = shlex.split(cmd)
    return check_output(cmd_splitted).decode('utf-8').strip()


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

def workflow_compile_cpp(
        input_cpp, add_flags='-I{}'.format(abs_path('../include')),
        executor=run_cmd_wrapper()):
    compiler = run_cmd_with_output('root-config --cxx')
    base_flags = run_cmd_with_output('root-config --cflags')
    link_flags = run_cmd_with_output('root-config --libs')

    output_exe = with_suffix(input_cpp, '.exe')

    executor('{} {} {} -o {} {} {}'.format(
        compiler, base_flags, add_flags, output_exe, input_cpp, link_flags))

#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Apr 15, 2021 at 06:42 PM +0200

import os.path as os_path
import shlex

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


###############
# I/O helpers #
###############

def ensure_dir(path, delete_if_exist=True):
    if os_path.isdir(path):
        if delete_if_exist:
            rmtree(path)
            makedirs(path)

    else:
        makedirs(path)


def abs_path(path, base_path=__file__):
    return os_path.abspath(
        os_path.join(os_path.dirname(os_path.abspath(base_path)), path))


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

def pipe_executor(cmd, **kwargs):
    def operation(params, debug=False):
        args = [a.format(**params) for a in shlex.split(cmd)]
        if debug:
            print('{}DEBUG: Executing:{} {}'.format(
                TC.YELLOW, TC.END, ' '.join(args)))
        output = check_output(args, **kwargs).decode('utf-8')
        if output:
            print(output)

    return operation


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


def append_path(path=None):
    path = getcwd if path is None else abs_path(path)
    environ['PATH'] = pathsep.join([path, environ['PATH']])


################################
# Ntuple filename manipulation #
################################

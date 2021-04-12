#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Apr 12, 2021 at 10:38 PM +0200

import os.path as os_path
import shlex

from dataclasses import dataclass, field
from typing import Dict, List, Any
from os import makedirs, listdir, chdir, getcwd, environ, pathsep, symlink
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


##############
# Containers #
##############

def pipe_executor(cmd, **kwargs):
    def operation(keys, debug=False):
        args = [a.format(**keys) for a in shlex.split(cmd)]
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
    chdir(os_path.abspath(workdir))
    output_dir = os_path.abspath(output_dir)

    for d, patterns in keep.items():
        ensure_dir(d, False)
        chdir(d)
        relpath = os_path.relpath(output_dir, os_path.abspath('.'))

        for p in patterns:
            for f in glob(os_path.join(relpath, p)):
                symlink(f, os_path.join('.', os_path.basename(f)))


################################
# Ntuple filename manipulation #
################################

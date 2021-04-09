#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri Apr 09, 2021 at 02:42 AM +0200

import os.path as os_path
import shlex

from dataclasses import dataclass, field
from typing import Dict, List, Any
from os import makedirs, listdir, chdir, getcwd
from datetime import datetime
from subprocess import check_output
from shutil import rmtree

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
    if os_path.isdir(path) and delete_if_exist:
        rmtree(path)
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


@dataclass
class Executor:
    op: List
    filters: Dict[str, Any] = field(default_factory=dict)
    generic_filters: Dict[str, Any] = field(default_factory=dict)
    inputs: List = field(default_factory=list)
    keep: Dict[str, str] = field(default_factory=dict)


class Processor:
    def __init__(self, inputs, workdir, keep=None, debug=False):
        self.inputs = inputs
        self.workdir = workdir
        self.debug = debug
        self.keep = dict() if keep is None else keep
        self.outputs = {-1: inputs}

    def process(self, executors):
        print('{}Processing {}...{}'.format(TC.BOLD+TC.GREEN, self.workdir,
                                            TC.END))

        for idx, exe in enumerate(executors):
            self.keep.update(exe.keep)
            workdir = os_path.join(os_path.abspath(self.workdir), str(idx))
            ensure_dir(workdir)

            keys = self.gen_keys(exe)
            chdir(workdir)

            if self.debug:
                print('{}DEBUG: Dir: {}{}'.format(TC.YELLOW, TC.END, getcwd()))

            # Now execute all operations
            for op in exe.op:
                op(keys, self.debug)

            # Take a snapshot of the current working dir
            self.outputs[idx] = [os_path.join(workdir, f)
                                 for f in listdir(workdir)]

    def link_keep(self):
        # Symbolic link generated files that match 'keep' patterns in separate
        # folders so that it's easier to find them.
        pass

    def gen_keys(self, exe):
        keys_filters = {k: f(list(self.outputs.values())[-1])
                        for k, f in exe.filters.items()}
        keys_generic_filters = {k: f(self.outputs)
                                for k, f in exe.generic_filters.items()}
        keys_filters.update(keys_generic_filters)

        # Always flatten list
        for k, v in keys_filters.items():
            if isinstance(v, list):
                keys_filters[k] = ' '.join(v)

        if self.debug:
            for k, v in keys_filters.items():
                print('{}DEBUG: Key: {}{} : {}'.format(TC.YELLOW, TC.END, k, v))

        return keys_filters


################################
# Ntuple filename manipulation #
################################

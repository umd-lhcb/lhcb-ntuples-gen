#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Apr 07, 2021 at 11:57 PM +0200

import os.path as os_path

from dataclasses import dataclass
from typing import Dict, List, Any
from os import makedirs


###############
# I/O helpers #
###############

def ensure_dir(path, delete_if_exist=True):
    if not os_path.isdir(path) or delete_if_exist:
        makedirs(path)


def abs_path(path, base_path=__file__):
    return os_path.abspath(os_path.join(base_path, path))


##############
# Containers #
##############

@dataclass
class Executor:
    filter: List
    exec: List
    inputs: List
    generic_filter: List = []
    keep: Dict[str, str] = dict()


class Processor:
    def __init__(self, inputs, workdir, keep=[]):
        self.input = inputs
        self.workdir = workdir
        self.keep = keep
        self.outputs = {-1: inputs}

    def process(self, executors):
        for idx, exe in enumerate(executors):
            self.keep.update(exe.keep)

    def link_keep(self):
        # Symbolic link generated files that match 'keep' patterns in separate
        # folders so that it's easier to find them.
        pass


################################
# Ntuple filename manipulation #
################################

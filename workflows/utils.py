#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Apr 07, 2021 at 05:22 PM +0200

from dataclasses import dataclass
from typing import Dict, List, Any


##############
# Containers #
##############

@dataclass
class Executor:
    filter: List
    exec: List
    generic_filter: List = []
    keep: Dict[str, str] = dict()


@dataclass
class Processor:
    input: Dict[int, List[str]]
    output: Dict[int, List[str]]
    workdir: str
    keep: List[str] = []

    def process(self, executors):
        for exe in executors:
            self.keep.update(exe.keep)

    def link_keep(self):
        # Symbolic link generated files that match 'keep' patterns in separate
        # folders so that it's easier to find them.
        pass

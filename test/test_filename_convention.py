#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Jun 11, 2020 at 12:48 AM +0800

from glob import glob
from pathlib import Path
from os.path import basename
from sys import exit


#################
# Configuration #
#################

NAMES_TO_CHECK = {
    'ntuple_file': ('**/*.root', lambda x: Path(x).stem),
    'ntuple_folder': ('**/*.root', lambda x: basename(Path(x).parents[0])),
    'dst_folder': ('**/*.dst', lambda x: basename(Path(x).parents[0])),
    'log_file': ('**/*.log', lambda x: Path(x).stem),
    'cond_file': ('**/cond-*.py', lambda x: Path(x).stem),
}


#################
# Filename glob #
#################

def glob_pattern(pattern, regulator):
    result = []

    for f in glob(pattern, recursive=True):
        name = regulator(f)
        if name not in result:
            result.append(name)

    return result


def glob_all(rules=NAMES_TO_CHECK):
    result = {}

    for name, rule in rules.items():
        result[name] = glob_pattern(*rule)

    return result


if __name__ == '__main__':

    a = glob_all()
    print(a)
    exit(0)

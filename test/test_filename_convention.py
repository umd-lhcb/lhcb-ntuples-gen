#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Jun 10, 2020 at 11:35 PM +0800

from glob import glob
from pathlib import Path
from os.path import basename


#################
# Configuration #
#################

NAMES_TO_CHECK = {
    'root_file': ('**/*.root', lambda x: Path(x).stem),
    'dst_folder': ('**/*.dst', lambda x: basename(Path(x).parents[0]))
}


###########
# Helpers #
###########

def glob_pattern(pattern, regulator):
    result = []

    for f in glob(pattern):
        name = regulator(f)
        if name not in result:
            result.append(name)

    return result


def glob_all(rules):
    result = {}

    for key, rule in rules.items():
        result[key] = glob_pattern(*rule)

    return result

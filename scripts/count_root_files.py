#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Aug 25, 2020 at 12:00 AM +0800

import sys
import json

from os import walk, popen


def find_all_subdirs(cur_dir, return_self=False):
    dirs = [x[0] for x in walk(cur_dir)]
    return dirs if return_self else dirs[1:]


def find_annex_info(dirs):
    return [
        json.load(popen('git annex info --fast --json --bytes {}'.format(d)))
        for d in dirs]


if __name__ == '__main__':
    dirs = find_all_subdirs(sys.argv[1])
    dirs_annex_info = find_annex_info(dirs)

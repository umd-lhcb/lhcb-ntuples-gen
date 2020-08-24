#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Aug 25, 2020 at 12:47 AM +0800

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


def file_size_prettifier(size):
    size = int(size)
    units = ['KiB', 'MiB', 'GiB']

    for unit in units:
        size = size / 1024
        if size <= 1 or len(str(int(size))) <= 3:
            break

    return (size, unit)


def print_output(annex_info):
    for i in annex_info:
        tot_size, tot_unit = file_size_prettifier(
            i['size of annexed files in working tree'])
        loc_size, loc_unit = file_size_prettifier(i['local annex size'])

        print('{:4d} .root   total: {:6.2f} {}   local: {:6.2f} {}   {}'.format(
            i['annexed files in working tree'],
            tot_size, tot_unit,
            loc_size, loc_unit,
            i['directory']
        ))


if __name__ == '__main__':
    dirs = find_all_subdirs(sys.argv[1])
    dirs_annex_info = find_annex_info(dirs)
    print_output(dirs_annex_info)

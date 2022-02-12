#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sat Feb 12, 2022 at 04:16 AM -0500

import json

from os import walk, popen
from argparse import ArgumentParser


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def parse_input():
    parser = ArgumentParser('''
list annexed ntuple sizes in all subdirectories.''')

    parser.add_argument('cur_dir',
                        help='''
specify directory.''')

    parser.add_argument('-s', '--exclude-self',
                        action='store_true',
                        help='''
not include current directory.''')

    return parser.parse_args()


def find_all_subdirs(cur_dir, exclude_self=False):
    dirs = [x[0] for x in walk(cur_dir)]
    return dirs if not exclude_self else dirs[1:]


def find_annex_info(dirs):
    return [
        json.load(popen('git annex info --fast --json --bytes {}'.format(d)))
        for d in dirs]


def file_size_prettifier(size):
    size = int(size)
    units = ['KiB', 'MiB', 'GiB']
    unit = ''

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

        print('{}{:4d}{} .root   total: {}{:6.2f} {}{}   local: {}{:6.2f} {}{}   '.format(
            Color.BOLD, i['annexed files in working tree'], Color.END,
            Color.BOLD, tot_size, tot_unit, Color.END,
            Color.BOLD, loc_size, loc_unit, Color.END,
        ) + Color.BLUE + Color.BOLD + i['directory'] + Color.END)


if __name__ == '__main__':
    args = parse_input()
    dirs = find_all_subdirs(args.cur_dir, args.exclude_self)
    dirs_annex_info = find_annex_info(dirs)
    print_output(dirs_annex_info)

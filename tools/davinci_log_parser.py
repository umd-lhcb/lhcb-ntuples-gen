#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu May 27, 2021 at 04:16 AM +0200

from __future__ import print_function

import re
import sys

from argparse import ArgumentParser
from collections import OrderedDict as odict
from glob import glob


################################
# Command line argument parser #
################################

def parse_input():
    parser = ArgumentParser(description='''
Parse and merge DaVinci log file stats, mainly for cutflow studies.
''')

    parser.add_argument('output_yml',
                        help='''
output YAML file.
''')

    parser.add_argument('input_log',
                        nargs='+',
                        help='''
input log files.
''')

    return parser.parse_args()


#############
# Filtering #
#############

def fltr_regex(filename, pattern=r'^TimingAuditor\.T\.\.\.\s+INFO\s+\w'):
    with open(filename) as f:
        result = [line for line in f if bool(re.match(pattern, line))]

    return result


def strip_regex(lst, pattern=r'^TimingAuditor\.T\.\.\.   INFO'):
    return [re.sub(pattern, '', i) for i in lst]


###################
# Data extraction #
###################

def normalize_data(lst):
    result = []

    for line in lst:
        data = line.split('|')[:-1]
        if len(data) > 1:
            data_normalized = [data[0].strip()]
            failed_col = 0

            for d in data[1:]:
                try:
                    num = float(d.strip())
                    data_normalized.append(num)
                except ValueError:
                    failed_col += 1
                    data_normalized.append(None)

            if failed_col < 2:
                result.append(data_normalized)

    return result


def extract_data(lst, name_idx=0, num_idx=4):
    result = odict()

    for idx, data in enumerate(lst):
        num_in = int(data[num_idx])

        try:
            num_out = int(lst[idx+1][num_idx])
            if num_out > num_in:
                num_out = None
        except Exception:
            num_out = None

        name = data[name_idx]
        result[name] = {'input': num_in, 'output': num_out}

    return result


###########
# Helpers #
###########

def update_dict(orig, new):
    for key, items in new.items():
        if type(items) in [dict, odict]:
            try:
                update_dict(orig[key], items)
            except KeyError:
                orig[key] = items
        else:
            try:
                orig[key] += items
            except Exception:
                orig[key] = items


def yaml_gen(data, indent='', indent_increment=' '*4):
    result = ''
    for key, items in data.items():
        result += '{}{}:'.format(indent, key)
        if type(items) in [dict, odict]:
            result += '\n'
            result += yaml_gen(items, indent=indent+indent_increment)
        elif items is None:
            result += ' null\n'
        else:
            result += ' {}\n'.format(items)
    return result


def file_parse(filename):
    data = fltr_regex(filename)
    data = strip_regex(data)
    data = normalize_data(data)
    return extract_data(data)


def glob_logfiles(files):
    log_filepaths = []
    for log in files:
        log_filepaths += glob(log)
    return log_filepaths


if __name__ == '__main__':
    args = parse_input()
    result = odict()

    for log_filename in glob_logfiles(args.input_log):
        parsed = file_parse(log_filename)
        update_dict(result, parsed)

    with open(args.output_yml, 'w') as f:
        f.write(yaml_gen(result))

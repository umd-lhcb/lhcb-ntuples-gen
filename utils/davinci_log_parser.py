#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Mar 03, 2020 at 05:03 PM +0800

import re
import sys

from collections import OrderedDict as odict


#############
# Filtering #
#############

def fltr_regex(filename, pattern=r'^TimingAuditor\.T\.\.\.'):
    with open(filename) as f:
        result = [l for l in f if bool(re.match(pattern, l))]

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


def extract_data(lst,
                 name_idx=0,
                 num_idx=4,
                 names=['SELECT:Phys/StdAllNoPIDsKaons',
                        'SELECT:Phys/StdAllNoPIDsPions',
                        'SelMyD0',
                        'SELECT:Phys/StdAllLoosePions',
                        'SelMyDst',
                        'SELECT:Phys/StdAllNoPIDsMuons',
                        'SelMyB0'
                        ],
                 last_name='SelMyRefitB02DstMu'):
    result = odict()

    for idx, data in enumerate(lst):
        if data[name_idx] in names:
            name = data[name_idx]
            num_in = int(data[num_idx])
            num_out = int(lst[idx+1][num_idx])
            result[name] = {'input': num_in, 'output': num_out}

        elif data[name_idx] == last_name:
            name = data[name_idx]
            num_in = int(data[num_idx])
            num_out = None
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
            except KeyError:
                orig[key] = items


def yaml_gen(data, indent='', indent_increment=' '*4):
    result = ''
    for key, items in data.items():
        result += '{}{}:'.format(indent, key)
        if type(items) in [dict, odict]:
            result += '\n'
            result += yaml_gen(items, indent=indent+indent_increment)
        else:
            result += ' {}\n'.format(items)
    return result


def file_parse(filename):
    data = fltr_regex(filename)
    data = strip_regex(data)
    data = normalize_data(data)
    return extract_data(data)


if __name__ == '__main__':
    output = sys.argv[1]
    result = odict()

    for log_filename in sys.argv[2:]:
        parsed = file_parse(log_filename)
        update_dict(result, parsed)

    with open(output, 'w') as f:
        f.write(yaml_gen(result))

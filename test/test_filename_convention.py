#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Jun 11, 2020 at 01:09 PM +0800

from datetime import datetime
from re import match

from glob import glob
from pathlib import Path
from os.path import basename

from sys import exit


##################
# Files to check #
##################

FILES_TO_CHECK = {
    'ntuple_file': ('**/*.root', lambda x: Path(x).stem),
    'ntuple_folder': ('**/*.root', lambda x: Path(x).parents[0]),
    'dst_folder': ('**/*.dst', lambda x: basename(Path(x).parents[0])),
    'log_file': ('**/*.log', lambda x: Path(x).stem),
    'cond_file': ('**/cond-*.py', lambda x: Path(x).stem),
}


####################################
# Define validation for each field #
####################################

def validate_date(s, date_fmt='%y_%m_%d'):
    try:
        datetime.strptime(s, date_fmt)
        return True
    except ValueError:
        return False


def validate_additional_flags(s, general_valid_pattern=r'^\w+$',
                              valid_patterns=[
                                  r'^dv\d+$',
                                  r'^py\d$',
                                  r'^sim\d+\w$',
                                  r'^step2$',
                                  r'^subset$',
                              ]):
    tot_err = 0
    fields = s.split('-')
    err_fields = []

    for f in fields:
        if True not in [bool(match(p, f)) for p in valid_patterns]:
            if not bool(match(general_valid_pattern, f)):
                tot_err += 1
                err_fields.append(f)

    if tot_err > 0:
        print('These fields are illegal: {}'.format(','.join(err_fields)))
        return False
    else:
        return True


ALLOWED_IN_FIELD = {
    'reco_sample': lambda x: x in ['Dst', 'D0', 'Dst_D0'],
    'date': validate_date,
    'type': lambda x: x in [
        'std',
        'mc',
        'cutflow_data',
        'cutflow_mc',
    ],
    'sample': lambda x: x in [
        'data',
        'cocktail',
        'all',
        # MC modes
        'Bd2DstTauNu',
    ],
    'year': lambda x: x in ['20'+str(i) for i in range(11, 70)],
    'polarity': lambda x: x in ['mu', 'md'],
    'dirac_path': lambda x: True if ' ' not in x else False,
    'additional_flags': validate_additional_flags,
}


def check_all_field(fields, allowed_in_field=ALLOWED_IN_FIELD):
    tot_err = 0

    for f, v in fields.items():
        if not allowed_in_field[f](v):
            tot_err += 1
            print('Field "{}" with value "{}" illegal.'.format(f, v))

    return not tot_err


######################################
# Validation rules for each filetype #
######################################

def field_dict_gen(possible_fields, actual_fields):
    return {possible_fields[i]: v for i, v in enumerate(actual_fields)}


def validate_ntuple_file_name(f):
    fields = f.split('--')

    if 'Beam' in fields[-1]:  # step 1 naming scheme
        fields_to_check = {
            k: fields[i] for i, k in enumerate(['reco_sample', 'date', 'type'])}
        fields_to_check['dirac_path'] = fields[-1]
        if len(fields) > 4:
            fields_to_check['additional_flags'] = fields[3]

    else:  # step 2 naming scheme
        fields_to_check = field_dict_gen([
            'reco_sample',
            'date',
            'type',
            'sample',
            'year',
            'polarity',
            'additional_flags'
        ], fields)

    result = check_all_field(fields_to_check)
    if not result:
        print('ntuple filename: {} is invalid.'.format(f))

    return not result


def validate_log_file_name(f):
    fields = f.split('-')
    fields_to_check = field_dict_gen([
        'reco_sample',
        'date',
        'type',
        'additional_flags'
    ], fields)

    result = check_all_field(fields_to_check)
    if not result:
        print('log filename: {} is invalid.'.format(f))

    return not result


NAMING_CONVENTIONS = {
    'ntuple_file': lambda x: [validate_ntuple_file_name(i) for i in x],
    'log_file': lambda x: [validate_log_file_name(i) for i in x],
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


def glob_all(files_to_check):
    result = {}

    for name, rule in files_to_check.items():
        result[name] = glob_pattern(*rule)

    return result


if __name__ == '__main__':
    files_to_check = glob_all({k: FILES_TO_CHECK[k]
                               for k in NAMING_CONVENTIONS.keys()})

    err_stauts = {k: NAMING_CONVENTIONS[k](v)
                  for k, v in files_to_check.items()}
    tot_err = sum([sum(v) for k, v in err_stauts.items()])
    exit(tot_err)

#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Oct 06, 2021 at 03:31 PM +0200

from datetime import datetime
from re import match, sub, search

from glob import glob
from pathlib import Path
from os.path import basename

from sys import exit as sys_exit


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

IGNORED_PATHS = ['lib', 'gen', 'studies', 'run2-rdx/reweight']


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
                                  r'^step\d+\.?\d*$',
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

    return True


def validate_year(years):
    tot_err = 0
    valid_years = ['20'+str(i) for i in range(11, 70)]

    for y in years.split('-'):
        if y not in valid_years:
            tot_err += 1

    return not tot_err > 0


RECO_SAMPLES = ['Dst', 'D0', 'Dst_D0']
TYPES = ['std', 'mc',
         'cutflow_data', 'cutflow_mc',
         'validation',
         'mix',
         'mu_misid']
SAMPLES = [
    'data', 'cocktail', 'all',
    # MC modes
    r'Bd\w.*',
    r'Bu\w.*',
]

ALLOWED_IN_FIELD = {
    'reco_sample': lambda x: x in RECO_SAMPLES,
    'date': validate_date,
    'type': lambda x: x in TYPES,
    'sample': lambda x: True in [bool(search(p, x)) for p in SAMPLES],
    'year': validate_year,
    'polarity': lambda x: x in ['mu', 'md', 'md-mu'],  # NOTE: We don't allow 'mu-md'
    'dirac_path': lambda x: ' ' not in x,
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
    try:
        return {possible_fields[i]: v for i, v in enumerate(actual_fields)}
    except IndexError:
        print('IndexError: possible fields: {}'.format(possible_fields))
        print('            actual fields: {}'.format(actual_fields))


class ValidateWrapper():
    def __init__(self, filetype):
        self.filetype = filetype

    def __call__(self, f):
        def wrapped(input_filename):
            result = check_all_field(f(input_filename))
            if not result:
                print('{}: {} is invalid.'.format(
                    self.filetype, input_filename))

            return not result
        return wrapped


@ValidateWrapper('ntuple filename')
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

    return fields_to_check


@ValidateWrapper('log filename')
def validate_log_file_name(f):
    return field_dict_gen([
        'reco_sample',
        'date',
        'type',
        'additional_flags'
    ], f.split('-'))


@ValidateWrapper('cond filename')
def validate_cond_file_name(f):
    fields = sub(r'^cond-', '', f).split('-')

    # NOTE: Because cond files uses '-' for both inter- and intra-separators,
    # this workaround is needed.
    if len(fields) > 3 and 'std' not in fields:
        fields = fields[0:3] + ['-'.join(fields[3:])]
    elif len(fields) >= 3 and 'std' in fields:
        fields = fields[0:2] + ['md-mu'] + ['-'.join(fields[2:])]

    return field_dict_gen([
        'type',
        'year',
        'polarity',
        'additional_flags'
    ], fields)


def validate_ntuple_folder_name(f):
    valid_first_lvl = [
        'ntuples',
        'gen',
        'run1-rdx',
        'run2-rdx',
    ]
    valid_second_lvl = [
        r'^samples$',
        r'^pre-0.9.0$',
        r'\d\.\d\.\d-\w+$',
        r'^run\d-\w+-step\d$',
        r'^ref-rdx-run1$',
        r'^test$',
    ]
    valid_mode = [p+'-'+m for p in RECO_SAMPLES for m in TYPES]

    field_dict = field_dict_gen([
        'first_lvl',
        'second_lvl',
        'mode'
    ], str(f).split('/'))
    err = False

    if 'second_lvl' not in field_dict:
        print('WARNING: ntuple exist in unexpected location: {}'.format(f))
        return err

    if field_dict['first_lvl'] not in valid_first_lvl or \
            True not in [bool(match(p, field_dict['second_lvl']))
                         for p in valid_second_lvl] or \
            ('mode' in field_dict.keys() and
             field_dict['mode'] not in valid_mode):
        err = True

    if err:
        print('ntuple folder: {} is not valid.'.format(f))
        return True  # NOTE: True means some error is detected.

    return err


@ValidateWrapper('dst folder')
def validate_dst_folder_name(f):
    fields = f.split('-')

    # NOTE: Because dst folder uses '-' for both inter- and intra-separators,
    # this workaround is needed.
    if len(fields) > 3:
        fields = fields[0:3] + ['-'.join(fields[3:])]

    return field_dict_gen([
        'sample',
        'year',
        'polarity',
        'additional_flags'
    ], fields)


NAMING_CONVENTIONS = {
    'ntuple_file': lambda x: [validate_ntuple_file_name(i) for i in x],
    'log_file': lambda x: [validate_log_file_name(i) for i in x],
    'cond_file': lambda x: [validate_cond_file_name(i) for i in x],
    'ntuple_folder': lambda x: [validate_ntuple_folder_name(i) for i in x],
    'dst_folder': lambda x: [validate_dst_folder_name(i) for i in x],
}


#################
# Filename glob #
#################

def glob_pattern(pattern, regulator, ignore=IGNORED_PATHS):
    result = []

    for f in glob(pattern, recursive=True):
        if f not in result:
            result.append(f)

    result = filter(lambda x: True not in [x.startswith(i) for i in ignore],
                    result)
    return [regulator(f) for f in result]


def glob_all(files_to_check):
    result = {}

    for name, rule in files_to_check.items():
        result[name] = glob_pattern(*rule)

    return result


if __name__ == '__main__':
    files_to_check = glob_all({k: FILES_TO_CHECK[k]
                               for k in NAMING_CONVENTIONS})

    err_stauts = {k: NAMING_CONVENTIONS[k](v)
                  for k, v in files_to_check.items()}
    tot_err = sum([sum(v) for k, v in err_stauts.items()])
    sys_exit(tot_err)

#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Dec 30, 2021 at 05:08 AM +0100

import re
import yaml
import shlex
import os.path as op  # Note: Can't use pathlib because that doesn't handle symbolic link well

from os import makedirs, chdir, symlink, system, pathsep
from datetime import datetime
from subprocess import check_output
from shutil import rmtree
from glob import glob
from inspect import getfullargspec
from pathlib import Path


######
# UI #
######

class TermColor:
    """
    Color sequences for UNIX terminal.
    """
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


################
# Path helpers #
################

def abs_path(path, base_path=op.abspath(op.dirname(__file__))):
    return op.abspath(op.join(base_path, path))


def with_suffix(path, ext):
    return op.splitext(path)[0] + ext


def ensure_dir(path, delete_if_exist=True, make_absolute=True, **kwargs):
    path = abs_path(path, **kwargs) if make_absolute else path

    if delete_if_exist and op.isdir(path):
        rmtree(path)

    try:
        makedirs(path)
    except FileExistsError:
        pass

    return path


def ensure_file(path, dir_replacement={'ntuples': 'ntuples_ext'}):
    if Path(path).exists():
        return path

    if dir_replacement:
        for src, tgt in dir_replacement.items():
            path = path.replace(src, tgt)

        ensure_file(path, None)

    raise ValueError(f'File not exist: {path}.')


def find_all_input(inputs,
                   patterns=['*.root'], blocked_patterns=['--aux'],
                   make_absolute=True):
    result = []
    if not isinstance(inputs, list):
        inputs = [inputs]
    if make_absolute:
        inputs = [abs_path(p) for p in inputs]

    for f in inputs:
        if op.isfile(f):
            result.append(op.abspath(f))
        elif op.isdir(f):
            for p in patterns:
                result += [op.abspath(g) for g in glob(op.join(f, p))]

    # Remove files that contains blocked patterns
    return [f for f in result if True not in [p in f for p in blocked_patterns]]


def aggregate_fltr(blocked=[], keep=[r'\.root'], debug=False):
    def inner(filename):
        filename = op.basename(filename)
        if debug:
            print(filename)

        for p in blocked:
            if bool(re.search(p, filename)):
                if debug:
                    print('Matched to pattern: {}'.format(p))
                return False

        for p in keep:
            if bool(re.search(p, filename)):
                if debug:
                    print('Matched to pattern: {}'.format(p))
                return True

        if debug:
            print('The file is neither blocked or kept. Ignoring it...')

        return False

    return inner


def aggregate_output(workdir, output_dir, keep):
    # Symbolic link generated files that match 'keep' patterns in separate
    # folders so that it's easier to find them.

    # NOTE: 'workdir' is usually the main workdir of the fulljob,
    #       'output_dir' the workdir of a subjob
    workdir = op.abspath(workdir)
    chdir(workdir)
    output_dir = op.abspath(output_dir)

    for d, fltr in keep.items():
        chdir(workdir)
        ensure_dir(d, False, False)
        chdir(d)
        relpath = op.relpath(output_dir, op.abspath('.'))

        for obj in glob(op.join(relpath, '*')):
            if fltr(obj):
                try:
                    symlink(obj, op.join('.', op.basename(obj)))
                except FileExistsError:
                    pass


################
# MISC helpers #
################

DATE_FMT = '%y_%m_%d'


def gen_date(fmt=DATE_FMT):
    return datetime.now().strftime(fmt)


def load_yaml_db(yaml_db=[
        'rdx/rdx-run1.yml',
        'rdx/rdx-run2.yml',
], base_path=abs_path('.')):
    result = dict()

    for db in yaml_db:
        with open(op.join(base_path, db)) as f:
            result.update(yaml.safe_load(f))

    return result


def filter_kwargs_func(kwargs, func):
    kw_func = getfullargspec(func).args
    return {k: kwargs[k] for k in kw_func if k in kwargs}


# NOTE: This is used to make wrapped functions taking all kwargs and only use
#       the ones needed by the wrapped function.
#
#       The implementation is admittedly a bit convoluted and if you don't
#       understand, try play with this decorator in an interactive Python shell
#       with:
#           python -i ./utils.py
#       The define:
#           @smart_kwarg
#           def f(a=1, b=2):
#               print(a-b)
def smart_kwarg(*args):
    def _smart_kwarg(func):
        def inner(*args, **kwargs):
            known_kws = filter_kwargs_func(kwargs, func)
            for k in add_kws:
                if k in kwargs:
                    known_kws[k] = kwargs[k]

            return func(*args, **known_kws)
        return inner

    if len(args) == 1 and callable(args[0]):
        add_kws = ['executor']
        return _smart_kwarg(args[0])

    add_kws = args[0]
    return _smart_kwarg


#####################
# Execution helpers #
#####################

def run_cmd_wrapper(only_print=False):
    def inner(cmd):
        print('  {}'.format(cmd))

        if not only_print:
            system(cmd)
    return inner


def run_cmd_with_output(cmd):
    cmd_splitted = shlex.split(cmd)
    return check_output(cmd_splitted).decode('utf-8').strip()


######################
# Naming conventions #
######################

def validate_date(date, fmt=DATE_FMT):
    try:
        datetime.strptime(date, fmt)
        return True
    except ValueError:
        return False


def validate_year(years):
    tot_err = 0
    valid_years = ['20'+str(i) for i in range(11, 70)]

    for y in years.split('-'):
        if y not in valid_years:
            tot_err += 1

    return not tot_err > 0


def validate_reco_mode(mode):
    return mode in ['std', 'mc', 'cutflow_data', 'cutflow_mc',
                    'mix', 'mu_misid']


def check_rules(fields, rules):
    required_rules = [i for i in rules if not i[1]]
    optional_rules = [i for i in rules if i[1]]

    result = dict()
    errors = dict()

    # First pass, only check required fields
    for name, _, checker in required_rules:
        rule_ok = False
        field = None

        for idx, field in enumerate(fields):
            rule_ok = checker(field)
            if rule_ok:
                result[name] = field
                fields.pop(idx)
                break

        if not rule_ok:
            errors[name] = field

    for name, _, checker in optional_rules:
        # If there's no additional field to consume, skip all optional rules
        rule_ok = len(fields) == 0

        for idx, field in enumerate(fields):
            rule_ok = checker(field)
            if rule_ok:
                result[name] = field
                fields.pop(idx)
                break

    if len(fields) > 0:
        errors['unconsumed_field'] = '; '.join(fields)

    # Let's reorder the result s.t. the ordering is consistent w/ rule ordering
    final_result = {n: result[n] for n, _, _ in rules if n in result}
    return final_result, errors


# We check if a ntuple name is legal here

NTP_STEP1_FIELDS = [
    ('particles', False, lambda x: True),  # The boolean indicates if the field is optional
    ('date', False, validate_date),
    ('reco_mode', False, validate_reco_mode),
    ('additional_flags', True, lambda x: not x.startswith('aux')),
    ('dirac_path', False, lambda x: '.DST' in x),
    ('index', True, lambda x: '-dv' in x),
    ('aux', True, lambda x: x.startswith('aux')),
]

NTP_STEP2_FIELDS = [
    ('particles', False, lambda x: True),
    ('date', False, validate_date),
    ('reco_mode', False, validate_reco_mode),
    ('input_data', False, lambda x: True),
    ('year', False, validate_year),
    ('polarity', False, lambda x: x in ['md', 'mu', 'md-mu']),
    ('additional_flags', True, lambda x: True),
]


def check_ntp_name(filename):
    is_step1 = '.DST' in filename
    rules = NTP_STEP1_FIELDS if is_step1 else NTP_STEP2_FIELDS
    fields = with_suffix(filename, '').split('--')

    result, errors = check_rules(fields, rules)
    return result, is_step1, errors


################################
# Ntuple filename manipulation #
################################

def find_year(filename):
    patterns = [r'_Collision(\d\d)_', r'--20(\d\d[-\d]*)--', r'MC_20(\d\d)_']

    for p in patterns:
        search = re.search(p, filename)
        if search:
            return '20' + search.group(1)

    raise ValueError("Can't find year from {}!".format(filename))


def find_polarity(filename):
    if 'MagDown' in filename or '--md--' in filename:
        return 'md'
    if 'MagUp' in filename or '--mu--' in filename:
        return 'mu'
    return 'md-mu'


def generate_step2_name(ntp_name, convert_mc_id=False):
    try:
        _, _, reco_mode, add_flag, lfn = ntp_name.split('--')
    except ValueError:
        _, _, reco_mode, lfn = ntp_name.split('--')
        add_flag = None

    date = gen_date()
    db = load_yaml_db()

    polarity_trans = {'Up': 'u', 'Down': 'd'}
    polarity = 'm'+polarity_trans[re.search(r'Mag(Up|Down)', lfn).group(1)]

    if 'Real_Data' in lfn:
        year = '20' + re.search(r'_Collision(\d\d)_', lfn).group(1)
        decay_mode = 'data'
    else:
        year = re.search(r'_(\d\d\d\d)_', lfn).group(1)
        decay_mode = re.search(r'_(\d\d\d\d\d\d\d\d)_', lfn).group(1)

        if convert_mc_id and db.get(decay_mode):
            decay_mode = db[decay_mode]['Filename']
            # NOTE: Remember to remove useless strings in the 'Filename' key and
            # replace ',' with '__'

    fields = [date, reco_mode, decay_mode, year, polarity]
    if add_flag is not None:
        fields.append(add_flag)
    return '--'.join(fields)


def parse_step2_name(ntp_name):
    ntp_name = ntp_name.strip('.root')
    _, _, reco_mode, decay_mode, year, polarity, *add_flag = \
        ntp_name.split('--')

    date = gen_date()
    fields = [date, reco_mode, decay_mode, year, polarity]
    if add_flag:
        fields.append(add_flag[0])
    return '--'.join(fields)


#####################
# Generic workflows #
#####################

def workflow_compile_cpp(
        input_cpp, add_flags='-I{}'.format(abs_path('../include')),
        executor=run_cmd_wrapper()):
    compiler = run_cmd_with_output('root-config --cxx')
    base_flags = run_cmd_with_output('root-config --cflags')
    link_flags = run_cmd_with_output('root-config --libs')

    output_exe = with_suffix(input_cpp, '.exe')

    executor('{} {} {} -o {} {} {}'.format(
        compiler, base_flags, add_flags, output_exe, input_cpp, link_flags))


def workflow_cached_ntuple(
        cmd, input_ntp, output_ntp, cache_suffix,
        executor=run_cmd_wrapper()):
    cached_ntp = with_suffix(input_ntp, '') + cache_suffix + '.root'

    if op.isfile(cached_ntp):
        print('Aux ntuple already cached!')
        symlink(cached_ntp, output_ntp)
    else:
        print('No aux ntuple cached, generating anew...')
        cmd = [cmd] if not isinstance(cmd, list) else cmd
        for c in cmd:
            executor(c)

        print('Creating an alias for generated ntuple...')
        cached_ntp_base = op.basename(cached_ntp)
        try:
            symlink(output_ntp, './'+cached_ntp_base)
        except FileNotFoundError:
            pass

    return output_ntp


def workflow_apply_weight(input_ntp, histo_folder, config,
                          output_ntp, cache_suffix,
                          **kwargs):
    histo_folder = abs_path(histo_folder)
    config = abs_path(config)

    year = find_year(input_ntp)
    polarity = find_polarity(input_ntp)

    # The executable is in 'scripts' folder!
    cmd = f'apply_histo_weight.py {input_ntp} {histo_folder} {output_ntp} -c {config} --year {year} --polarity {polarity}'
    workflow_cached_ntuple(
        cmd, input_ntp, output_ntp, cache_suffix, **kwargs)
    return output_ntp

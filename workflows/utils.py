#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Sep 13, 2022 at 01:24 AM -0400

import re
import yaml
import shlex
import sys
import fnmatch
import os.path as op  # NOTE: Can't use pathlib because that doesn't handle symbolic link well

from os import makedirs, chdir, system
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


def download_file(path, fail_on_download_error=True):
    print(f'{path} not present locally, downloading with git-annex...')
    ret_val = run_cmd(f'git annex get {path}')

    if ret_val:
        print(f'Failed to download: {path}')

        if fail_on_download_error:
            sys.exit(255)


def ensure_file(path):
    if Path(path).exists():
        return path
    if not op.exists(path):
        download_file(path)
        return path


def find_all_input(inputs,
                   patterns=['*.root'], blocked_patterns=['--aux'],
                   make_absolute=True):
    result = []
    if not isinstance(inputs, list):
        inputs = [inputs]
    if make_absolute:
        inputs = [abs_path(p) for p in inputs]

    matched = []
    for i in inputs:
        matched.extend(glob(i))

    for f in matched:
        if op.islink(f) or op.isfile(f):  # allow broken symblink to pass
            result.append(op.abspath(f))
        elif op.isdir(f):
            for p in patterns:
                result += [op.abspath(g) for g in glob(op.join(f, p))]
                if re.search(fnmatch.translate(p), f):  # Allow dirs to be matched
                    result.append(f)

    # Remove files that contains blocked patterns
    return [f for f in result if True not in
            [bool(re.search(p, f)) for p in blocked_patterns]]


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
#       Then define:
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
        add_kws = ['debug']
        return _smart_kwarg(args[0])

    add_kws = args[0]
    return _smart_kwarg


#####################
# Execution helpers #
#####################

@smart_kwarg
def run_cmd(cmd, debug=False, with_output=False):
    if debug:
        print(f'  {cmd}')

    if with_output:
        return check_output(shlex.split(cmd)).decode('utf-8').strip()

    if not debug:
        return system(cmd)


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
                    'mix', 'mu_misid',
                    'ghost', 'ghost1', 'ghost2', 'ghost_norm']


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
        rule_ok = len(fields) == 0  # If there's no field to consume, skip all optional rules

        for idx, field in enumerate(fields):
            rule_ok = checker(field)
            if rule_ok:
                result[name] = field
                fields.pop(idx)
                break

    if len(fields) > 0:
        errors['unconsumed_field'] = '; '.join(fields)

    # Let's reorder the result s.t. the ordering is consistent w/ rule ordering
    return {n: result[n] for n, _, _ in rules if n in result}, errors


NTP_STEP1_FIELDS = [
    ('particles', False, lambda x: True),  # The boolean indicates if the field is optional
    ('date', False, validate_date),
    ('reco_mode', False, validate_reco_mode),
    ('additional_flags', True,
     lambda x: not x.startswith('aux') and not x[0].isdigit()),
    ('lfn', False, lambda x: '.DST' in x and '__aux' not in x),
    ('index', True, lambda x: '-dv' in x and x[0].isdigit()),
    ('aux', True, lambda x: x.startswith('aux')),
]

NTP_STEP2_FIELDS = [
    ('particles', False, lambda x: True),
    ('date', False, validate_date),
    ('reco_mode', False, validate_reco_mode),
    ('decay_mode', False, lambda x: True),
    ('year', False, validate_year),
    ('polarity', False, lambda x: x in ['md', 'mu', 'md-mu']),
    ('additional_flags', True, lambda x: True),
    ('index', True, lambda x: x.isdecimal()),
    ('aux', True, lambda x: x.startswith('aux')),
]


def check_ntp_name(filename):
    is_step1 = '.DST' in filename
    rules = NTP_STEP1_FIELDS if is_step1 else NTP_STEP2_FIELDS
    fields = with_suffix(filename, '').split('--')

    result, errors = check_rules(fields, rules)
    return result, errors, is_step1


################################
# Ntuple filename manipulation #
################################

def find_year(filename):
    patterns = [r'_Collision(\d\d)_', r'--20(\d\d[-\d]*)--', r'MC_20(\d\d)_']

    for p in patterns:
        search = re.search(p, filename)
        if search:
            return '20' + search.group(1)

    raise ValueError(f"Can't find year from {filename}!")


def find_polarity(filename):
    if 'MagDown' in filename or '--md--' in filename:
        return 'md'
    if 'MagUp' in filename or '--mu--' in filename:
        return 'mu'
    return 'md-mu'


def find_decay_mode(lfn, convert_mc_id=False):
    if 'Real_Data' in lfn:
        return 'data'

    decay_mode = re.search(r'_(\d\d\d\d\d\d\d\d)_', lfn).group(1)

    if convert_mc_id:
        # NOTE: Here we convert 8-digit MC ID to a human-readable decay mode
        # NOTE: Remember to remove useless strings in the 'Filename' key and
        #       replace ',' with '__' in the YAML files.
        db = load_yaml_db()
        return db[decay_mode]['Filename']

    return decay_mode


def generate_step2_name(ntp_name,
                        convert_mc_id=False, keep_index=True, date=None):
    ntp_name = op.basename(ntp_name)
    fields, errors, is_step1 = check_ntp_name(ntp_name)
    if len(errors) > 0:
        raise ValueError(f'ntuple name {ntp_name} is NOT a legal name!')

    date = gen_date() if not date else date  # Need to have a consistent date!
    reco_mode = fields['reco_mode']

    if is_step1:
        polarity = find_polarity(ntp_name)
        year = find_year(ntp_name)
        decay_mode = find_decay_mode(fields['lfn'], convert_mc_id)
    else:
        polarity, year = fields['polarity'], fields['year']
        _decay_mode = fields['decay_mode']
        if _decay_mode == 'data' or not _decay_mode[0].isdigit():
            decay_mode = _decay_mode
        else:
            decay_mode = find_decay_mode(f'_{_decay_mode}_')

    output = [date, reco_mode, decay_mode, year, polarity]
    if 'additional_flags' in fields:
        output.append(fields['additional_flags'])
    if keep_index and 'index' in fields:
        step2_idx = re.search(r'(\d+)', fields['index']).group(1)
        output.append(step2_idx)
    return '--'.join(output)


#####################
# Generic workflows #
#####################

def aggregate_fltr(blocked=[], keep=[r'\.root'], debug=False):
    def inner(filename):
        filename = op.basename(filename)
        if debug:
            print(filename)

        for p in blocked:
            if bool(re.search(p, filename)):
                if debug:
                    print('Matched to blocked pattern: {}'.format(p))
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


def aggregate_output(workdir, output_dir, keep, debug=False):
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
                run_cmd(f'ln -s {op.abspath(obj)} {op.basename(obj)}', debug)


@smart_kwarg
def workflow_compile_cpp(
        input_cpp, add_flags='-I{}'.format(abs_path('../include')),
        **kwargs):
    compiler = run_cmd('root-config --cxx', with_output=True, **kwargs)
    base_flags = run_cmd('root-config --cflags', with_output=True, **kwargs)
    link_flags = run_cmd('root-config --libs', with_output=True, **kwargs)

    output_exe = with_suffix(input_cpp, '.exe')
    run_cmd(f'{compiler} {base_flags} {add_flags} -o {output_exe} {input_cpp} {link_flags}', **kwargs)


@smart_kwarg
def workflow_cached_ntuple(cmd, input_ntp, output_ntp, cache_suffix,
                           **kwargs):
    cached_ntp = with_suffix(input_ntp, '') + cache_suffix + '.root'

    print("\n== workflow_cached_ntuple ==")
    print("cached_ntp: "+cached_ntp)

    if op.isfile(cached_ntp):
        print('Aux ntuple already cached!')
        run_cmd(f'ln -s {cached_ntp} {output_ntp}', **kwargs)
    elif op.islink(cached_ntp):
        download_file(cached_ntp)
        print('Aux ntuple cached and downloaded')
        run_cmd(f'ln -s {cached_ntp} {output_ntp}', **kwargs)
    else:
        print('No aux ntuple cached, generating anew...')
        cmd = [cmd] if not isinstance(cmd, list) else cmd
        for c in cmd:
            run_cmd(c, **kwargs)

        print('Creating an alias for generated ntuple...')
        run_cmd(f'ln -s {output_ntp} ./{op.basename(cached_ntp)}', **kwargs)

    return output_ntp


def workflow_apply_weight(input_ntp, histo_folder, config,
                          output_ntp, cache_suffix,
                          **kwargs):
    histo_folder = abs_path(histo_folder)
    config = abs_path(config)

    year = find_year(input_ntp)
    polarity = find_polarity(input_ntp)

    # NOTE: The 'apply_histo_weight.py' is in 'scripts' folder!
    cmd = f'apply_histo_weight.py {input_ntp} {histo_folder} {output_ntp} -c {config} --year {year} --polarity {polarity}'
    return workflow_cached_ntuple(
        cmd, input_ntp, output_ntp, cache_suffix, **kwargs)


@smart_kwarg([])
def workflow_prep_dir(job_name, inputs,
                      output_dir=abs_path('../gen'),
                      patterns=['*.root'],
                      blocked_patterns=['--aux'],
                      delete_if_exist=True,
                      ):
    TC = TermColor
    print('{}==== Job: {} ===={}'.format(TC.BOLD+TC.GREEN, job_name, TC.END))

    # Need to figure out the absolute path
    input_files = find_all_input(inputs, patterns, blocked_patterns)
    if not input_files:
        print("{}Can't find any file with the pattern '{}'{}".format(
            TC.BOLD+TC.RED, inputs, TC.END))
        sys.exit(1)

    subworkdirs = {op.splitext(op.basename(i))[0]
                   if op.isfile(i) else op.basename(i): i for i in input_files}

    # Now ensure the working dir
    workdir = ensure_dir(
        op.join(output_dir, job_name), delete_if_exist=delete_if_exist)

    return subworkdirs, workdir


def workflow_split_base(inputs, input_yml, job_name='split', prefix='Dst_D0',
                        workflow_data=None, workflow_mc=None,
                        **kwargs):
    date = gen_date()  # NOTE: Need a consistent date!
    subworkdirs, workdir = workflow_prep_dir(
        job_name, inputs, patterns=['*.DST'], **kwargs)

    for subjob, input_dir in subworkdirs.items():
        subflow = workflow_mc if 'MC_' in subjob or 'mc' in subjob \
            else workflow_data
        subflow(
            input_dir, input_yml, job_name=subjob, output_dir=workdir,
            date=date, **kwargs)

    # Let's manually aggregate output
    chdir(workdir)
    makedirs('ntuple')
    makedirs('ntuple_aux')
    for sj in subworkdirs:
        run_cmd(f'mv {sj}/ntuple ntuple/{prefix}--{generate_step2_name(sj+".root", date=date)}', **kwargs)
        run_cmd(f'mv {sj}/ntuple_aux ntuple_aux/{sj}', **kwargs)

    # Also merge ntuples
    makedirs('ntuple_merged')
    uniq_names = set(generate_step2_name(sj+'.root', keep_index=False,
                                         date=date)
                     for sj in subworkdirs)
    with open(abs_path(input_yml), 'r') as f:
        yml_config = yaml.safe_load(f)
    merge_prefix = list(yml_config['output'].keys())

    for name in uniq_names:
        for p in merge_prefix:
            if glob(f'ntuple/*/{p}--{name}--*.root'):
                print(f'Merging prefix {p} of {name}...')
                run_cmd(f'hadd -fk ntuple_merged/{p}--{name}.root ntuple/*/{p}--{name}--*.root', **kwargs)

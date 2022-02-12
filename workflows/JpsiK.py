#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sat Feb 12, 2022 at 04:41 PM -0500

import sys
import os.path as op

from argparse import ArgumentParser
from os import chdir, makedirs
from functools import partial

from pyBabyMaker.base import TermColor as TC

sys.path.insert(0, op.dirname(op.abspath(__file__)))

from utils import (
    run_cmd,
    abs_path, ensure_dir, find_all_input,
    aggregate_fltr, aggregate_output, check_ntp_name, find_decay_mode,
    smart_kwarg,
    generate_step2_name,
    workflow_apply_weight
)

from rdx import workflow_single_ntuple as workflow_single_ntuple_rdx


#################################
# Command line arguments parser #
#################################

def parse_input():
    parser = ArgumentParser(description='workflow for J/psi K reweighting.')

    parser.add_argument('job_name', help='specify job name.')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug mode.')

    return parser.parse_args()


###########
# Helpers #
###########

JpsiK_default_fltr = aggregate_fltr(
    keep=[r'^(JpsiK).*\.root'], blocked=['--aux'])

JpsiK_default_output_fltrs = {
    'ntuple': JpsiK_default_fltr,
    'ntuple_aux': aggregate_fltr(keep=['--aux']),
}


####################################
# Workflows: aux ntuple generation #
####################################

@smart_kwarg
def workflow_pid(
        input_ntp, output_ntp='pid.root',
        pid_histo_folder='../run2-rdx/reweight/pid/root-run2-rdx_oldcut',
        pid_config='../run2-rdx/reweight/pid/run2-rdx_oldcut.yml',
        **kwargs):
    return workflow_apply_weight(input_ntp, pid_histo_folder, pid_config,
                                 output_ntp, '--aux_pid', **kwargs)


@smart_kwarg
def workflow_trk(
        input_ntp, output_ntp='trk.root',
        trk_histo_folder='../run2-rdx/reweight/tracking/root-run2-general',
        trk_config='../run2-rdx/reweight/tracking/run2-general.yml',
        **kwargs):
    return workflow_apply_weight(input_ntp, trk_histo_folder, trk_config,
                                 output_ntp, '--aux_trk', **kwargs)


#######################
# Workflows: wrappers #
#######################

def workflow_single_ntuple(input_ntp, input_yml, output_suffix, aux_workflows,
                           cpp_template='../postprocess/cpp_templates/JpsiK.cpp',
                           **kwargs):
    workflow_single_ntuple_rdx(
        input_ntp, input_yml, output_suffix, aux_workflows,
        cpp_template=cpp_template, **kwargs)


@smart_kwarg([])
def workflow_prep_dir(job_name, inputs,
                      output_dir=abs_path('../gen'),
                      patterns=['*.root'],
                      blocked_patterns=['--aux'],
                      ):
    print('{}==== Job: {} ===={}'.format(TC.BOLD+TC.GREEN, job_name, TC.END))

    # Need to figure out the absolute path
    input_files = find_all_input(inputs, patterns, blocked_patterns)
    subworkdirs = {op.splitext(op.basename(i))[0]
                   if op.isfile(i) else op.basename(i): i for i in input_files}

    # Now ensure the working dir
    workdir = ensure_dir(op.join(output_dir, job_name))

    return subworkdirs, workdir


###################
# Workflows: main #
###################

def workflow_data(inputs, input_yml, job_name='data', **kwargs):
    aux_workflows = []
    subworkdirs, workdir = workflow_prep_dir(job_name, inputs, **kwargs)
    chdir(workdir)

    for subdir, input_ntp in subworkdirs.items():
        ensure_dir(subdir, make_absolute=False)
        chdir(subdir)  # Switch to the workdir of the subjob

        output_suffix = generate_step2_name(input_ntp)
        workflow_single_ntuple(
            input_ntp, input_yml, output_suffix, aux_workflows, **kwargs)

        aggregate_output('..', subdir, JpsiK_default_output_fltrs)
        chdir('..')  # Switch back to parent workdir


def workflow_mc(inputs, input_yml, job_name='mc',
                **kwargs):
    aux_workflows = [workflow_pid, workflow_trk]
    subworkdirs, workdir = workflow_prep_dir(job_name, inputs, **kwargs)
    chdir(workdir)

    for subdir, input_ntp in subworkdirs.items():
        ensure_dir(subdir, make_absolute=False)
        chdir(subdir)  # Switch to the workdir of the subjob

        fields = check_ntp_name(input_ntp)[0]
        if 'decay_mode' in fields:
            decay_mode = fields['decay_mode']
        else:
            decay_mode = find_decay_mode(fields['lfn'])

        output_suffix = generate_step2_name(input_ntp)
        workflow_single_ntuple(
            input_ntp, input_yml, output_suffix, aux_workflows,
            cli_vars={'cli_mc_id': decay_mode},
            **kwargs)

        aggregate_output('..', subdir, JpsiK_default_output_fltrs)
        chdir('..')  # Switch back to parent workdir


def workflow_split(inputs, input_yml, job_name='split',
                   **kwargs):
    subworkdirs, workdir = workflow_prep_dir(
        job_name, inputs, patterns=['*.DST'], **kwargs)

    for subjob, input_dir in subworkdirs.items():
        subflow = workflow_mc if 'MC_' in subjob or 'mc' in subjob \
            else workflow_data
        subflow(
            input_dir, input_yml, job_name=subjob, output_dir=workdir, **kwargs)

    # Let's manually aggregate output
    chdir(workdir)
    makedirs('ntuple')
    makedirs('ntuple_aux')
    for subjob in subworkdirs:
        run_cmd(f'mv {subjob}/ntuple ntuple/{generate_step2_name(subjob+".root")}', **kwargs)
        run_cmd(f'mv {subjob}/ntuple_aux ntuple_aux/{subjob}', **kwargs)


#####################
# Production config #
#####################

JOBS = {
    # Run 2
    # Run 2 debug
    'JpsiK-ntuple-run2-data-demo': partial(
        workflow_data,
        '../run2-JpsiK/samples/JpsiK--22_02_09--std--data--2016--md--dv45-subset.root',
        '../postprocess/JpsiK-run2/JpsiK-run2.yml',
    ),
}

args = parse_input()

if args.job_name in JOBS:
    JOBS[args.job_name](job_name=args.job_name, debug=args.debug)
else:
    print('Unknown job name: {}'.format(args.job_name))

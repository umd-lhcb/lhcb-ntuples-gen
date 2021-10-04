#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Oct 05, 2021 at 12:37 AM +0200

import sys
import os
import os.path as op

from argparse import ArgumentParser, Action
from os import chdir

from pyBabyMaker.base import TermColor as TC

sys.path.insert(0, op.dirname(op.abspath(__file__)))

from utils import (
    run_cmd_wrapper,
    append_path, abs_path, ensure_dir, find_all_input, aggragate_output,
    generate_step2_name, parse_step2_name,
    workflow_compile_cpp
)


#################################
# Command line arguments parser #
#################################

def parse_input():
    parser = ArgumentParser(description='workflow for R(D(*)).')

    parser.add_argument('job_name', help='''
specify job name.
''')

    parser.add_argument('-d', '--debug', action='store_true', help='''
enable debug mode
''')

    return parser.parse_args()


#############
# Workflows #
#############

def workflow_data_mc(job_name, inputs,
                     output_dir=abs_path('../gen'),
                     patterns=['*.root'],
                     blocked_patterns=['__aux'],
                     executor=run_cmd_wrapper()
                     ):
    print('{}== Job: {} =={}'.format(TC.BOLD+TC.GREEN, job_name, TC.END))

    # Need to figure out the absolute path
    input_files = find_all_input(inputs, patterns, blocked_patterns)
    subworkdirs = {op.splitext(op.basename(i))[0]: i
                   for i in input_files}

    # Now ensure the working dir
    workdir = ensure_dir(op.join(output_dir, job_name))

    return subworkdirs, workdir, executor


def workflow_data(job_name, inputs, input_yml,
                  output_ntp_name_gen=generate_step2_name, **kwargs):
    subworkdirs, workdir, executor = workflow_data_mc(
        job_name, inputs, **kwargs)
    chdir(workdir)
    cpp_template = abs_path('../postprocess/cpp_templates/rdx.cpp')

    for subdir, full_filename in subworkdirs.items():
        print('{}Working on {}...{}'.format(TC.GREEN, full_filename, TC.END))
        ensure_dir(subdir, make_absolute=False)
        chdir(subdir)  # Switch to the workdir of the subjob

        executor('babymaker -i {} -o baby.cpp -n {} -t {}'.format(
            abs_path(input_yml), full_filename, cpp_template))
        workflow_compile_cpp('baby.cpp')

        # aggragate_output('..', subdir, {
            # 'ntuple': ['*--std--*.root']
        # })
        chdir('..')  # Switch back to parent workdir


# def workflow_mc(job_name, inputs, output_dir, debug, kws,
                # script='mc.sh', output_ntp_name_gen=generate_step2_name):

                     # path_to_append=[
                         # '../lib/python/TrackerOnlyEmu/scripts'
                     # ],
    # subworkdirs, workdir = workflow_general(job_name, inputs, output_dir)
    # chdir(workdir)
    # exe = pipe_executor(
        # script + ' ' + '"{input_ntp}" "{input_yml}" "{output_suffix}"')

    # for subdir, full_filename in subworkdirs.items():
        # print('{}Working on {}...{}'.format(TC.GREEN, full_filename, TC.END))
        # ensure_dir(subdir)
        # chdir(subdir)  # Switch to the workdir of the subjob

        # params = {
            # 'input_ntp': full_filename,
            # 'input_yml': kws['input_yml'],
            # 'output_suffix': output_ntp_name_gen(full_filename)
        # }
        # exe(params, debug)

        # aggragate_output('..', subdir, {
            # 'ntuple': ['*--mc--*.root']
        # })

        # chdir('..')  # Switch back to parent workdir


#####################
# Production config #
#####################

args = parse_input()
executor = run_cmd_wrapper(args.debug)

JOBS = {
    'rdx-ntuple-run2-oldcut': lambda name: workflow_data(
        name,
        '../ntuples/0.9.4-trigger_emulation/Dst_D0-std',
        '../postprocess/rdx-run2/rdx-run2_with_run1_cuts.yml',
        executor=run_cmd_wrapper(args.debug)
    ),
}


if args.job_name in JOBS:
    JOBS[args.job_name](args.job_name)
else:
    print('Unknown job name: {}'.format(args.job_name))

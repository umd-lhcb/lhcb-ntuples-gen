#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Oct 05, 2021 at 03:21 AM +0200

import sys
import os
import os.path as op

from argparse import ArgumentParser, Action
from os import chdir
from shutil import rmtree

from pyBabyMaker.base import TermColor as TC

sys.path.insert(0, op.dirname(op.abspath(__file__)))

from utils import (
    run_cmd_wrapper,
    append_path, abs_path, ensure_dir, find_all_input, aggragate_output,
    generate_step2_name, parse_step2_name,
    workflow_compile_cpp, workflow_cached_ntuple
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


######################
# Workflows: helpers #
######################

def workflow_ubdt(input_ntp,
                  trees=['TupleB0/DecayTree', 'TupleBminus/DecayTree'],
                  **kwargs):
    weight_file = abs_path('../run2-rdx/weights_run2_no_cut_ubdt.xml')
    cmd = 'addUBDTBranch {} mu_isMuonTight {} ubdt.root {}'.format(
        input_ntp, weight_file, ' '.join(trees))
    workflow_cached_ntuple(cmd, input_ntp, **kwargs)
    try:
        rmtree('./weights')
    except FileNotFoundError:
        pass


def workflow_hammer(input_ntp,
                    trees=['TupleB0/DecayTree', 'TupleBminus/DecayTree'],
                    **kwargs):
    run = 'run1' if '2011' in input_ntp or '2012' in input_ntp else 'run2'
    cmd = ['ReweightRDX '+input_ntp+' hammer.root '+t+' '+run for t in trees]
    workflow_cached_ntuple(
        cmd, input_ntp, output_ntp='hammer.root', cache_suffix='__aux_hammer',
        **kwargs)


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


#############
# Workflows #
#############

def workflow_data(job_name, inputs, input_yml,
                  use_ubdt=True,
                  output_ntp_name_gen=generate_step2_name, **kwargs):
    subworkdirs, workdir, executor = workflow_data_mc(
        job_name, inputs, **kwargs)
    chdir(workdir)
    cpp_template = abs_path('../postprocess/cpp_templates/rdx.cpp')

    for subdir, input_ntp in subworkdirs.items():
        print('{}Working on {}...{}'.format(TC.GREEN, input_ntp, TC.END))
        ensure_dir(subdir, make_absolute=False)
        chdir(subdir)  # Switch to the workdir of the subjob

        if use_ubdt:
            # Generate a ubdt ntuple
            workflow_ubdt(input_ntp, executor=executor)
            bm_cmd = 'babymaker -i {} -o baby.cpp -n {} -t {} -f ubdt.root'
        else:
            bm_cmd = 'babymaker -i {} -o baby.cpp -n {} -t {}'

        executor(bm_cmd.format(abs_path(input_yml), input_ntp, cpp_template))
        workflow_compile_cpp('baby.cpp', executor=executor)

        output_suffix = output_ntp_name_gen(input_ntp)
        executor('./baby.exe --{}'.format(output_suffix))

        aggragate_output('..', subdir, {
            'ntuple': ['*--std--*.root', 'Dst*.root', 'D0*.root']
        })
        chdir('..')  # Switch back to parent workdir


def workflow_mc(job_name, inputs, input_yml,
                output_ntp_name_gen=generate_step2_name, **kwargs):
    subworkdirs, workdir, executor = workflow_data_mc(
        job_name, inputs, **kwargs)
    chdir(workdir)
    cpp_template = abs_path('../postprocess/cpp_templates/rdx.cpp')

    for subdir, input_ntp in subworkdirs.items():
        print('{}Working on {}...{}'.format(TC.GREEN, input_ntp, TC.END))
        ensure_dir(subdir, make_absolute=False)
        chdir(subdir)  # Switch to the workdir of the subjob

        # Generate a HAMMER ntuple
        workflow_hammer(input_ntp, executor=executor)

        executor('babymaker -i {} -o baby.cpp -n {} -t {} -f hammer.root'.format(
            abs_path(input_yml), input_ntp, cpp_template))
        workflow_compile_cpp('baby.cpp', executor=executor)

        output_suffix = output_ntp_name_gen(input_ntp)
        executor('./baby.exe --{}'.format(output_suffix))

        aggragate_output('..', subdir, {
            'ntuple': ['*--mc--*.root', 'Dst*.root', 'D0*.root']
        })
        chdir('..')  # Switch back to parent workdir


#####################
# Production config #
#####################

args = parse_input()
executor = run_cmd_wrapper(args.debug)

JOBS = {
    # Run 2
    'rdx-ntuple-run2-data-oldcut': lambda name: workflow_data(
        name,
        '../ntuples/0.9.4-trigger_emulation/Dst_D0-std',
        '../postprocess/rdx-run2/rdx-run2_with_run1_cuts.yml',
        executor=executor
    ),
    'rdx-ntuple-run2-mc-demo': lambda name: workflow_mc(
        name,
        '../run2-rdx/samples/Dst_D0--21_07_30--mc--Bd2DstMuNu--2016--md--py8-sim09j-dv45-subset.root',
        '../postprocess/rdx-run2/rdx-run2_with_run1_cuts.yml',
        output_ntp_name_gen=parse_step2_name,
        executor=executor
    ),
    # Run 1
    'rdx-ntuple-run1-data': lambda name: workflow_data(
        name,
        '../ntuples/0.9.2-2011_production/Dst_D0-std',
        '../postprocess/rdx-run1/rdx-run1.yml',
        use_ubdt=False,
        executor=executor
    ),
    'ref-rdx-ntuple-run1-data': lambda name: workflow_data(
        name,
        '../ntuples/ref-rdx-run1/Dst-mix',
        '../postprocess/ref-rdx-run1/rdst-2011-mix.yml',
        use_ubdt=False,
        output_ntp_name_gen=parse_step2_name,
        executor=executor
    )
}


if args.job_name in JOBS:
    JOBS[args.job_name](args.job_name)
else:
    print('Unknown job name: {}'.format(args.job_name))

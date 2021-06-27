#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sun Jun 27, 2021 at 02:47 AM +0200

import sys
import os
import os.path as os_path

from argparse import ArgumentParser, Action
from os import chdir

from pyBabyMaker.base import TermColor as TC

sys.path.insert(0, os_path.dirname(os_path.abspath(__file__)))

from utils import (
    abs_path, ensure_dir, find_all_input, append_path, pipe_executor,
    aggragate_output,
    generate_step2_name, parse_step2_name
)


#################################
# Command line arguments parser #
#################################

class AddKwsAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict(kv.split(':') for kv in values))


def parse_input():
    parser = ArgumentParser(description='workflow for R(D(*)).')

    parser.add_argument('job_name', help='''
specify job name.
''')

    parser.add_argument('inputs', nargs='+', help='''
specify initial input files.
''')

    parser.add_argument('-d', '--debug', action='store_true', help='''
enable debug mode
''')

    parser.add_argument('-m', '--mode', required=True, help='''
specify workflow mode.
''')

    parser.add_argument('-o', '--output-dir',
                        default=abs_path('../gen'), help='''
specify output dir.
''')

    parser.add_argument('-A', '--additional_kws', nargs='+', default=dict(),
                        action=AddKwsAction,
                        help='''
specify optional additional keywords passing to the workflow.''')

    return parser.parse_args()


###########
# Helpers #
###########

def ensure_output_dir(output_dir, **kwargs):
    output_dir = os_path.abspath(output_dir)
    ensure_dir(output_dir, **kwargs)
    return output_dir


#############
# Workflows #
#############

def workflow_general(job_name, inputs, output_dir,
                     global_path_to_append=[
                         '../lib/python/TrackerOnlyEmu/scripts'
                     ],
                     path_to_append=[
                         './rdx',
                         '../scripts'
                     ],
                     input_patterns=['*.root'],
                     ):
    print('{}== Job: {} =={}'.format(TC.BOLD+TC.GREEN, job_name, TC.END))
    for p in global_path_to_append+path_to_append:
        append_path(p)

    # Need to figure out the absolute path
    input_files = find_all_input(inputs, input_patterns)
    subworkdirs = {os_path.splitext(os_path.basename(i))[0]: i
                   for i in input_files}

    # Now ensure the working dir
    workdir = ensure_output_dir(os_path.join(output_dir, job_name))

    return subworkdirs, workdir


def workflow_trigger_emulation(job_name, inputs, output_dir, debug, kws):
    subworkdirs, workdir = workflow_general(job_name, inputs, output_dir)
    chdir(workdir)
    exe = pipe_executor('trigger_emulation.sh {input_ntp}')

    for subdir, full_filename in subworkdirs.items():
        print('{}Working on {}...{}'.format(TC.GREEN, full_filename, TC.END))
        ensure_dir(subdir)
        chdir(subdir)  # Switch to the workdir of the subjob

        params = {
            'input_ntp': full_filename
        }
        exe(params, debug)

        aggragate_output('..', subdir, {
            'ntuple': ['*.root'],
            'plots_raster': ['*.png'],
            'plots_vector': ['*.pdf'],
        })

        chdir('..')  # Switch back to parent workdir


def workflow_trigger_emulation_fs_vs_to(job_name, inputs, output_dir, debug,
                                        kws):
    subworkdirs, workdir = workflow_general(job_name, inputs, output_dir)
    chdir(workdir)
    exe = pipe_executor(
        'trigger_emulation_fs_vs_to.sh {input_ntp1} {input_ntp2}')

    ntps = list(subworkdirs.values())
    subdir = list(subworkdirs.keys())[0] + '--fs_vs_to'
    params = {
        'input_ntp1': ntps[0],
        'input_ntp2': ntps[1]
    }

    print('{}Working on {}...{}'.format(TC.GREEN, subdir, TC.END))
    ensure_dir(subdir)
    chdir(subdir)  # Switch to the workdir of the subjob

    exe(params, debug)

    aggragate_output('..', subdir, {
        'ntuple': ['*.root'],
        'plots_raster': ['*.png'],
        'plots_vector': ['*.pdf'],
    })

    chdir('..')  # Switch back to parent workdir


def workflow_cutflow(job_name, inputs, output_dir, debug, kws):
    subworkdirs, workdir = workflow_general(job_name, inputs, output_dir)
    chdir(workdir)
    exe = pipe_executor('cutflow.sh "{input_ntps}" {input_yml} {mode}')

    ntps = [n for n in subworkdirs.values()
            if False not in [kw in n for kw in kws['keep'].split(',')]]
    params = {
        'input_ntps': ' '.join(ntps),
        'input_yml': kws['input_yml'],
        'mode': kws['mode'],
    }

    print('{}Working on {}...{}'.format(TC.GREEN, workdir, TC.END))
    exe(params, debug)


def workflow_data(job_name, inputs, output_dir, debug, kws,
                  script='data.sh', output_ntp_name_gen=generate_step2_name):
    subworkdirs, workdir = workflow_general(job_name, inputs, output_dir)
    chdir(workdir)
    exe = pipe_executor(
        script + ' ' + '"{input_ntp}" "{input_yml}" "{output_suffix}"')

    for subdir, full_filename in subworkdirs.items():
        print('{}Working on {}...{}'.format(TC.GREEN, full_filename, TC.END))
        ensure_dir(subdir)
        chdir(subdir)  # Switch to the workdir of the subjob

        params = {
            'input_ntp': full_filename,
            'input_yml': kws['input_yml'],
            'output_suffix': output_ntp_name_gen(full_filename)
        }
        exe(params, debug)

        aggragate_output('..', subdir, {
            'ntuple': ['*--std--*.root']
        })

        chdir('..')  # Switch back to parent workdir


########
# Main #
########

WORKFLOWS = {
    'trigger_emulation': workflow_trigger_emulation,
    'trigger_emulation_fs_vs_to': workflow_trigger_emulation_fs_vs_to,
    'cutflow': workflow_cutflow,
    'data': workflow_data,
    'data_no_mu_bdt': lambda *args: workflow_data(
        *args, script='data_no_mu_bdt.sh'),
    'data_ref': lambda *args: workflow_data(
        *args, script='data_no_mu_bdt.sh',
        output_ntp_name_gen=parse_step2_name),
}

if __name__ == '__main__':
    args = parse_input()

    WORKFLOWS[args.mode](
        args.job_name, args.inputs, args.output_dir, args.debug,
        args.additional_kws)

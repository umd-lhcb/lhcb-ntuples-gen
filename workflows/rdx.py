#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Apr 13, 2021 at 02:46 AM +0200

import sys
import os.path as os_path

from argparse import ArgumentParser
from os import chdir

sys.path.insert(0, os_path.dirname(os_path.abspath(__file__)))

from utils import (
    abs_path, ensure_dir, find_all_input, append_path, pipe_executor,
    aggragate_output
)


#################################
# Command line arguments parser #
#################################

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

    parser.add_argument('-m', '--mode', default=None, help='''
specify workflow mode.
''')

    parser.add_argument('-o', '--output-dir',
                        default=abs_path('../gen'), help='''
specify output dir.
''')

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
                         './rdx'
                     ],
                     input_patterns=['*.root']):
    for p in global_path_to_append+path_to_append:
        append_path(p)

    # Need to figure out the absolute path
    input_files = find_all_input(inputs, input_patterns)
    subworkdirs = {os_path.splitext(os_path.basename(i))[0]: i
                   for i in input_files}

    # Now ensure the working dir
    workdir = ensure_output_dir(os_path.join(output_dir, job_name))

    return subworkdirs, workdir


def workflow_mc(job_name, inputs, output_dir, debug):
    subworkdirs, workdir = workflow_general(job_name, inputs, output_dir)
    chdir(workdir)
    exe = pipe_executor('mc.sh {input_ntp}')

    for d, f in subworkdirs.items():
        ensure_dir(d)
        chdir(d)  # Switch to the workdir of the subjob
        params = {
            'input_ntp': f
        }
        exe(params, debug)
        aggragate_output('..', d, {'root': ['*.root']})
        chdir('..')  # Switch back to parent workdir


WORKFLOWS = {
    'mc': workflow_mc,
}


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    if args.mode:
        WORKFLOWS[args.mode](
            args.job_name, args.inputs, args.output_dir, args.debug)

#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sat Apr 10, 2021 at 01:29 AM +0200

import sys
import os.path as os_path

from argparse import ArgumentParser

sys.path.insert(0, os_path.dirname(os_path.abspath(__file__)))

from utils import Executor, Processor
from utils import pipe_executor, abs_path


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


#############
# Workflows #
#############

WF_TEST = [
    Executor(
        [pipe_executor('echo {input}'),
         pipe_executor('touch {input}.txt')],
        {'input': lambda files: [os_path.basename(f)
                                 for f in files if f.endswith('.root')]}
    ),
    Executor(
        [pipe_executor('cp {input} test2.txt')],
        {'input': lambda files: [f for f in files if f.endswith('.txt')]}
    )
]

WF_MC = [
    # First, generate trigger emulations
    Executor(
        [pipe_executor('run2-rdx-hlt1.py {input} b0_hlt1.root -t TupleB0/DecayTree')],
        {'input': lambda files: [f for f in files if f.endswith('.root')]}
    ),
]


#######################
# Workflow processors #
#######################

def workflow_test(inputs, output_dir, debug):
    proc = Processor(inputs, output_dir, keep={'txt': '*.txt'}, debug=debug)
    proc.process(WF_TEST)


def workflow_mc(inputs, job_name, debug):
    proc = Processor(inputs, job_name, keep={'txt': '*.txt'}, debug=debug)
    proc.process(WF_MC)


WF_PROCESSORS = {
    'test': workflow_test,
    'mc': workflow_mc,
}


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    if args.mode:
        output_dir = os_path.join(args.output_dir, args.job_name)
        WF_PROCESSORS[args.mode](args.inputs, output_dir, args.debug)
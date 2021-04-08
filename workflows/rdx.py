#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri Apr 09, 2021 at 12:10 AM +0200

import sys
import os.path as os_path

from argparse import ArgumentParser

sys.path.insert(0, os_path.dirname(os_path.abspath(__file__)))

from utils import Executor, Processor


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

    return parser.parse_args()


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    print(args)

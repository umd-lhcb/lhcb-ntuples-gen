#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Dec 28, 2021 at 04:21 PM +0100

from argparse import ArgumentParser
from glob import glob
from os.path import basename


#################################
# Command line arguments parser #
#################################

def parse_input():
    parser = ArgumentParser(description='skim ganga output ntuples.')

    parser.add_argument('input_folder', help='specify ganga job folder.')
    parser.add_argument('output_folder',
                        help='specify output folder for skimmed ntuples.')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug mode.')

    return parser.parse_args()


###########
# Helpers #
###########

def is_num(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


def fltr_subjob_folders(job_folder):
    raw = glob(f'{job_folder}/*')
    return [i for i in raw if is_num(basename(i))]


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

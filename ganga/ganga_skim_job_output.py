#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Dec 28, 2021 at 05:05 PM +0100

import os

from argparse import ArgumentParser
from glob import glob
from os.path import basename, abspath


#################
# Configurables #
#################

PROJECT_ROOT = abspath(f'{abspath(__file__)}/../..')
OUTPUT_NTP_SUFFIX = '{}-dv'


#################################
# Command line arguments parser #
#################################

def parse_input():
    parser = ArgumentParser(description='skim ganga output ntuples.')

    parser.add_argument('input_folder', help='specify ganga job folder.')
    parser.add_argument('output_folder',
                        help='specify output folder for skimmed ntuples.')
    parser.add_argument('skim_config', help='specify skim config')

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


def find_ntp_name(folders):
    return basename(glob(f'{folders[0]}/*.root')[0])


def fltr_subjob_ntps(job_folder):
    raw = glob(f'{job_folder}/*')
    folders = [i+'/output' for i in raw if is_num(basename(i))]
    ntp_name = find_ntp_name(folders)
    return [i+f'/{ntp_name}' for i in folders], [basename(i) for i in raw]


def output_idx_gen(input_ntp_folder):
    return input_ntp_folder


def output_ntp_name_gen(output_folder, input_ntp_folder):
    suffix = OUTPUT_NTP_SUFFIX.format(output_idx_gen(input_ntp_folder))
    return f'{output_folder}--{suffix}.root'


def run_skim(debug=False):
    exe = f'{PROJECT_ROOT}/scripts/haddcut.py'

    def executor(input_ntp, output_ntp, config):
        cmd = f'{exe} {output_ntp} {input_ntp} -c {config}'
        if debug:
            print(cmd)
        else:
            os.system(cmd)

    return executor


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    if args.debug:
        print(f'lhcb-ntuples-gen project root path is: {PROJECT_ROOT}')

    exe = run_skim(args.debug)

    input_ntps, folder_idx = fltr_subjob_ntps(args.input_folder)
    for ntp, idx in zip(input_ntps, folder_idx):
        output_ntp = f'{args.output_folder}/{output_ntp_name_gen(args.output_folder, idx)}'
        exe(ntp, output_ntp, args.skim_config)

#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sun Feb 13, 2022 at 01:37 PM -0500

import os
import sys

from argparse import ArgumentParser
from glob import glob
from os.path import basename, abspath, isdir
from os import makedirs


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

    parser.add_argument('output_folder',
                        help='specify output folder for skimmed ntuples.')
    parser.add_argument('input_folder', help='specify ganga job folder.')
    parser.add_argument('skim_config', help='specify skim config')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug mode.')

    parser.add_argument('-c', '--copy', action='store_true',
                        help='just copy and rename ntuples, do no skimming.')

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


def pad_idx(idxs):
    return max(len(i) for i in idxs)


## Returns the root files that actually exist
def fltr_subjob_ntps(job_folder):
    raw = [i for i in glob(f'{job_folder}/*') if is_num(basename(i))]
    folders = [i+'/output' for i in raw]
    ntps, subfolders = [], []
    for folder in folders:
        rootfiles = glob(f'{folder}/*.root')
        if len(rootfiles) == 0: print(f'\nWARNING: No .root files in {folder}\n')
        for f in rootfiles:
            ntps.append(f)
            subfolders.append(f.split('/')[-3])
    return ntps, subfolders


def output_idx_gen(input_ntp_folder, padding):
    return '0'*(padding - len(input_ntp_folder)) + input_ntp_folder


def output_ntp_name_gen(output_folder, input_ntp_folder, padding):
    suffix = OUTPUT_NTP_SUFFIX.format(output_idx_gen(input_ntp_folder, padding))
    return f'{basename(output_folder)}--{suffix}.root'


def run_skim(debug=False):
    exe = f'{PROJECT_ROOT}/scripts/haddcut.py'

    def executor(input_ntp, output_ntp, config):
        print(f'  Skimming {input_ntp} as {output_ntp}...')
        cmd = f'{exe} {output_ntp} {input_ntp} -c {config}'
        if debug:
            print(cmd)
        else:
            os.system(cmd)

    return executor


def run_cp(debug=False):
    def executor(input_ntp, output_ntp, config):
        print(f'  Copying {input_ntp} as {output_ntp}...')
        cmd = f'cp {input_ntp} {output_ntp}'
        if debug:
            print(cmd)
        else:
            os.system(cmd)

    return executor


def ensure_dir(folder):
    if not isdir(folder):
        makedirs(folder)


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    if args.debug:
        print(f'lhcb-ntuples-gen project root path is: {PROJECT_ROOT}')
        print(f'Input dir: {args.input_folder}')

    output_folder = args.output_folder.replace('.root', '')
    ensure_dir(output_folder)
    exe = run_skim(args.debug) if not args.copy else run_cp(args.debug)

    input_ntps, folder_idx = fltr_subjob_ntps(args.input_folder)

    padding = pad_idx(folder_idx)
    for ntp, idx in zip(input_ntps, folder_idx):
        output_ntp = f'{output_folder}/{output_ntp_name_gen(output_folder, idx, padding)}'
        exe(ntp, output_ntp, args.skim_config)

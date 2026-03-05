#!/usr/bin/env python3
#
# Author: Lucas Meyer Garcia
# Merge step2 ntuples

from argparse import ArgumentParser
from glob import glob
import os.path as op
# import yaml
# from subprocess import Popen, PIPE, STDOUT
from os import system

#################################
# Command line arguments parser #
#################################

BASE_PATH = op.abspath(op.dirname(op.abspath(__file__)) + '/..')
SPEC_YML = BASE_PATH + '/../rdx-run2-analysis-v2/fit/spec/histos.yml'


def parseInput():
    parser = ArgumentParser(description='Move step1 ntuples to folders.')

    parser.add_argument(
        'inFolder',
        help=
        'Specify folder containing full step2 output (e.g. gen/Dst_D0-mc-tracker_only-sig_norm-all). Supports wildcard (*).'
    )
    parser.add_argument('-n',
                        '--dryRun',
                        action='store_true',
                        help='Create target folders but do not move files.')

    return parser.parse_args()


########
# Aux  #
########


## Add colors for terminal output
def cTerm(msg, color):
    num = 30
    if color == 'red': num = 91
    if color == 'green': num = 92
    if color == 'yellow': num = 93
    if color == 'blue': num = 94
    if color == 'magenta': num = 95
    if color == 'cyan': num = 96
    return f'\033[{num};1m{msg}\033[0m'


## Run shell command and print output only to terminal
def runCmd(cmd, color='magenta', dry_run=False):
    print(cTerm(cmd, color) + '\n')
    if dry_run:
        return 0
    return system(cmd)


def combine_fields(fields, sep="--"):
    comb = ''
    for field in fields[0:-1]:
        comb += field + sep
    return comb + fields[-1]


########
# Main #
########

if __name__ == '__main__':
    args = parseInput()

    folders = glob(args.inFolder)
    # Check matches
    if folders == []:
        print(cTerm(f'No folders matching {args.inFolder}. Exiting.', 'red'))

    for folder in folders:
        print(cTerm(f'Merging {folder} ntuples', 'green') + '\n')
        path_unmerged = f'{folder}/ntuple'
        parent_dir = op.dirname(folder)

        ## Checking if folder is empty
        ntps = glob(f'{path_unmerged}/*root')
        if ntps == []:
            print(cTerm(f'{folder} has no .root files, skipping', 'red'))
            continue

        # Check output files to be produced
        output_ntps = []
        date = ntps[0].split('--')[1]
        for ntp in ntps:
            ntp_fields = op.basename(ntp).split('--')
            output_ntp = combine_fields(ntp_fields[0:-1])
            if output_ntp not in output_ntps:
                output_ntps.append(output_ntp)

        for output in output_ntps:
            output_dir = f'{parent_dir}/{date}--merged--{op.basename(folder)}'
            if not op.isdir(output_dir) or args.dryRun:
                runCmd(f'mkdir -p {output_dir}',
                       color='cyan',
                       dry_run=args.dryRun)
            runCmd(
                f'hadd -fk {output_dir}/{output}.root {path_unmerged}/{output}--*.root',
                dry_run=args.dryRun)

#!/usr/bin/env python3
#
# Author: Lucas Meyer Garcia, Manuel Franco Sevilla
# Move step2 ntuples to rdx-run2-analysis-v2 with appropriate folder structure

from argparse import ArgumentParser
from glob import glob
import os.path as op
import yaml
from subprocess import Popen, PIPE, STDOUT

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
        'Specify folder containing step2 ntuples to be moved. Supports wildcard (*).'
    )
    parser.add_argument('outFolder',
                        help='Specify folder to receive step2 ntuples.')
    parser.add_argument('-s',
                        '--histoSpec',
                        default=SPEC_YML,
                        help='histo spec YAML.')
    parser.add_argument('-n',
                        '--dryRun',
                        action='store_true',
                        help='Create target folders but do not move files.')

    return parser.parse_args()


########
# Aux  #
########


def pdfFromMCID(mcID, spec):
    if mcID == '90000000': return 'data', 'data'

    # D** have multiple templates per MC ID: name these guys by hand rather than using pdf name
    dststIDs = {
        '13874020': 'Ds2D0',
        '13674000': 'Ds2Dst',
        '11874430': 'DststMu',
        '11874440': 'DststTau',
        '12873450': 'Dstst0Mu',
        '12873460': 'Dstst0Tau'
    }
    for channel, pdfs in spec.items():
        for pdfName, pdf in pdfs.items():
            if mcID in str(pdf['file_filtering']):
                if mcID in dststIDs: return dststIDs[mcID], pdf['plot_group']
                return pdfName, pdf['plot_group']

    return 'unknown'


def findPolatirity(tag):
    if tag == 'md':
        return 'MagDown'
    elif tag == 'mu':
        return 'MagUp'
    else:
        return None


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
def runCmd(cmd, dry_run=False):
    print(cTerm(' '.join(cmd), 'magenta') + '\n')
    if dry_run:
        return 0
    with Popen(cmd,
               stdout=PIPE,
               stderr=STDOUT,
               bufsize=1,
               universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')
        return p.returncode


########
# Main #
########

if __name__ == '__main__':
    args = parseInput()

    with open(args.histoSpec) as f:
        spec = yaml.safe_load(f)

    folders = glob(args.inFolder)

    # Check matches
    if folders == []:
        print(f'No folders matching {args.inFolder}. Exiting.')

    for folder in folders:
        if '--merged--' not in folder:
            print(
                f'WARNING Expected "--merged--" in folder name: {folder}. Skipping.'
            )
            continue

        ## Checking if folder is empty
        ntps = glob(f'{folder}/*root')
        if ntps == []:
            print(cTerm(f'{folder} has no .root files, skipping', 'red'))
            continue

        for ntp in ntps:
            ntp_fields = op.splitext(op.basename(ntp))[0].split('--')

            if '--std--' in ntp: group, pdf, mcID = 'data', 'data', 'std'
            elif '--mu_misid--' in ntp:
                group, pdf, mcID = 'data', 'data', 'fake_mu'
            else:
                mcID = ntp_fields[3]
                pdf, group = pdfFromMCID(mcID, spec)

            ## Find polarity
            pol = findPolatirity(ntp_fields[5])
            if pol is None:
                print(
                    f'WARNING Expected mu or md in ntuple name: {ntp}. Skipping.'
                )
                continue

            ## Find year
            year = ntp_fields[4]
            if year not in ['2016', '2017', '2018']:
                print(f'WARNING Unexpected year: {year}. Skipping.')
                continue

            ## Folder to which sample is going to be moved
            newFolder = f'{args.outFolder}/{year}/{group}/{pdf}-{mcID}-{pol}/'
            if not op.isdir(newFolder): runCmd(['mkdir', '-p', newFolder])

            runCmd(['mv', ntp, newFolder], dry_run=args.dryRun)

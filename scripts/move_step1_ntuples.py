#!/usr/bin/env python3
#
# Author: Manuel Franco Sevilla
# Move step1 ntuples to folders

from argparse import ArgumentParser
from glob import glob
import os.path as op
import yaml
from subprocess import Popen, PIPE, STDOUT

#################################
# Command line arguments parser #
#################################

BASE_PATH = op.abspath(op.dirname(op.abspath(__file__)) + '/..')
SPEC_YML = BASE_PATH + '/../rdx-run2-analysis/fit/spec/histos.yml'

def parseInput():
    parser = ArgumentParser(description='Move step1 ntuples to folders.')

    parser.add_argument('inFolder', help='specify folder containing folders with ntuples.')
    parser.add_argument('outFolder', help='specify folder containing folders with ntuples.')
    parser.add_argument('-s', '--histoSpec', default=SPEC_YML, help='histo spec YAML.')

    return parser.parse_args()


########
# Aux  #
########

def pdfFromMCID(mcID, spec):
    if mcID == '90000000': return 'data', 'data'
    
    for channel, pdfs in spec.items():
        for pdfName, pdf in pdfs.items():
            if mcID in str(pdf['file_filtering']): return pdfName, pdf['plot_group']

    return 'unknown'

## Add colors for terminal output
def cTerm(msg, color):
    num = 30
    if color == 'red':     num = 91
    if color == 'green':   num = 92
    if color == 'yellow':  num = 93
    if color == 'blue':    num = 94
    if color == 'magenta': num = 95
    if color == 'cyan':    num = 96
    return f'\033[{num};1m{msg}\033[0m'

## Run shell command and print output only to terminal
def runCmd(cmd):
    print('\n'+cTerm(' '.join(cmd),'magenta')+'\n')
    with Popen(cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True) as p:
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

    for folder in glob(f'{args.inFolder}/*'):
        if '.DST' not in folder: continue

        ## Checking if folder is empty
        ntps = glob(f'{folder}/*root')
        if ntps == []:
            print(cTerm(f'{folder} has no .root files, skipping', 'red'))
            continue
           
        ## Find mcID and pdf name from histos.yml
        if '--std--' in folder: group, pdf, mcID = 'data', 'data', 'std'
        elif '--mu_misid--' in folder: group, pdf, mcID = 'data', 'data', 'fake_mu'
        else:
            mcID = folder.split('_')[-2]
            pdf, group = pdfFromMCID(mcID, spec)

        ## Find polarity
        pol = 'MagDown'
        if 'MagUp' in folder: pol = 'MagUp'

        ## Find year
        year = '2016'
        if 'MC_2017' in folder or 'Collision17' in folder: year = '2017'
        if 'MC_2018' in folder or 'Collision18' in folder: year = '2018'

        ## Group folder
        groupFolder = f'{args.outFolder}/{year}/{group}'
        if not op.isdir(groupFolder): runCmd(['mkdir', '-p', groupFolder])

        ## Folder to which sample is going to be moved
        newFolder = f'{groupFolder}/{pdf}-{mcID}-{pol}'
        if op.isdir(newFolder):
            print(cTerm(f'{newFolder} already exists, skipping {folder}', 'red'))
            continue

        ## Fixing the annex if files inside are symlinks, otherwise, moving the folder
        if op.islink(ntps[0]):
            runCmd(['mkdir', newFolder])
            ## Have to git mv each ntuple because * does not work
            for ntp in ntps:
                runCmd(['git', 'mv', ntp, newFolder])
            runCmd(['git', 'annex', 'add', newFolder+'/*root'])
            runCmd(['git', 'annex', 'fix'])
        else: runCmd(['mv', folder, newFolder])

            

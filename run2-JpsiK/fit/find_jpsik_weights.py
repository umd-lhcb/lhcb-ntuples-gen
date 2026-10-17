#!/usr/bin/env python3
#
# Author: Manuel Franco Sevilla
# Find reweighting for B kinematics from B -> J/Psi K

import sys
import datetime
import json
from pathlib import Path
from shlex import join
from subprocess import Popen, PIPE, STDOUT
from argparse import ArgumentParser
from glob import glob

#################################
# Command line arguments parser #
#################################

def parseInput():
    parser = ArgumentParser(
        description='Find reweighting for B kinematics from B -> J/Psi K.'
    )

    parser.add_argument('-d', '--dataFolder', default='../ntuples/0.9.18-JpsiK-L0DiMuon/JpsiK-data/step2/',
                        help='Folder with data ntuples.')
    parser.add_argument('-m', '--mcFolder', default='../ntuples/0.9.18-JpsiK-L0DiMuon/JpsiK-mc/step2/',
                        help='Folder with MC ntuples.')
    parser.add_argument('-o', '--outFolder', default='gen/',
                        help='Folder for output files.')
    parser.add_argument('--years', nargs='+', choices=['2016', '2017', '2018'],
                        default=['2016', '2017', '2018'], help='Years to process.')
    parser.add_argument('--cut', default=None,
                        help='Uproot selection for both data (before the mass fit) and MC, e.g. nspd_ok.')
    parser.add_argument('--method', choices=['bins', 'gb'], default='bins')
    parser.add_argument('--n-bins', type=int, default=100)
    parser.add_argument('--n-neighs', type=float, default=5.0)
    parser.add_argument('--bins-min-in-bin', type=float, default=0.1)

    return parser.parse_args()

#######################
# Auxiliary functions #
#######################

def cTerm(msg, color):
    num = 30
    if color == 'red':     num = 91
    if color == 'green':   num = 92
    if color == 'yellow':  num = 93
    if color == 'blue':    num = 94
    if color == 'magenta': num = 95
    if color == 'cyan':    num = 96
    return f'\033[{num};1m{msg}\033[0m'

## Run shell command and print output to terminal and logfile
def runCmdLog(cmd, outFile, mode='w'):
    print('\n'+cTerm(join(cmd)+' | tee '+outFile,'magenta')+'\n')
    with open(outFile, mode) as f, Popen(cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')
            f.write(line)
    if p.returncode:
        raise SystemExit(f'Command failed with status {p.returncode}; see {outFile}')

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

    ## Executables
    scriptFolder = Path(__file__).resolve().parent
    fitExe    = str(scriptFolder / 'fit_and_sweight.py')
    weightExe = str(scriptFolder / 'gen_weights.py')

    # Validate all requested years before starting any expensive fits.
    inputs = {}
    for year in args.years:
        dataFiles = sorted(glob(f'{args.dataFolder}/*{year}*.root'))
        mcFiles = sorted(glob(f'{args.mcFolder}/*{year}*.root'))
        if not dataFiles or not mcFiles:
            raise SystemExit(f'Missing data or MC ROOT inputs for {year}; check folders or --years.')
        inputs[year] = (dataFiles, mcFiles)
    Path(args.outFolder).mkdir(parents=True, exist_ok=True)

    for year in args.years:
        dataFiles, mcFiles = inputs[year]
        weightFile = str(Path(args.outFolder) / f'run2-JpsiK-{year}-md-B-ndof_ntracks__pt_eta.root')
        muFile = Path(args.outFolder) / f'run2-JpsiK-{year}-mu-B-ndof_ntracks__pt_eta.root'
        if Path(weightFile).exists() or muFile.exists() or muFile.is_symlink():
            raise SystemExit(f'Weight outputs for {year} already exist; choose a new --outFolder.')
        ## Running fit
        print(f'\nWORKING ON {year}\n')
        timeStamp = datetime.datetime.now().strftime('%y_%m_%d_%H_%M_%S')
        fitFolder = f'{args.outFolder}/JpsiK-{timeStamp}-std-fit-{year}'
        Path(fitFolder).mkdir()
        with open(fitFolder + '/inputs.json', 'w') as f:
            json.dump({'data': dataFiles, 'mc': mcFiles, 'settings': vars(args)}, f, indent=2)
        cmd = [sys.executable, fitExe, '--dataLabel', f'{year} data', '-p', str(scriptFolder / 'fit_params/init.yml'), '-o', fitFolder]
        if args.cut:
            cmd += ['--cut', args.cut]
        cmd += ['-i'] + [ntuple+':tree' for ntuple in dataFiles]
        runCmdLog(cmd, fitFolder + '/fit.log')
        fitFile = fitFolder + '/fit.root'

        ## Finding weights
        cmd = [sys.executable, weightExe, '-d', fitFile, '-o', weightFile,
               '--method', args.method, '--n-bins', str(args.n_bins),
               '--n-neighs', str(args.n_neighs), '--bins-min-in-bin', str(args.bins_min_in_bin)]
        if args.cut:
            cmd += ['--mc-cut', args.cut]
        cmd += ['-m'] + mcFiles
        runCmdLog(cmd, fitFolder + '/weight.log')
        muFile.symlink_to(Path(weightFile).name)

        print('\n'+cTerm(f'New maps: {weightFile} (MagUp links to the same map). Nominal maps were not replaced.', 'green')+'\n')

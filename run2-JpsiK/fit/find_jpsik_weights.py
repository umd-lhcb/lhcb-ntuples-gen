#!/usr/bin/env python3
#
# Author: Manuel Franco Sevilla
# Find reweighting for B kinematics from B -> J/Psi K

import sys
import yaml
import datetime
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

    parser.add_argument('-d', '--dataFolder', default='../ntuples/0.9.8-JpsiK_L0/JpsiK-std-step2/',
                        help='Folder with data ntuples.')
    parser.add_argument('-m', '--mcFolder', default='../ntuples/0.9.8-JpsiK_L0/JpsiK-mc-step2/',
                        help='Folder with MC ntuples.')
    parser.add_argument('-o', '--outFolder', default='gen/',
                        help='Folder for output files.')

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
    print('\n'+cTerm(' '.join(cmd)+' | tee '+outFile,'magenta')+'\n')
    f = open(outFile, mode)
    with Popen(cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')
            f.write(line)
    return p.returncode

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
    fitExe    = './fit/fit_and_sweight.py'
    weightExe = './fit/gen_weights.py'
    
    ## Running fit
    timeStamp = datetime.datetime.now().strftime('%y_%m_%d_%H_%M')
    fitFolder = f'{args.outFolder}/JpsiK-{timeStamp}-std-fit-2016'
    runCmd(['mkdir', '-p', fitFolder])
    cmd = [fitExe, '-p', 'fit/fit_params/init.yml', '-o', fitFolder, '-i']
    for ntuple in sorted(glob(f'{args.dataFolder}/*')):
        cmd.append(ntuple+':tree')
    runCmdLog(cmd, fitFolder + '/fit.log')
    fitFile = fitFolder + '/fit.root'

    ## Finding weights
    weightFile = args.outFolder+'/run2-JpsiK-2016-md-B-ndof_ntracks__pt_eta.root'
    cmd = [weightExe, '-d', fitFile, '-o', weightFile, '-m']
    for ntuple in sorted(glob(f'{args.mcFolder}/*')):
        cmd.append(ntuple)
    runCmdLog(cmd, fitFolder + '/weight.log')

    ## The mu file is a soft link always pointing at the md file, so it doesn't need to be updated
    weightFolder = 'reweight/JpsiK/root-run2-JpsiK_oldcut/'
    mdFile = 'run2-JpsiK-2016-md-B-ndof_ntracks__pt_eta.root'
    print('\n'+cTerm(f' cp -f {weightFile} {weightFolder}{mdFile}','green')+'\n')
   
    

#!/usr/bin/env python3
#
# Author: Manuel Franco Sevilla
# Validate step1 ntuples by comparing them to a previous production

from argparse import ArgumentParser
import ROOT
from glob import glob
import os

#################################
# Command line arguments parser #
#################################

def parseInput():
    parser = ArgumentParser(description='Validate step1 ntuples by comparing them to a previous production.')

    parser.add_argument('-n', '--newFolder', help='specify folder containing subfolders with new ntuples.')
    parser.add_argument('-o', '--oldFolder', help='specify folder containing subfolders with old ntuples.',
                        default='ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/')
    parser.add_argument('-c', '--cut', default='',
                        help='compare entries after applying cut, eg "b_ENDVERTEX_X > 1 && b_P > 50000"', )

    return parser.parse_args()


########
# Main #
########

if __name__ == '__main__':
    args = parseInput()
    
    baseNew = args.newFolder
    baseOld = args.oldFolder
    if args.cut != '': print(f'Applying cut {args.cut}')
    for folderNew in glob(f'{baseNew}/*'):
        mcID = folderNew.split('_')[-2]
        pol = 'MagDown'
        if 'MagUp' in folderNew: pol = 'MagUp'
        
        ## Finding the folder in the old production with the same MC ID
        for folderOld in glob(f'{baseOld}/*'):
            if mcID in folderOld and pol in folderOld: break
        print()
        
        ## Comparing ntuples
        for treeName in ['Bminus', 'B0']:
            new = ROOT.TChain(f'Tuple{treeName}/DecayTree')
            old = ROOT.TChain(f'Tuple{treeName}/DecayTree')
            newFiles = new.Add(f'{folderNew}/*dv.root')
            oldFiles = old.Add(f'{folderOld}/*dv.root')
            Nnew = float(new.GetEntries(args.cut))
            Nold = float(old.GetEntries(args.cut))
            diff = (Nnew-Nold)/Nold*100
            print(f'For {mcID}_{pol:<7} {treeName:>7}: new = {Nnew:>11,.0f}, old = {Nold:>11,.0f}, diff = {diff:>8.4f}%.   {newFiles} vs {oldFiles} files')


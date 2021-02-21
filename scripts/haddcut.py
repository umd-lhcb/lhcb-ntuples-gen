#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sun Feb 21, 2021 at 05:23 PM +0100
# Description: Merge and apply cuts on input .root files, each with multiple
#              trees, to a single output .root file.
#
#              Note that this is still based on Python 2, because on lxplus,
#              ROOT is compiled with Python 2 only.

# NOTE: Remove the __future__ imports once ROOT is available with Python 3 on
#       lxplus.
from __future__ import print_function

try:
    import configparser
except ImportError:
    import ConfigParser as configparser  # Python 2 fallback

import ROOT
ROOT.PyConfig.DisableRootLogon = True  # Don't read .rootlogon.py

from argparse import ArgumentParser
from ROOT import TTree, TDirectory, TChain, TFile


################################
# Command line argument parser #
################################

def parse_input():
    parser = ArgumentParser(description='''
merge and apply cuts on input .root files to a single output .root file.
''')

    parser.add_argument('output_ntp', help='''
        output ntuple.
''')

    parser.add_argument('input_ntp', help='''
        input ntuple.
''')

    return parser.parse_args()


###########
# Helpers #
###########

def path_basename(full_path):
    splitted = full_path.split('/')
    return '/'.join(splitted[:-1]), splitted[-1]  # UNIX-like basename


####################
# Ntuple operation #
####################

def traverse_ntp(ntp, pwd='/'):
    trees = []

    for key in ntp.GetListOfKeys():
        obj = key.ReadObj()
        if isinstance(obj, TDirectory):
            trees += traverse_ntp(obj, pwd + key.GetName() + '/')

        elif isinstance(obj, TTree):
            trees.append(pwd + obj.GetName())

        else:
            print('Skipping object {} of type {}'.format(
                obj.GetName(), type(obj)))

    return trees


def create_chains(input_ntp_name, trees):
    chains = dict()

    for tree_path in trees:
        _, tree_name = path_basename(tree_path)
        if tree_path not in chains:
            chains[tree_path] = TChain(tree_name, tree_name)
        chains[tree_path].Add(input_ntp_name+tree_path)

    return chains


def skim_chains(output_ntp_name, chains, cuts):
    ntp = TFile(output_ntp_name, 'recreate')

    for full_path, chain in chains.items():
        path, _ = path_basename(full_path)
        if not ntp.GetDirectory(path):
            ntp.mkdir(path[1:])
        ntp.cd(path)
        tree = chain.CopyTree('')  # FIXME placeholder for cuts
        tree.Write()

    ntp.Close()


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

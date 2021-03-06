#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue May 04, 2021 at 12:21 PM +0200
# Description: Merge and apply cuts on input .root files, each with multiple
#              trees, to a single output .root file.
#
#              Note that this is still based on Python 2, because on lxplus,
#              ROOT is compiled with Python 2 only.

# NOTE: On lxplus, invoke this script with python2:
#       python2 ./haddcut.py ...

# NOTE: Remove the __future__ imports once ROOT is available with Python 3 on
#       lxplus.
from __future__ import print_function

try:
    import configparser
except ImportError:
    import ConfigParser as configparser  # Python 2 fallback

import yaml

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  # Don't hijack argparse!
ROOT.PyConfig.DisableRootLogon = True  # Don't read .rootlogon.py

from argparse import ArgumentParser
from glob import glob
from collections import defaultdict
from ROOT import TTree, TDirectory, TChain, TFile


################################
# Command line argument parser #
################################

def parse_input():
    parser = ArgumentParser(description='''
merge and apply cuts on input .root files to a single output .root file.
''')

    parser.add_argument('output_ntp',
                        help='''
        output ntuple.
''')

    parser.add_argument('input_ntp',
                        nargs='+',
                        help='''
        input ntuple.
''')

    parser.add_argument('--config', '-c',
                        default=False,
                        help='''
specify the optional selection config file. By default all trees and entries are kept.
''')

    return parser.parse_args()


######################
# YAML config parser #
######################

def parse_config(config_file):
    if config_file:
        with open(config_file) as f:
            raw_config = yaml.safe_load(f)
    else:
        raw_config = dict()

    config = defaultdict(lambda: {
        'keep': True,
        'selection': [''],
        'deactivate': [],
        'activate': [],
    })

    for tree, sub_config in raw_config.items():
        config[tree].update(sub_config)

    # Possibly inherit config from other trees
    for tree, sub_config in config.items():
        for key in ['selection', 'deactivate', 'activate']:
            if not isinstance(sub_config[key], list):
                try:
                    ref_tree = sub_config[key]
                    sub_config[key] = config[ref_tree][key]
                except:
                    print('Cannot resolve {}.{}, fallback to default...'.format(
                        tree, key
                    ))
                    if key == 'selection':
                        sub_config[key] = ['']
                    else:
                        sub_config[key] = []

    return config


###########
# Helpers #
###########

def path_basename(full_path):
    splitted = full_path.split('/')
    return '/'.join(splitted[:-1]), splitted[-1]  # UNIX-like basename


def concat_selections(sels):
    if sels == ['']:
        return ''
    return ' && '.join('({})'.format(s) for s in sels)


def glob_ntuples(paths):
    return [m for p in paths for m in glob(p)]


############
# ROOT I/O #
############

class ROOTFile:
    def __init__(self, path, mode):
        self.path = path
        self.mode = mode

    def __enter__(self):
        self.file = TFile(self.path, self.mode)
        if self.file.IsZombie() or not self.file.IsOpen():
            raise ValueError('Cannot open {} in mode {}'.format(
                self.path, self.mode))
        return self.file

    def __exit__(self, obj_type, value, traceback):
        self.file.Close()


####################
# Ntuple operation #
####################

def keep_latest_cycle(tkeys):
    result = []

    oldkey = None
    for key in tkeys:
        if oldkey and oldkey.GetName() != key.GetName():
            result.append(oldkey)
        oldkey = key
    result.append(oldkey)

    return result


def traverse_ntp(ntp, pwd=''):
    trees = []

    for key in keep_latest_cycle(ntp.GetListOfKeys()):
        obj = key.ReadObj()
        if isinstance(obj, TDirectory):
            trees += traverse_ntp(obj, pwd + key.GetName() + '/')

        elif isinstance(obj, TTree):
            trees.append(pwd + obj.GetName())

        else:
            print('Skipping object {} of type {}'.format(
                obj.GetName(), type(obj)))

    return trees


def update_chains(input_ntp_name, chains, trees):
    for tree_path in trees:
        _, tree_name = path_basename(tree_path)
        if tree_path not in chains:
            chains[tree_path] = TChain(tree_name, tree_name)
        chains[tree_path].Add(input_ntp_name+'/'+tree_path)


def skim_chains(output_ntp_name, chains, config):
    with ROOTFile(output_ntp_name, 'recreate') as ntp:
        for full_path, chain in chains.items():
            if config[full_path]['keep']:
                print('Processing tree: {}'.format(full_path))
                path, _ = path_basename(full_path)

                if not ntp.GetDirectory(path):
                    ntp.mkdir(path)
                ntp.cd(path)

                # Remove branches, if specified
                for br in config[full_path]['deactivate']:
                    chain.SetBranchStatus(br, 0)

                # Activate branches, if specified
                for br in config[full_path]['activate']:
                    chain.SetBranchStatus(br, 1)

                tree = chain.CopyTree(concat_selections(
                    config[full_path]['selection']
                ))
                # tree.Write()

        # NOTE: Sometimes tree.Write would complain about null-pointers. In that
        #       case, comment out the tree.Write() line and uncomment the line
        #       below. No idea why this works though.
        ntp.Write('', TFile.kOverwrite)


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()
    config = parse_config(args.config)
    chains = dict()
    print('Output file: {}'.format(args.output_ntp))

    for ntp_path in glob_ntuples(args.input_ntp):
        with ROOTFile(ntp_path, 'read') as ntp:
            print('Adding {}...'.format(ntp_path))
            trees = traverse_ntp(ntp)
            update_chains(ntp_path, chains, trees)

    print('Start skimming...')
    skim_chains(args.output_ntp, chains, config)

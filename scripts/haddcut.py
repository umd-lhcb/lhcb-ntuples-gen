#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Mar 02, 2022 at 09:42 PM -0500
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

import yaml

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  # Don't hijack argparse!
ROOT.PyConfig.DisableRootLogon = True  # Don't read .rootlogon.py

from argparse import ArgumentParser
from glob import glob
from collections import defaultdict

from ROOT import TTree, TDirectory, TChain, TFile
from ROOT import RDF, RDataFrame


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

    parser.add_argument('-s', '--silent',
                        action='store_true',
                        help='do no print output')

    parser.add_argument('-c', '--config',
                        default=False,
                        help='''
specify the optional selection config file. By default all trees and entries are kept.
''')

    parser.add_argument('-m', '--mode',
                        default='chain',
                        choices=['chain', 'friend'],
                        help='''
specify working mode.
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
        self.file = TFile(path, mode)
        # do some basic corruption checks
        if self.file.IsZombie():
            print(f'\nFailed to open {path} in {mode} mode\n')
            raise ValueError
        if mode.lower() in ["read", "update"]: # if file exists, check nonempty
            if not check_ROOTFile_nonempty(path):
                print(f'\n{path} has no events in any trees!\n')
                raise ValueError

    def __enter__(self):
        if not self.file.IsOpen():
            print(f'\n{path} file closed unexpectedly\n')
            raise ValueError
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


def check_ROOTFile_nonempty(path):
    file = TFile(path)
    tree_paths = traverse_ntp(file)
    is_nonempty = False
    for tree_path in tree_paths:
        tree = file.Get(tree_path)
        try:
            if tree.GetEntries() > 0: is_nonempty = True
        except:
            file.Close()
            print(f'Failed to get # entries for {path}:{tree_path}')
            raise ValueError
    file.Close()
    return is_nonempty


def get_branch_names(tree):
    return [br.GetName() for br in tree.GetListOfBranches()]


# For 'chain' mode #############################################################
def update_chains(input_ntp_name, chains, tree_paths):
    for tree_path in tree_paths:
        _, tree_name = path_basename(tree_path)
        if tree_path not in chains:
            chains[tree_path] = TChain(tree_name, tree_name)
        chains[tree_path].Add(input_ntp_name+'/'+tree_path)


def skim_chains(output_ntp_name, chains, config):
    with ROOTFile(output_ntp_name, 'recreate') as ntp:
        for full_path, chain in chains.items():
            if config[full_path]['keep']:
                if not args.silent: print('Processing tree: {}'.format(full_path))
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
                tree.Write('', TFile.kOverwrite)

        # NOTE: Sometimes tree.Write would complain about null-pointers. In that
        #       case, comment out the tree.Write() line and uncomment the line
        #       below. No idea why this works though.
        ntp.Write('', TFile.kOverwrite)


# For 'friend' mode ############################################################
def update_friend(input_ntp, friends, tree_branch_dict, tree_paths):
    for tree_path in tree_paths:
        tree = input_ntp.Get(tree_path)
        tree.BuildIndex('runNumber', 'eventNumber')

        if tree_path not in friends:
            friends[tree_path] = tree
            tree_branch_dict[tree_path] = get_branch_names(tree)
        else:
            friends[tree_path].AddFriend(tree)
            tree_branch_dict[tree_path] += get_branch_names(tree)


def make_output_vec(branches):
    output = ROOT.std.vector('string')()
    for br in branches:
        output.push_back(br)
    return output


def merge_friend(output_ntp_name, friends, tree_branch_dict, config):
    # Here we don't drop any branch. We do only keep specified trees.
    opts = RDF.RSnapshotOptions()
    opts.fMode = 'UPDATE'

    for full_path, tree in friends.items():
        if config[full_path]['keep']:
            rd1 = RDataFrame(tree)
            cut = concat_selections(config[full_path]['selection'])

            if cut:
                rd2 = rd1.Filter(cut)
            else:
                rd2 = rd1

            output_br = make_output_vec(tree_branch_dict[full_path])
            rd2.Snapshot(full_path, output_ntp_name, output_br, opts)


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()
    config = parse_config(args.config)

    if args.mode == 'chain':
        chains = dict()
        if not args.silent: print('Output file: {}'.format(args.output_ntp))

        for ntp_path in glob_ntuples(args.input_ntp):
            if not args.silent: print('Adding {}...'.format(ntp_path))
            with ROOTFile(ntp_path, 'read') as ntp:
                update_chains(ntp_path, chains, traverse_ntp(ntp))

        if not args.silent: print('Slimming ntuple into '+args.output_ntp)
        skim_chains(args.output_ntp, chains, config)

    elif args.mode == 'friend':
        ntps = []
        friends = dict()
        tree_branch_dict = dict()

        for ntp_path in glob_ntuples(args.input_ntp):
            if not args.silent: print('Adding {}...'.format(ntp_path))
            ntp = TFile(ntp_path, 'read')
            ntps.append(ntp)

            update_friend(ntp, friends, tree_branch_dict, traverse_ntp(ntp))

        if not args.silent: print('Merging all friend trees into '+args.output_ntp)
        merge_friend(args.output_ntp, friends, tree_branch_dict, config)

        for n in ntps:
            n.Close()

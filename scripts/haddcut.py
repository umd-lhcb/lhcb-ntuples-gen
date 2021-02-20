#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sat Feb 20, 2021 at 03:47 AM +0100
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
from collections import namedtuple
from ROOT import TTree, TDirectory


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

TTreeDir = namedtuple('TTreeDir', 'path name')


####################
# Ntuple operation #
####################

def traverse_ntp(ntp, pwd=None):
    list_of_trees = dict()

    for key in ntp.GetListOfKeys():
        obj = key.ReadObj()
        if isinstance(obj, TDirectory):
            path = key.GetName() if not pwd else pwd+'/'+key.GetName()
            list_of_trees.update(traverse_ntp(obj, path))

        elif isinstance(obj, TTree):
            list_of_trees[TTreeDir(pwd, key.GetName())] = obj

        else:
            print('Skipping object {} of type {}'.format(
                obj.GetName(), type(obj)))

    return list_of_trees


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Feb 17, 2021 at 01:46 AM +0100
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


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

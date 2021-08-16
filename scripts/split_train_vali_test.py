#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Aug 16, 2021 at 05:27 PM +0200

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  # Don't hijack argparse!
ROOT.PyConfig.DisableRootLogon = True  # Don't read .rootlogon.py

from argparse import ArgumentParser
from os.path import basename, splitext


################################
# Command line argument parser #
################################

def parse_input():
    parser = ArgumentParser(description='''
split a single ntuple to train, validation, and test ntuples based on a given
percentage.
''')

    parser.add_argument('ntp', help='input ntuple.')

    parser.add_argument('tree', help='input tree.')

    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='enable debug output.')

    parser.add_argument('-o', '--output-dir',
                        default='.',
                        help='output directory.')

    parser.add_argument('-T', '--train-ratio',
                        type=int,
                        default=35,
                        help='specify train ntuple ratio.')

    parser.add_argument('-V', '--validation-ratio',
                        type=int,
                        default=35,
                        help='specify validation ntuple ratio.')

    parser.add_argument('--seed',
                        default='42',
                        help='specify random seed.')

    return parser.parse_args()


###########
# Helpers #
###########

def get_filename(path):
    return basename(splitext(path)[0])


def get_cuts(train, validation, br='rand_split'):
    result = dict()

    result['train'] = (
        '0 <= {}'.format(br),
        '{} < {}'.format(br, train)
    )
    result['valid'] = (
        '{} <= {}'.format(train, br),
        '{} < {}'.format(br, train+validation)
    )
    result['test'] = (
        '{} <= {}'.format(train+validation, br),
        '{} <= 100'.format(br)
    )

    return result


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    cuts = get_cuts(args.train_ratio, args.validation_ratio)
    if args.debug:
        for key, val in cuts.items():
            print('sample: {}, cuts: {}'.format(key, val))

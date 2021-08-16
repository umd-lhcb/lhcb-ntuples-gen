#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Aug 16, 2021 at 06:04 PM +0200

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  # Don't hijack argparse!
ROOT.PyConfig.DisableRootLogon = True  # Don't read .rootlogon.py

from argparse import ArgumentParser
from os.path import basename, splitext, join

from ROOT import gInterpreter, RDataFrame


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
    return {
        'train': '{lb} <= {br} && {br} < {ub}'.format(
            br=br, lb=0, ub=train),
        'valid': '{lb} <= {br} && {br} < {ub}'.format(
            br=br, lb=train, ub=train+validation),
        'test': '{lb} <= {br} && {br} <= {ub}'.format(
            br=br, lb=train+validation, ub=100)
    }


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    gInterpreter.Declare('auto rand_gen = TRandom3({});'.format(args.seed))

    init_frame = RDataFrame(args.tree, args.ntp)
    rand_frame = init_frame.Define('rand_split', 'rand_gen.Uniform(0, 100)')
    if args.debug:
        print('loaded {} with {} entries'.format(
            args.ntp, rand_frame.Count().GetValue()))

    cuts = get_cuts(args.train_ratio, args.validation_ratio)
    for sample, cut in cuts.items():
        subsample_frame = rand_frame.Filter(cut)
        output_ntp = join(args.output_dir, '{}_{}.root'.format(
            get_filename(args.ntp), sample))

        subsample_frame.Snapshot(args.tree, output_ntp)

        if args.debug:
            print('sample: {}, cuts: {}'.format(sample, cut))
            print('wrote {} with {} entries'.format(
                output_ntp, subsample_frame.Count().GetValue()))

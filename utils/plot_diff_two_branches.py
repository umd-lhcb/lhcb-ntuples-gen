#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Thu Sep 26, 2019 at 12:23 PM -0400

import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from argparse import ArgumentParser
from find_common_uid import find_common_uid
from plot_single_branch import BINS
from plot_single_branch import read_branch, gen_histo, plot


#################################
# Command line arguments parser #
#################################

def parse_input():
    parser = ArgumentParser(description='''
generate two plots (diff, norm) comparing a branch of tree contained two
n-tuple.''')

    parser.add_argument('-n', '--ref',
                        nargs='?',
                        required=True,
                        help='''
path to reference n-tuple.''')

    parser.add_argument('-N', '--comp',
                        nargs='?',
                        required=True,
                        help='''
path to comparison n-tuple.''')

    parser.add_argument('-t', '--refTree',
                        nargs='?',
                        required=True,
                        help='''
supply tree name in the reference n-tuple.''')

    parser.add_argument('-T', '--compTree',
                        nargs='?',
                        required=True,
                        help='''
supply tree name in the comparison n-tuple.''')

    parser.add_argument('-b', '--branch',
                        nargs='?',
                        required=True,
                        help='''
supply a single branch name in both n-tuples.''')

    parser.add_argument('-o', '--output',
                        nargs='?',
                        required=True,
                        help='''
path to output directory.''')

    parser.add_argument('--bins',
                        nargs='?',
                        type=int,
                        default=BINS,
                        help='''
number of bins. default to {}.'''.format(BINS))

    parser.add_argument('--yAxisScale',
                        nargs='?',
                        default='linear',
                        help='''
y axis scale (linear or log).''')

    return parser.parse_args()


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    ref_branch = read_branch(args.ref, args.refTree, args.branch)
    comp_branch = read_branch(args.comp, args.compTree, args.branch)

    _, ref_idx, comp_idx = find_common_uid(args.ref, args.comp, args.refTree,
                                           args.compTree)

    # Keep the intersection between the two branches, also only keep events that
    # are unique
    ref_branch = ref_branch[ref_idx]
    comp_branch = comp_branch[comp_idx]

    diff_filename = args.branch + '_diff.png'
    diff_norm_filename = args.branch + '_diff_norm.png'

    # Plot the difference
    diff = comp_branch - ref_branch
    mean = diff.mean()
    std = diff.std()
    histo, bins = gen_histo(diff, args.bins)

    plot(histo, bins, os.path.join(args.output, diff_filename),
         args.branch+' (diff)', mean, std, args.yAxisScale)

    # Plot the normalized difference
    diff_norm = diff / ref_branch
    mean = diff_norm.mean()
    std = diff_norm.std()
    histo, bins = gen_histo(diff_norm, args.bins)

    plot(histo, bins, os.path.join(args.output, diff_norm_filename),
         args.branch+' (diff norm)', mean, std, args.yAxisScale)

#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Thu Sep 26, 2019 at 01:31 AM -0400

import uproot
import numpy as np

from argparse import ArgumentParser
from functools import partial
from matplotlib import pyplot as plt


################
# Configurable #
################

BINS = 200

FONT_FAMILY = 'monospace'
FONT_SIZE = '14'
PLT_STYLE = 'ggplot'


#################################
# Command line arguments parser #
#################################

def parse_input():
    parser = ArgumentParser(description='''
generate a pdf plot from a branch of tree contained in a n-tuple.'''
                            )

    parser.add_argument('ntuple',
                        help='''
path to n-tuple.''')

    parser.add_argument('tree',
                        help='''
tree name in n-tuple.''')

    parser.add_argument('branch',
                        help='''
branch name in tree.''')

    parser.add_argument('-o', '--output',
                        nargs='?',
                        required=True,
                        help='''
path to output pdf file.''')

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


######
# IO #
######

def read_branch(ntuple, tree=None, branch=None):
    ntp = uproot.open(ntuple)
    return ntp[tree].array(branch)


def gen_histo(array, bins=BINS):
    histo_range = (array.min(), array.max())
    return np.histogram(array, bins, histo_range)


########
# Plot #
########

def plot(histo, bins, output, title, mean, std, yAxisScale='linear'):
    plt.rcParams.update({'font.family': FONT_FAMILY})
    plt.rcParams.update({'font.size': FONT_SIZE})
    plt.style.use(PLT_STYLE)

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_yscale(yAxisScale)

    ax.bar(bins[:-1], histo, width=np.diff(bins),
           align='edge', color='blue', edgecolor='blue',
           label='mean: {:.2g} std: {:.2g}'.format(mean, std))
    ax.legend()

    plt.tight_layout(pad=0.1)  # Remove all paddings
    fig.savefig(output)


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    branch = read_branch(args.ntuple, args.tree, args.branch)

    mean = branch.mean()
    std = branch.std()
    histo, bins = gen_histo(branch, args.bins)

    plot(histo, bins, args.output, args.branch, mean, std, args.yAxisScale)

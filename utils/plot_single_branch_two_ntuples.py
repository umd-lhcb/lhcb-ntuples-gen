#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Tue Oct 01, 2019 at 04:22 PM -0400

import uproot
import numpy as np
import matplotlib as mp

from argparse import ArgumentParser
from matplotlib import pyplot as plt
from plot_single_branch import BINS
from plot_single_branch import PLT_STYLE, FONT_SIZE, FONT_FAMILY


#################################
# Command line arguments parser #
#################################

def parse_input():
    parser = ArgumentParser(description='''
generate a plot from the same branch of tree contained in two n-tuples.'''
                            )

    parser.add_argument('-n', '--ntuple1',
                        nargs='?',
                        required=True,
                        help='''
path to the first n-tuple.''')

    parser.add_argument('-N', '--ntuple2',
                        nargs='?',
                        required=True,
                        help='''
path to the second n-tuple.''')

    parser.add_argument('-t', '--tree1',
                        nargs='?',
                        required=True,
                        help='''
supply tree name in the first n-tuple.''')

    parser.add_argument('-T', '--tree2',
                        nargs='?',
                        required=True,
                        help='''
supply tree name in the second n-tuple.''')

    parser.add_argument('-b', '--branch',
                        nargs='?',
                        required=True,
                        help='''
branch name in both n-tuples.''')

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


######
# IO #
######

def read_branch(ntuple, tree=None, branch=None):
    ntp = uproot.open(ntuple)
    return ntp[tree].array(branch)


def gen_histo(array, bins=BINS, scale=1.05):
    min = array.min()
    max = array.max()

    min = min*scale if min < 0 else min/scale
    max = max/scale if min < 0 else max*scale

    return np.histogram(array, bins, (min, max))


########
# Plot #
########

def tick_formatter(x, p):
    X = str(x)
    if len(X) > 4:
        return '{:2g}'.format(x)
    else:
        return x


def plot_single_branch_two_ntuples(
    histo1, bins1, histo2, bins2, output, title, num1, num2,
        yAxisScale='linear'):
    plt.style.use(PLT_STYLE)
    plt.rcParams.update({'font.family': FONT_FAMILY})
    plt.rcParams.update({'font.size': FONT_SIZE})

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_yscale(yAxisScale)

    # Transparent colors
    BLUE = mp.colors.colorConverter.to_rgba('blue', alpha=.5)
    RED = mp.colors.colorConverter.to_rgba('red', alpha=.5)

    ax.bar(bins1[:-1], histo1, width=np.diff(bins1),
           align='edge', color=BLUE, edgecolor=BLUE,
           label='tot: {:.4g}'.format(num1))
    ax.bar(bins2[:-1], histo2, width=np.diff(bins1),
           align='edge', color=RED, edgecolor=RED,
           label='tot: {:.4g}'.format(num2))
    ax.legend()
    ax.set_title(title)
    # Reformat x-ticks
    ax.get_xaxis().set_major_formatter(
        mp.ticker.FuncFormatter(tick_formatter)
    )

    plt.tight_layout(pad=0.1)  # Remove all paddings
    fig.savefig(output)

    # Close figure
    fig.clf()
    plt.close(fig)


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    branch1 = read_branch(args.ntuple1, args.tree1, args.branch)
    branch2 = read_branch(args.ntuple2, args.tree2, args.branch)

    (histo1, bins1), (histo2, bins2) = \
        map(lambda x: gen_histo(x, args.bins), (branch1, branch2))

    plot_single_branch_two_ntuples(
        histo1, bins1, histo2, bins2, args.output, args.branch,
        branch1.size, branch2.size, args.yAxisScale)

#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Oct 12, 2021 at 03:32 AM +0200

import sys
import ROOT

from tabulate import tabulate
from argparse import ArgumentParser

################################
# Command line argument parser #
################################

def parse_input():
    parser = ArgumentParser(description='print the content of a ROOT histogram')

    parser.add_argument('ntp', help='input ntuple.')

    parser.add_argument('-H', '--histo', default='eff',
                        help='path to histo in the ntuple.')

    parser.add_argument('-O', '--overunder', action='store_true',
                        help='print over and under flow bins.')

    parser.add_argument('-f', '--format', default='pretty',
                        help='specify table format.')

    parser.add_argument('-m', '--multiline', action='store_true',
                        help='multiple lines for header row.')

    parser.add_argument('-T', '--transpose', action='store_true',
                        help='transpose the x, y axis')

    return parser.parse_args()


###########
# Helpers #
###########

def bin_info(histo, bin_idx, bin_lbl, multiline=True):
    bin_idx_max = getattr(histo, 'GetNbins{}'.format(bin_lbl))()
    axis = getattr(histo, 'Get{}axis'.format(bin_lbl))()

    if bin_idx == 0:
        lbl = '(U)'
    elif bin_idx == bin_idx_max + 1:
        lbl = '(O)'
    else:
        lbl = '({:.1f})'.format(axis.GetBinCenter(bin_idx))

    fmt = '{} \n {}' if multiline else '{} {}'

    return fmt.format(bin_idx, lbl)


def get_other_bins(lbl, axes=['X', 'Y', 'Z']):
    return [b for b in axes if b != lbl]


def loop_over_idx(histo, lbl, overunder=True):
    (lower, upper) = (0, 2) if overunder else (1, 1)
    idx_max = getattr(histo, "GetNbins{}".format(lbl))()
    return range(lower, idx_max+upper)


def get_val(histo, *bin_spec, method='GetBinContent'):
    args = dict(bin_spec)
    getter = getattr(histo, method)

    if 'Z' in args:
        return getter(args['X'], args['Y'], args['Z'])
    return getter(args['X'], args['Y'])


#############################
# Histogram content getters #
#############################

def get_th2_content(histo, overunder=True, multiline=False, transpose=False):
    tab = []
    lbl0, lbl1 = ['Y', 'X'] if not transpose else ['X', 'Y']
    headers = [lbl0 + ' \\ ' + lbl1]

    for i in loop_over_idx(histo, lbl0, overunder):
        row = []
        row.append(bin_info(histo, i, lbl0, False))

        for j in loop_over_idx(histo, lbl1, overunder):
            headers.append(bin_info(histo, j, lbl1, multiline=multiline))

            # Assume symmetric error
            row.append('{:.2f} ± {:.2f}'.format(
                get_val(histo, (lbl0, i), (lbl1, j)),
                get_val(histo, (lbl0, i), (lbl1, j), method='GetBinErrorLow')))

        tab.append(row)

    return tab, headers


def get_th3_content(histo, overunder=True, multiline=False, transpose=False,
                    project_axis='y'):
    tab = []
    pass


if __name__ == '__main__':
    args = parse_input()
    ntp = ROOT.TFile(args.ntp, "read")

    print("File: {}, Histo: {}".format(args.ntp, args.histo))

    histo = ntp.Get(args.histo)
    tab, headers = get_th2_content(
        histo, args.overunder, args.multiline, args.transpose)
    print(tabulate(tab, headers=headers, tablefmt=args.format))

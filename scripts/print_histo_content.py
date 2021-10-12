#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Oct 12, 2021 at 04:29 AM +0200

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

    parser.add_argument('-D', '--dimension', default='2',
                        help='specify dimension of the histo.')

    parser.add_argument('-A', '--axis', default='Y',
                        help='specify axis to slice for TH3.')

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


def get_other_lbls(lbl, axes=['X', 'Y', 'Z']):
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

def get_th2_content(histo, overunder=True, multiline=False, transpose=False,
                    lbl0='Y',
                    formatter=lambda x, y: tabulate(x, headers=y)):
    lbl0, lbl1 = ['Y', 'X'] if not transpose else ['X', 'Y']
    tab = []
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

    return formatter(tab, headers)


def get_th3_content(histo, overunder=True, multiline=False, transpose=False,
                    lbl0='Y',
                    formatter=lambda x, y: tabulate(x, headers=y)):
    output = 'Slicing axis: {}\n\n'.format(lbl0)
    lbl1, lbl2 = get_other_lbls(lbl0)
    if transpose:
        lbl1, lbl2 = lbl2, lbl1

    for i in loop_over_idx(histo, lbl0, overunder):
        output += '## {}, {}\n'.format(lbl0, bin_info(histo, i, lbl0, False))
        tab = []
        headers = [lbl1 + ' \\ ' + lbl2]

        for j in loop_over_idx(histo, lbl1, overunder):
            row = []
            row.append(bin_info(histo, j, lbl1, False))

            for k in loop_over_idx(histo, lbl2, overunder):
                headers.append(bin_info(histo, k, lbl2, multiline=multiline))

                # Assume symmetric error
                row.append('{:.2f} ± {:.2f}'.format(
                    get_val(histo, (lbl0, i), (lbl1, j), (lbl2, k)),
                    get_val(histo, (lbl0, i), (lbl1, j), (lbl2, k),
                            method='GetBinErrorLow')))

            tab.append(row)

        output += formatter(tab, headers)
        output += '\n\n'

    return output


########
# Main #
########

GETTERS = {
    '2': get_th2_content,
    '3': get_th3_content,
}

if __name__ == '__main__':
    args = parse_input()
    ntp = ROOT.TFile(args.ntp, "read")
    formatter = lambda x, y: tabulate(x, headers=y, tablefmt=args.format)
    getter = GETTERS[args.dimension]
    lbl0 = args.axis.upper()

    print("File: {}, Histo: {}".format(args.ntp, args.histo))

    histo = ntp.Get(args.histo)
    print(getter(
        histo, args.overunder, args.multiline, args.transpose, lbl0, formatter))

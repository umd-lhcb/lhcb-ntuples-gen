#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri Oct 01, 2021 at 02:34 AM +0200

import sys
import ROOT

from tabulate import tabulate
from argparse import ArgumentParser


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


def bin_info(histo, bin_idx, bin_idx_max,
             axis=lambda x: x.GetXaxis(), multiline=True):
    if bin_idx == 0:
        lbl = '(U)'
    elif bin_idx == bin_idx_max + 1:
        lbl = '(O)'
    else:
        lbl = '({:.1f})'.format(axis(histo).GetBinCenter(bin_idx))

    fmt = '{} \n {}' if multiline else '{} {}'

    return fmt.format(bin_idx, lbl)


def get_th2_content(histo, overunder=True, multiline=False, transpose=False):
    tab = []
    first_col = []
    headers = ['y \\ x'] if not transpose else ['x \\ y']

    x_max = histo.GetNbinsX()
    y_max = histo.GetNbinsY()
    (lower, upper) = (0, 2) if overunder else (1, 1)

    for y in range(lower, y_max+upper):
        row = []
        if not transpose:
            first_col.append(
                bin_info(histo, y, y_max, lambda x: x.GetYaxis(), False))
        else:
            headers.append(
                bin_info(histo, y, y_max, lambda x: x.GetYaxis(),
                         multiline=multiline))

        for x in range(lower, x_max+upper):
            if not transpose:
                headers.append(bin_info(histo, x, x_max, multiline=multiline))
            else:
                first_col.append(bin_info(histo, x, x_max, multiline=False))

            row.append('{:.2f} (-{:.2f} +{:.2f})'.format(
                histo.GetBinContent(x, y),
                histo.GetBinErrorLow(x, y), histo.GetBinErrorUp(x, y)))

        tab.append(row)

    if transpose:
        tab = zip(*tab)

    return [[lbl] + list(r) for r, lbl in zip(tab, first_col)], headers


if __name__ == '__main__':
    args = parse_input()
    ntp = ROOT.TFile(args.ntp, "read")

    print("File: {}, Histo: {}".format(args.ntp, args.histo))

    histo = ntp.Get(args.histo)
    tab, headers = get_th2_content(
        histo, args.overunder, args.multiline, args.transpose)
    print(tabulate(tab, headers=headers, tablefmt=args.format))

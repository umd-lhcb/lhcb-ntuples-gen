#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Dec 16, 2021 at 12:44 AM +0100

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

    parser.add_argument('--aliases', nargs='+', default=['p', 'η', 'nTrk'])

    return parser.parse_args()


###########
# Helpers #
###########

def bin_info(histo, bin_idx, bin_lbl, multiline=True):
    bin_idx_max = getattr(histo, 'GetNbins{}'.format(bin_lbl))()
    axis = getattr(histo, 'Get{}axis'.format(bin_lbl))()
    bins = list(axis.GetXbins())

    if bin_idx == 0:
        lbl = '(U)'
    elif bin_idx == bin_idx_max + 1:
        lbl = '(O)'
    # elif bin_idx == bin_idx_max:
    #     lbl = '({:.1f}, {:.1f})'.format(bins[bin_idx-1], bins[bin_idx])
    elif bin_idx == 1:
        lbl = ('({:.1f},{:.1f})'.format(bins[bin_idx-1], bins[bin_idx]))
    else:
        lbl = '({:.1f})'.format(bins[bin_idx])

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
                    formatter=lambda x, y: tabulate(x, headers=y),
                    aliases=dict()):
    lbl0, lbl1 = ['Y', 'X'] if not transpose else ['X', 'Y']
    tab = []
    headers = [aliases[lbl0] + ' \\ ' + aliases[lbl1]]

    for i in loop_over_idx(histo, lbl0, overunder):
        row = []
        row.append(bin_info(histo, i, lbl0, False))

        for j in loop_over_idx(histo, lbl1, overunder):
            headers.append(bin_info(histo, j, lbl1, multiline=multiline))

            # Assume symmetric error
            val = get_val(histo, (lbl0, i), (lbl1, j))
            err = get_val(histo, (lbl0, i), (lbl1, j), method='GetBinErrorLow')

            if str(val) != 'nan':
                row.append('{:.2f} ± {:.2f}'.format(val, err))
            else:
                row.append(val)

        tab.append(row)

    return formatter(tab, headers)


def get_th3_content(histo, overunder=True, multiline=False, transpose=False,
                    lbl0='Y',
                    formatter=lambda x, y: tabulate(x, headers=y),
                    aliases=dict()):
    output = 'Slicing axis: {}\n\n'.format(aliases[lbl0])
    lbl1, lbl2 = get_other_lbls(lbl0)
    if transpose:
        lbl1, lbl2 = lbl2, lbl1

    for i in loop_over_idx(histo, lbl0, overunder):
        output += '## {}, {}\n'.format(
            aliases[lbl0], bin_info(histo, i, lbl0, False))
        tab = []
        headers = [aliases[lbl1] + ' \\ ' + aliases[lbl2]]

        for j in loop_over_idx(histo, lbl1, overunder):
            row = []
            row.append(bin_info(histo, j, lbl1, False))

            for k in loop_over_idx(histo, lbl2, overunder):
                headers.append(bin_info(histo, k, lbl2, multiline=multiline))

                # Assume symmetric error
                val = get_val(histo, (lbl0, i), (lbl1, j), (lbl2, k))
                err = get_val(histo, (lbl0, i), (lbl1, j), (lbl2, k),
                              method='GetBinErrorLow')

                if str(val) != 'nan':
                    row.append('{:.2f} ± {:.2f}'.format(val, err))
                else:
                    row.append(val)

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
    aliases = dict(zip(['X', 'Y', 'Z'], args.aliases))

    print("File: {}, Histo: {}".format(args.ntp, args.histo))

    histo = ntp.Get(args.histo)
    print(getter(
        histo, args.overunder, args.multiline, args.transpose, lbl0,
        formatter, aliases))

#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Sep 23, 2021 at 02:36 PM +0200

import sys
import ROOT

from tabulate import tabulate


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


def get_th2_content(histo):
    tab = []
    headers = ['y \\ x']
    x_max = histo.GetNbinsX()
    y_max = histo.GetNbinsY()

    for y in range(y_max+2):
        row = [bin_info(histo, y, y_max, lambda x: x.GetYaxis(), False)]

        for x in range(x_max+2):
            headers.append(bin_info(histo, x, x_max))
            row.append('{:.2f}'.format(histo.GetBinContent(x, y)))

        tab.append(row)

    return tab, headers


if __name__ == '__main__':
    ntp = ROOT.TFile(sys.argv[1], "read")

    try:
        histo_name = sys.argv[2]
    except IndexError:
        histo_name = "eff"

    print("File: {}, Histo: {}".format(sys.argv[1], histo_name))

    histo = ntp.Get(histo_name)
    tab, headers = get_th2_content(histo)
    print(tabulate(tab, headers=headers, tablefmt='pretty'))

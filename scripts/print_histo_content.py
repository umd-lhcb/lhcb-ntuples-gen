#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Sep 23, 2021 at 12:35 AM +0200

import sys
import ROOT

from tabulate import tabulate


def get_th2_content(histo):
    result = []

    for y in range(histo.GetNbinsY()+1):
        row = [y]
        for x in range(histo.GetNbinsX()+1):
            row.append('{:.3f}'.format(histo.GetBinContent(x, y)))
        result.append(row)

    return result


if __name__ == '__main__':
    ntp = ROOT.TFile(sys.argv[1], "read")

    try:
        histo_name = sys.argv[2]
    except IndexError:
        histo_name = "eff"

    print("File: {}, Histo: {}".format(sys.argv[1], histo_name))

    histo = ntp.Get(histo_name)
    tab = get_th2_content(histo)
    print(tabulate(tab, headers=['y \\ x']+[
        str(i) for i in range(histo.GetNbinsX()+1)]))

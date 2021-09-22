#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Sep 22, 2021 at 11:52 PM +0200

import sys
import ROOT


def print_th2_content(histo):
    for x in range(histo.GetNbinsX()+1):
        for y in range(histo.GetNbinsY()+1):
            print('x: {}, y: {}, val: {}'.format(
                x, y, histo.GetBinContent(x, y)))


if __name__ == '__main__':
    ntp = ROOT.TFile(sys.argv[1], "read")

    try:
        histo_name = sys.argv[2]
    except IndexError:
        histo_name = "eff"

    print("File: {}, Histo: {}".format(sys.argv[1], histo_name))

    histo = ntp.Get(histo_name)
    print_th2_content(histo)

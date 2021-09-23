#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Sep 23, 2021 at 02:24 AM +0200
# Description: Merge and apply cuts on input .root files, each with multiple
#              trees, to a single output .root file.
#
#              Note that this is still based on Python 2, because on lxplus,
#              ROOT is compiled with Python 2 only.

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  # Don't hijack argparse!
ROOT.PyConfig.DisableRootLogon = True  # Don't read .rootlogon.py

from argparse import ArgumentParser

from ROOT import gInterpreter, RDataFrame
from ROOT.std import vector


################################
# Command line argument parser #
################################

def parse_input():
    parser = ArgumentParser(description='''
apply weights from a histogram to a ntuple.
''')

    parser.add_argument('input_ntp', help='input ntuple.')

    parser.add_argument('input_histo_ntp', help='input ntuple with histo.')

    parser.add_argument('output_ntp', help='output ntuple.')

    parser.add_argument('-t', '--tree', default='TupleB0/DecayTree',
                        help='specify input tree')

    parser.add_argument('--histo-name', default='eff',
                        help='specify histo name.')

    parser.add_argument('-x', '--x-name', default='mu_P',
                        help='specify x variable expression.')

    parser.add_argument('-y', '--y-name', default='ETA(mu_P, mu_PZ)',
                        help='specify y variable expression.')

    parser.add_argument('-w', '--wt-name', default='wt_pid_mu',
                        help='specify weight branch name.')

    return parser.parse_args()


###############
# C++ helpers #
###############

gInterpreter.Declare('''
#include <cmath>

#include <TMath.h>

using namespace std;

Double_t ETA(Double_t p, Double_t pz) {
  return 0.5 * TMath::Log((p + pz) / (p - pz));
}

Double_t GET_WEIGHT(Double_t x, Double_t y, TH2D* histo) {
  auto bin_idx = histo->FindBin(x, y);
  Double_t wt = histo->GetBinContent(bin_idx);

  if (isnan(wt)) {
    return -999.0;
  } else if (wt < 0.000001) {
    return -1.0;
  }
  return wt;
}
''')


def load_histo(input_histo_ntp, histo_name):
    gInterpreter.Declare(
        '''
        auto input_ntp = new TFile("{}", "read");
        auto histo = dynamic_cast<TH2D*>(input_ntp->Get("{}"));
        '''.format(input_histo_ntp, histo_name)
    )


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    load_histo(args.input_histo_ntp, args.histo_name)

    init_frame = RDataFrame(args.tree, args.input_ntp)
    histo_frame = init_frame.Define('x', args.x_name).Define('y', args.y_name)
    wt_frame = histo_frame.Define(args.wt_name, 'GET_WEIGHT(x, y, histo)')

    count_tot = wt_frame.Count().GetValue()
    count_bad = wt_frame.Filter('{} < 0'.format(args.wt_name)).Count().GetValue()
    count_nan = wt_frame.Filter('{} < -10'.format(args.wt_name)).Count().GetValue()

    output_brs = vector('string')(['runNumber', 'eventNumber', args.wt_name])
    wt_frame.Snapshot(args.tree, args.output_ntp, output_brs)

    print('Total event processed: {}, bad: {}, nan: {}. Bad fraction: {:.1f}%'.format(
        count_tot, count_bad, count_nan, count_bad / count_tot * 100))

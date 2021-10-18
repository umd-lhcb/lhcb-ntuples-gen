#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Oct 18, 2021 at 03:20 AM +0200
# Description: Merge and apply cuts on input .root files, each with multiple
#              trees, to a single output .root file.
#
#              Note that this is still based on Python 2, because on lxplus,
#              ROOT is compiled with Python 2 only.

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  # Don't hijack argparse!
ROOT.PyConfig.DisableRootLogon = True  # Don't read .rootlogon.py

from argparse import ArgumentParser
from yaml import safe_load
from glob import glob

from ROOT import gInterpreter, RDataFrame
from ROOT.std import vector


#################
# Configurables #
#################

DEFAULT_TREES = ['TupleB0/DecayTree', 'TupleBminus/DecayTree']
DEFAULT_WT_CONFIG = {
    'particle': 'Mu_nopt',
    'histo_name': 'eff',
    'vars': [
        'mu_PT',
        'ETA(mu_P, mu_PZ)',
        'nTracks'
    ]
}


##################
# Config parsers #
##################

def parse_input():
    parser = ArgumentParser(description='''
apply weights from a histogram to a ntuple.
''')

    parser.add_argument('input_ntp', help='input ntuple.')

    parser.add_argument('histo_folder',
                        help='folder that contains histo ntuples.')

    parser.add_argument('output_ntp', help='output ntuple.')

    parser.add_argument('-c', '--config', help='config file.', default=None)

    parser.add_argument('--year', default='2016', help='specify year.')
    parser.add_argument('--polarity', default='md', help='specify polarity.')

    return parser.parse_args()


def parse_config(yaml_file):
    if not yaml_file:
        config = dict()
        config['trees'] = DEFAULT_TREES
        config['config']['wpid'] = DEFAULT_WT_CONFIG
        return config

    with open(yaml_file, 'r') as f:
        config = safe_load(f)

    # Load defaults
    if 'trees' not in config:
        config['trees'] = DEFAULT_TREES

    for br in config['config']:
        for key, val in DEFAULT_WT_CONFIG.items():
            if key not in config['config'][br]:
                config['config'][br][key] = val

    return config


###########
# Helpers #
###########

def glob_histos(root_dir):
    return glob('{}/*.root'.format(root_dir))


def find_histo(histos, year, polarity, name):
    # Always return the first match
    return [h for h in histos if year in h and polarity in h and name in h][0]


###############
# C++ helpers #
###############

gInterpreter.Declare('''
#include <cmath>

#include <TMath.h>

using namespace std;

TFile* ntp_histo;
TH1D*  histo_1d;
TH2D*  histo_2d;
TH3D*  histo_3d;

Double_t ETA(Double_t p, Double_t pz) {
  return 0.5 * TMath::Log((p + pz) / (p - pz));
}

Double_t GET_WEIGHT(Double_t x, TH1D* histo) {
  auto bin_idx = histo->FindBin(x);
  Double_t wt = histo->GetBinContent(bin_idx);

  if (isnan(wt) || wt < 0) return -999.0;
  return wt;
}

Double_t GET_WEIGHT(Double_t x, Double_t y, TH2D* histo) {
  auto bin_idx = histo->FindBin(x, y);
  Double_t wt = histo->GetBinContent(bin_idx);

  if (isnan(wt) || wt < 0) return -999.0;
  return wt;
}

Double_t GET_WEIGHT(Double_t x, Double_t y, Double_t z, TH3D* histo) {
  auto bin_idx = histo->FindBin(x, y, z);
  Double_t wt = histo->GetBinContent(bin_idx);

  if (isnan(wt) || wt < 0) return -999.0;
  return wt;
}
''')


def load_histo(year, polarity, particle):
    gInterpreter.Declare('ntp_histo = new TFile("{}", "read");'.format(
        histo_ntp))

    gInterpreter.Declare('''
        histo_{dim}d = dynamic_cast<TH{dim}D*>(ntp_histo->Get("{name}"));
        '''.format(dim=dimension, name=histo_name)
    )


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()
    histos = glob_histos(args.histo_folder)
    config = parse_config(args.config)
    loaded_histos = dict()

    for tree in config['trees']:
        init_frame = RDataFrame(tree, args.input_ntp)
        frames = [init_frame]

        for br, directive in config['config']:
            args = ', '.join(directive['vars'])

            wt_histo = load_histo()
            wt_frame = frames[-1].Define(
                br, 'GET_WEIGHT({}, {})'.format(args, wt_histo))

    load_histo(args.input_histo_ntp, args.histo_name)

    histo_frame = init_frame.Define('x', args.x_name).Define('y', args.y_name)
    wt_frame = histo_frame.Define(args.wt_name, 'GET_WEIGHT(x, y, histo)')

    count_tot = wt_frame.Count().GetValue()
    count_bad = wt_frame.Filter('{} < 0'.format(args.wt_name)).Count().GetValue()

    output_brs = vector('string')(['runNumber', 'eventNumber', args.wt_name])
    wt_frame.Snapshot(args.tree, args.output_ntp, output_brs)

    print('Total event processed: {}, bad: {}. Bad fraction: {:.1f}%'.format(
        count_tot, count_bad, count_bad / count_tot * 100))

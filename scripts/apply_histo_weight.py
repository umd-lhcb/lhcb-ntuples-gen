#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Oct 18, 2021 at 03:47 AM +0200
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


def find_histo(histos, year, polarity, particle):
    # Always return the first match
    return [h for h in histos
            if year in h and polarity in h and particle in h][0]


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


def load_histo(year, polarity, particle, histo_name, histo_dim,
               histos, loaded_histos):
    histo_lbl = '_'.join([year, polarity, particle])

    if histo_lbl in loaded_histos:
        return loaded_histos[histo_lbl]

    try:
        ntp_filename = find_histo(histos, year, polarity, particle)
    except IndexError:
        raise(ValueError('Histo {} cannot be loaded! Abort!'.format(histo_lbl)))

    gInterpreter.Declare('auto ntp_{} = new TFile("{}", "read");'.format(
        histo_lbl, ntp_filename))
    gInterpreter.Declare('''
        auto histo_{lbl} = dynamic_cast<TH{dim}D*>(ntp_{lbl}->Get("{name}"));
        '''.format(lbl=histo_lbl, dim=histo_dim, name=histo_name)
    )

    loaded_histos[histo_lbl] = 'histo_' + histo_lbl
    return loaded_histos[histo_lbl]


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()
    histos = glob_histos(args.histo_folder)
    config = parse_config(args.config)
    loaded_histos = dict()

    for tree in config['trees']:
        print('Processing tree {}...'.format(tree))
        init_frame = RDataFrame(tree, args.input_ntp)
        frames = [init_frame]
        output_brs = vector('string')(['runNumber', 'eventNumber'])

        for br, directive in config['config'].items():
            print('Processing {}...'.format(br))
            params = ', '.join(directive['vars'])

            histo_name = directive['histo_name']
            histo_dim = len(directive['vars'])

            wt_histo = load_histo(
                args.year, args.polarity, directive['particle'],
                histo_name, histo_dim, histos, loaded_histos)
            wt_frame = frames[-1].Define(
                br, 'GET_WEIGHT({}, {})'.format(params, wt_histo))
            frames.append(wt_frame)

            output_brs.push_back(br)

        frames[-1].Snapshot(tree, args.output_ntp, output_brs)

#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sun Feb 27, 2022 at 11:36 PM -0500
# Description: Apply weights from histos.

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  # Don't hijack argparse!
ROOT.PyConfig.DisableRootLogon = True  # Don't read .rootlogon.py

from argparse import ArgumentParser
from yaml import safe_load
from glob import glob

from ROOT import gInterpreter, RDataFrame
from ROOT.std import vector
from ROOT.RDF import RSnapshotOptions


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
    ],
    'skip_tree': [],
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
    # NOTE: We add '-' around 'particle' to make sure the match is exact
    particle = '-{}-'.format(particle)
    # Always return the first match
    return [h for h in histos
            if year in h and polarity in h and particle in h][0]


def resolve_params(params, idx):
    resolved = []

    for p in params:
        cands = p.split(';')
        cands = [i.strip() for i in cands if i != '']

        try:
            resolved.append(cands[idx])
        except IndexError:
            resolved.append(cands[0])

    print('  Histo variables: {}'.format(', '.join(resolved)))

    return resolved


###############
# C++ helpers #
###############

gInterpreter.Declare('''
#include <cmath>

#include <TMath.h>

using namespace std;

Double_t P(Double_t px, Double_t py, Double_t pz) {
  return TMath::Sqrt(px*px + py*py + pz*pz);
}

Double_t ETA(Double_t p, Double_t pz) {
  return 0.5 * TMath::Log((p + pz) / (p - pz));
}

Double_t ETA(Double_t px, Double_t py, Double_t pz) {
  auto p = P(px, py, pz);
  return ETA(p, pz);
}

Double_t GUARD(Double_t val, Double_t low, Double_t high, Double_t offset=0.01) {
  if (val <= low) return low + offset;
  if (val >= high) return high - offset;
  return val;
}

Int_t GET_BIN(Double_t x, TH1D* histo) {
  return histo->FindFixBin(x);
}

Int_t GET_BIN(Double_t x, Double_t y, TH2D* histo) {
  return histo->FindFixBin(x, y);
}

Int_t GET_BIN(Double_t x, Double_t y, Double_t z, TH3D* histo) {
  return histo->FindFixBin(x, y, z);
}

Double_t GET_WEIGHT(Double_t x, TH1D* histo) {
  auto bin_idx = GET_BIN(x, histo);
  Double_t wt = histo->GetBinContent(bin_idx);

  if (isnan(wt) || wt < 0) return -999.0;
  return wt;
}

Double_t GET_WEIGHT(Double_t x, Double_t y, TH2D* histo) {
  auto bin_idx = GET_BIN(x, y, histo);
  Double_t wt = histo->GetBinContent(bin_idx);

  if (isnan(wt) || wt < 0) return -999.0;
  return wt;
}

Double_t GET_WEIGHT(Double_t x, Double_t y, Double_t z, TH3D* histo) {
  auto bin_idx = GET_BIN(x, y, z, histo);
  Double_t wt = histo->GetBinContent(bin_idx);

  if (isnan(wt) || wt < 0) return -999.0;
  return wt;
}
''')


def load_histo(year, polarity, particle, histo_name, histo_dim,
               histos, loaded_histos):
    histo_lbl = '_'.join([year, polarity, particle])+'_'+histo_name

    if histo_lbl in loaded_histos:
        return loaded_histos[histo_lbl]

    try:
        ntp_filename = find_histo(histos, year, polarity, particle)
    except IndexError:
        raise(ValueError('Histo {} cannot be loaded! Abort!'.format(histo_lbl)))

    print('  Loading histo {} from ntuple {}'.format(histo_name, ntp_filename))
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
    output_opts = RSnapshotOptions()
    output_opts.fMode = 'UPDATE'
    first_write = True

    for idx, tree in enumerate(config['trees']):
        print('Processing tree {}...'.format(tree))
        init_frame = RDataFrame(tree, args.input_ntp)
        frames = [init_frame]
        output_brs = vector('string')(['runNumber', 'eventNumber'])

        for br, directive in config['config'].items():
            if tree in directive['skip_tree']:
                continue

            print('  Processing {}...'.format(br))
            params = ', '.join(resolve_params(directive['vars'], idx))

            histo_name = directive['histo_name']
            histo_dim = len(directive['vars'])
            debug_br = 'debug_{}_bin_idx'.format(br)

            wt_histo = load_histo(
                args.year, args.polarity, directive['particle'],
                histo_name, histo_dim, histos, loaded_histos)
            wt_frame = frames[-1].Define(
                br, 'GET_WEIGHT({}, {})'.format(params, wt_histo)).Define(
                    debug_br, 'GET_BIN({}, {})'.format(params, wt_histo))
            frames.append(wt_frame)

            output_brs.push_back(br)
            output_brs.push_back(debug_br)

        if first_write:
            frames[-1].Snapshot(tree, args.output_ntp, output_brs)
            first_write = False
        else:
            frames[-1].Snapshot(tree, args.output_ntp, output_brs, output_opts)

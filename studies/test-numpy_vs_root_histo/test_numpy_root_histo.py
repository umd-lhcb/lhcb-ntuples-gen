#!/usr/bin/env python

import numpy as np
import uproot

from ROOT import RDataFrame, gInterpreter

#################
# Configuration #
#################

inputHistoNtp = '../../run2-JpsiK/gen/run2-JpsiK-2016-md-B-ndof_ntracks__pt_eta.root'
inputBrNtp = '../../run2-JpsiK/fit/fit_results/JpsiK-22_02_26_23_52-std-fit/fit.root'
inputTree = 'tree'

outputNumpy = './h_numpy.root'
outputRoot = './h_root.root'

histoName = 'h_occupancy'
histoBrs = ['b_ownpv_ndof', 'ntracks']


###################
# Numpy histogram #
###################

def getWeights(histo, branches, binSpecs):
    binIdx = []

    for br, spec in zip(branches, binSpecs):
        tmpIdx = np.digitize(br, spec) - 1
        # handle over/underflow
        tmpIdx = np.where(tmpIdx == -1, 0, tmpIdx)
        tmpIdx = np.where(tmpIdx >= spec.size-1, spec.size-2, tmpIdx)
        binIdx.append(tmpIdx)

    return histo[tuple(binIdx)]


histoUproot = uproot.open(inputHistoNtp)[histoName].to_numpy()
brUproot = list(uproot.concatenate(
    f'{inputBrNtp}:{inputTree}', histoBrs, library='np').values())
wtUproot = getWeights(histoUproot[0], brUproot, histoUproot[1:])


##################
# ROOT histogram #
##################

gInterpreter.Declare('''
Int_t GET_BIN(Double_t x, Double_t y, TH2D* histo) {
  return histo->FindFixBin(x, y);
}

Double_t GET_WEIGHT(Double_t x, Double_t y, TH2D* histo) {
  auto bin_idx = GET_BIN(x, y, histo);
  Double_t wt = histo->GetBinContent(bin_idx);
  return wt;
}
''')

gInterpreter.Declare(f'auto histoNtp = new TFile("{inputHistoNtp}", "read");')
gInterpreter.Declare(f'auto histo = dynamic_cast<TH2D*>(histoNtp->Get("{histoName}"));')

brRootFm = RDataFrame(inputTree, inputBrNtp)
wtRootFm = brRootFm.Define('wt', f'GET_WEIGHT({",".join(histoBrs)}, histo)')
wtRoot = wtRootFm.AsNumpy(columns=['wt'])['wt']


###################
# Compare results #
###################

counter = 0

for i in range(wtUproot.size):
    if wtUproot[i] != wtRoot[i]:
        print(f'At idx {i}, {wtUproot[i]} != {wtRoot[i]}')
        counter += 1

print(f'Total # of disagreements: {counter}')

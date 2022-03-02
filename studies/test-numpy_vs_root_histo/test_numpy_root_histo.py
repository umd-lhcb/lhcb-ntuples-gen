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
    histoPadded = np.pad(histo, tuple((1, 1) for _ in range(histo.ndim)))
    binIdx = tuple(np.digitize(br, spec)
                   for br, spec in zip(branches, binSpecs))

    return histoPadded[tuple(binIdx)]


histoUproot = uproot.open(inputHistoNtp)[histoName].to_numpy()
brUproot = list(uproot.concatenate(
    f'{inputBrNtp}:{inputTree}', histoBrs, library='np').values())
wtUproot = getWeights(histoUproot[0], brUproot, histoUproot[1:])


##################
# ROOT histogram #
##################

gInterpreter.Declare('''
Int_t getBin(Double_t x, Double_t y, TH2D* histo) {
  return histo->FindFixBin(x, y);
}

auto getWeight(Double_t x, Double_t y, TH2D* histo) {
  auto binIdx = getBin(x, y, histo);
  return histo->GetBinContent(binIdx);
}
''')

gInterpreter.Declare(f'auto histoNtp = new TFile("{inputHistoNtp}", "read");')
gInterpreter.Declare(f'auto histo = dynamic_cast<TH2D*>(histoNtp->Get("{histoName}"));')

brRootFm = RDataFrame(inputTree, inputBrNtp)
wtRootFm = brRootFm.Define('wt', f'getWeight({",".join(histoBrs)}, histo)')
wtRoot = wtRootFm.AsNumpy(columns=['wt'])['wt']


###################
# Compare results #
###################

counter = 0

for i in range(wtUproot.size):
    if wtUproot[i] != wtRoot[i]:
        print(f'At idx {i}, {wtUproot[i]} != {wtRoot[i]}')
        counter += 1

print(f'Total # of disagreements: {counter}/{wtRoot.size}')

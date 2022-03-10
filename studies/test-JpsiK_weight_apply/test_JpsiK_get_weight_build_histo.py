#!/usr/bin/env python
# Description: Test that weight application and histogram building are
#              consistent between ROOT and numpy

import numpy as np
import uproot

from ROOT import RDataFrame, gInterpreter
from ROOT.RDF import TH2DModel
from tabulate import tabulate


#################
# Configuration #
#################

mcNtpN = '../../ntuples/0.9.6-2016_production/JpsiK-mc-step2/JpsiK--22_03_10--mc--12143001--2016--md.root'
mcTreeN = 'tree'

histoNtpN = '../../run2-JpsiK/reweight/JpsiK/root-run2-JpsiK_oldcut/run2-JpsiK-2016-md-B-ndof_ntracks__pt_eta.root'
histoN = 'h_occupancy'


#################
# Histo w/ ROOT #
#################

gInterpreter.Declare('''
Int_t getBin(Double_t x, Double_t y, TH2D* histo) {
  return histo->FindFixBin(x, y);
}

auto getWeight(Double_t x, Double_t y, TH2D* histo) {
  auto binIdx = getBin(x, y, histo);
  return histo->GetBinContent(binIdx);
}
''')

gInterpreter.Declare(f'auto histoNtp = new TFile("{histoNtpN}", "read");')
gInterpreter.Declare(f'auto histo = dynamic_cast<TH2D*>(histoNtp->Get("{histoN}"));')

dfInit = RDataFrame(mcTreeN, mcNtpN)
df = dfInit.Define('wjk_alt', 'getWeight(b_ownpv_ndof, ntracks, histo)').Define('wt', 'wpid*wtrk*wjk_alt')

# NOTE: This comes from the existing ntuple
mcRootBrs = df.AsNumpy(columns=['wjk_occ', 'wjk_alt'])
wtJkOccRoot = mcRootBrs['wjk_occ']
wtJkOccAltRoot = mcRootBrs['wjk_alt']

histoRootMdl = TH2DModel(
    'histoRoot', 'histoRoot',
    20, 1, 200, 20, 0, 450
)
histoRoot = df.Histo2D(histoRootMdl, 'b_ownpv_ndof', 'ntracks', 'wt')


##################
# Histo w/ numpy #
##################

mcNumpyBrsN = ['b_ownpv_ndof', 'ntracks', 'wpid', 'wtrk', 'wjk_occ']
mcNumpyBrs = uproot.concatenate(f'{mcNtpN}:{mcTreeN}', mcNumpyBrsN, library='np')


def getWeights(branches, histoRaw):
    histo, *binSpecs = histoRaw
    histoPadded = np.pad(histo, tuple((1, 1) for _ in range(histo.ndim)))
    binIdx = tuple(np.digitize(br, spec)
                   for br, spec in zip(branches, binSpecs))

    return histoPadded[binIdx]

histoWtNp = uproot.open(histoNtpN)[histoN].to_numpy()

wtJkOccNp = getWeights(
    (mcNumpyBrs['b_ownpv_ndof'], mcNumpyBrs['ntracks']), histoWtNp)
histoNumpy, *_ = np.histogram2d(
    mcNumpyBrs['b_ownpv_ndof'], mcNumpyBrs['ntracks'],
    (20, 20), ((1, 200), (0, 450)),
    weights=mcNumpyBrs['wpid']*mcNumpyBrs['wtrk']*wtJkOccNp
)

tabData = []


##############
# Comparison #
##############
# Test the weights are the same
assert np.logical_and.reduce(wtJkOccAltRoot == wtJkOccNp)

for i in range(wtJkOccNp.size):
    if not wtJkOccNp[i] == wtJkOccRoot[i]:
        print(f'Weight not equal at {i}, ROOT: {wtJkOccRoot[i]}, Np: {wtJkOccNp[i]}')

print(f'Total size: {wtJkOccRoot.size}')
assert np.logical_and.reduce(wtJkOccNp == wtJkOccRoot)

# Test the histograms are the same
for i in range(20):
    for j in range(20):
        assert histoRoot.GetBinContent(i+1, j+1) == histoNumpy[i][j]
        tabData.append([
            f'({i}, {j})', f'{histoRoot.GetBinContent(i+1, j+1)}',
            f'{histoNumpy[i][j]}'
        ])

print(tabulate(
    tabData, headers=['index', 'MC yld (ROOT)', 'MC yld (np)'],
    tablefmt='github'))

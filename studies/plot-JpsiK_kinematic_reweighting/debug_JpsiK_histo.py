#!/usr/bin/env python

import numpy as np
import uproot

from ROOT import RDataFrame
from ROOT.RDF import TH2DModel


#################
# Configuration #
#################

mcNtpN = '../../ntuples/0.9.6-2016_production/JpsiK-mc-step2/JpsiK--22_03_04--mc--12143001--2016--md/JpsiK--22_03_04--mc--12143001--2016--md--000.root'
mcTreeN = 'tree'


#################
# Histo w/ ROOT #
#################

df = RDataFrame(mcTreeN, mcNtpN)

histoRootMdl = TH2DModel(
    'histoRoot', 'histoRoot',
    20, 1, 200, 20, 0, 450
)
histoRoot = df.Histo2D(histoRootMdl, 'b_ownpv_ndof', 'ntracks')


##################
# Histo w/ numpy #
##################

mcNumpyBrsN = ['b_ownpv_ndof', 'ntracks', 'wpid', 'wtrk']
mcNumpyBrs = uproot.concatenate(f'{mcNtpN}:{mcTreeN}', mcNumpyBrsN, library='np')

histoNumpy, *_ = np.histogram2d(
    mcNumpyBrs['b_ownpv_ndof'], mcNumpyBrs['ntracks'],
    (20, 20), ((1, 200), (0, 450))
)

for i in range(20):
    for j in range(20):
        print(f'Current idx: {i}, {j}')
        print(f'ROOT histo value: {histoRoot.GetBinContent(i+1, j+1)}')
        print(f'numpy histo value: {histoNumpy[i][j]}')
        assert histoRoot.GetBinContent(i+1, j+1) == histoNumpy[i][j]

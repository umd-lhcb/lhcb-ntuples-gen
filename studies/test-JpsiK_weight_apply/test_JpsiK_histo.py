#!/usr/bin/env python

import numpy as np
import uproot

from ROOT import RDataFrame
from ROOT.RDF import TH2DModel

from tabulate import tabulate


#################
# Configuration #
#################

mcNtpN = '../../ntuples/0.9.6-2016_production/JpsiK-mc-step2/JpsiK--22_03_04--mc--12143001--2016--md/JpsiK--22_03_04--mc--12143001--2016--md--000.root'
mcTreeN = 'tree'


#################
# Histo w/ ROOT #
#################

dfInit = RDataFrame(mcTreeN, mcNtpN)
df = dfInit.Define('wt', 'wpid*wtrk')

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

histoNumpy, *_ = np.histogram2d(
    mcNumpyBrs['b_ownpv_ndof'], mcNumpyBrs['ntracks'],
    (20, 20), ((1, 200), (0, 450)),
    weights=mcNumpyBrs['wpid']*mcNumpyBrs['wtrk']
    #  weights=mcNumpyBrs['wpid']*mcNumpyBrs['wtrk']*mcNumpyBrs['wjk_occ']
)

tabData = []

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

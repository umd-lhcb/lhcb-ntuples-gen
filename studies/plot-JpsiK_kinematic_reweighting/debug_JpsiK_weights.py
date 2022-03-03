#!/usr/bin/env python

import numpy as np
import uproot

from tabulate import tabulate
from uproot import concatenate


#################
# Configurables #
#################

# histoNtpN = '../../run2-JpsiK/reweight/JpsiK/root-run2-JpsiK_oldcut/run2-JpsiK-2016-md-B-ndof_ntracks__pt_eta.root'
histoNtpN = '../../run2-JpsiK/reweight/JpsiK/root-run2-JpsiK_oldcut/run2-JpsiK-2016-md-B-ndof_ntracks__pt_eta-old.root'

mcNtpsN = [
    '../../ntuples/0.9.6-2016_production/JpsiK-mc-step2/JpsiK--22_03_03--mc--12143001--2016--md/*.root:tree',
    '../../ntuples/0.9.6-2016_production/JpsiK-mc-step2/JpsiK--22_03_03--mc--12143001--2016--mu/*.root:tree',
]

histoMcRawN = 'h_occupancy_mc_raw'
histoDataRawN = 'h_occupancy_data_raw'
histoRatioN = 'h_occupancy'

mcBrsN = ['b_ownpv_ndof', 'ntracks', 'wjk_occ', 'wpid', 'wtrk']


#########################################
# Rebuild histogram from step-2 ntuples #
#########################################

mcBrs = concatenate(mcNtpsN, mcBrsN, library='np')

hResult, *hBins = np.histogram2d(
    mcBrs['b_ownpv_ndof'], mcBrs['ntracks'], (20, 20), ((1, 200), (0, 450)),
    weights=mcBrs['wjk_occ']*mcBrs['wpid']*mcBrs['wtrk'])


############################
# Load existing histograms #
############################

histoNtp= uproot.open(histoNtpN)

hData, *_ = histoNtp[histoDataRawN].to_numpy()
hMc, *_ = histoNtp[histoMcRawN].to_numpy()
hRatio, *_ = histoNtp[histoRatioN].to_numpy()


##################
# Generate table #
##################

# assert 'Applied' == 'MC yield' or 0
TAB_GEN = {
    'index': lambda i, j: f'({i}, {j})',
    'data yld': lambda i, j: hData[i, j],
    'MC yld': lambda i, j: hMc[i, j],
    'data/MC wt': lambda i, j: hRatio[i, j],
    '<MC yld rwt>': lambda i, j: hMc[i, j] * hRatio[i, j],
    'MC yld rwt': lambda i, j: hResult[i, j],
    'diff': lambda i, j: hMc[i, j] * hRatio[i, j] - hResult[i, j]
}

tab = [list(TAB_GEN)]

for i in range(len(hBins[0]) - 1):
    for j in range(len(hBins[1]) - 1):
        tab.append([f(i, j) for f in TAB_GEN.values()])

print(tabulate(tab[1:], headers=tab[0], tablefmt='github'))

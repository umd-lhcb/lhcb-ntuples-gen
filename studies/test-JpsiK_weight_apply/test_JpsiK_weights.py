#!/usr/bin/env python

import numpy as np
import uproot

from tabulate import tabulate
from uproot import concatenate


#################
# Configurables #
#################

histoNtpN = '../../run2-JpsiK/reweight/JpsiK/root-run2-JpsiK_oldcut/run2-JpsiK-2016-md-B-ndof_ntracks__pt_eta.root'

mcNtpsN = [
   '../../ntuples/0.9.6-2016_production/JpsiK-mc-step2/JpsiK--22_03_09--mc--12143001--2016--md.root:tree',
   '../../ntuples/0.9.6-2016_production/JpsiK-mc-step2/JpsiK--22_03_09--mc--12143001--2016--mu.root:tree',
]

histoMcRawN = 'h_occupancy_mc_raw'
histoDataRawN = 'h_occupancy_data_raw'
histoRatioN = 'h_occupancy'

mcBrsN = ['b_ownpv_ndof', 'ntracks', 'wjk_occ', 'wpid', 'wtrk']


#########################################
# Rebuild histogram from step-2 ntuples #
#########################################

mcBrsRaw = concatenate(mcNtpsN, mcBrsN, library='np')

# Apply a global cut
globalCut = mcBrsRaw['ntracks'] < 450
mcBrs = {k: v[globalCut] for k, v in mcBrsRaw.items()}

hResult, *hResultBins = np.histogram2d(
    mcBrs['b_ownpv_ndof'], mcBrs['ntracks'], (20, 20), ((1, 200), (0, 450)),
    weights=mcBrs['wjk_occ'])
hMc, *hMcBins = np.histogram2d(
    mcBrs['b_ownpv_ndof'], mcBrs['ntracks'], (20, 20), ((1, 200), (0, 450)))


############################
# Load existing histograms #
############################

histoNtp= uproot.open(histoNtpN)

hData, *hDataBins = histoNtp[histoDataRawN].to_numpy()
hRatio, *hRatioBins = histoNtp[histoRatioN].to_numpy()


##################
# Generate table #
##################

def relDiff(i, j):
    if hResult[i, j] == 0:
        return 0
    return (hMc[i, j] * hRatio[i, j] - hResult[i, j]) / hResult[i, j]


# assert 'Applied' == 'MC yield' or 0
TAB_GEN = {
    'index': lambda i, j: f'({i}, {j})',
    'data yld': lambda i, j: hData[i, j],
    'MC yld': lambda i, j: hMc[i, j],
    'data/MC wt': lambda i, j: hRatio[i, j],
    '<MC yld rwt>': lambda i, j: hMc[i, j] * hRatio[i, j],
    'MC yld rwt': lambda i, j: hResult[i, j],
    'rel diff': relDiff
}

tabHead = list(TAB_GEN)
tabData = []

for i in range(len(hResultBins[0]) - 1):
    for j in range(len(hResultBins[1]) - 1):
        tabData.append([f(i, j) for f in TAB_GEN.values()])

tabDataLarge = [r for r in tabData if np.abs(r[-1]) >= 0.01]
print('\nThese bins have large relative differences:')
print(tabulate(tabDataLarge, headers=tabHead, tablefmt='github'))

print('\nStats for all bins:')
print(tabulate(tabData, headers=tabHead, tablefmt='github'))

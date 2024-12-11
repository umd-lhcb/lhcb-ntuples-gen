import ROOT
from glob import glob
import os

baseNew = 'ntuples/0.9.12-all_years/Dst_D0-mc-tracker_only/'
baseOld = 'ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/'
for folderNew in glob(f'{baseNew}/*'):
    mcID = folderNew.split('_')[-2]
    pol = 'MagDown'
    if 'MagUp' in folderNew: pol = 'MagUp'
    ## Finding the folder in the old production with the same MC ID
    for folderOld in glob(f'{baseOld}/*'):
        if mcID in folderOld and pol in folderOld: break
    #print(f'Folder new = {folderNew} and old = {folderOld}')
    print()
    ## Comparing ntuples
    for treeName in ['Bminus', 'B0']:
        new = ROOT.TChain(f'Tuple{treeName}/DecayTree')
        old = ROOT.TChain(f'Tuple{treeName}/DecayTree')
        newFiles = new.Add(f'{folderNew}/*dv.root')
        oldFiles = old.Add(f'{folderOld}/*dv.root')
        Nnew = float(new.GetEntries())
        Nold = float(old.GetEntries())
        diff = (Nnew-Nold)/Nold*100
        print(f'For {mcID}_{pol:<7} {treeName:>7}: new = {Nnew:>11,.0f}, old = {Nold:>11,.0f}, diff = {diff:>8.4f}%.   {newFiles} vs {oldFiles} files')
        # cut = 'b_ENDVERTEX_X > 1 && b_P > 50000'
        # if treeName == 'B0': cut = cut.replace('b_', 'b0_')
        # Nnew = float(new.GetEntries(cut))
        # Nold = float(old.GetEntries(cut))
        # diff = (Nnew-Nold)/Nold*100
        # print(f'For {cut}: new = {Nnew:>11,.0f}, old = {Nold:>11,.0f}, diff = {diff:>8.4f}%')


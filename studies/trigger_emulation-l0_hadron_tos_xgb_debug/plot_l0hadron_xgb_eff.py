#!/usr/bin/env python
#
# Script to merge the emu ntuples with the XGB output and plot turn-on curves

import os
import pathlib
import sys

def runCmd(cmd):
    print('\n \033[92m'+cmd+'\033[0m')
    os.system(cmd)

def mergePlot(tag, var, trigs, basecut, minx, maxx, nbins):
    print('\n===== Merging emu ntuples with XGB output and plotting turn-on curves for '+tag)
    ## Ntuples without the XGB output
    tagEmu = tag[tag.find('--')+2:]
    tagEmu = tagEmu[tagEmu.find('--')+2:]
    emuFolder = '../ntuple-RDX_l0_hadron_tos_training_sample/'
    ntpEmu = emuFolder+'l0hadron_emu_'+tagEmu+'.root'
    if not pathlib.Path(ntpEmu).is_file():
        print(ntpEmu+' does not exist. You need to generate it first')

    ## Folder with the XGB file
    xgbFolder = '../../../TrackerOnlyEmu/studies/l0hadron_train_xgb/'
    ntpXgb = xgbFolder+'l0hadron-'+tag+'.root'
    if not pathlib.Path(ntpXgb).is_file():
        sys.exit(ntpXgb+' does not exist. Make sure lhcb-ntuples-gen and TrackerOnlyEmu are on the same folder')

    ## Merging emu ntuples with XGB output
    haddEx = '../../scripts/haddcut.py '
    ntp = 'l0hadron_full_'+tag+'.root'
    if not pathlib.Path(ntp).is_file():
        runCmd(haddEx+ntp+' '+ntpEmu+' '+ntpXgb+' -s -m friend')
    
    ## Plot options
    plotEx = 'root -l \'../../scripts/plot_trigger_wefficiencies.C'
    binning = str(minx)+', '+str(maxx)+', '+str(nbins)
    strigs = '", "'.join(trigs)

    ## Plotting turn-on curves
    runCmd('mkdir -p '+tag)
    runCmd(plotEx+'("'+ntp+'", "'+var+'", {"'+strigs+'"},"'+basecut+'", '+binning+', "'+tag+'")\'')

d0Trigs = ['d0_L0HadronDecision_TOS', 'd0_l0_hadron_prob','d0_l0_hadron_tos_emu_no_bdt','d0_l0_hadron_tos_emu']
kTrigs = [trig.replace('d0_','k_') for trig in d0Trigs]

cutTm = 'max(k_L0Calo_HCAL_TriggerET, pi_L0Calo_HCAL_TriggerET) > 0'
cutNtm = 'max(k_L0Calo_HCAL_TriggerET, pi_L0Calo_HCAL_TriggerET) <= 0'
cutTmK = 'k_L0Calo_HCAL_TriggerET > 0'
cutNtmK = 'k_L0Calo_HCAL_TriggerET <= 0'

mergePlot('xgb_4_300_d0--tm_train--tm_valid', "d0_PT/1000", d0Trigs, "1", 0, 20, 40)
mergePlot('xgb_4_300_d0--ntm_train--ntm_valid', "d0_PT/1000", d0Trigs[0:3], "1", 0, 20, 40)


mergePlot('xgb_4_300_d0--all_train--all_valid', "d0_PT/1000", d0Trigs[0:3], "1", 0, 20, 40)

mergePlot('xgb_4_300_d0--all_train--all_valid', "FitVar_El/1000", d0Trigs[0:3], "1", 0, 4, 20)
mergePlot('xgb_4_300_d0--all_train--all_valid', "FitVar_Mmiss2/1000000", d0Trigs[0:3], "1", -2, 9, 20)
mergePlot('xgb_4_300_d0--all_train--all_valid', "FitVar_q2/1000000", d0Trigs[0:3], "1", -2, 11, 20)
mergePlot('xgb_4_300_d0--all_train--all_valid', "b0_ISOLATION_BDT", d0Trigs[0:3], "1", -1, 1, 20)

mergePlot('xgb_4_300_d0--all_train--all_valid', "d0_PT/1000", d0Trigs[0:3], cutTm, 0, 20, 40)
mergePlot('xgb_4_300_d0--all_train--all_valid', "d0_PT/1000", d0Trigs[0:3], cutNtm, 0, 20, 40)

mergePlot('xgb_4_300_k--all_train--all_valid', "k_PT/1000", kTrigs[0:2], "1", 0, 20, 40)
mergePlot('xgb_4_300_k--all_train--all_valid', "k_PT/1000", kTrigs[0:2], cutTmK, 0, 20, 40)
mergePlot('xgb_4_300_k--all_train--all_valid', "k_PT/1000", kTrigs[0:2], cutNtmK, 0, 20, 40)



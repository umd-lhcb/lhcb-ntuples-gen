#!/usr/bin/env python
#
# Script to merge the emu ntuples with the BDT output and plot turn-on curves

import os
import pathlib
import sys

def run_cmd(cmd):
    print('\n \033[92m'+cmd+'\033[0m')
    os.system(cmd)

def mergePlot(tag):
    print('\n===== Merging emu ntuples with BDT output and plotting turn-on curves for '+tag)
    ## Ntuples without the BDT output
    emuFolder = '../ntuple-RDX_l0_hadron_tos_training_sample/'
    ntpEmu = emuFolder+'l0hadron_emu_tm_train.root'
    if 'valid' in tag: ntpEmu = emuFolder+'l0hadron_emu_tm_valid.root'
    if 'ntm' in tag: ntpEmu = emuFolder+'l0hadron_emu_ntm.root'
    if not pathlib.Path(ntpEmu).is_file():
        print(ntpEmu+' does not exist. You need to generate it first')
    ## Folder with the BDT
    bdtFolder = '../l0hadron_train_bdt/'
    ntpBdt = bdtFolder+'l0hadron_'+tag+'.root'
    if not pathlib.Path(ntpBdt).is_file():
        sys.exit(ntpBdt+' does not exist. Make sure lhcb-ntuples-gen and TrackerOnlyEmu are on the same folder')

    ## Executables
    haddEx = '../../scripts/haddcut.py '
    plotEx = '../../scripts/plot_trigger_efficiencies.py '
    ## Plot options
    cOptions = ' --ext png --ratio-plot --bins 40 -b d0_L0HadronDecision_TOS d0_l0_hadron_tos_emu_no_bdt d0_l0_hadron_tos_emu -k d0_PT --xlabel "\$D^0$ \$p_T$" -o turnon'
    spdCut = 'SPDl450 -c "NumSPDHits<450" "NumSPDHits<450" "NumSPDHits<450"'
    treeName = '/TupleB0/DecayTree'
    titleWide = ' -D 0 20000 --title "Wide L0Hadron TOS '+tag+'"'

    ## Merging emu ntuples with BDT output
    ntp = 'l0hadron_full_'+tag+'.root'
    if not pathlib.Path(ntp).is_file():
        run_cmd(haddEx+ntp+' '+ntpBdt+' '+ntpEmu+' -s -m friend')

    ## Plotting turn-on curves
    run_cmd(plotEx+' -n '+ntp+treeName + titleWide + cOptions)
    run_cmd(plotEx+' -n '+ntp+treeName + titleWide + cOptions + spdCut)


mergePlot('bdt40_tm_train')
mergePlot('bdt4_tm_train')
mergePlot('bdt40_tm_valid')
mergePlot('bdt4_tm_valid')
mergePlot('bdt4_ntm')

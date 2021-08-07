#!/usr/bin/env python
#
# Script to generate various samples for the trigger emulation

import os
import pathlib

def run_cmd(cmd):
    print('\n \033[92m'+cmd+'\033[0m')
    os.system(cmd)

def mergeSlim(tag, ntpIn, ntpTrig):
    tmpFile1 = 'l0had_emu_'+tag+'_full_tmp.root'
    tmpFile2 = 'l0had_emu_'+tag+'_tmp.root'
    run_cmd('../../scripts/haddcut.py '+tmpFile1+' '+ntpIn+' -s -c l0hadron_sample_'+tag+'.yml')
    run_cmd('../../scripts/haddcut.py '+tmpFile2+' '+tmpFile1+' '+ntpTrig
    +' -s -c l0hadron_sample_'+tag+'.yml -m friend')
    ntpOut = 'l0hadron_emu_'+tag+'.root'
    run_cmd('../../scripts/haddcut.py '+ntpOut+' '+tmpFile2+' -s -c l0hadron_sample_'+tag+'.yml')
    return ntpOut

ntpIn = '../../ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root'
ntpTrig = 'l0hadron_emu.root'

print('\n===== Running L0Hadron emulation and producing (non) truth-matched ntuples')
run_cmd('../../lib/python/TrackerOnlyEmu/scripts/run2-rdx-l0_hadron.py '+ntpIn+' '+ntpTrig+' -t TupleB0/DecayTree')
# Slimming the non-truthmatched ntuple and merging it with the trigger emulation
mergeSlim('ntm', ntpIn, ntpTrig)
# Slimming the truthmatched ntuple and merging it with the trigger emulation, dividing it into samples
ntpTm = mergeSlim('tm', ntpIn, ntpTrig)
run_cmd('root -l \'../../scripts/split_train_vali_test.C("'+ntpTm+'")\'')
# run_cmd('rm *_tmp.root')
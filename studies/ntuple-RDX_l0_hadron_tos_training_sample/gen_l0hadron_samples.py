#!/usr/bin/env python
#
# Script to generate various samples for the trigger emulation

import os
import pathlib
import sys

from os.path import splitext


###########
# Helpers #
###########

def runCmd(cmd):
    print('   \033[92m'+cmd+'\033[0m')
    os.system(cmd)


######################
# Generating ntuples #
######################

def emulate(ntpIn, ntpOut='l0hadron_emu.root'):
    exe = '../../lib/python/TrackerOnlyEmu/scripts/run2-rdx-l0_hadron.py'
    cmd = f'{exe} {ntpIn} {ntpOut} -t TupleB0/DecayTree'
    runCmd(cmd)
    return ntpOut


def mergeSlim(tag, ntpIn, ntpTrig):
    exe = '../../scripts/haddcut.py'
    yml = 'l0hadron_sample_'+tag+'.yml'
    print('\n===== Running L0Hadron emulation and merging ntuples with '+yml)

    tmpFile1 = 'l0had_emu_'+tag+'_full_tmp.root'
    tmpFile2 = 'l0had_emu_'+tag+'_tmp.root'

    runCmd(f'{exe} {tmpFile1} {ntpIn} -s -c {yml}')
    runCmd(f'{exe} {tmpFile2} {tmpFile1} {ntpTrig} -s -c {yml} -m friend')

    ntpOut = 'l0hadron_emu_'+tag+'.root'
    runCmd(f'{exe} {ntpOut} {tmpFile2} -s -c {yml}')

    return ntpOut


def splitTrainValid(ntpIn, ratio='50:50'):
    base = splitext(ntpIn)[0]
    ntpsOut = [base+'_'+mode+'.root' for mode in ['train', 'valid', 'test']]

    runCmd(f'root -l \'../../scripts/split_train_vali_test.C("{ntpIn}", "{ratio}")\'')
    return ntpsOut


#############
# Workflows #
#############

def workflowEmulateThenSplit(ntpIn):
    ## Emulate the trigger first
    ntpTrig = emulate(ntpIn)

    ## Slimming the non-truthmatched ntuple and merging it with the trigger emulation
    ntpNtm = mergeSlim('ntm', ntpIn, ntpTrig)
    splitTrainValid(ntpNtm)

    ## Slimming the truthmatched ntuple and merging it with the trigger emulation, dividing it into samples
    ntpTm = mergeSlim('tm', ntpIn, ntpTrig)
    splitTrainValid(ntpTm)

    ## Slimming the full ntuple and merging it with the trigger emulation, dividing it into samples
    ntpAll = mergeSlim('all', ntpIn, ntpTrig)
    splitTrainValid(ntpAll, '35:35')

    runCmd('rm *_tmp.root')


########
# Main #
########

if __name__ == '__main__':
    ntpIn = '../../ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root'

    if not pathlib.Path(ntpIn).is_file():
        sys.exit(ntpIn+' does not exist, you need to download it')

    if len(sys.argv) == 1 or sys.argv[1] == 'EmuThenSplit':
        workflowEmulateThenSplit(ntpIn)

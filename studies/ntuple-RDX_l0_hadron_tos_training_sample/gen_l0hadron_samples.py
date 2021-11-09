#!/usr/bin/env python
#
# Script to generate various samples for the trigger emulation

import os
import pathlib
import sys

from os.path import splitext, isfile


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


def splitTrainValid(ntpIn, ratio='50:50', modes=['train', 'valid', 'test']):
    base = splitext(ntpIn)[0]
    modes_orig = ['train', 'valid', 'test']
    ntpsOutOrig = [base+'_'+mode+'.root' for mode in modes_orig]  # ROOT macro generates fixed output names
    ntpsOut = [base+'_'+mode+'.root' for mode in modes]

    runCmd(f'root -l \'../../scripts/split_train_vali_test.C("{ntpIn}", "{ratio}")\'')

    for ntpOrig, ntp in zip(ntpsOutOrig, ntpsOut):
        if not isfile(ntp):
            runCmd(f'mv {ntpOrig} {ntp}')

    return ntpsOut


def slim(tag, ntpIn):
    yml = 'l0hadron_sample_'+tag+'.yml'
    ntpOut = 'l0hadron_emu_'+tag+'_tmp.root'

    runCmd(f'../../scripts/haddcut.py {ntpOut} {ntpIn} -s -c {yml}')
    return ntpOut


def mergeFriend(ntpOut, ntpsIn):
    runCmd(f'../../scripts/haddcut.py -m friend {ntpOut} {" ".join(ntpsIn)}')
    return ntpOut


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


def workflowSplitThenEmulate(ntpIn):
    ntpTm = slim('tm', ntpIn)
    ntpTmTrain, ntpTmValid, _, = splitTrainValid(ntpTm)
    ntpTmEmu = emulate(ntpTm, 'l0hadron_emu_tm.root')
    mergeSlim('tm', ntpTm, ntpTmEmu)

    ntpNtm = slim('ntm', ntpIn)
    ntpNtmTrain, ntpNtmValid, _, = splitTrainValid(ntpNtm)
    ntpNtmEmu = emulate(ntpNtm, 'l0hadron_emu_ntm.root')
    mergeSlim('ntm', ntpNtm, ntpNtmEmu)

    ntpAll = slim('all', ntpIn)
    ntpAllTrain, ntpAllValid, _ = splitTrainValid(ntpAll, '35:35')
    ntpAllEmu = emulate(ntpAll, 'l0hadron_emu_all.root')
    mergeSlim('all', ntpAll, ntpAllEmu)

    for idx, ntp in enumerate([ntpTmTrain, ntpTmValid,
                               ntpNtmTrain, ntpNtmValid,
                               ntpAllTrain, ntpAllValid]):
        ntpEmu = emulate(ntp, f'l0hadron_emu_{idx}_tmp.root')
        mergeFriend(ntp.replace('_tmp', ''), [ntpEmu, ntp])

    runCmd('rm *_tmp.root')


########
# Main #
########

if __name__ == '__main__':
    ntpIn = '../../ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root'

    if not pathlib.Path(ntpIn).is_file():
        sys.exit(ntpIn+' does not exist, you need to download it')

    if len(sys.argv) == 1 or sys.argv[1] == 'EmuThenSplit':
        print('Emulate then split')
        workflowEmulateThenSplit(ntpIn)
    else:
        print('Split then emulate')
        workflowSplitThenEmulate(ntpIn)

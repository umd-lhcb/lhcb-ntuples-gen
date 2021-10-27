#!/usr/bin/env python
#
# Description: Debugging for L0Hadron TOS emulation, including:
#              - Generation of training and validation ntuples
#              - Training of BDT and XGB
#              - Plotting

import os
import sys

from os.path import isfile
from os.path import splitext


###########
# Helpers #
###########

def runCmd(cmd):
    print('  \033[92m'+cmd+'\033[0m')
    os.system(cmd)


######################
# Generating ntuples #
######################

def slim(tag, ntpIn):
    yml = 'l0hadron_sample_'+tag+'.yml'
    ntpOut = 'l0hadron_emu_'+tag+'.root'

    if isfile(ntpOut):
        print('File exists: {}'.format(ntpOut))
        return ntpOut

    runCmd('../../scripts/haddcut.py '+ntpOut+' '+ntpIn+' -s -c '+yml)
    return ntpOut


def merge(ntpOut, ntpsIn):
    if isfile(ntpOut):
        print('Already merged.')
        return ntpOut

    runCmd('hadd -fk {} {}'.format(ntpOut, ' '.join(ntpsIn)))
    return ntpOut


def rename(ntpOut, ntpIn):
    if isfile(ntpOut):
        return ntpOut

    runCmd('mv {} {}'.format(ntpIn, ntpOut))
    return ntpOut


def splitTrainValid(ntpIn):
    base = splitext(ntpIn)[0]
    ntpsOut = [base+'_'+mode+'.root' for mode in ['train', 'valid', 'test']]

    if False not in [isfile(f) for f in ntpsOut]:
        print('Already split.')
        return ntpsOut

    runCmd('root -l \'../../scripts/split_train_vali_test.C("'+ntpIn+'", "50:50")\'')
    return ntpsOut


ntpIn = '../../ntuples/0.9.5-bugfix/Dst_D0-mc/Dst_D0--21_10_08--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root'

if not isfile(ntpIn):
    sys.exit(ntpIn+' does not exist, you need to download it')

## Slimming the trigger-matched ntuple
ntpTm = slim('tm', ntpIn)
ntpTmTrain, ntpTmValid, _ = splitTrainValid(ntpTm)

## Slimming the non-trigger-matched ntuple
ntpNtm = slim('ntm', ntpIn)
ntpNtmTrain, ntpNtmValid, _ = splitTrainValid(ntpNtm)

## Merge the training samples for XGB
ntpTrainXgb = merge('run2-rdx-train_xgb.root', [ntpTmTrain, ntpNtmTrain])

## Merge the validation samples
ntpValid = merge('run2-rdx-train_xgb.root', [ntpTmValid, ntpNtmValid])

## Only use trigger-matched training sample for BDG
ntpTrainBdt = rename('run2-rdx-train_bdt.root', ntpTmTrain)

## Remove unused ntuples
# runCmd('rm l0hadron_emu*.root')


####################
# Train on ntuples #
####################

def train(tag, ntpIn, ntpOut, dumped):
    exe = '../../lib/python/TrackerOnlyEmu/scripts/run2-rdx-l0_hadron_trainload_'+tag+'.py'
    runCmd(exe+' '+ntpIn+' '+ntpOut+' --dump-bdt '+dumped)
    return ntpOut, dumped


# _, bdt4 = train('bdt', ntpTrainBdt, 'tmp.root', 'bdt4.pickle')


###############
# Debug plots #
###############

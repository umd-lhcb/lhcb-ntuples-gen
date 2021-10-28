#!/usr/bin/env python
#
# Script to generate various samples for the trigger emulation

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
    runCmd('../../scripts/haddcut.py '+ntpOut+' '+ntpIn+' -s -c '+yml)
    return ntpOut


def merge(ntpOut, ntpsIn):
    runCmd('hadd -fk {} {}'.format(ntpOut, ' '.join(ntpsIn)))
    return ntpOut


def splitTrainValid(ntpIn):
    base = splitext(ntpIn)[0]
    ntpsOut = [base+'_'+mode+'.root' for mode in ['train', 'valid', 'test']]
    runCmd('root -l \'../../scripts/split_train_vali_test.C("'+ntpIn+'", "50:50")\'')
    return ntpsOut


# ntpIn = '../../ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root'
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
ntpValid = merge('run2-rdx-valid.root', [ntpTmValid, ntpNtmValid])

## Only use trigger-matched training sample for BDT
ntpTrainBdt = merge('run2-rdx-train_bdt.root', [ntpTmTrain])

## Remove unused ntuples
runCmd('rm l0hadron_emu*.root')

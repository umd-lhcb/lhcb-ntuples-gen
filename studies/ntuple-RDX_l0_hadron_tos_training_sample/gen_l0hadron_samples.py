#!/usr/bin/env python
#
# Script to generate various samples for the trigger emulation

import os
import pathlib
import sys

# ntpIn = '../../ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root'
ntpIn = '../../ntuples/0.9.5-bugfix/Dst_D0-mc/Dst_D0--21_10_08--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root'

if not pathlib.Path(ntpIn).is_file():
    sys.exit(ntpIn+' does not exist, you need to download it')


def runCmd(cmd):
    print('\n \033[92m'+cmd+'\033[0m')
    os.system(cmd)


def mergeSlim(tag, ntpIn):
    yml = 'l0hadron_sample_'+tag+'.yml'
    ntpOut = 'l0hadron_emu_'+tag+'.root'
    runCmd('../../scripts/haddcut.py '+ntpOut+' '+ntpIn+' -s -c '+yml)
    return ntpOut


## Slimming the non-truthmatched ntuple and merging it with the trigger emulation
ntpNtm = mergeSlim('ntm', ntpIn)
runCmd('root -l \'../../scripts/split_train_vali_test.C("'+ntpNtm+'", "60:40")\'')

## Slimming the truthmatched ntuple and merging it with the trigger emulation, dividing it into samples
ntpTm = mergeSlim('tm', ntpIn)
runCmd('root -l \'../../scripts/split_train_vali_test.C("'+ntpTm+'", "60:40")\'')

runCmd('hadd -fk run2_rdx-train.root l0hadron_emu_ntm_train.root l0hadron_emu_tm_train.root')
runCmd('hadd -fk run2_rdx-valid.root l0hadron_emu_ntm_valid.root l0hadron_emu_tm_valid.root')

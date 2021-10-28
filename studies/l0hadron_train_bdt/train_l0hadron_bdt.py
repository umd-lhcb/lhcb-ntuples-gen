#!/usr/bin/env python
#
# Script to train BDTs and produce training, validation and
# non-truth-matched (ntm) ntuples with the BDT output

import os
import pathlib
import sys

def run_cmd(cmd):
    print('\n \033[92m'+cmd+'\033[0m')
    os.system(cmd)

def checkFile(srcFile):
    if not pathlib.Path(srcFile).is_file():
        sys.exit(srcFile+' does not exist.')


## Checking if source ntuples from lhcb-ntuples-gen exist
srcFolder = '../ntuple-RDX_l0_hadron_tos_training_sample/'
ntpTrain = 'l0hadron_emu_tm_train.root'
ntpValid = 'l0hadron_emu_tm_valid.root'
ntpNtm = 'l0hadron_emu_ntm.root'
checkFile(srcFolder+ntpTrain)
checkFile(srcFolder+ntpValid)
checkFile(srcFolder+ntpNtm)

## Training and loading normal BDTs
bdtEx = '../../lib/python/TrackerOnlyEmu/scripts/l0hadron_trainload_bdt_xgb.py '
cl = 'bdt'
run_cmd(bdtEx+srcFolder+ntpTrain+' -o '+cl+'4.pickle --max-depth 4 -c '+cl)
run_cmd(bdtEx+srcFolder+ntpTrain+' -o l0hadron_'+cl+'4_tm_train.root --load-cl '+cl+'4.pickle')
run_cmd(bdtEx+srcFolder+ntpValid+' -o l0hadron_'+cl+'4_tm_valid.root --load-cl '+cl+'4.pickle')
run_cmd(bdtEx+srcFolder+ntpNtm+' -o l0hadron_'+cl+'4_ntm.root --load-cl '+cl+'4.pickle')

## Training and loading overtrained BDTs (4 MINUTES)
run_cmd(bdtEx+srcFolder+ntpTrain+' -o '+cl+'40.pickle --max-depth 40 -c '+cl)
run_cmd(bdtEx+srcFolder+ntpTrain+' -o l0hadron_'+cl+'40_tm_train.root --load-cl '+cl+'40.pickle')
run_cmd(bdtEx+srcFolder+ntpValid+' -o l0hadron_'+cl+'40_tm_valid.root --load-cl '+cl+'40.pickle')

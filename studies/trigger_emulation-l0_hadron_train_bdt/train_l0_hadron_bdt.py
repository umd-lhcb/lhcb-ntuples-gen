#!/usr/bin/env python
# Author: Manuel Franco Sevilla
# Description: Script to train BDTs and produce training, validation and
#              non-trigger-matched (ntm) ntuples with the BDT output

import os
import pathlib
import sys

# Checking if source ntuples from lhcb-ntuples-gen exist
srcFolder = '../ntuple-RDX_l0_hadron_tos_training_sample/'
ntpTrain = 'l0hadron_emu_tm_train.root'
ntpValid = 'l0hadron_emu_tm_valid.root'
ntpNtm = 'l0hadron_emu_ntm.root'


def runCmd(cmd):
    print('\n \033[92m'+cmd+'\033[0m')
    os.system(cmd)


def checkFile(srcFile):
    if not pathlib.Path(srcFile).is_file():
        sys.exit('{} does not exist. Run the script inside {} folder'.format(
            srcFile, srcFolder))


checkFile(srcFolder+ntpTrain)
checkFile(srcFolder+ntpValid)
checkFile(srcFolder+ntpNtm)

# Training and loading normal BDTs
bdtEx = '../../lib/python/TrackerOnlyEmu/scripts/l0hadron_trainload_bdt_xgb.py '
cl = 'bdt'
runCmd(bdtEx+srcFolder+ntpTrain+' -o '+cl+'4.pickle --max-depth 4 -c '+cl)
runCmd(bdtEx+srcFolder+ntpTrain+' -o l0hadron_'+cl+'4_tm_train.root --load-cl '+cl+'4.pickle')
runCmd(bdtEx+srcFolder+ntpValid+' -o l0hadron_'+cl+'4_tm_valid.root --load-cl '+cl+'4.pickle')
runCmd(bdtEx+srcFolder+ntpNtm+' -o l0hadron_'+cl+'4_ntm.root --load-cl '+cl+'4.pickle')

# Training and loading overtrained BDTs (4 MINUTES)
runCmd(bdtEx+srcFolder+ntpTrain+' -o '+cl+'40.pickle --max-depth 40 -c '+cl)
runCmd(bdtEx+srcFolder+ntpTrain+' -o l0hadron_'+cl+'40_tm_train.root --load-cl '+cl+'40.pickle')
runCmd(bdtEx+srcFolder+ntpValid+' -o l0hadron_'+cl+'40_tm_valid.root --load-cl '+cl+'40.pickle')

#!/usr/bin/env python
#
# Script to train XGBs and produce training, validation and
# non-truth-matched (ntm) ntuples with the XGB output

import os
import pathlib
import sys

def runCmd(cmd):
    print('\n \033[92m'+cmd+'\033[0m')
    os.system(cmd)

def checkFile(srcFile,srcFolder = '../../../lhcb-ntuples-gen/studies/ntuple-RDX_l0_hadron_tos_training_sample/'):
    file = srcFolder+srcFile
    if not pathlib.Path(file).is_file():
        sys.exit(file+' does not exist. Make sure lhcb-ntuples-gen and TrackerOnlyEmu are on the same folder')
    else: return file

def trainLoad(ntpIn, ntpOuts, particle='d0', depth=4, ntrees=300):
    xgbEx = '../../scripts/l0hadron_trainload_xgb.py '
    tagPick = 'xgb_'+str(depth)+'_'+str(ntrees)+'_'+particle
    tagTrain = tagPick+'--'+ntpIn[ntpIn.find('emu_')+4:].replace('.root','')
    xgbFile = tagPick+'.pickle'
    runCmd(xgbEx+ntpIn+' -o '+xgbFile+' --max-depth '+str(depth)+' --ntrees '+str(ntrees)+' -p '+particle)
    for ntp in ntpOuts:
        tagOut = ntp[ntp.find('emu_')+4:]
        ntpOut = 'l0hadron-'+tagTrain+'--'+tagOut
        runCmd(xgbEx+ntp+' -o '+ntpOut+' --load-xgb '+xgbFile+' -p '+particle)

## Adding source folder and checking if source ntuples from lhcb-ntuples-gen exist
ntpAllTrain = checkFile('l0hadron_emu_all_train.root')
ntpAllValid = checkFile('l0hadron_emu_all_valid.root')
ntpTm = checkFile('l0hadron_emu_tm.root')
ntpTmTrain = checkFile('l0hadron_emu_tm_train.root')
ntpTmValid = checkFile('l0hadron_emu_tm_valid.root')
ntpNtm = checkFile('l0hadron_emu_ntm.root')
ntpNtmTrain = checkFile('l0hadron_emu_ntm_train.root')
ntpNtmValid = checkFile('l0hadron_emu_ntm_valid.root')

## Training and loading the XGBoost classifier
trainLoad(ntpTmTrain, [ntpTmValid,ntpNtm], 'd0', 4, 300)
# trainLoad(ntpNtmTrain, [ntpNtmValid,ntpTm], 'd0', 4, 300)
# trainLoad(ntpAllTrain, [ntpAllValid], 'd0', 4, 300)
# trainLoad(ntpAllTrain, [ntpAllValid], 'k', 4, 300)
# trainLoad(ntpAllTrain, [ntpAllValid], 'k', 6, 500)

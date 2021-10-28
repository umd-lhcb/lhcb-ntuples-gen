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

    runCmd(f'../../scripts/haddcut.py {ntpOut} {ntpIn} -s -c {yml}')
    return ntpOut


def merge(ntpOut, ntpsIn):
    if isfile(ntpOut):
        print('Already merged.')
        return ntpOut

    runCmd('hadd -fk {} {}'.format(ntpOut, ' '.join(ntpsIn)))
    return ntpOut


def mergeFriend(ntpOut, ntpsIn):
    pass


def rename(ntpOut, ntpIn):
    if isfile(ntpOut):
        return ntpOut

    runCmd(f'cp {ntpIn} {ntpOut}')
    return ntpOut


def splitTrainValid(ntpIn):
    base = splitext(ntpIn)[0]
    ntpsOut = [base+'_'+mode+'.root' for mode in ['train', 'valid', 'test']]

    if False not in [isfile(f) for f in ntpsOut]:
        print('Already split.')
        return ntpsOut

    runCmd('root -l \'../../scripts/split_train_vali_test.C("'+ntpIn+'", "50:50")\'')
    return ntpsOut


ntpIn = '../../ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root'
# ntpIn = '../../ntuples/0.9.5-bugfix/Dst_D0-mc/Dst_D0--21_10_08--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root'

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
ntpTrainBdt = rename('run2-rdx-train_bdt.root', ntpTmTrain)


####################
# Train on ntuples #
####################

def train(tag, ntpIn, dumped, ntpOut='tmp.root', depth=4, ntrees=300):
    if isfile(dumped):
        print('Already trained.')
        return dumped, ntpOut

    exe = '../../lib/python/TrackerOnlyEmu/scripts/run2-rdx-l0_hadron_trainload_'+tag+'.py'
    runCmd(f'{exe} {ntpIn} {ntpOut} --dump {dumped} --max-depth {depth} --ntrees {ntrees} --debug')
    return dumped, ntpOut


bdt4, _ = train('bdt', ntpTrainBdt, 'bdt4.pickle')
xgb4, _ = train('xgb', ntpTrainXgb, 'xgb4.pickle')

## Over-train
bdt40, _ = train('bdt', ntpTrainBdt, 'bdt40.pickle', depth=100)


##########################
# Generate debug ntuples #
##########################

def apply(tag, ntpIn, ntpOut, dumped):
    if isfile(ntpOut):
        print('Trigger emulation already applied.')
        return ntpOut

    exe = '../../lib/python/TrackerOnlyEmu/scripts/run2-rdx-l0_hadron_trainload_'+tag+'.py'
    runCmd(f'{exe} {ntpIn} {ntpOut} --load {dumped} --debug')
    return ntpOut


ntpBdt4 = apply('bdt', ntpValid, 'run2-rdx-bdt4.root', bdt4)
ntpBdt4Tm = apply('bdt', ntpTmValid, 'run2-rdx-bdt4-tm.root', bdt4)
ntpBdt4Ntm = apply('bdt', ntpNtmValid, 'run2-rdx-bdt4-ntm.root', bdt4)

ntpXgb4 = apply('xgb', ntpValid, 'run2-rdx-xgb4.root', xgb4)
ntpBdt4Xgb4 = merge('run2-rdx-bdt4_xgb4.root', [ntpBdt4, ntpXgb4])

## Over-train, apply on the same ntuple
ntpBdt40 = apply('bdt', ntpTrainBdt, 'run2-rdx-bdt40-tm-train.root', bdt40)


###############
# Debug plots #
###############

def plotL0Hadron(ntpIn, triggers,
                 outPref='b0',
                 tree='TupleB0/DecayTree',
                 title='L0Hadron TOS',
                 legends=[
                     'Real response in FullSim',
                     'Emulated (no BDT)',
                     'Emulated (BDT)'
                 ],
                 cuts=[
                     'nspdhits < 450',
                     'nspdhits < 450',
                     'nspdhits < 450'
                 ]):
    exe = '../../scripts/plot_trigger_efficiencies.py'

    cmd = exe+''' \\
        -n {ntp}/{tree} -b {trg} -o {outPref} --title "{title}" \\
        --ratio-plot \\
        -k d0_pt -D 0 20 \\
        -l {legends} \\
        -c {cuts} \\
        --xlabel "\\$D^0$ \\$p_T$ [GeV]"
    '''.format(ntp=ntpIn, tree=tree, trg=' '.join([f'"{i}"' for i in triggers]),
               outPref=outPref, title=title,
               legends=' '.join(['"{}"'.format(i) for i in legends]),
               cuts=' '.join(['"{}"'.format(i) for i in cuts])
               )
    runCmd(cmd)


bdtTrgsToPlot = [
    'd0_l0_hadron_tos',
    'd0_l0_hadron_tos_emu_no_bdt',
    'd0_l0_hadron_tos_emu_bdt',
]

xgbTrgsToPlot = [
    'd0_l0_hadron_tos',
    'd0_l0_hadron_tos_emu_xgb'
]


plotL0Hadron(ntpBdt4, bdtTrgsToPlot, 'b0-bdt4', title='L0Hadron TOS valid')
plotL0Hadron(ntpBdt4Tm, bdtTrgsToPlot, 'b0-bdt4',
             title='L0Hadron TOS tm valid')
plotL0Hadron(ntpBdt4Ntm, bdtTrgsToPlot, 'b0-bdt4',
             title='L0Hadron TOS ntm valid')

plotL0Hadron(ntpXgb4, xgbTrgsToPlot, 'b0-xgb4',
             legends=['Real response in FullSim', 'Emulated (XGB)'])

## Over-train, apply on the same ntuple
plotL0Hadron(ntpBdt40, bdtTrgsToPlot, 'b0-bdt40',
             title='L0Hadron TOS tm trained')

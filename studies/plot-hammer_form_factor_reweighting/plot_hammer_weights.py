#!/usr/bin/env python
#
# Description: Debugging for L0Hadron TOS emulation, including:
#              - Generation of training and validation ntuples
#              - Training of BDT and XGB
#              - Plotting

import os
import sys

from os.path import isdir
from os.path import splitext

from glob import glob


###########
# Helpers #
###########

def runCmd(cmd):
    print('  \033[92m'+cmd+'\033[0m')
    os.system(cmd)


ntpInFolder = '../../gen/rdx-ntuple-run2-mc-dss'

if not isdir(ntpInFolder):
    print(f'The ntuple folder {ntpInFolder} does not exist!')
    print('Run "make rdx-ntuple-run2-mc-dss" in project root to generate the ntuples first!')
    sys.exit(1)

ntpsIn = glob(f'{ntpInFolder}/ntuple/*.root')


def findLep(truthmatch):
    if truthmatch % 10 == 1:
        return r'\tau \nu'
    return r'\mu \nu'


def findDst(truthmatch):
    mapDst = {
        11: r'D^{*0}_0',
        12: r'D^{0}_1',
        13: r"D^{'0}_1",
        14: r'D^{*0}_2',
        21: r'D^{*+}_0',
        22: r'D^{+}_1',
        23: r"D^{'+}_1",
        24: r'D^{*+}_2',
    }

    if (truthmatch // 10) not in mapDst:
        return 'D_{unknown}'

    return mapDst[truthmatch // 10]


#########
# Plots #
#########

# def plotL0Hadron(ntpIn, triggers,
                 # outPref='b0',
                 # tree='TupleB0/DecayTree',
                 # title='L0Hadron TOS',
                 # legends=[
                     # 'Real response in FullSim',
                     # 'Emulated (no BDT)',
                     # 'Emulated (BDT)',
                     # 'Emulated (XGB)',
                 # ],
                 # cuts=[
                     # 'nspdhits < 450',
                     # 'nspdhits < 450',
                     # 'nspdhits < 450',
                     # 'nspdhits < 450',
                 # ]):
    # exe = '../../scripts/plot_trigger_efficiencies.py'

    # cmd = exe+''' \\
        # -n {ntp}/{tree} -b {trg} -o {outPref} --title "{title}" \\
        # --ratio-plot \\
        # -k d0_pt -D 0 20 \\
        # -l {legends} \\
        # -c {cuts} \\
        # --xlabel "\\$D^0$ \\$p_T$ [GeV]"
    # '''.format(ntp=ntpIn, tree=tree, trg=' '.join([f'"{i}"' for i in triggers]),
               # outPref=outPref, title=title,
               # legends=' '.join(['"{}"'.format(i) for i in legends]),
               # cuts=' '.join(['"{}"'.format(i) for i in cuts])
               # )
    # runCmd(cmd)


# bdtTrgsToPlot = [
    # 'd0_l0_hadron_tos',
    # 'd0_l0_hadron_tos_emu_no_bdt',
    # 'd0_l0_hadron_tos_emu_bdt',
# ]

# xgbTrgsToPlot = [
    # 'd0_l0_hadron_tos',
    # 'd0_l0_hadron_tos_emu_xgb'
# ]


# plotL0Hadron(ntpBdt4, bdtTrgsToPlot, title='L0Hadron TOS bdt4 valid')
# plotL0Hadron(ntpBdt4Tm, bdtTrgsToPlot, title='L0Hadron TOS bdt4 tm valid')
# plotL0Hadron(ntpBdt4Ntm, bdtTrgsToPlot, title='L0Hadron TOS bdt4 ntm valid')

# plotL0Hadron(ntpXgb4, xgbTrgsToPlot, title='L0Hadron TOS xgb4 valid',
             # legends=['Real response in FullSim', 'Emulated (XGB)'])

# ## BDT vs XGB
# plotL0Hadron(
    # ntpBdt4Xgb4,
    # [
        # 'd0_l0_hadron_tos',
        # 'd0_l0_hadron_tos_emu_no_bdt',
        # 'd0_l0_hadron_tos_emu_bdt',
        # 'd0_l0_hadron_tos_emu_xgb'
    # ],
    # title='L0Hadron TOS bdt4 xgb4 valid'
# )

# ## Over-train, apply on the same ntuple
# plotL0Hadron(ntpBdt40, bdtTrgsToPlot, title='L0Hadron TOS bdt40 tm trained')

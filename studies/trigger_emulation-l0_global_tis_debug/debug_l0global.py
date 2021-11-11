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


##########################
# Generate debug ntuples #
##########################

def apply(ntpIn, ntpOut):
    if isfile(ntpOut):
        print('Trigger emulation already applied.')
        return ntpOut

    exe = '../../lib/python/TrackerOnlyEmu/scripts/run2-rdx-l0_global_tis.py'
    runCmd(f'{exe} {ntpIn} {ntpOut} --debug')
    return ntpOut


ntpNorm = '../../ntuples/0.9.5-bugfix/Dst_D0-mc/Dst_D0--21_10_08--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574011_D0TAUNU.SAFESTRIPTRIG.DST.root'

ntpEmuNorm = apply(ntpNorm, 'rdx-run2-emu-norm.root')


###############
# Debug plots #
###############

def plotL0Global(ntpIn, triggers,
                 outPref='b0',
                 tree='TupleB0/DecayTree',
                 title='L0Global TOS',
                 legends=[
                     'Real response in FullSim',
                     'Emulated',
                 ],
                 cuts=[
                     'nspdhits < 450',
                     'nspdhits < 450',
                     'nspdhits < 450',
                     'nspdhits < 450',
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


# plotL0Global(ntpEmuNorm, , title='L0Hadron TOS bdt4 valid')

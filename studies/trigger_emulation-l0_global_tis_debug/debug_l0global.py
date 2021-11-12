#!/usr/bin/env python
#
# Description: Debugging for L0Global TIS emulation, including:
#              - Emulating the trigger on the normalization
#              - Merging several histograms
#              - Plotting

import os
import sys

from os.path import isfile
from os.path import splitext

from ROOT import TFile, TH2D, TMath, std
from TrackerOnlyEmu.loader import load_file


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


#######################
# Generate histograms #
#######################

def renameHisto(ntpInName, ntpOutName, oldName, newName):
    ntpIn = TFile.Open(ntpInName, 'READ')
    ntpOut = TFile.Open(ntpOutName, 'RECREATE')

    histo = ntpIn.Get(oldName)
    histo.SetName(newName)

    ntpOut.cd()
    histo.Write()

    return ntpOutName


def findBinning(ntpInName, histoName, binLbls):
    ntpIn = TFile.Open(ntpInName, 'READ')
    histo = ntpIn.Get(histoName)

    result = []
    for lbl in binLbls:
        axis = getattr(histo, f'Get{lbl.upper()}axis')()
        result.append((axis.GetNbins(), list(axis.GetXbins())))
    return result


def listToCppArray(l, dataType='Double_t'):
    vec = std.vector(dataType)(l)
    return vec.data()


def buildHisto(ntpInName, ntpOutName, bin_spec, name, x='b0_PZ', y='b0_PT',
               val='b0_L0Global_TIS', treeName='TupleB0/DecayTree'):
    nbinsx, xbins = bin_spec[0]
    nbinsy, ybins = bin_spec[1]

    print(xbins)

    histo = TH2D(name, name,
                 nbinsx, listToCppArray(xbins), nbinsy, listToCppArray(ybins))

    # ntpIn = TFile.Open(ntpInName, 'READ')
    # tree = ntpIn.Get(treeName)

    # print('here')
    # idx = 0
    # for event in tree:
        # br_x = getattr(event, x)
        # br_y = getattr(event, y)
        # br_val = getattr(event, val)

        # # bin_idx = histo.FindFixBin(ROOT.TMath.Log(br_x), ROOT.TMath.Log(br_y))

        # print(br_x, br_y, br_val)
        # idx += 1
        # if idx > 5:
            # break


# Rename the trigger efficiency from real data & write in a new file
ntpData = load_file('<triggers/l0/l0_tis_efficiency.root>')
ntpOut = renameHisto(ntpData, 'out.root', 'Jpsi_data_eff1', 'data_2016')

histoBinSpec = findBinning(ntpData, 'Jpsi_data_eff1', ['x', 'y'])

buildHisto(ntpNorm, 'test.root', histoBinSpec, 'test')


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

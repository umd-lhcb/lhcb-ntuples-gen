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

from ROOT import TFile, TH2D, TMath, std, TH1D
from TrackerOnlyEmu.loader import load_file


###########
# Helpers #
###########

Log = TMath.Log


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

NTP_WRT_MODE = 'UPDATE'


def renameHisto(ntpInName, ntpOutName, oldName, newName,
                writeMode=NTP_WRT_MODE):
    ntpIn = TFile.Open(ntpInName, 'READ')
    ntpOut = TFile.Open(ntpOutName, writeMode)

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
        result.append(list(axis.GetXbins()))

    return result


def buildHisto(ntpInName, ntpOutName, bin_spec, name, x='b0_PZ', y='b0_PT',
               particle='b0', treeName='TupleB0/DecayTree'):
    xbins, ybins = bin_spec

    # Need to convert bin boundaries to C++ arrays
    # NOTE: This can't happen outside this function, as the returned C++ pointer
    # will be garbage-collected, making the whole thing malfunctioning
    v_xbins = std.vector('Double_t')(xbins)
    v_ybins = std.vector('Double_t')(ybins)

    histoTot = TH2D(f'{name}_tot', f'{name}_tot',
                    len(xbins)-1, v_xbins.data(), len(ybins)-1, v_ybins.data())
    # For TISTOS method
    histoTos = TH2D(f'{name}_tos', f'{name}_tos',
                    len(xbins)-1, v_xbins.data(), len(ybins)-1, v_ybins.data())
    histoTistos = TH2D(f'{name}_tistos', f'{name}_tistos',
                       len(xbins)-1, v_xbins.data(),
                       len(ybins)-1, v_ybins.data())
    histoEff = TH2D(f'{name}_eff', f'{name}_eff',
                    len(xbins)-1, v_xbins.data(), len(ybins)-1, v_ybins.data())

    ntpIn = TFile.Open(ntpInName, 'READ')
    tree = ntpIn.Get(treeName)
    tis, tos = [f'{particle}_{i}'
                for i in ['L0Global_TIS', 'L0HadronDecision_TOS']]

    for event in tree:
        brX = Log(getattr(event, x))
        brY = Log(getattr(event, y))
        brTis = getattr(event, tis)
        brTos = getattr(event, tos)

        histoTot.Fill(brX, brY)

        if brTos:
            histoTos.Fill(brX, brY)
        if brTis and brTos:
            histoTistos.Fill(brX, brY)

    # Find the TISTOS efficiency of TIS
    histoEff.Divide(histoTistos, histoTos)

    ntpOut = TFile.Open(ntpOutName, NTP_WRT_MODE)
    ntpOut.cd()
    histoTot.Write()
    histoTos.Write()
    histoTistos.Write()
    histoEff.Write()


# Rename the trigger efficiency from real data & write in a new file
ntpData = load_file('<triggers/l0/l0_tis_efficiency.root>')
ntpOut = renameHisto(ntpData, 'out.root', 'Jpsi_data_eff1', 'data_2016',
                     writeMode='RECREATE')

# Find the binning scheme for the sample
histoBinSpec = findBinning(ntpData, 'Jpsi_data_eff1', ['x', 'y'])

buildHisto(ntpNorm, 'out.root', histoBinSpec, 'norm')


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

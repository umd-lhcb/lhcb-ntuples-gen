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

from ROOT import TFile, TH2D, TH1D, TMath, std, TEfficiency
from TrackerOnlyEmu.loader import load_file
from itertools import product


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


ntpNorm = '../../ntuples/0.9.5-bugfix/Dst_D0-mc/Dst_D0--21_10_08--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root'
ntpSig = '../../ntuples/0.9.5-bugfix/Dst_D0-mc/Dst_D0--21_10_08--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574011_D0TAUNU.SAFESTRIPTRIG.DST.root'

# ntpEmuNorm = apply(ntpNorm, 'rdx-run2-emu-norm.root')


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


def findBinningLite(histo, binLbls):
    result = []

    for lbl in binLbls:
        axis = getattr(histo, f'Get{lbl.upper()}axis')()
        result.append(list(axis.GetXbins()))

    return result


def findBinning(ntpInName, histoName, binLbls):
    ntpIn = TFile.Open(ntpInName, 'READ')
    histo = ntpIn.Get(histoName)
    return findBinningLite(histo, binLbls)


def buildHistoBinnedProjection(histo, name):
    nbinsX = histo.GetNbinsX()
    nbinsY = histo.GetNbinsY()
    histoBinProj = TH1D(f'{name}_proj_bin', f'{name}_proj_bin',
                        nbinsX*nbinsY, 0, nbinsX*nbinsY)

    idx = 0
    for xIdx, yIdx in product(range(1, nbinsX+1), range(1, nbinsY+1)):
        idx += 1
        binIdx = histo.GetBin(xIdx, yIdx)
        histoBinProj.SetBinContent(idx, histo.GetBinContent(binIdx))

    return histoBinProj


def buildHistoFromHisto(ntpInName, ntpOutName, histoName, name,
                        writeMode=NTP_WRT_MODE):
    ntpIn = TFile.Open(ntpInName, 'READ')
    ntpOut = TFile.Open(ntpOutName, writeMode)

    histo = ntpIn.Get(histoName)
    histoX = histo.ProjectionX(f'{name}_proj_x', 1, histo.GetNbinsX())
    histoY = histo.ProjectionY(f'{name}_proj_y', 1, histo.GetNbinsY())

    ntpOut.cd()
    histoX.Write()
    histoY.Write()

    return ntpOutName


def buildHisto(ntpInName, ntpOutName, bin_spec, name,
               x='b0_TRUEP_Z', y='b0_TRUEPT',
               particle='b0', treeName='TupleB0/DecayTree', spdCut=True,
               tosTrg='L0MuonDecision_TOS'):
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
    histoTis = TH2D(f'{name}_tis', f'{name}_tis',
                    len(xbins)-1, v_xbins.data(), len(ybins)-1, v_ybins.data())
    histoTistos = TH2D(f'{name}_tistos', f'{name}_tistos',
                       len(xbins)-1, v_xbins.data(),
                       len(ybins)-1, v_ybins.data())
    histoNotTos = TH2D(f'{name}_not_tos', f'{name}_not_tos',
                       len(xbins)-1, v_xbins.data(),
                       len(ybins)-1, v_ybins.data())
    histoTisNotTos = TH2D(f'{name}_tis_not_tos', f'{name}_tis_not_tos',
                          len(xbins)-1, v_xbins.data(),
                          len(ybins)-1, v_ybins.data())

    ntpIn = TFile.Open(ntpInName, 'READ')
    tree = ntpIn.Get(treeName)
    tis, tos = [f'{particle}_{i}'
                for i in ['L0Global_TIS', tosTrg]]

    for event in tree:
        brX = Log(getattr(event, x))
        brY = Log(getattr(event, y))
        brTis = getattr(event, tis)
        brTos = getattr(event, tos)
        brSpd = getattr(event, 'NumSPDHits')

        # Apply a global nSPDhits cut
        if spdCut and brSpd >= 450:
            continue

        histoTot.Fill(brX, brY)

        if brTis:
            histoTis.Fill(brX, brY)
        if brTos:
            histoTos.Fill(brX, brY)
        if brTis and brTos:
            histoTistos.Fill(brX, brY)

        if not brTos:
            histoNotTos.Fill(brX, brY)
        if brTis and not brTos:
            histoTisNotTos.Fill(brX, brY)

    histoTosX = histoTos.ProjectionX(f'{name}_tos_proj_x')
    histoTosY = histoTos.ProjectionY(f'{name}_tos_proj_y')
    histoTisX = histoTis.ProjectionX(f'{name}_tis_proj_x')
    histoTisY = histoTis.ProjectionY(f'{name}_tis_proj_y')
    histoTotX = histoTot.ProjectionX(f'{name}_tot_proj_x')
    histoTotY = histoTot.ProjectionY(f'{name}_tot_proj_y')
    histoTistosX = histoTistos.ProjectionX(f'{name}_tistos_proj_x')
    histoTistosY = histoTistos.ProjectionY(f'{name}_tistos_proj_y')
    histoNotTosX = histoNotTos.ProjectionX(f'{name}_not_tos_proj_x')
    histoNotTosY = histoNotTos.ProjectionY(f'{name}_not_tos_proj_y')
    histoTisNotTosX = histoTisNotTos.ProjectionX(f'{name}_tis_not_tos_proj_x')
    histoTisNotTosY = histoTisNotTos.ProjectionY(f'{name}_tis_not_tos_proj_y')

    histoTosBin = buildHistoBinnedProjection(histoTos, f'{name}_tos')
    histoTisBin = buildHistoBinnedProjection(histoTis, f'{name}_tis')
    histoTotBin = buildHistoBinnedProjection(histoTot, f'{name}_tot')
    histoTistosBin = buildHistoBinnedProjection(histoTistos, f'{name}_tistos')
    histoNotTosBin = buildHistoBinnedProjection(histoNotTos, f'{name}_not_tos')
    histoTisNotTosBin = buildHistoBinnedProjection(
        histoTisNotTos, f'{name}_tis_not_tos')

    # Generate efficiency histograms
    histoEffProjX = TEfficiency(histoTistosX, histoTosX)
    histoEffProjX.SetName(f'{name}_eff_proj_x')
    histoEffProjY = TEfficiency(histoTistosY, histoTosY)
    histoEffProjY.SetName(f'{name}_eff_proj_y')
    histoEffProjBin = TEfficiency(histoTistosBin, histoTosBin)
    histoEffProjBin.SetName(f'{name}_eff_proj_bin')

    histoEffProjXDir = TEfficiency(histoTisX, histoTotX)
    histoEffProjXDir.SetName(f'{name}_eff_proj_x_dir')
    histoEffProjYDir = TEfficiency(histoTisY, histoTotY)
    histoEffProjYDir.SetName(f'{name}_eff_proj_y_dir')
    histoEffProjBinDir = TEfficiency(histoTisBin, histoTotBin)
    histoEffProjBinDir.SetName(f'{name}_eff_proj_bin_dir')

    histoEffProjXNotTos = TEfficiency(histoTisNotTosX, histoNotTosX)
    histoEffProjXNotTos.SetName(f'{name}_eff_proj_x_not_tos')
    histoEffProjYNotTos = TEfficiency(histoTisNotTosY, histoNotTosY)
    histoEffProjYNotTos.SetName(f'{name}_eff_proj_y_not_tos')
    histoEffProjBinNotTos = TEfficiency(histoTisNotTosBin, histoNotTosBin)
    histoEffProjBinNotTos.SetName(f'{name}_eff_proj_bin_not_tos')

    ntpOut = TFile.Open(ntpOutName, NTP_WRT_MODE)
    ntpOut.cd()
    histoTot.Write()
    histoTos.Write()
    histoTistos.Write()
    histoNotTos.Write()
    histoTisNotTos.Write()

    histoTosBin.Write()
    histoTistosBin.Write()
    histoTisNotTosBin.Write()

    histoEffProjX.Write()
    histoEffProjY.Write()
    histoEffProjBin.Write()
    histoEffProjXDir.Write()
    histoEffProjYDir.Write()
    histoEffProjBinDir.Write()
    histoEffProjXNotTos.Write()
    histoEffProjYNotTos.Write()
    histoEffProjBinNotTos.Write()


# Rename the trigger efficiency from real data & write in a new file
ntpData = load_file('<triggers/l0/l0_tis_efficiency.root>')
ntpOut = buildHistoFromHisto(
    ntpData, 'l0global.root', 'Jpsi_data_eff1', 'data_2016',
    writeMode='RECREATE')

# Find the binning scheme for the sample
histoBinSpec = findBinning(ntpData, 'Jpsi_data_eff1', ['x', 'y'])

buildHisto(ntpNorm, ntpOut, histoBinSpec, 'norm')
buildHisto(ntpSig, ntpOut, histoBinSpec, 'sig')


###############
# Debug plots #
###############

def plotL0Global(ntpIn, histos, out,
                 title='L0Global TIS efficiency (TISTOS method)',
                 xlabel=r'$\log(p_z)$',
                 legend_loc='lower right', legends=None):
    exe = '../../scripts/plot_teffiencies.py'

    cmd = f'''{exe} \\
        {ntpIn} -H {' '.join(histos)} -o {out} --title "{title}" \\
        --legend-loc "{legend_loc}" \\
        --xlabel "{xlabel}"'''

    if legends:
        legends = ' '.join([f'"{i}"' for i in legends])
        cmd += f' -l {legends}'

    runCmd(cmd)


plotL0Global(ntpOut, ['norm_eff_proj_x', 'sig_eff_proj_x'],
             'l0_global_tis_eff_log_pz',
             title='L0Global TIS efficiencies (TISTOS method)')
plotL0Global(ntpOut, ['norm_eff_proj_y', 'sig_eff_proj_y'],
             'l0_global_tis_eff_log_pt',
             legend_loc='upper left',
             xlabel=r'$\log(p_T)$',
             title='L0Global TIS efficiencies (TISTOS method)')
plotL0Global(ntpOut, ['norm_eff_proj_bin', 'sig_eff_proj_bin'],
             'l0_global_tis_eff_bin_idx',
             legend_loc='upper left',
             xlabel=r'Bin index',
             title='L0Global TIS efficiencies (TISTOS method)')

plotL0Global(ntpOut, ['norm_eff_proj_x_dir', 'sig_eff_proj_x_dir'],
             'l0_global_tis_eff_log_pz_dir',
             title='L0Global TIS efficiencies (direct method)')
plotL0Global(ntpOut, ['norm_eff_proj_y_dir', 'sig_eff_proj_y_dir'],
             'l0_global_tis_eff_log_pt_dir',
             legend_loc='upper left',
             xlabel=r'$\log(p_T)$',
             title='L0Global TIS efficiencies (direct method)')
plotL0Global(ntpOut, ['norm_eff_proj_bin_dir', 'sig_eff_proj_bin_dir'],
             'l0_global_tis_eff_bin_idx_dir',
             legend_loc='upper left',
             xlabel=r'Bin index',
             title='L0Global TIS efficiencies (direct method)')

plotL0Global(ntpOut, ['norm_eff_proj_x', 'sig_eff_proj_x',
                      'norm_eff_proj_x_dir', 'sig_eff_proj_x_dir'],
             'l0_global_tis_eff_log_pz_comp',
             title='L0Global TIS efficiencies (TISTOS vs real TIS)',
             legends=['norm (TISTOS)', 'sig (TISTOS)',
                      'norm (real TIS)', 'sig (real TIS)'])
plotL0Global(ntpOut, ['norm_eff_proj_y', 'sig_eff_proj_y',
                      'norm_eff_proj_y_dir', 'sig_eff_proj_y_dir'],
             'l0_global_tis_eff_log_pt_comp',
             legend_loc='upper left',
             xlabel=r'$\log(p_T)$',
             title='L0Global TIS efficiencies (TISTOS vs real TIS)',
             legends=['norm (TISTOS)', 'sig (TISTOS)',
                      'norm (real TIS)', 'sig (real TIS)'])
plotL0Global(ntpOut, ['norm_eff_proj_bin', 'sig_eff_proj_bin',
                      'norm_eff_proj_bin_dir', 'sig_eff_proj_bin_dir'],
             'l0_global_tis_eff_bin_idx_comp',
             legend_loc='upper left',
             xlabel=r'Bin index',
             title='L0Global TIS efficiencies (TISTOS vs real TIS)',
             legends=['norm (TISTOS)', 'sig (TISTOS)',
                      'norm (real TIS)', 'sig (real TIS)'])

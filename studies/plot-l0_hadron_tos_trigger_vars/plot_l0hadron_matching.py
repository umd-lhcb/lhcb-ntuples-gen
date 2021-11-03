#!/usr/bin/env python
#
# Script to compare the distributions of truth-matched and non-truth-matched events

import os
import pathlib
import sys


def runCmd(cmd):
    print('\n \033[92m'+cmd+'\033[0m')
    os.system(cmd)


def plotTM(var, minx=99, maxx=0):
    ntp = '../../ntuples/0.9.5-bugfix/Dst_D0-mc/Dst_D0--21_10_08--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root'
    if not pathlib.Path(ntp).is_file():
        sys.exit(ntp+' does not exist, you need to download it')

    plotEx = 'plotbr -n '+ntp+'/TupleB0/DecayTree '
    legend = '-l "TriggerET > 0" "TriggerET < 0" '
    vars = '-b '+var+' '+var+' '
    xrange = '-XD '+str(minx)+' '+str(maxx)+' '
    xlabel = '-XL '+var+' '
    ylabel = '-YL "Fraction of candidates" '
    norm = '--normalize '

    if maxx < minx:
        xrange = ' '
    bins = '--bins 50 '
    if 'L0Calo_HCAL_region' in var:
        bins = '--bins 3 '

    ## Plotting events that do NOT pass the trigger
    trigTM = '(k_L0Calo_HCAL_TriggerET>0 | pi_L0Calo_HCAL_TriggerET>0)'
    if 'k_' in var:
        trigTM = '(k_L0Calo_HCAL_TriggerET>0)'
        commonCut = '!k_L0HadronDecision_TOS'
    else:
        commonCut = '!d0_L0HadronDecision_TOS'

    cuts = '--cuts "'+trigTM+' & '+commonCut+'" "!'+trigTM+' & '+commonCut+'" '
    title = '--title '+commonCut
    out = '-o TrigNo_'+var+'.png '
    plotCmd = plotEx+legend+cuts+out+vars+xrange+bins+xlabel+ylabel+norm+title

    if 'pi_' in var:
        plotCmd = plotCmd.replace('k_', 'pi_')
    runCmd(plotCmd)

    ## Plotting events that pass the K, pi, or D0 trigger
    if 'k_' in var:
        commonCut = 'k_L0HadronDecision_TOS'
    else:
        commonCut = 'd0_L0HadronDecision_TOS'

    cuts = '--cuts "'+trigTM+' & '+commonCut+'" "!'+trigTM+' & '+commonCut+'" '
    title = '--title '+commonCut
    out = out.replace('TrigNo', 'TrigYes')
    plotCmd = plotEx+legend+cuts+out+vars+xrange+bins+xlabel+ylabel+norm+title

    if 'pi_' in var:
        plotCmd = plotCmd.replace('k_', 'pi_')
    runCmd(plotCmd)


plotTM('nTracks', 0, 600)
plotTM('NumSPDHits', 0, 800)
plotTM('d0_PT', 0, 20000)
plotTM('d0_P', 0, 300000)
plotTM('k_L0Calo_HCAL_realET', 0, 12000)
plotTM('k_L0Calo_HCAL_xProjection', -4500, 4500)
plotTM('k_L0Calo_HCAL_yProjection', -3500, 3500)
plotTM('k_L0Calo_HCAL_region', -1, 1)
plotTM('pi_L0Calo_HCAL_realET', 0, 12000)
plotTM('pi_L0Calo_HCAL_xProjection', -4500, 4500)
plotTM('pi_L0Calo_HCAL_yProjection', -3500, 3500)
plotTM('pi_L0Calo_HCAL_region', -1, 1)

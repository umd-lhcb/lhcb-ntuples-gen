#!/usr/bin/env python3
#
# Script to run several cutflows

import os
import pathlib

from utils import run_cmd_wrapper


###########
# Helpers #
###########

run_cmd = run_cmd_wrapper(only_print=False)


def do_cutflow(ntp1, ntp2, outfolder, rfactor=1, mode='std'):
    print('\n======= Running cutflow and saving output to '+outfolder)
    pathlib.Path(outfolder).mkdir(parents=True, exist_ok=True)
    outyml1 = outfolder + "/run1_yields.yml"
    outyml2 = outfolder + "/run2_yields.yml"
    run_cmd('./scripts/cutflow_output_yml_gen.py '+' '.join(ntp1)+' -s -o '+outyml1+' -m run1-'+mode)
    run_cmd('./scripts/cutflow_output_yml_gen.py '+' '.join(ntp2)+' -s -o '+outyml2+' -m run2-'+mode)
    csvfile = outfolder + "/cutflow.csv"
    texfile = csvfile.replace('.csv', '.tex')
    mdfile = csvfile.replace('.csv', '.md')
    run_cmd('./scripts/cutflow_gen.py -o '+outyml1+' -t '+outyml2+' -n > '+csvfile+' -r '+str(rfactor))
    run_cmd('cat '+csvfile+' | tabgen.py -f latex_booktabs_raw > '+texfile)
    run_cmd('cat '+csvfile+' | tabgen.py -f github > '+mdfile)
    print('\n  cat '+mdfile+'\n')


#####################
# Production config #
#####################

## BARE MC ntuples
r1_bare = [
    'ntuples/0.9.4-trigger_emulation/Dst_D0-cutflow_mc/Dst_D0--21_05_29--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagUp-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root',
    'ntuples/0.9.4-trigger_emulation/Dst_D0-cutflow_mc/Dst_D0--21_05_29--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root'
]
r2_bare = [
    'ntuples/0.9.4-trigger_emulation/Dst_D0-cutflow_mc/Dst_D0--21_05_29--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagUp-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root',
    'ntuples/0.9.4-trigger_emulation/Dst_D0-cutflow_mc/Dst_D0--21_05_29--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root'
]

## B -> D*+ mu nu MC ntuples
r1_dstmu = [
    'ntuples/0.9.3-production_for_validation/Dst_D0-mc/Dst_D0--21_01_30--mc--MC_2012_Beam4000GeV-2012-MagDown-Nu2.5-Pythia8_Sim08e_Digi13_Trig0x409f0045_Reco14a_Stripping20Filtered_11574020_DSTTAUNU.SAFESTRIPTRIG.DST.root'
]
r2_dstmu = [
    'ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root'
]

## Data ntuples
r1_data = [
    'ntuples/0.9.2-2011_production/Dst_D0-std/Dst_D0--20_10_12--std--LHCb_Collision11_Beam3500GeV-VeloClosed-MagDown_Real_Data_Reco14_Stripping21r1_90000000_SEMILEPTONIC.DST.root'
]
r2_data = [
    'ntuples/0.9.4-trigger_emulation/Dst_D0-std/Dst_D0--21_04_27--std--LHCb_Collision16_Beam6500GeV-VeloClosed-MagDown_Real_Data_Reco16_Stripping28r1_90000000_SEMILEPTONIC.DST.root'
]

## Running BARE, D*+ mu, and Data cutflows
## rfactors are calculated from the sample yields in Dirac (for MC) and lumi x xsec (for data)
do_cutflow(r1_bare, r2_bare, 'gen/cutflow_bare-sig', (522494+502736)/(520046+515913.), 'std-sig')
do_cutflow(r1_bare, r2_bare, 'gen/cutflow_bare-nor', (522494+502736)/(520046+515913.), 'std-nor')
do_cutflow(r1_bare, r2_bare, 'gen/cutflow_bare-dss', (522494+502736)/(520046+515913.), 'std-dss')
do_cutflow(r1_dstmu, r2_dstmu, 'gen/cutflow_dstmu', 614577*0.247*0.080/(1500395*0.105*0.059))
do_cutflow(r1_data, r2_data, 'gen/cutflow_data', 1/1.41/2)

#!/usr/bin/env python3
#
# Script to run several cutflows

from utils import run_cmd_wrapper, abs_path, ensure_dir, with_suffix


###########
# Helpers #
###########

run_cmd = run_cmd_wrapper(only_print=False)


def gen_cutflow_yml(ntp1, ntp2, outyml1, outyml2, mode):
    run_cmd('cutflow_output_yml_gen.py {} -s -o {} -m run1-{}'.format(
        ' '.join([abs_path(n) for n in ntp1]), outyml1, mode))
    run_cmd('cutflow_output_yml_gen.py {} -s -o {} -m run2-{}'.format(
        ' '.join([abs_path(n) for n in ntp2]), outyml2, mode))


def gen_cutflow(outyml1, outyml2, csvfile, texfile, mdfile, rfactor):
    run_cmd('cutflow_gen.py -o {} -t {} -n > {} -r {}'.format(
        outyml1, outyml2, csvfile, rfactor))
    run_cmd('cat {} | tabgen.py -f latex_booktabs_raw > {}'.format(
        csvfile, texfile))
    run_cmd('cat {} | tabgen.py -f github > {}'.format(
        csvfile, mdfile))


def do_cutflow(ntp1, ntp2, outfolder, rfactor=1, mode='std'):
    print('\n======= Running cutflow and saving output to '+outfolder)
    outfolder = ensure_dir('../gen/{}'.format(outfolder))

    outyml1 = outfolder + "/run1_yields.yml"
    outyml2 = outfolder + "/run2_yields.yml"
    gen_cutflow_yml(ntp1, ntp2, outyml1, outyml2, mode)

    csvfile = outfolder + "/cutflow.csv"
    texfile = with_suffix(csvfile, '.tex')
    mdfile = with_suffix(csvfile, '.md')
    gen_cutflow(outyml1, outyml2, csvfile, texfile, mdfile, rfactor)

    print()
    run_cmd('cat {}'.format(mdfile))


#####################
# Production config #
#####################

## BARE MC ntuples
r1_bare = [
    '../ntuples/0.9.4-trigger_emulation/Dst_D0-cutflow_mc/Dst_D0--21_05_29--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagUp-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root',
    '../ntuples/0.9.4-trigger_emulation/Dst_D0-cutflow_mc/Dst_D0--21_05_29--cutflow_mc--bare--MC_2011_Beam3500GeV-2011-MagDown-Nu2-Pythia8_Sim08h_Digi13_Trig0x40760037_Reco14c_Stripping20r1NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root'
]
r2_bare = [
    '../ntuples/0.9.4-trigger_emulation/Dst_D0-cutflow_mc/Dst_D0--21_05_29--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagUp-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root',
    '../ntuples/0.9.4-trigger_emulation/Dst_D0-cutflow_mc/Dst_D0--21_05_29--cutflow_mc--bare--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09b_Trig0x6138160F_Reco16_Turbo03_Stripping26NoPrescalingFlagged_11874091_ALLSTREAMS.DST.root'
]

## B -> D*+ mu nu MC ntuples
r1_dstmu = [
    '../ntuples/0.9.3-production_for_validation/Dst_D0-mc/Dst_D0--21_01_30--mc--MC_2012_Beam4000GeV-2012-MagDown-Nu2.5-Pythia8_Sim08e_Digi13_Trig0x409f0045_Reco14a_Stripping20Filtered_11574020_DSTTAUNU.SAFESTRIPTRIG.DST.root'
]
r2_dstmu = [
    '../ntuples/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root'
]

## Data ntuples
r1_data = [
    '../ntuples/0.9.2-2011_production/Dst_D0-std/Dst_D0--20_10_12--std--LHCb_Collision11_Beam3500GeV-VeloClosed-MagDown_Real_Data_Reco14_Stripping21r1_90000000_SEMILEPTONIC.DST.root'
]
r2_data = [
    '../ntuples/0.9.4-trigger_emulation/Dst_D0-std/Dst_D0--21_04_27--std--LHCb_Collision16_Beam6500GeV-VeloClosed-MagDown_Real_Data_Reco16_Stripping28r1_90000000_SEMILEPTONIC.DST.root'
]

## Running BARE, D*+ mu, and Data cutflows
## rfactors are calculated from the sample yields in Dirac (for MC) and lumi x xsec (for data)
do_cutflow(r1_bare, r2_bare, 'cutflow_bare-sig',
           (522494+502736)/(520046+515913.), 'std-sig')
do_cutflow(r1_bare, r2_bare, 'cutflow_bare-nor',
           (522494+502736)/(520046+515913.), 'std-nor')
do_cutflow(r1_bare, r2_bare, 'cutflow_bare-dss',
           (522494+502736)/(520046+515913.), 'std-dss')
do_cutflow(r1_dstmu, r2_dstmu, 'cutflow_dstmu',
           614577*0.247*0.080/(1500395*0.105*0.059))
do_cutflow(r1_data, r2_data, 'cutflow_data', 1/1.41/2)

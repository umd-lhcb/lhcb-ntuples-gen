#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Mar 24, 2022 at 02:24 AM -0400

import sys
import os.path as op

from argparse import ArgumentParser
from os import chdir
from functools import partial

sys.path.insert(0, op.dirname(op.abspath(__file__)))

from utils import (
    ensure_dir,
    aggregate_fltr, aggregate_output,
    smart_kwarg,
    generate_step2_name,
    workflow_apply_weight, workflow_prep_dir, workflow_split_base
)

from rdx import workflow_single_ntuple as workflow_single_ntuple_rdx


#################################
# Command line arguments parser #
#################################

def parse_input():
    parser = ArgumentParser(description='workflow for J/psi K reweighting.')

    parser.add_argument('job_name', help='specify job name.')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug mode.')

    return parser.parse_args()


###########
# Helpers #
###########

JpsiK_default_fltr = aggregate_fltr(
    keep=[r'^(JpsiK).*\.root'], blocked=['--aux'])

JpsiK_default_output_fltrs = {
    'ntuple': JpsiK_default_fltr,
    'ntuple_aux': aggregate_fltr(keep=['--aux']),
}


####################################
# Workflows: aux ntuple generation #
####################################

@smart_kwarg
def workflow_pid(
        input_ntp, output_ntp='pid.root',
        pid_histo_folder='../run2-JpsiK/reweight/pid/root-run2-JpsiK_DLLmu_conditional_on_isMuon-shifted',
        pid_config='../run2-JpsiK/reweight/pid/run2-JpsiK_DLLmu_conditional_on_isMuon.yml',
        **kwargs):
    return workflow_apply_weight(input_ntp, pid_histo_folder, pid_config,
                                 output_ntp, '--aux_pid', **kwargs)

@smart_kwarg
def workflow_pid_withIsMuon(
        input_ntp, output_ntp='pid_withIsMuon.root',
        pid_histo_folder='../run2-JpsiK/reweight/pid/root-run2-JpsiK_withIsMuon-shifted',
        pid_config='../run2-JpsiK/reweight/pid/run2-JpsiK_withIsMuon.yml',
        **kwargs):
    return workflow_apply_weight(input_ntp, pid_histo_folder, pid_config,
                                 output_ntp, '--aux_pid_withIsMuon', **kwargs)


@smart_kwarg
def workflow_trk(
        input_ntp, output_ntp='trk.root',
        trk_histo_folder='../run2-JpsiK/reweight/tracking/root-run2-general',
        trk_config='../run2-JpsiK/reweight/tracking/run2-general.yml',
        **kwargs):
    return workflow_apply_weight(input_ntp, trk_histo_folder, trk_config,
                                 output_ntp, '--aux_trk', **kwargs)


@smart_kwarg
def workflow_jk_PIDcuts_DLLKweight(
        input_ntp, output_ntp='jk_PIDcuts_DLLKweight.root',
        jk_histo_folder='../run2-JpsiK/reweight/JpsiK/root-run2-JpsiK_PIDcuts_DLLKweight',
        jk_config='../run2-JpsiK/reweight/JpsiK/run2-JpsiK_PIDcuts_DLLKweight.yml',
        **kwargs):
    return workflow_apply_weight(input_ntp, jk_histo_folder, jk_config,
                                 output_ntp, '--aux_jk_PIDcuts_DLLKweight', **kwargs)

@smart_kwarg
def workflow_jk_PIDcuts(
        input_ntp, output_ntp='jk_PIDcuts.root',
        jk_histo_folder='../run2-JpsiK/reweight/JpsiK/root-run2-JpsiK_PIDcuts',
        jk_config='../run2-JpsiK/reweight/JpsiK/run2-JpsiK_PIDcuts.yml',
        **kwargs):
    return workflow_apply_weight(input_ntp, jk_histo_folder, jk_config,
                                 output_ntp, '--aux_jk_PIDcuts', **kwargs)

@smart_kwarg
def workflow_jk_PIDweights(
        input_ntp, output_ntp='jk_PIDweights.root',
        jk_histo_folder='../run2-JpsiK/reweight/JpsiK/root-run2-JpsiK_PIDweights',
        jk_config='../run2-JpsiK/reweight/JpsiK/run2-JpsiK_PIDweights.yml',
        **kwargs):
    return workflow_apply_weight(input_ntp, jk_histo_folder, jk_config,
                                 output_ntp, '--aux_jk_PIDweights', **kwargs)

@smart_kwarg
def workflow_jk_PIDweights_IsMuonCut(
        input_ntp, output_ntp='jk_PIDweights_IsMuonCut.root',
        jk_histo_folder='../run2-JpsiK/reweight/JpsiK/root-run2-JpsiK_PIDweights_IsMuonCut',
        jk_config='../run2-JpsiK/reweight/JpsiK/run2-JpsiK_PIDweights_IsMuonCut.yml',
        **kwargs):
    return workflow_apply_weight(input_ntp, jk_histo_folder, jk_config,
                                 output_ntp, '--aux_jk_PIDweights_IsMuonCut', **kwargs)


#######################
# Workflows: wrappers #
#######################

def workflow_single_ntuple(input_ntp, input_yml, output_suffix, aux_workflows,
                           cpp_template='../postprocess/cpp_templates/JpsiK.cpp',
                           **kwargs):
    return workflow_single_ntuple_rdx(
        input_ntp, input_yml, output_suffix, aux_workflows,
        cpp_template=cpp_template, **kwargs)


###################
# Workflows: main #
###################

def workflow_data(inputs, input_yml, job_name='data', date=None, **kwargs):
    aux_workflows = []
    subworkdirs, workdir = workflow_prep_dir(job_name, inputs, **kwargs)
    chdir(workdir)

    for subdir, input_ntp in subworkdirs.items():
        ensure_dir(subdir, make_absolute=False)
        chdir(subdir)  # Switch to the workdir of the subjob

        output_suffix = generate_step2_name(input_ntp, date=date)
        workflow_single_ntuple(
            input_ntp, input_yml, output_suffix, aux_workflows, **kwargs)

        aggregate_output('..', subdir, JpsiK_default_output_fltrs)
        chdir('..')  # Switch back to parent workdir


def workflow_mc(inputs, input_yml, job_name='mc', date=None, **kwargs):
    aux_workflows = [workflow_pid, workflow_pid_withIsMuon, workflow_trk, 
                     workflow_jk_PIDcuts_DLLKweight, workflow_jk_PIDcuts, workflow_jk_PIDweights, workflow_jk_PIDweights_IsMuonCut]
    subworkdirs, workdir = workflow_prep_dir(job_name, inputs, **kwargs)
    chdir(workdir)

    for subdir, input_ntp in subworkdirs.items():
        ensure_dir(subdir, make_absolute=False)
        chdir(subdir)  # Switch to the workdir of the subjob

        # Hard-code the MC decay mode for now
        decay_mode = '12143001'

        output_suffix = generate_step2_name(input_ntp, date=date)
        workflow_single_ntuple(
            input_ntp, input_yml, output_suffix, aux_workflows,
            cli_vars={'cli_mc_id': decay_mode},
            **kwargs)

        aggregate_output('..', subdir, JpsiK_default_output_fltrs)
        chdir('..')  # Switch back to parent workdir


def workflow_split(inputs, input_yml, job_name='split', **kwargs):
    return workflow_split_base(
        inputs, input_yml, job_name=job_name, prefix='JpsiK',
        workflow_data=workflow_data, workflow_mc=workflow_mc,
        **kwargs)


#####################
# Production config #
#####################

JOBS = {
    # Run 2
    'JpsiK-ntuple-run2-data': partial(
        workflow_split,
        # '../ntuples/0.9.6-2016_production/JpsiK-std',
        '../ntuples/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/JpsiK-data/*--std--*',
        '../postprocess/JpsiK-run2/JpsiK-run2.yml'
    ),
    'JpsiK-ntuple-run2-mc': partial(
        workflow_split,
        # '../ntuples/0.9.9-JpsiK_noPID/JpsiK-mc',
        '../ntuples/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/JpsiK-mc/*--mc--*',
        '../postprocess/JpsiK-run2/JpsiK-run2.yml'
    ),
    # Run 2 debug
    'JpsiK-ntuple-run2-data-demo': partial(
        workflow_data,
        '../run2-JpsiK/samples/JpsiK--22_02_09--std--data--2016--md--dv45-subset.root',
        '../postprocess/JpsiK-run2/JpsiK-run2.yml'
    ),
    'JpsiK-ntuple-run2-mc-demo': partial(
        workflow_mc,
        '../run2-JpsiK/samples/JpsiK--22_02_22--mc--Bu2JpsiK--2016--md--py8-sim09k-dv45-subset.root',
        '../postprocess/JpsiK-run2/JpsiK-run2.yml'
    ),
    'JpsiK-ntuple-run2-mc-sub': partial(
        workflow_split,
        [
            '../ntuples/0.9.6-2016_production/JpsiK-mc/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST--000-dv.root',
            '../ntuples/0.9.6-2016_production/JpsiK-mc/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST--001-dv.root',
            '../ntuples/0.9.6-2016_production/JpsiK-mc/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST--002-dv.root',
            '../ntuples/0.9.6-2016_production/JpsiK-mc/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST--003-dv.root',
            '../ntuples/0.9.6-2016_production/JpsiK-mc/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST--004-dv.root',
        ],
        '../postprocess/JpsiK-run2/JpsiK-run2.yml',
    ),
}

if __name__ == '__main__':
    args = parse_input()

    if args.job_name in JOBS:
        JOBS[args.job_name](job_name=args.job_name, debug=args.debug)
    else:
        print('Unknown job name: {}'.format(args.job_name))

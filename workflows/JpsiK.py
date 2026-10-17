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
from pathos.multiprocessing import ProcessingPool as Pool

sys.path.insert(0, op.dirname(op.abspath(__file__)))

from utils import (
    ensure_dir, abs_path, safe_merge, workflow_cached_ntuple,
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
        trees=['tree'], **kwargs):
    return workflow_apply_weight(input_ntp, pid_histo_folder, pid_config,
                                 output_ntp, '--aux_pid', trees=trees, **kwargs)

# @smart_kwarg
# def workflow_pid_withIsMuon(
#         input_ntp, output_ntp='pid_withIsMuon.root',
#         pid_histo_folder='../run2-JpsiK/reweight/pid/root-run2-JpsiK_withIsMuon-shifted',
#         pid_config='../run2-JpsiK/reweight/pid/run2-JpsiK_withIsMuon.yml',
#         trees=['tree'], **kwargs):
#     return workflow_apply_weight(input_ntp, pid_histo_folder, pid_config,
#                                  output_ntp, '--aux_pid_withIsMuon', trees=trees, **kwargs)


@smart_kwarg
def workflow_trk(
        input_ntp, output_ntp='trk.root',
        trk_histo_folder='../run2-JpsiK/reweight/tracking/root-run2-general',
        trk_config='../run2-JpsiK/reweight/tracking/run2-general.yml',
        trees=['tree'], **kwargs):
    return workflow_apply_weight(input_ntp, trk_histo_folder, trk_config,
                                 output_ntp, '--aux_trk', trees=trees, **kwargs)


# @smart_kwarg
# def workflow_jk_PIDcuts_DLLKweight(
#         input_ntp, output_ntp='jk_PIDcuts_DLLKweight.root',
#         jk_histo_folder='../run2-JpsiK/reweight/JpsiK/root-run2-JpsiK_PIDcuts_DLLKweight',
#         jk_config='../run2-JpsiK/reweight/JpsiK/run2-JpsiK_PIDcuts_DLLKweight.yml',
#         trees=['tree'], **kwargs):
#     return workflow_apply_weight(input_ntp, jk_histo_folder, jk_config,
#                                  output_ntp, '--aux_jk_PIDcuts_DLLKweight', trees=trees, **kwargs)

# @smart_kwarg
# def workflow_jk_PIDcuts(
#         input_ntp, output_ntp='jk_PIDcuts.root',
#         jk_histo_folder='../run2-JpsiK/reweight/JpsiK/root-run2-JpsiK_PIDcuts',
#         jk_config='../run2-JpsiK/reweight/JpsiK/run2-JpsiK_PIDcuts.yml',
#         trees=['tree'], **kwargs):
#     return workflow_apply_weight(input_ntp, jk_histo_folder, jk_config,
#                                  output_ntp, '--aux_jk_PIDcuts', trees=trees, **kwargs)

# @smart_kwarg
# def workflow_jk_PIDweights(
#         input_ntp, output_ntp='jk_PIDweights.root',
#         jk_histo_folder='../run2-JpsiK/reweight/JpsiK/root-run2-JpsiK_PIDweights',
#         jk_config='../run2-JpsiK/reweight/JpsiK/run2-JpsiK_PIDweights.yml',
#         trees=['tree'], **kwargs):
#     return workflow_apply_weight(input_ntp, jk_histo_folder, jk_config,
#                                  output_ntp, '--aux_jk_PIDweights', trees=trees, **kwargs)

@smart_kwarg
def workflow_jk_PIDweights_IsMuonCut(
        input_ntp, output_ntp='jk_PIDweights_IsMuonCut.root',
        jk_histo_folder='../run2-JpsiK/reweight/JpsiK/root-run2-JpsiK_PIDweights_IsMuonCut',
        jk_config='../run2-JpsiK/reweight/JpsiK/run2-JpsiK_PIDweights_IsMuonCut.yml',
        trees=['tree'], **kwargs):
    return workflow_apply_weight(input_ntp, jk_histo_folder, jk_config,
                                 output_ntp, '--aux_jk_PIDweights_IsMuonCut', trees=trees, **kwargs)


@smart_kwarg
def workflow_jk_nspd_correction(input_ntp, output_ntp='jk_nspd_correction.root',
                                nspd_params='../run2-JpsiK/fit/nspd_correction_results/JpsiK-26_09_23_23_56-fit-nspd-2016/nspd_conditional_poisson.yml',
                                trees=['tree'], **kwargs):
    params = abs_path(nspd_params)
    script = abs_path('../scripts/apply_nspdhits_JpsiK_correction.py')
    cmd = f'{sys.executable} {script} {input_ntp} {output_ntp} --params {params} --trees ' + ' '.join(trees)
    print(f'Applying JpsiK conditional-Poisson NSPD correction: {params}')
    return workflow_cached_ntuple(cmd, input_ntp, output_ntp, '--aux_jk_nspd_correction', **kwargs)


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

def workflow_generic_single(maindir, subdir, date, input_ntp, input_yml,
                            aux_workflows, **kwargs):
    chdir(maindir)
    ensure_dir(subdir, make_absolute=False)
    chdir(subdir)
    output_suffix = generate_step2_name(input_ntp, date=date)
    workflow_single_ntuple(
        input_ntp, input_yml, output_suffix, aux_workflows, **kwargs)
    aggregate_output('..', subdir, JpsiK_default_output_fltrs)


def workflow_parallel(inputs, input_yml, job_name, date, aux_workflows,
                      num_of_workers=12, merge=False, **kwargs):
    if num_of_workers < 1:
        raise ValueError('num_of_workers must be positive')
    subworkdirs, workdir = workflow_prep_dir(job_name, inputs, **kwargs)
    job_directives = [
        {
            'maindir': workdir,
            'subdir': subdir,
            'date': date,
            'input_ntp': input_ntp,
            'input_yml': input_yml,
            'aux_workflows': aux_workflows,
        }
        for subdir, input_ntp in subworkdirs.items()
    ]
    with Pool(ncpus=num_of_workers) as pool:
        pool.map(lambda d: workflow_generic_single(**d, **kwargs), job_directives)
        pool.close()
        pool.join()
        pool.clear()
    if merge: safe_merge(workdir, subworkdirs, **kwargs)


def workflow_data(inputs, input_yml, job_name='data', date=None,
                  num_of_workers=20, merge=False, **kwargs):
    return workflow_parallel(inputs, input_yml, job_name, date, [],
                             num_of_workers=num_of_workers, merge=merge, **kwargs)


def workflow_mc(inputs, input_yml, job_name='mc', date=None,
                num_of_workers=20, merge=False, **kwargs):
    aux_workflows = [workflow_pid, workflow_trk, workflow_jk_PIDweights_IsMuonCut, workflow_jk_nspd_correction] 
                    #  workflow_pid_withIsMuon, workflow_jk_PIDcuts_DLLKweight, workflow_jk_PIDcuts, workflow_jk_PIDweights]
    cli_vars = dict(kwargs.pop('cli_vars', {}))
    cli_vars['cli_mc_id'] = '12143001'
    return workflow_parallel(inputs, input_yml, job_name, date, aux_workflows,
                             num_of_workers=num_of_workers, merge=merge,
                             cli_vars=cli_vars, **kwargs)


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
        workflow_data,
        # '../ntuples/0.9.6-2016_production/JpsiK-std',
        '../ntuples/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/JpsiK-data/*--std--*',
        '../postprocess/JpsiK-run2/JpsiK-run2.yml',
        merge=True
    ),
    'JpsiK-ntuple-run2-mc': partial(
        workflow_mc,
        # '../ntuples/0.9.9-JpsiK_noPID/JpsiK-mc',
        '../ntuples/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/JpsiK-mc/*--mc--*',
        '../postprocess/JpsiK-run2/JpsiK-run2.yml',
        merge=True
    ),
    # Run 2 debug
    'JpsiK-ntuple-run2-data-demo': partial(
        workflow_data,
        '../run2-JpsiK/samples/JpsiK--22_02_09--std--data--2016--md--dv45-subset.root',
        '../postprocess/JpsiK-run2/JpsiK-run2.yml',
        merge=True
    ),
    'JpsiK-ntuple-run2-mc-demo': partial(
        workflow_mc,
        '../run2-JpsiK/samples/JpsiK--22_02_22--mc--Bu2JpsiK--2016--md--py8-sim09k-dv45-subset.root',
        '../postprocess/JpsiK-run2/JpsiK-run2.yml',
        merge=True
    ),
    'JpsiK-ntuple-run2-mc-sub': partial(
        workflow_mc,
        [
            '../ntuples/0.9.6-2016_production/JpsiK-mc/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST--000-dv.root',
            '../ntuples/0.9.6-2016_production/JpsiK-mc/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST--001-dv.root',
            '../ntuples/0.9.6-2016_production/JpsiK-mc/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST--002-dv.root',
            '../ntuples/0.9.6-2016_production/JpsiK-mc/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST--003-dv.root',
            '../ntuples/0.9.6-2016_production/JpsiK-mc/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST/JpsiK--22_02_22--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09k_Trig0x6139160F_Reco16_Turbo03a_Stripping28r2NoPrescalingFlagged_12143001_ALLSTREAMS.DST--004-dv.root',
        ],
        '../postprocess/JpsiK-run2/JpsiK-run2.yml',
        merge=True
    ),
}

if __name__ == '__main__':
    args = parse_input()

    if args.job_name in JOBS:
        JOBS[args.job_name](job_name=args.job_name, debug=args.debug)
    else:
        print('Unknown job name: {}'.format(args.job_name))

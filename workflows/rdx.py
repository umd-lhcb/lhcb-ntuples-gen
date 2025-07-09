#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Mar 23, 2023 at 02:23 PM -0400

import sys
import os.path as op
import time

from argparse import ArgumentParser
from os import chdir
from functools import partial
from pathos.multiprocessing import ProcessingPool as Pool

sys.path.insert(0, op.dirname(op.abspath(__file__)))

from utils import (
    run_cmd, abs_path, ensure_dir, ensure_file,
    aggregate_fltr, aggregate_output, check_ntp_name, find_decay_mode,
    load_yaml_db, smart_kwarg,
    generate_step2_name, find_year,
    workflow_compile_cpp, workflow_cached_ntuple, workflow_apply_weight,
    workflow_prep_dir, workflow_split_base
)
from utils import TermColor as TC


#################################
# Command line arguments parser #
#################################

def parse_input():
    parser = ArgumentParser(description='workflow for R(D(*)).')

    parser.add_argument('job_name', help='specify job name.')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug mode.')

    return parser.parse_args()


###########
# Helpers #
###########

rdx_default_fltr = aggregate_fltr(
    keep=[r'^(Dst|D0|ghost|e).*\.root'], blocked=['--aux'])

rdx_default_output_fltrs = {
    'ntuple': rdx_default_fltr,
    'ntuple_aux': aggregate_fltr(keep=['--aux']),
}


def rdx_mc_blocked_trees(decay_mode):
    known_trees = ['D0', 'Dst']
    tree_dict = {
        'D0': 'TupleBminus/DecayTree',
        'Dst': 'TupleB0/DecayTree'
    }
    raw_db = load_yaml_db()

    if decay_mode not in raw_db or 'Keep' not in raw_db[decay_mode]:
        return None

    # NOTE: Here we are returning trees to BLOCK!!
    return [tree_dict[t] for t in known_trees
            if t not in raw_db[decay_mode]['Keep']]


####################################
# Workflows: aux ntuple generation #
####################################

@smart_kwarg
def workflow_ubdt(input_ntp, output_ntp='ubdt.root',
                  trees=['TupleB0/DecayTree', 'TupleBminus/DecayTree'],
                  particle='mu',
                  **kwargs):
    cmd = f'AddUBDTBranch -i {input_ntp} -o {output_ntp} -t {",".join(trees)} -p {particle}'
    return workflow_cached_ntuple(
        cmd, input_ntp, output_ntp, '--aux_ubdt', **kwargs)


@smart_kwarg
def workflow_hammer(input_ntp, output_ntp='hammer.root',
                    trees=['TupleB0/DecayTree', 'TupleBminus/DecayTree'],
                    **kwargs):
    run = 'run1' if '2011' in input_ntp or '2012' in input_ntp else 'run2'
    cmd = [f'ReweightRDX {input_ntp} {output_ntp} {t} {run}' for t in trees]
    return workflow_cached_ntuple(
        cmd, input_ntp, output_ntp, '--aux_hammer', **kwargs)


@smart_kwarg
def workflow_hammer_alt(input_ntp, output_ntp='hammer_alt.root',
                        trees=['TupleB0/DecayTree', 'TupleBminus/DecayTree'],
                        **kwargs):
    run = 'run1' if '2011' in input_ntp or '2012' in input_ntp else 'run2'
    cmd = [f'ReweightRDXDefault {input_ntp} {output_ntp} {t} {run}' for t in trees]
    return workflow_cached_ntuple(
        cmd, input_ntp, output_ntp, '--aux_hammer_alt', **kwargs)

@smart_kwarg
def workflow_hammer_dst10sig(input_ntp, output_ntp='hammer_dst10sig.root',
                             trees=['TupleB0/DecayTree', 'TupleBminus/DecayTree'],
                             **kwargs):
    run = 'run1' if '2011' in input_ntp or '2012' in input_ntp else 'run2'
    cmd = [f'ReweightRDXDst10Sig {input_ntp} {output_ntp} {t} {run}' for t in trees]
    return workflow_cached_ntuple(
        cmd, input_ntp, output_ntp, '--aux_hammer_dst10sig', **kwargs)

@smart_kwarg
def workflow_hammer_dstnocorr(input_ntp, output_ntp='hammer_dstnocorr.root',
                              trees=['TupleB0/DecayTree', 'TupleBminus/DecayTree'],
                              **kwargs):
    run = 'run1' if '2011' in input_ntp or '2012' in input_ntp else 'run2'
    cmd = [f'ReweightRDXDstNoCorr {input_ntp} {output_ntp} {t} {run}' for t in trees]
    return workflow_cached_ntuple(
        cmd, input_ntp, output_ntp, '--aux_hammer_dstnocorr', **kwargs)

@smart_kwarg
def workflow_hammer_dst10signocorr(input_ntp, output_ntp='hammer_dst10signocorr.root',
                                   trees=['TupleB0/DecayTree', 'TupleBminus/DecayTree'],
                                   **kwargs):
    run = 'run1' if '2011' in input_ntp or '2012' in input_ntp else 'run2'
    cmd = [f'ReweightRDXDstNoCorr10Sig {input_ntp} {output_ntp} {t} {run}' for t in trees]
    return workflow_cached_ntuple(
        cmd, input_ntp, output_ntp, '--aux_hammer_dst10signocorr', **kwargs)

@smart_kwarg
def workflow_hammer_run1(input_ntp, output_ntp='hammer_dstrun1.root',
                         trees=['TupleB0/DecayTree', 'TupleBminus/DecayTree'],
                         **kwargs):
    run = 'run1' if '2011' in input_ntp or '2012' in input_ntp else 'run2'
    cmd = [f'ReweightRDXDstRun1 {input_ntp} {output_ntp} {t} {run}' for t in trees]
    return workflow_cached_ntuple(
        cmd, input_ntp, output_ntp, '--aux_hammer_dstrun1', **kwargs)

@smart_kwarg
def workflow_hammer_norescale(input_ntp, output_ntp='hammer_norescale.root',
                              trees=['TupleB0/DecayTree', 'TupleBminus/DecayTree'],
                              **kwargs):
    run = 'run1' if '2011' in input_ntp or '2012' in input_ntp else 'run2'
    cmd = [f'ReweightRDXRemoveRescale {input_ntp} {output_ntp} {t} {run}' for t in trees]
    return workflow_cached_ntuple(
        cmd, input_ntp, output_ntp, '--aux_hammer_norescale', **kwargs)

@smart_kwarg
def workflow_trigger_emu(input_ntp, output_ntp='trg_emu.root',
                         trees=['TupleB0/DecayTree', 'TupleBminus/DecayTree'],
                         **kwargs):
    Bmeson = lambda tree: 'b0' if 'B0' in tree else 'b'
    cmd = [f'run2-rdx-trg_emu.py {input_ntp} {output_ntp} -t {t} -B {Bmeson(t)}'
           for t in trees]
    return workflow_cached_ntuple(
        cmd, input_ntp, output_ntp, '--aux_trg_emu', **kwargs)


@smart_kwarg
def workflow_pid(
        input_ntp, output_ntp='pid.root',
        pid_histo_folder='../run2-rdx/reweight/pid/old/root-run2-rdx_oldcut-shifted',
        pid_config='../run2-rdx/reweight/pid/run2-rdx_oldcut.yml',
        **kwargs):
    return workflow_apply_weight(input_ntp, pid_histo_folder, pid_config,
                                 output_ntp, '--aux_pid', **kwargs)


@smart_kwarg
def workflow_trk(
        input_ntp, output_ntp='trk.root',
        trk_histo_folder='../run2-rdx/reweight/tracking/root-run2-general',
        trk_config='../run2-rdx/reweight/tracking/run2-general.yml',
        **kwargs):
    return workflow_apply_weight(input_ntp, trk_histo_folder, trk_config,
                                 output_ntp, '--aux_trk', **kwargs)

@smart_kwarg
def workflow_jk(
        input_ntp, output_ntp='jk.root',
        trk_histo_folder='../run2-rdx/reweight/JpsiK/root-run2-JpsiK',
        trk_config='../run2-rdx/reweight/JpsiK/run2-JpsiK.yml',
        **kwargs):
    return workflow_apply_weight(input_ntp, trk_histo_folder, trk_config,
                                 output_ntp, '--aux_jk', **kwargs)

@smart_kwarg
def workflow_jkp(
        input_ntp, output_ntp='jk.root',
        trk_histo_folder='../run2-rdx/reweight/JpsiKp/root-run2-JpsiKp',
        trk_config='../run2-rdx/reweight/JpsiKp/run2-JpsiKp.yml',
        **kwargs):
    return workflow_apply_weight(input_ntp, trk_histo_folder, trk_config,
                                 output_ntp, '--aux_jk', **kwargs)

@smart_kwarg
def workflow_misid(
        input_ntp,
        misid_aux_ntp='../run2-rdx/reweight/misid/histos/dif.root',
        misid_config='../run2-rdx/reweight/misid/run2-rdx.yml',
        k_smr_name='k_smr',
        pi_smr_name='pi_smr',
        **kwargs):
    output_ntp = 'misid.root'
    aux_ntp = abs_path(misid_aux_ntp)
    config = abs_path(misid_config)
    year = find_year(input_ntp)

    cmd = f'ApplyMisIDWeight -a -i {input_ntp} -o {output_ntp} -x {aux_ntp} -c {config} -Y {year} --kSmrBrName {k_smr_name} --piSmrBrName {pi_smr_name}'
    return workflow_cached_ntuple(
        cmd, input_ntp, output_ntp, '--aux_misid', **kwargs)


@smart_kwarg
def workflow_vertex(
        input_ntp, output_ntp='vertex.root',
        vertex_aux_ntp='../run2-rdx/reweight/vertex/smearing_vec.root',
        **kwargs):
    aux_ntp = abs_path(vertex_aux_ntp)

    cmd = f'ApplyVertexSmear -i {input_ntp} -o {output_ntp} -x {aux_ntp}'
    return workflow_cached_ntuple(
        cmd, input_ntp, output_ntp, '--aux_vertex', **kwargs)

# @smart_kwarg
# def workflow_vertex_scale(
#         input_ntp, output_ntp='vertex_scale.root',
#         **kwargs):
#     cmd = f'GetScaledVariationWeights -i {input_ntp} -o {output_ntp}'
#     return workflow_cached_ntuple(
#         cmd, input_ntp, output_ntp, '--aux_vertex_scale', **kwargs)


#######################
# Workflows: wrappers #
#######################

@smart_kwarg([])
def workflow_bm_cli(bm_cmd, cli_vars=None, blocked_input_trees=None,
                    blocked_output_trees=None, directive_override=None):
    if blocked_input_trees:
        bm_cmd += ' -B '+' '.join(blocked_input_trees)

    if blocked_output_trees:
        bm_cmd += ' -X '+' '.join(blocked_output_trees)

    if cli_vars:
        bm_cmd += ' -V '+' '.join([str(k)+':'+str(v)
                                   for k, v in cli_vars.items()])

    if directive_override:
        bm_cmd += ' -D '+' '.join([str(k)+':'+str(v)
                                   for k, v in directive_override.items()])

    return bm_cmd


def workflow_single_ntuple(input_ntp, input_yml, output_suffix, aux_workflows,
                           cpp_template='../postprocess/cpp_templates/rdx.cpp',
                           **kwargs):
    input_ntp = ensure_file(input_ntp)
    print('{}Working on {}...{}'.format(TC.GREEN, input_ntp, TC.END))
    cpp_template = abs_path(cpp_template)

    bm_cmd = 'babymaker -i {} -o baby.cpp -n {} -t {}'

    aux_ntuples = [w(input_ntp, **kwargs) for w in aux_workflows]
    if aux_ntuples:
        bm_cmd += ' -f ' + ' '.join(aux_ntuples)

    bm_cmd = workflow_bm_cli(bm_cmd, **kwargs).format(
        abs_path(input_yml), input_ntp, cpp_template)

    run_cmd(bm_cmd, **kwargs)
    workflow_compile_cpp('baby.cpp', **kwargs)
    run_cmd('./baby.exe --{}'.format(output_suffix), **kwargs)


###################
# Workflows: main #
###################

def workflow_generic_single(maindir, subdir,
                         date, input_ntp, input_yml, aux_workflows,
                         **kwargs):
    chdir(maindir)
    ensure_dir(subdir, make_absolute=False)
    chdir(subdir)  # Switch to the workdir of the subjob

    output_suffix = generate_step2_name(input_ntp, date=date)
    workflow_single_ntuple(
        input_ntp, input_yml, output_suffix, aux_workflows, **kwargs)

    aggregate_output('..', subdir, rdx_default_output_fltrs)


def workflow_data(inputs, input_yml, job_name='data', use_ubdt=True,
                  use_misid=False, date=None, num_of_workers=12,
                  trees=[
                      'TupleB0/DecayTree',
                      'TupleB0WSMu/DecayTree',
                      'TupleB0WSPi/DecayTree',
                      'TupleBminus/DecayTree',
                      'TupleBminusWS/DecayTree'
                  ],
                  **kwargs):
    aux_workflows = [workflow_ubdt] if use_ubdt else []
    if use_misid:
        aux_workflows.append(workflow_misid)
    subworkdirs, workdir = workflow_prep_dir(job_name, inputs, **kwargs)

    job_directives = [
        {
            'maindir': workdir,
            'subdir': subdir,
            'date': date,
            'input_ntp': input_ntp,
            'input_yml': input_yml,
            'aux_workflows': aux_workflows,
            'trees': trees
        }
        for subdir, input_ntp in subworkdirs.items()
    ]

    with Pool(ncpus=num_of_workers) as pool:
        pool.map(lambda d: workflow_generic_single(**d, **kwargs), job_directives)
        pool.close()
        pool.join()
        pool.clear()


# Just an alias
def workflow_mc_ghost(*args, **kwargs):
    workflow_data(*args, **kwargs)


def workflow_mc_single(maindir, subdir,
                       date, input_ntp, input_yml, aux_workflows, **kwargs):
    chdir(maindir)
    ensure_dir(subdir, make_absolute=False)
    chdir(subdir)  # Switch to the workdir of the subjob

    fields = check_ntp_name(input_ntp)[0]
    if 'decay_mode' in fields:
        decay_mode = fields['decay_mode']
    else:
        decay_mode = find_decay_mode(fields['lfn'])
    blocked_input_trees = rdx_mc_blocked_trees(decay_mode)

    trees = ['TupleBminus/DecayTree', 'TupleB0/DecayTree']
    if blocked_input_trees is not None:
        if 'D0' in blocked_input_trees:
            trees = ['TupleB0/DecayTree']
        elif 'Dst' in blocked_input_trees:
            trees =  ['TupleBminus/DecayTree']

    output_suffix = generate_step2_name(input_ntp, date=date)
    if 'cli_vars' not in kwargs:
        kwargs['cli_vars'] = dict()
    kwargs['cli_vars']['cli_mc_id'] = decay_mode
    if 'year' in fields:
        kwargs['cli_vars']['cli_mc_year'] = fields['year']
    else:
        kwargs['cli_vars']['cli_mc_year'] = find_year(fields['lfn'])

    workflow_single_ntuple(
        input_ntp, input_yml, output_suffix, aux_workflows,
        blocked_input_trees=blocked_input_trees, trees=trees, **kwargs)

    aggregate_output('..', subdir, rdx_default_output_fltrs)


def workflow_mc(inputs, input_yml, job_name='mc', date=None,
                use_hammer=True, use_hammer_alt=False, use_hammer_dst10sig=False,
                use_hammer_dstnocorr=False, use_hammer_dst10signocorr=False,
                use_hammer_dstrun1=False, use_hammer_no_rescale=False,
                num_of_workers=12, **kwargs):
    if (any(elem in inputs for elem in ["15574081", "15574082", "15574083"])):
        aux_workflows = [
            workflow_trigger_emu, workflow_pid, workflow_trk, workflow_jkp,
            workflow_vertex#, workflow_vertex_scale
        ]
    else:
        aux_workflows = [
            workflow_trigger_emu, workflow_pid, workflow_trk, workflow_jk,
            workflow_vertex#, workflow_vertex_scale
        ]
    if use_hammer:
        aux_workflows.append(workflow_hammer)
    if use_hammer_alt:
        aux_workflows.append(workflow_hammer_alt)
    if use_hammer_dst10sig:
        aux_workflows.append(workflow_hammer_dst10sig)
    if use_hammer_dstnocorr:
        aux_workflows.append(workflow_hammer_dstnocorr)
    if use_hammer_dst10signocorr:
        aux_workflows.append(workflow_hammer_dst10signocorr)
    if use_hammer_dstrun1:
        aux_workflows.append(workflow_hammer_run1)
    if use_hammer_no_rescale:
        aux_workflows.append(workflow_hammer_norescale)

    subworkdirs, workdir = workflow_prep_dir(job_name, inputs, **kwargs)

    job_directives = [
        {
            'maindir': workdir,
            'subdir': subdir,
            'date': date,
            'input_ntp': input_ntp,
            'input_yml': input_yml,
            'aux_workflows': aux_workflows
        }
        for subdir, input_ntp in subworkdirs.items()
    ]

    with Pool(ncpus=num_of_workers) as pool:
        pool.map(lambda d: workflow_mc_single(**d, **kwargs), job_directives)
        pool.close()
        pool.join()
        pool.clear()


def workflow_split(inputs, input_yml, job_name='split', **kwargs):
    return workflow_split_base(
        inputs, input_yml, job_name=job_name, prefix='Dst_D0',
        workflow_data=workflow_data, workflow_mc=workflow_mc,
        **kwargs)


def workflow_split_mc_ghost(inputs, input_yml, job_name='split', **kwargs):
    return workflow_split_base(
        inputs, input_yml, job_name=job_name, prefix='Dst_D0',
        workflow_data=workflow_mc_ghost, workflow_mc=workflow_mc_ghost,
        **kwargs)


#####################
# Production config #
#####################

JOBS = {
    # External Run 2
    'RJpsi-ntuple-run2-mc_ghost-16': partial(
        workflow_mc_ghost,
        '../ntuples/ref-RJpsi-run2/IncJpsi/*2016*',
        '../postprocess/rdx-run2/rdx-run2_ghost.yml',
        trees=['JpsiRecTuple/DecayTree'],
        prefix='Jpsi',
        particle='BachMu'
    ),
    'RJpsi-ntuple-run2-mc_ghost-17': partial(
        workflow_mc_ghost,
        '../ntuples/ref-RJpsi-run2/IncJpsi/*2017*',
        '../postprocess/rdx-run2/rdx-run2_ghost.yml',
        trees=['JpsiRecTuple/DecayTree'],
        prefix='Jpsi',
        particle='BachMu'
    ),
    'RJpsi-ntuple-run2-mc_ghost-18': partial(
        workflow_mc_ghost,
        '../ntuples/ref-RJpsi-run2/IncJpsi/*2018*',
        '../postprocess/rdx-run2/rdx-run2_ghost.yml',
        trees=['JpsiRecTuple/DecayTree'],
        prefix='Jpsi',
        particle='BachMu'
    ),
    # Run 2 data
    'Dst_D0-std': partial(
        workflow_split,
        '../ntuples/0.9.6-2016_production/Dst_D0-std/',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
    ),
    'rdx-ntuple-run2-data-cut_opt': partial(
        workflow_split,
        '../ntuples/0.9.6-2016_production/Dst_D0-std/',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        cli_vars={'cli_cutflow': 'true'}
    ),
    'Dst_D0-mu_misid': partial(
        workflow_split,
        '../ntuples/0.9.6-2016_production/Dst_D0-mu_misid/',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        cli_vars={'cli_misid': 'true'},
        use_misid=True,
        use_ubdt=False
    ),
    'rdx-ntuple-run2-misid_study': partial(
        workflow_split,
        '../ntuples/0.9.6-2016_production/Dst_D0-mu_misid/',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        cli_vars={'cli_misid_study': 'true'},
        use_ubdt=False
    ),
    # Run 2 MC
    'rdx-ntuple-run2-mc_ghost': partial(
        workflow_split_mc_ghost,
        '../ntuples/0.9.7-rdx_production/Dst_D0-ghost/Dst_D0--*ghost_norm*',
        '../postprocess/rdx-run2/rdx-run2_ghost.yml',
        trees=['TupleBminus/DecayTree']
    ),
    'rdx-ntuple-run2-mc': partial(
        workflow_mc,
        '../ntuples/0.9.5-bugfix/Dst_D0-mc',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        blocked_patterns=['--aux', 'MC_2012']
    ),
    'rdx-ntuple-run2-mc-cut_opt': partial(
        workflow_mc,
        '../ntuples/0.9.5-bugfix/Dst_D0-mc',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        cli_vars={'cli_cutflow': 'true'},
        blocked_patterns=['--aux', 'MC_2012']
    ),
    # Run 2 MC full sim for Lb
    'Dst_D0-mc-fullsim-Lb': partial(
        workflow_split,
        [
            f'../ntuples/0.9.11-Lb-mc-fullsim/*{i}*.DST'
            for i in [15574081, 15574082, 15574083]
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        use_hammer=False,
        num_of_workers=20
    ),
    # Run 2 MC tracker only
    'Dst_D0-mc-tracker_only-sig_norm': partial(
        workflow_split,
        [
            # D0
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573012*.DST', # norm
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573001*.DST', # sig
            # D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11574021*.DST', # norm, D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773410*.DST', # norm, D*0
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11574011*.DST', # sig, D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773400*.DST', # sig, D*0
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        # use_hammer_alt=True,
        use_hammer_dstrun1=True,
        num_of_workers=20
    ),
    ### DDX including DDspi for the D* (unused D0 ntuples with DDspi also produced)
    'Dst_D0-mc-tracker_only-DDX': partial(
        workflow_split,
        [f'../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*{i}*.DST'
            for i in [
                11894600, 12893600, 11894200, 12893610,
                11894610, 12895400, 11894210, 12895000,
                11895400
            ]
         ]
         +
         [f'../ntuples/0.9.10-DstDspi/Dst_D0-mc-tracker_only/*{i}*.DST' for i in [11894400, 12895410]]
        ,
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        use_hammer=False,
        num_of_workers=20
    ),
    # 'rdx-ntuple-run2-mc-to-missing-ddx': partial(
    #     workflow_split,
    #     ['../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11895400*.DST'],
    #     '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
    #     use_hammer=False,
    #     num_of_workers=20
    # ),
    # 'rdx-ntuple-run2-mc-to-missing-ddx-DstDspi': partial(
    #     workflow_split,
    #     [f'../ntuples/0.9.10-DstDspi/Dst_D0-mc-tracker_only/*{i}*.DST' for i in [11894400, 12895410]],
    #     '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
    #     use_hammer=False,
    #     num_of_workers=20
    # ),
    'Dst_D0-mc-tracker_only-Dstst': partial(
        workflow_split,
        [
            f'../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*{i}*.DST'
            for i in [11874430, 11874440, 12873450, 12873460]
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        # use_hammer_alt=True,
        use_hammer_no_rescale=True, # not nominally used for D**
        num_of_workers=20
    ),
    'Dst_D0-mc-tracker_only-Dstst_heavy': partial(
        workflow_split,
        [
            f'../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*{i}*.DST'
            for i in [12675011, 11674401, 12675402, 11676012, 12875440]
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        use_hammer=False,
        num_of_workers=20
    ),
    'Dst_D0-mc-tracker_only-D_s': partial(
        workflow_split,
        [
            f'../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*{i}*.DST'
            for i in [13874020, 13674000]
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        # use_hammer_alt=True,
        num_of_workers=20
    ),
    # Run 2 debug
    'rdx-ntuple-run2-mu_misid-demo': partial(
        workflow_data,
        '../ntuples/0.9.6-2016_production/Dst_D0-mu_misid/*MagDown*.DST/*--000-dv.root',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        cli_vars={'cli_misid': 'true'},
        use_misid=True
    ),
    'rdx-ntuple-run2-misid_study-demo': partial(
        workflow_data,
        '../ntuples/0.9.6-2016_production/Dst_D0-mu_misid/*MagDown*.DST/*--000-dv.root',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        cli_vars={'cli_misid_study': 'true'}
    ),
    'rdx-ntuple-run2-data-demo': partial(
        workflow_split,
        '../ntuples/0.9.6-2016_production/Dst_D0-std/*MagDown*.DST/*--000-dv.root',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
    ),
    'rdx-ntuple-run2-data-debug': partial(
        workflow_split,
        '../ntuples/0.9.6-2016_production/Dst_D0-std/*MagDown*.DST/*-00?-dv.root',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml'
    ),
    'rdx-ntuple-run2-data-no-Dst-veto': partial(
        workflow_data,
        [
            '../ntuples/0.9.4-trigger_emulation/Dst_D0-std',
            '../ntuples/0.9.5-bugfix/Dst_D0-cutflow_data',
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        cli_vars={'cli_no_dst_veto': '100.0'}
    ),
    'rdx-ntuple-run2-mc-to-sig-norm-no-Dst-veto': partial(
        workflow_split,
        [
            # D0
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573012*.DST', # norm
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573001*.DST', # sig
            # D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11574021*.DST', # norm, D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773410*.DST', # norm, D*0
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11574011*.DST', # sig, D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773400*.DST', # sig, D*0
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        use_hammer=False,
        num_of_workers=20,
        cli_vars={'cli_no_dst_veto': '100.0'}
    ),
    'rdx-ntuple-run2-mc-to-dst0norm-for-vertexsmear': partial(
        workflow_split,
        '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773410*.DST', # norm, D*0
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        cli_vars={'cli_misid_study': 'true'},
        num_of_workers=20
    ),
    'rdx-ntuple-run2-mc-demo': partial(
        workflow_mc,
        '../ntuples/0.9.5-bugfix/Dst_D0-mc/*MagDown*11574011*.root',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
    ),
    'rdx-ntuple-run2-mc-demo-ddx': partial(
        workflow_mc,
        '../ntuples/0.9.5-bugfix/Dst_D0-mc/*MagDown*11894600*.root',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
    ),
    'rdx-ntuple-run2-mc-to-demo': partial(
        workflow_split,
        '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*MagDown*11574021*.DST',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        blocked_patterns=['--aux', r'--([1-9][0-9][0-9]|0[1-9][0-9])-dv']
    ),
    'rdx-ntuple-run2-mc-to-ddx-test': partial(
        workflow_split,
        [f'../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*{i}*.DST' for i in \
                [11894600, 12893600, 11894200, 12893610,
                 11894610, 12895400, 11894210, 12895000,
                 11895400]],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        use_hammer=False,
        blocked_patterns=['--aux', r'--([1-9][0-9]|[1-9][0-9][0-9]|[0-9][1-9][0-9])-dv'],
        num_of_workers=20
    ),
    'rdx-ntuple-run2-mc-dss': partial(
        workflow_mc,
        '../ntuples/0.9.5-bugfix/Dst_D0-mc/*MagDown*11874430*.root',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
    ),
    'rdx-ntuple-run2-mc-sub': partial(
        workflow_split,
        '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*MagDown*12773410*.DST',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
    ),
    'rdx-ntuple-run2-mc-to-sig-norm-demo': partial(
        workflow_split,
        [
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573012*.DST/*--00?-dv.root',
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573001*.DST/*--00?-dv.root',
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
    ),
    'rdx-ntuple-run2-mc-to-dstst-debug': partial(
        workflow_split,
        [
            f'../../misc/ntuples_subset_TO_2016_dstst/*{i}*.DST'
            for i in [11874430, 11874440, 12873450, 12873460]
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
    ),
    'rdx-ntuple-run2-mc-to-sig-norm-dst-ff-debug-10sig': partial(
        workflow_split,
        [
            # D0
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573012*.DST', # norm
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573001*.DST', # sig
            # D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11574021*.DST', # norm, D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773410*.DST', # norm, D*0
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11574011*.DST', # sig, D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773400*.DST', # sig, D*0
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        blocked_patterns=['--aux', r'--([1-9][0-9][0-9])-dv', 'MagUp'],
        use_hammer_dst10sig=True,
        num_of_workers=20
    ),
    'rdx-ntuple-run2-mc-to-sig-norm-dst-ff-debug': partial(
        workflow_split,
        [
            # D0
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573012*.DST', # norm
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573001*.DST', # sig
            # D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11574021*.DST', # norm, D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773410*.DST', # norm, D*0
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11574011*.DST', # sig, D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773400*.DST', # sig, D*0
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        blocked_patterns=['--aux', r'--([1-9][0-9][0-9])-dv', 'MagUp'],
        use_hammer_alt=True,
        num_of_workers=20
    ),
    'rdx-ntuple-run2-mc-to-sig-norm-dst-ff-debug-10sig-nocorr': partial(
        workflow_split,
        [
            # D0
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573012*.DST', # norm
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573001*.DST', # sig
            # D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11574021*.DST', # norm, D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773410*.DST', # norm, D*0
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11574011*.DST', # sig, D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773400*.DST', # sig, D*0
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        blocked_patterns=['--aux', r'--([1-9][0-9][0-9])-dv', 'MagUp'],
        use_hammer_dst10signocorr=True,
        num_of_workers=20
    ),
    'rdx-ntuple-run2-mc-to-sig-norm-dst-ff-debug-nocorr': partial(
        workflow_split,
        [
            # D0
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573012*.DST', # norm
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573001*.DST', # sig
            # D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11574021*.DST', # norm, D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773410*.DST', # norm, D*0
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11574011*.DST', # sig, D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773400*.DST', # sig, D*0
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        blocked_patterns=['--aux', r'--([1-9][0-9][0-9])-dv', 'MagUp'],
        use_hammer_dstnocorr=True,
        num_of_workers=20
    ),
    'rdx-ntuple-run2-mc-to-sig-norm-dst-ff-debug-phoebe': partial(
        workflow_split,
        [
            # D0
            # '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573012*.DST', # norm
            # '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573001*.DST', # sig
            # D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11574021*.DST', # norm, D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773410*.DST', # norm, D*0
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11574011*.DST', # sig, D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773400*.DST', # sig, D*0
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        # blocked_patterns=['--aux', r'--([1-9][0-9][0-9])-dv', 'MagUp'],
        use_hammer_dstrun1=True,
        num_of_workers=20
    ),
    'rdx-ntuple-run2-mc-to-sig-norm-dst-ff-debug-no-rescale': partial(
        workflow_split,
        [
            # D0
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573012*.DST', # norm
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573001*.DST', # sig
            # D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11574021*.DST', # norm, D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773410*.DST', # norm, D*0
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*11574011*.DST', # sig, D*
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773400*.DST', # sig, D*0
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        blocked_patterns=['--aux', r'--([1-9][0-9][0-9])-dv', 'MagUp'],
        use_hammer_no_rescale=True,
        num_of_workers=20
    ),
    'rdx-ntuple-run2-mc-to-dst0normsubsamp-for-vertexsmear': partial(
        workflow_split,
        '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12773410*.DST', # norm, D*0
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        blocked_patterns=['--aux', r'--([1-9][0-9][0-9])-dv', 'MagUp'],
        cli_vars={'cli_misid_study': 'true'},
        num_of_workers=20
    ),
    # Run 1
    'rdx-ntuple-run1-data': partial(
        workflow_data,
        '../ntuples/0.9.5-bugfix/Dst_D0-std',
        '../postprocess/rdx-run1/rdx-run1.yml',
        use_ubdt=False
    ),
    # Run 1 debug
    'rdx-ntuple-run1-data-D0-comp': partial(
        workflow_data,
        '../ntuples/0.9.5-bugfix/Dst_D0-std/*MagDown*.root',
        '../postprocess/ref-rdx-run1/ref-rdx-run1-D0.yml',
        use_ubdt=False,
        cli_vars={
            'cli_fewer_cuts': 'true',
            'no_mass_window_cut': 'true',
        }
    ),
    'rdx-ntuple-run1-data-Dst-comp': partial(
        workflow_data,
        '../ntuples/0.9.5-bugfix/Dst_D0-std/*MagDown*.root',
        '../postprocess/ref-rdx-run1/ref-rdx-run1-Dst.yml',
        use_ubdt=False,
        cli_vars={'cli_fewer_cuts': 'true'}
    ),
    # Reference Run 1
    'ref-rdx-ntuple-run1-data-Dst': partial(
        workflow_data,
        '../ntuples/ref-rdx-run1/Dst-mix/Dst--21_10_21--mix--all--2011-2012--md-mu--phoebe.root',
        '../postprocess/ref-rdx-run1/ref-rdx-run1-Dst.yml',
        use_ubdt=False
    ),
    'ref-rdx-ntuple-run1-data-Dst-comp': partial(
        workflow_data,
        [
            '../ntuples/ref-rdx-run1/Dst-std/Dst--20_09_16--std--data--2011--md--phoebe.root',
            '../ntuples/ref-rdx-run1/Dst-mix/Dst--21_10_21--mix--all--2011-2012--md-mu--phoebe.root',
        ],
        '../postprocess/ref-rdx-run1/ref-rdx-run1-Dst.yml',
        use_ubdt=False,
        cli_vars={'cli_fewer_cuts': 'true'}
    ),
    'ref-rdx-ntuple-run1-data-D0': partial(
        workflow_data,
        '../ntuples/ref-rdx-run1/D0-mix/D0--21_10_21--mix--all--2011-2012--md-mu--phoebe.root',
        '../postprocess/ref-rdx-run1/ref-rdx-run1-D0.yml',
        use_ubdt=False
    ),
    'ref-rdx-ntuple-run1-data-D0-comp': partial(
        workflow_data,
        '../ntuples/ref-rdx-run1/D0-mix/D0--21_10_21--mix--all--2011-2012--md-mu--phoebe.root',
        '../postprocess/ref-rdx-run1/ref-rdx-run1-D0.yml',
        use_ubdt=False,
        cli_vars={'cli_fewer_cuts': 'true'}
    ),
}

if __name__ == '__main__':
    start = time.time()
    args = parse_input()

    if args.job_name in JOBS:
        JOBS[args.job_name](job_name=args.job_name, debug=args.debug)
    else:
        print('Unknown job name: {}'.format(args.job_name))

    end = time.time()
    d = (end - start) / 3600
    h = int(d)
    m = int((d - h) * 60)
    s = int(((d - h) * 60 - m) * 60)
    print(f'\nFinished processing {args.job_name} in {h}h {m}m {s}s')

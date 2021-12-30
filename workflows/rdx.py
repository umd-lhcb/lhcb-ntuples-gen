#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Dec 30, 2021 at 04:01 PM +0100

import sys
import os
import os.path as op

from argparse import ArgumentParser, Action
from os import chdir
from shutil import rmtree

from pyBabyMaker.base import TermColor as TC

sys.path.insert(0, op.dirname(op.abspath(__file__)))

from utils import (
    run_cmd_wrapper,
    abs_path, ensure_dir, ensure_file, find_all_input,
    aggregate_fltr, aggregate_output,
    load_yaml_db, smart_kwarg,
    generate_step2_name, parse_step2_name,
    workflow_compile_cpp, workflow_cached_ntuple, workflow_apply_weight
)


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
    keep=[r'^(Dst|D0).*\.root'], blocked=['--aux'])

rdx_default_output_fltrs = {
    'ntuple': rdx_default_fltr,
    'ntuple_aux': aggregate_fltr(keep=['--aux']),
}


def rdx_mc_fltr(decay_mode):
    db = load_yaml_db()
    # Unfortunately we need to use 'Filename' as the key so we need to re-build
    # the dict on the fly
    db = {v['Filename']: v['Keep'] for v in db.values() if 'Keep' in v}

    if decay_mode not in db:
        return rdx_default_fltr
    return aggregate_fltr(keep=[r'^({}).*\.root'.format(
        '|'.join(db[decay_mode]))])


def rdx_mc_add_info(decay_mode):
    known_trees = ['D0', 'Dst']
    tree_dict = {
        'D0': 'TupleBminus/DecayTree',
        'Dst': 'TupleB0/DecayTree'
    }

    raw_db = load_yaml_db()

    try:
        # Actually, the MC ID is feed in
        int(decay_mode)
        decay_mode = raw_db[decay_mode]['Filename']
    except ValueError:
        pass

    # Unfortunately we need to use 'Filename' as the key so we need to re-build
    # the dict on the fly
    db_keep = {v['Filename']: v['Keep']
               for v in raw_db.values() if 'Keep' in v}
    db_id = {v['Filename']: k for k, v in raw_db.items()}

    try:
        decay_id = db_id[decay_mode]
    except KeyError:
        decay_id = '0'

    if decay_mode not in db_keep:
        return None, decay_id

    # NOTE: Here we are returning trees to BLOCK!!
    return [tree_dict[t] for t in known_trees
            if t not in db_keep[decay_mode]], decay_id


####################################
# Workflows: aux ntuple generation #
####################################

@smart_kwarg
def workflow_ubdt(input_ntp, output_ntp='ubdt.root',
                  trees=['TupleB0/DecayTree', 'TupleBminus/DecayTree'],
                  **kwargs):
    weight_file = abs_path('../run2-rdx/weights_run2_no_cut_ubdt.xml')
    cmd = f'addUBDTBranch {input_ntp} mu_isMuonTight {weight_file} {output_ntp} {" ".join(trees)}'
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
        pid_histo_folder='../run2-rdx/reweight/pid/root-run2-rdx_oldcut',
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


@smart_kwarg
def workflow_single_ntuple(input_ntp, input_yml, output_suffix, aux_workflows,
                           cpp_template='../postprocess/cpp_templates/rdx.cpp',
                           executor=run_cmd_wrapper(),
                           **kwargs):
    input_ntp = ensure_file(input_ntp)
    print('{}Working on {}...{}'.format(TC.GREEN, input_ntp, TC.END))
    cpp_template = abs_path(cpp_template)

    bm_cmd = 'babymaker -i {} -o baby.cpp -n {} -t {}'

    aux_ntuples = [w(input_ntp, executor=executor, **kwargs)
                   for w in aux_workflows]
    if aux_ntuples:
        bm_cmd += ' -f ' + ' '.join(aux_ntuples)

    bm_cmd = workflow_bm_cli(bm_cmd, **kwargs)

    executor(bm_cmd.format(abs_path(input_yml), input_ntp, cpp_template))
    workflow_compile_cpp('baby.cpp', executor=executor)

    executor('./baby.exe --{}'.format(output_suffix))


@smart_kwarg([])
def workflow_data_mc(job_name, inputs,
                     output_dir=abs_path('../gen'),
                     patterns=['*.root'],
                     blocked_patterns=['--aux'],
                     ):
    print('{}==== Job: {} ===={}'.format(TC.BOLD+TC.GREEN, job_name, TC.END))

    # Need to figure out the absolute path
    input_files = find_all_input(inputs, patterns, blocked_patterns)
    subworkdirs = {op.splitext(op.basename(i))[0]: i
                   for i in input_files}

    # Now ensure the working dir
    workdir = ensure_dir(op.join(output_dir, job_name))

    return subworkdirs, workdir


#############
# Workflows #
#############

def workflow_data(job_name, inputs, input_yml,
                  use_ubdt=True,
                  output_ntp_name_gen=generate_step2_name,
                  output_fltr=rdx_default_output_fltrs,
                  **kwargs):
    subworkdirs, workdir = workflow_data_mc(job_name, inputs, **kwargs)
    chdir(workdir)
    aux_workflows = [workflow_ubdt] if use_ubdt else []

    for subdir, input_ntp in subworkdirs.items():
        ensure_dir(subdir, make_absolute=False)
        chdir(subdir)  # Switch to the workdir of the subjob

        output_suffix = output_ntp_name_gen(input_ntp)
        workflow_single_ntuple(
            input_ntp, input_yml, output_suffix, aux_workflows, **kwargs)

        aggregate_output('..', subdir, output_fltr)
        chdir('..')  # Switch back to parent workdir


def workflow_mc(job_name, inputs, input_yml,
                output_ntp_name_gen=generate_step2_name,
                output_fltr=rdx_default_output_fltrs,
                **kwargs):
    subworkdirs, workdir = workflow_data_mc(job_name, inputs, **kwargs)
    chdir(workdir)
    aux_workflows = [
        workflow_hammer, workflow_trigger_emu, workflow_pid, workflow_trk
    ]

    for subdir, input_ntp in subworkdirs.items():
        ensure_dir(subdir, make_absolute=False)
        chdir(subdir)  # Switch to the workdir of the subjob

        output_suffix = output_ntp_name_gen(input_ntp)
        decay_mode = output_suffix.split('--')[2]
        blocked_input_trees, decay_id = rdx_mc_add_info(decay_mode)

        output_suffix = output_ntp_name_gen(input_ntp)
        workflow_single_ntuple(
            input_ntp, input_yml, output_suffix, aux_workflows,
            cli_vars={'cli_mc_id': decay_id},
            blocked_input_trees=blocked_input_trees, **kwargs)

        aggregate_output('..', subdir, output_fltr)
        chdir('..')  # Switch back to parent workdir


#####################
# Production config #
#####################

args = parse_input()
executor = run_cmd_wrapper(args.debug)

JOBS = {
    # Run 2
    'rdx-ntuple-run2-data-oldcut': lambda name: workflow_data(
        name,
        '../ntuples/0.9.5-bugfix/Dst_D0-cutflow_data',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        executor=executor
    ),
    'rdx-ntuple-run2-mc-fs': lambda name: workflow_mc(
        name,
        '../ntuples/0.9.5-bugfix/Dst_D0-mc',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        executor=executor,
        blocked_patterns=['--aux', 'MC_2012']
    ),
    # Run 2 debug
    'rdx-ntuple-run2-mc-dss': lambda name: workflow_mc(
        name,
        [
            '../ntuples/0.9.5-bugfix/Dst_D0-mc/Dst_D0--21_10_15--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11874430_D0TAUNU.SAFESTRIPTRIG.DST.root',
            # '../ntuples/0.9.5-bugfix/Dst_D0-mc/Dst_D0--21_10_15--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11874440_D0TAUNU.SAFESTRIPTRIG.DST.root',
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        executor=executor
    ),
    'rdx-ntuple-run2-data-oldcut-debug': lambda name: workflow_data(
        name,
        '../ntuples/0.9.5-bugfix/Dst_D0-cutflow_data',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        executor=executor,
        cli_vars={'cli_cutflow': 'true'},
        directive_override={'one_cand_only/enable': 'false'}
    ),
    'rdx-ntuple-run2-data-oldcut-no-Dst-veto': lambda name: workflow_data(
        name,
        [
            '../ntuples/0.9.4-trigger_emulation/Dst_D0-std',
            '../ntuples/0.9.5-bugfix/Dst_D0-cutflow_data',
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        executor=executor,
        cli_vars={'cli_no_dst_veto': '100.0'}
    ),
    'rdx-ntuple-run2-mc-demo': lambda name: workflow_mc(
        name,
        '../ntuples/0.9.5-bugfix/Dst_D0-mc/Dst_D0--21_10_08--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574011_D0TAUNU.SAFESTRIPTRIG.DST.root',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        executor=executor
    ),
    # Run 1
    'rdx-ntuple-run1-data': lambda name: workflow_data(
        name,
        '../ntuples/0.9.5-bugfix/Dst_D0-std',
        '../postprocess/rdx-run1/rdx-run1.yml',
        use_ubdt=False,
        executor=executor
    ),
    # Run 1 debug
    'rdx-ntuple-run1-data-D0-comp': lambda name: workflow_data(
        name,
        '../ntuples/0.9.5-bugfix/Dst_D0-std/Dst_D0--21_10_07--std--LHCb_Collision11_Beam3500GeV-VeloClosed-MagDown_Real_Data_Reco14_Stripping21r1_90000000_SEMILEPTONIC.DST.root',
        '../postprocess/ref-rdx-run1/ref-rdx-run1-D0.yml',
        use_ubdt=False,
        executor=executor,
        cli_vars={
            'cli_fewer_cuts': 'true',
            'no_mass_window_cut': 'true',
        }
    ),
    # Reference Run 1
    'ref-rdx-ntuple-run1-data-Dst': lambda name: workflow_data(
        name,
        '../ntuples/ref-rdx-run1/Dst-mix/Dst--21_10_21--mix--all--2011-2012--md-mu--phoebe.root',
        '../postprocess/ref-rdx-run1/ref-rdx-run1-Dst.yml',
        use_ubdt=False,
        output_ntp_name_gen=parse_step2_name,
        executor=executor
    ),
    'ref-rdx-ntuple-run1-data-Dst-comp': lambda name: workflow_data(
        name,
        [
            '../ntuples/ref-rdx-run1/Dst-std/Dst--20_09_16--std--data--2011--md--phoebe.root',
            '../ntuples/ref-rdx-run1/Dst-mix/Dst--21_10_21--mix--all--2011-2012--md-mu--phoebe.root',
        ],
        '../postprocess/ref-rdx-run1/ref-rdx-run1-Dst.yml',
        use_ubdt=False,
        output_ntp_name_gen=parse_step2_name,
        executor=executor,
        cli_vars={'cli_fewer_cuts': 'true'}
    ),
    'ref-rdx-ntuple-run1-data-D0': lambda name: workflow_data(
        name,
        '../ntuples/ref-rdx-run1/D0-mix/D0--21_10_21--mix--all--2011-2012--md-mu--phoebe.root',
        '../postprocess/ref-rdx-run1/ref-rdx-run1-D0.yml',
        use_ubdt=False,
        output_ntp_name_gen=parse_step2_name,
        executor=executor
    ),
    'ref-rdx-ntuple-run1-data-D0-comp': lambda name: workflow_data(
        name,
        [
            '../ntuples/ref-rdx-run1/D0-mix/D0--21_10_21--mix--all--2011-2012--md-mu--phoebe.root',
            # '../ntuples/ref-rdx-run1/D0-std/D0--19_09_05--std--data--2012--md--phoebe.root',
        ],
        '../postprocess/ref-rdx-run1/ref-rdx-run1-D0.yml',
        use_ubdt=False,
        output_ntp_name_gen=parse_step2_name,
        executor=executor,
        cli_vars={'cli_fewer_cuts': 'true'}
    ),
}

if args.job_name in JOBS:
    JOBS[args.job_name](args.job_name)
else:
    print('Unknown job name: {}'.format(args.job_name))

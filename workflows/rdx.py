#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Jun 14, 2022 at 01:38 AM -0400

import sys
import os.path as op

from argparse import ArgumentParser
from os import chdir
from functools import partial

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
    keep=[r'^(Dst|D0).*\.root'], blocked=['--aux'])

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
                  **kwargs):
    cmd = f'AddUBDTBranch -i {input_ntp} -o {output_ntp} -t {",".join(trees)}'
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

@smart_kwarg
def workflow_jk(
        input_ntp, output_ntp='jk.root',
        trk_histo_folder='../run2-rdx/reweight/JpsiK/root-run2-JpsiK',
        trk_config='../run2-rdx/reweight/JpsiK/run2-JpsiK.yml',
        **kwargs):
    return workflow_apply_weight(input_ntp, trk_histo_folder, trk_config,
                                 output_ntp, '--aux_jk', **kwargs)

@smart_kwarg
def workflow_misid(
        input_ntp, output_ntp='misid.root',
        misid_aux_ntp='../run2-rdx/reweight/misid/histos/dif.root',
        misid_config='../run2-rdx/reweight/misid/run2-rdx.yml',
        **kwargs):
    aux_ntp = abs_path(misid_aux_ntp)
    config = abs_path(misid_config)
    year = find_year(input_ntp)

    cmd = f'ApplyMisIDWeight -a -i {input_ntp} -o {output_ntp} -x {aux_ntp} -c {config} -Y {year}'
    return workflow_cached_ntuple(
        cmd, input_ntp, output_ntp, '--aux_misid', **kwargs)


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

def workflow_data(inputs, input_yml, job_name='data', use_ubdt=True,
                  use_misid=False, date=None,
                  **kwargs):
    aux_workflows = [workflow_ubdt] if use_ubdt else []
    if use_misid:
        aux_workflows.append(workflow_misid)

    subworkdirs, workdir = workflow_prep_dir(job_name, inputs, **kwargs)
    chdir(workdir)

    for subdir, input_ntp in subworkdirs.items():
        ensure_dir(subdir, make_absolute=False)
        chdir(subdir)  # Switch to the workdir of the subjob

        output_suffix = generate_step2_name(input_ntp, date=date)
        workflow_single_ntuple(
            input_ntp, input_yml, output_suffix, aux_workflows,
            trees=[
                'TupleB0/DecayTree',
                'TupleB0WSMu/DecayTree',
                'TupleB0WSPi/DecayTree',
                'TupleBminus/DecayTree',
                'TupleBminusWS/DecayTree'
            ], **kwargs)

        aggregate_output('..', subdir, rdx_default_output_fltrs)
        chdir('..')  # Switch back to parent workdir


def workflow_mc(inputs, input_yml, job_name='mc', date=None,
                **kwargs):
    aux_workflows = [
        workflow_hammer, workflow_trigger_emu,
        workflow_pid, workflow_trk, workflow_jk,
    ]
    subworkdirs, workdir = workflow_prep_dir(job_name, inputs, **kwargs)
    chdir(workdir)

    for subdir, input_ntp in subworkdirs.items():
        ensure_dir(subdir, make_absolute=False)
        chdir(subdir)  # Switch to the workdir of the subjob

        fields = check_ntp_name(input_ntp)[0]
        if 'decay_mode' in fields:
            decay_mode = fields['decay_mode']
        else:
            decay_mode = find_decay_mode(fields['lfn'])
        blocked_input_trees = rdx_mc_blocked_trees(decay_mode)

        output_suffix = generate_step2_name(input_ntp, date=date)
        # FIXME: Very dirty hack
        if 'cli_vars' not in kwargs:
            kwargs['cli_vars'] = dict()
        kwargs['cli_vars']['cli_mc_id'] = decay_mode

        workflow_single_ntuple(
            input_ntp, input_yml, output_suffix, aux_workflows,
            blocked_input_trees=blocked_input_trees, **kwargs)

        aggregate_output('..', subdir, rdx_default_output_fltrs)
        chdir('..')  # Switch back to parent workdir


def workflow_split(inputs, input_yml, job_name='split', **kwargs):
    return workflow_split_base(
        inputs, input_yml, job_name=job_name, prefix='Dst_D0',
        workflow_data=workflow_data, workflow_mc=workflow_mc,
        **kwargs)


#####################
# Production config #
#####################

JOBS = {
    # Run 2
    'rdx-ntuple-run2-data': partial(
        workflow_split,
        '../ntuples/0.9.6-2016_production/Dst_D0-std',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
    ),
    'rdx-ntuple-run2-data-cut_opt': partial(
        workflow_split,
        '../ntuples/0.9.6-2016_production/Dst_D0-std',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        cli_vars={'cli_cutflow': 'true'}
    ),
    'rdx-ntuple-run2-mu_misid': partial(
        workflow_split,
        '../ntuples/0.9.6-2016_production/Dst_D0-mu_misid',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        cli_vars={'cli_misid': 'true'},
        use_misid=True
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
    'rdx-ntuple-run2-misid_study': partial(
        workflow_split,
        '../ntuples/0.9.6-2016_production/Dst_D0-mu_misid',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        cli_vars={'cli_misid_study': 'true'}
    ),
    # Run 2 debug
    'rdx-ntuple-run2-mu_misid-demo': partial(
        workflow_data,
        '../ntuples/0.9.6-2016_production/Dst_D0-mu_misid/Dst_D0--22_03_01--mu_misid--LHCb_Collision16_Beam6500GeV-VeloClosed-MagDown_Real_Data_Reco16_Stripping28r2_90000000_SEMILEPTONIC.DST/Dst_D0--22_03_01--mu_misid--LHCb_Collision16_Beam6500GeV-VeloClosed-MagDown_Real_Data_Reco16_Stripping28r2_90000000_SEMILEPTONIC.DST--000-dv.root',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        cli_vars={'cli_misid': 'true'},
        use_misid=True
    ),
    'rdx-ntuple-run2-misid_study-demo': partial(
        workflow_data,
        '../ntuples/0.9.6-2016_production/Dst_D0-mu_misid/Dst_D0--22_03_01--mu_misid--LHCb_Collision16_Beam6500GeV-VeloClosed-MagDown_Real_Data_Reco16_Stripping28r2_90000000_SEMILEPTONIC.DST/Dst_D0--22_03_01--mu_misid--LHCb_Collision16_Beam6500GeV-VeloClosed-MagDown_Real_Data_Reco16_Stripping28r2_90000000_SEMILEPTONIC.DST--000-dv.root',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        cli_vars={'cli_misid_study': 'true'}
    ),
    'rdx-ntuple-run2-data-demo': partial(
        workflow_data,
        '../ntuples/0.9.6-2016_production/Dst_D0-std/Dst_D0--22_02_07--std--LHCb_Collision16_Beam6500GeV-VeloClosed-MagDown_Real_Data_Reco16_Stripping28r2_90000000_SEMILEPTONIC.DST/Dst_D0--22_02_07--std--LHCb_Collision16_Beam6500GeV-VeloClosed-MagDown_Real_Data_Reco16_Stripping28r2_90000000_SEMILEPTONIC.DST--000-dv.root',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
    ),
    'rdx-ntuple-run2-data-debug': partial(
        workflow_data,
        '../ntuples/0.9.5-bugfix/Dst_D0-cutflow_data',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        cli_vars={'cli_cutflow': 'true'},
        directive_override={'one_cand_only/enable': 'false'}
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
    'rdx-ntuple-run2-mc-demo': partial(
        workflow_mc,
        '../ntuples/0.9.5-bugfix/Dst_D0-mc/Dst_D0--21_10_08--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574011_D0TAUNU.SAFESTRIPTRIG.DST.root',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
    ),
    'rdx-ntuple-run2-mc-demo-ddx': partial(
        workflow_mc,
        '../ntuples/0.9.5-bugfix/Dst_D0-mc/Dst_D0--21_10_26--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11894600_D0TAUNU.SAFESTRIPTRIG.DST.root',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
    ),
    'rdx-ntuple-run2-mc-to-demo': partial(
        workflow_split,
        '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/Dst_D0--21_10_26--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_11894600_D0TAUNU.SAFESTRIPTRIG.DST',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
        blocked_patterns=['--aux', r'--([1-9][0-9][0-9]|0[1-9][0-9])-dv']
    ),
    'rdx-ntuple-run2-mc-dss': partial(
        workflow_mc,
        '../ntuples/0.9.5-bugfix/Dst_D0-mc/Dst_D0--21_10_15--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11874430_D0TAUNU.SAFESTRIPTRIG.DST.root',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
    ),
    'rdx-ntuple-run2-mc-sub': partial(
        workflow_split,
        '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/Dst_D0--22_02_24--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_12773410_D0TAUNU.SAFESTRIPTRIG.DST',
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
    ),
    'rdx-ntuple-run2-mc-to-sig-norm': partial(
        workflow_split,
        [
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573010*',
            '../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/*12573000*',
        ],
        '../postprocess/rdx-run2/rdx-run2_oldcut.yml',
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
        '../ntuples/0.9.5-bugfix/Dst_D0-std/Dst_D0--21_10_07--std--LHCb_Collision11_Beam3500GeV-VeloClosed-MagDown_Real_Data_Reco14_Stripping21r1_90000000_SEMILEPTONIC.DST.root',
        '../postprocess/ref-rdx-run1/ref-rdx-run1-D0.yml',
        use_ubdt=False,
        cli_vars={
            'cli_fewer_cuts': 'true',
            'no_mass_window_cut': 'true',
        }
    ),
    'rdx-ntuple-run1-data-Dst-comp': partial(
        workflow_data,
        '../ntuples/0.9.5-bugfix/Dst_D0-std/Dst_D0--21_10_07--std--LHCb_Collision11_Beam3500GeV-VeloClosed-MagDown_Real_Data_Reco14_Stripping21r1_90000000_SEMILEPTONIC.DST.root',
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
    args = parse_input()

    if args.job_name in JOBS:
        JOBS[args.job_name](job_name=args.job_name, debug=args.debug)
    else:
        print('Unknown job name: {}'.format(args.job_name))

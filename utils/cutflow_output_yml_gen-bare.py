#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Jun 11, 2020 at 10:20 PM +0800

import uproot
import sys

sys.path.insert(0, '../../utils')

from yaml import safe_load
from argparse import ArgumentParser
from davinci_log_parser import yaml_gen
from pyTuplingUtils.utils import extract_uid
from pyTuplingUtils.cutflow import CutflowGen, CutflowRule as Rule
from pyTuplingUtils.io import read_branch


ALIASES = {
    'SeqMyB0': 'Total events',
    'StrippedBCands': r'Stripped $D^0 \mu^-$',
    'SelMyD0': r'$D^0 \rightarrow K^- \pi^+$ (tighter $K \pi$)',
    'SelMyDst': r'$D^{*+} \rightarrow D^0 \pi^+$',
    'SelMyB0': r'$\bar{B}^0 \rightarrow D^{*+} \mu^-$',
    'SelMyRefitB02DstMu': r'Refit $\bar{B}^0$ decay tree',
}

CUTFLOW_STEP1 = {
    'run1': [
        Rule('mu_L0Global_TIS & (b0_L0Global_TIS | dst_L0HadronDecision_TOS)', key='L0'),
        Rule('k_Hlt1TrackAllL0Decision_TOS | pi_Hlt1TrackAllL0Decision_TOS', key='Hlt1'),
        Rule('d0_Hlt2CharmHadD02HH_D02KPiDecision_TOS', key='Hlt2'),
    ],
    'run2': [
        Rule('mu_L0Global_TIS & (b0_L0Global_TIS | dst_L0HadronDecision_TOS)', key='L0'),
        Rule('k_Hlt1Phys_Dec', key='Hlt1'),
        Rule('d0_Hlt2XcMuXForTauB2XcMuDecision_Dec', key='Hlt2'),
    ]
}

CUTFLOW_STEP2 = [
    Rule('mu_is_mu & mu_pid_mu > 2', r'$\mu$ PID'),
    Rule('iso_bdt < 0.15', r'$\text{IsoBDT}_{\Upsilon(\text{4s})} < 0.15$'),
    Rule('b0_m < 5280', r'$m_{\Upsilon(\text{4s})} < 5280$'),
]


################################
# Command line argument parser #
################################

def parse_input(descr='Generate cutflow output YAML based on input ntuple and YAML.'):
    parser = ArgumentParser(description=descr)

    parser.add_argument('ntp_step1',
                        help='specify step 1 ntuple path.')

    parser.add_argument('ntp_step2',
                        help='specify step 2 ntuple path.')

    parser.add_argument('input_yml',
                        help='specify input YAML path.')

    parser.add_argument('output_yml',
                        help='specify output YAML path.')

    parser.add_argument('mode',
                        help='specify mode.')

    parser.add_argument('-t1', '--tree1',
                        default='TupleB0/DecayTree',
                        help='specify tree name in the step 1 ntuple.'
                        )

    parser.add_argument('-t2', '--tree2',
                        default='b0dst',
                        help='specify tree name in the step 2 ntuple.'
                        )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_input()

    _, _, total_size, uniq_size, _ = extract_uid(
        uproot.open(args.ntp_step1), args.tree1)

    with open(args.input_yml) as f:
        result = safe_load(f)

    for cut, val in result.items():
        if cut in ALIASES:
            val['name'] = ALIASES[cut]
        if val['output'] is None:
            val['output'] = uniq_size

    result_addon_step1 = CutflowGen(
        args.ntp_step1, args.tree1, CUTFLOW_STEP1[args.mode], total_size).do()
    for k, v in result_addon_step1.items():
        cand_before_restripping = v['output']

    cand_after_restripping = read_branch(
        uproot.open(args.ntp_step2), args.tree2, 'runNumber').size
    result_addon_step1['Stripping'] = {
        'input': cand_before_restripping,
        'output': cand_after_restripping
    }

    result_addon_step2 = CutflowGen(
        args.ntp_step2, args.tree2, CUTFLOW_STEP2, cand_after_restripping).do()

    result.update(result_addon_step1)
    result.update(result_addon_step2)

    with open(args.output_yml, 'w') as f:
        f.write(yaml_gen(result))

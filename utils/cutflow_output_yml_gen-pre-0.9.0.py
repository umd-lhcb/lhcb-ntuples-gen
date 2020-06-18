#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Jun 18, 2020 at 09:13 PM +0800

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
    'SelMyD0': r'$D^0 \rightarrow K^- \pi^+$ (tighter $K\pi$)',
    'SelMyDst': r'$D^{*+} \rightarrow D^0 \pi^+$',
    'SelMyB0': r'$\bar{B}^0 \rightarrow D^{*+} \mu^-$',
    'SelMyRefitB02DstMu': r'Refit $\bar{B}^0$ decay tree',
}

CUTFLOW = {
    'run1': [
        # Trigger
        Rule('muplus_L0Global_TIS & (Y_L0Global_TIS | Dst_2010_minus_L0HadronDecision_TOS)', key='L0'),
        Rule('Kplus_Hlt1TrackAllL0Decision_TOS | piminus0_Hlt1TrackAllL0Decision_TOS', key='Hlt1'),
        Rule('D0_Hlt2CharmHadD02HH_D02KPiDecision_TOS', key='Hlt2'),
        # Step 2
        Rule('muplus_isMuon & muplus_PIDmu > 2 & muplus_PIDe < 1 & muplus_P < 100.0*GeV', r'$\mu$ PID'),
        Rule('Y_ISOLATION_BDT < 0.15', r'$\text{IsoBDT}_{B^0} < 0.15$'),
        Rule('Y_MM < 5280 & Y_DIRA_OWNPV > 0.9995', r'$B^0$ cuts'),
        # Newer step 2 cuts
        Rule('Kplus_PT > 800.0*MeV & !Kplus_isMuon & Kplus_IPCHI2_OWNPV > 45', r'$K$ cuts'),
        Rule('piminus0_PT > 800.0*MeV & !piminus0_isMuon & piminus0_IPCHI2_OWNPV > 45', r'$\pi$ cuts'),
        Rule('piminus_TRACK_GhostProb < 0.5', r'$\pi_{soft}$ cuts'),
        Rule('D0_P > 2.0*GeV & D0_DIRA_OWNPV > 0.9998 & D0_FDCHI2_OWNPV > 250 & ABS(D0_MM - PDG_M_D0) < 23.4 & (Kplus_PT > 1.7*GeV | piminus0_PT > 1.7*GeV)', r'$D^0$ cuts'),
        Rule('Dst_2010_minus_ENDVERTEX_CHI2 / Dst_2010_minus_ENDVERTEX_NDOF < 10 & ABS(Dst_2010_minus_MM - D0_MM - 145.43) < 2', r'$D^*$ cuts'),
    ],
    'run2': [
        # Trigger
        Rule('muplus_L0Global_TIS & (Y_L0Global_TIS | Dst_2010_minus_L0HadronDecision_TOS)', key='L0'),
        Rule('Kplus_Hlt1Phys_Dec', key='Hlt1'),
        Rule('D0_Hlt2XcMuXForTauB2XcMuDecision_Dec', key='Hlt2'),
        # Step 2
        Rule('muplus_isMuon & muplus_PIDmu > 2 & muplus_PIDe < 1 & muplus_P < 100.0*GeV', r'$\mu$ PID'),
        Rule('Y_ISOLATION_BDT < 0.15', r'$\text{IsoBDT}_{B^0} < 0.15$'),
        Rule('Y_MM < 5280 & Y_DIRA_OWNPV > 0.9995', r'$B^0$ cuts'),
        # Newer step 2 cuts
        Rule('Kplus_PT > 800.0*MeV & !Kplus_isMuon & Kplus_IPCHI2_OWNPV > 45', r'$K$ cuts'),
        Rule('piminus0_PT > 800.0*MeV & !piminus0_isMuon & piminus0_IPCHI2_OWNPV > 45', r'$\pi$ cuts'),
        Rule('piminus_TRACK_GhostProb < 0.5', r'$\pi_{soft}$ cuts'),
        Rule('D0_P > 2.0*GeV & D0_DIRA_OWNPV > 0.9998 & D0_FDCHI2_OWNPV > 250 & ABS(D0_MM - PDG_M_D0) < 23.4 & (Kplus_PT > 1.7*GeV | piminus0_PT > 1.7*GeV)', r'$D^0$ cuts'),
        Rule('Dst_2010_minus_ENDVERTEX_CHI2 / Dst_2010_minus_ENDVERTEX_NDOF < 10 & ABS(Dst_2010_minus_MM - D0_MM - 145.43) < 2', r'$D^*$ cuts'),
    ]
}


################################
# Command line argument parser #
################################

def parse_input(descr='Generate cutflow output YAML based on input ntuple and YAML.'):
    parser = ArgumentParser(description=descr)

    parser.add_argument('ntp',
                        help='specify input ntuple path.')

    parser.add_argument('input_yml',
                        help='specify input YAML path.')

    parser.add_argument('output_yml',
                        help='specify output YAML path.')

    parser.add_argument('mode',
                        help='specify mode.')

    parser.add_argument('-t', '--tree',
                        default='TupleB0/DecayTree',
                        help='specify tree name in the input ntuple.'
                        )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_input()
    _, _, _, uniq_size, _ = extract_uid(uproot.open(args.ntp), args.tree)

    with open(args.input_yml) as f:
        result = safe_load(f)

    for cut, val in result.items():
        if cut in ALIASES:
            val['name'] = ALIASES[cut]
        if val['output'] is None:
            val['output'] = uniq_size

    result_addon = CutflowGen(
        args.ntp, args.tree, CUTFLOW[args.mode], uniq_size).do()
    result.update(result_addon)

    with open(args.output_yml, 'w') as f:
        f.write(yaml_gen(result))

#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Jun 24, 2020 at 09:32 PM +0800

import uproot
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from yaml import safe_load
from argparse import ArgumentParser
from davinci_log_parser import yaml_gen
from pyTuplingUtils.utils import extract_uid
from pyTuplingUtils.cutflow import CutflowGen, CutflowRule as Rule
from pyTuplingUtils.cutflow import cutflow_uniq_events_outer


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
        # Newer step 2 cuts
        Rule('Kplus_PT > 800.0*MeV & !Kplus_isMuon & Kplus_IPCHI2_OWNPV > 45', r'Kaon'),
        Rule('piminus0_PT > 800.0*MeV & !piminus0_isMuon & piminus0_IPCHI2_OWNPV > 45', r'Pion'),
        Rule('D0_P > 2.0*GeV & D0_FDCHI2_OWNPV > 250 & ABS(D0_MM - PDG_M_D0) < 23.4 & ((Kplus_PT > 1.7*GeV & Kplus_Hlt1TrackAllL0Decision_TOS) | (piminus0_PT > 1.7*GeV & piminus0_Hlt1TrackAllL0Decision_TOS)) & log(D0_IP_OWNPV) > -3.5 & D0_IPCHI2_OWNPV > 9', r'$D^0 \\rightarrow K \\pi$'),
        Rule('muplus_isMuon & muplus_PIDmu > 2 & muplus_PIDe < 1 & muplus_P < 100.0*GeV & ETA(muplus_P,muplus_PZ)>1.7 & ETA(muplus_P,muplus_PZ)<5 & LOG10pp(muplus_PX, muplus_PY, muplus_PZ, Kplus_PX, Kplus_PY, Kplus_PZ)>-6.5 & LOG10pp(muplus_PX, muplus_PY, muplus_PZ, piminus0_PX, piminus0_PY, piminus0_PZ)>-6.5 & LOG10pp(muplus_PX, muplus_PY, muplus_PZ, piminus_PX, piminus_PY, piminus_PZ)>-6.5', r'$\mu$'),
        Rule('piminus_TRACK_GhostProb < 0.25 & Dst_2010_minus_ENDVERTEX_CHI2 / Dst_2010_minus_ENDVERTEX_NDOF < 10 & ABS(Dst_2010_minus_MM - D0_MM - 145.43) < 2', r'$D^{*+} \rightarrow D^0 \pi$'),
        Rule('Y_ISOLATION_BDT < 0.15 & (Y_ENDVERTEX_CHI2/Y_ENDVERTEX_NDOF) < 6 & Y_MM<5280 & Y_DIRA_OWNPV>0.9995 & sin(Y_FlightDir_Zangle)*Y_FD_OWNPV < 7', r'$B^0 \rightarrow D^{*+} \mu$')
    ],
    'run2': [
        # Trigger
        Rule('muplus_L0Global_TIS & (Y_L0Global_TIS | Dst_2010_minus_L0HadronDecision_TOS)', key='L0'),
        Rule('Kplus_Hlt1TrackMVALooseDecision_TOS | piminus0_Hlt1TrackMVALooseDecision_TOS  | D0_Hlt1TwoTrackMVADecision_TOS', key='Hlt1'),
        Rule('D0_Hlt2XcMuXForTauB2XcMuDecision_Dec', key='Hlt2'),
        # Newer step 2 cuts
        Rule('Kplus_PT > 800.0*MeV & !Kplus_isMuon & Kplus_IPCHI2_OWNPV > 45', r'Kaon'),
        Rule('piminus0_PT > 800.0*MeV & !piminus0_isMuon & piminus0_IPCHI2_OWNPV > 45', r'Pion'),
        Rule('D0_P > 2.0*GeV & D0_FDCHI2_OWNPV > 250 & ABS(D0_MM - PDG_M_D0) < 23.4 & ((Kplus_PT > 1.7*GeV & Kplus_Hlt1TrackMVALooseDecision_TOS) | (piminus0_PT > 1.7*GeV & piminus0_Hlt1TrackMVALooseDecision_TOS)) & log(D0_IP_OWNPV) > -3.5 & D0_IPCHI2_OWNPV > 9', r'$D^0 \\rightarrow K \\pi$'),
        Rule('muplus_isMuon & muplus_PIDmu > 2 & muplus_PIDe < 1 & muplus_P < 100.0*GeV & ETA(muplus_P,muplus_PZ)>1.7 & ETA(muplus_P,muplus_PZ)<5 & LOG10pp(muplus_PX, muplus_PY, muplus_PZ, Kplus_PX, Kplus_PY, Kplus_PZ)>-6.5 & LOG10pp(muplus_PX, muplus_PY, muplus_PZ, piminus0_PX, piminus0_PY, piminus0_PZ)>-6.5 & LOG10pp(muplus_PX, muplus_PY, muplus_PZ, piminus_PX, piminus_PY, piminus_PZ)>-6.5', r'$\mu$'),
        Rule('piminus_TRACK_GhostProb < 0.25 & Dst_2010_minus_ENDVERTEX_CHI2 / Dst_2010_minus_ENDVERTEX_NDOF < 10 & ABS(Dst_2010_minus_MM - D0_MM - 145.43) < 2', r'$D^{*+} \rightarrow D^0 \pi$'),
        Rule('Y_ISOLATION_BDT < 0.15 & (Y_ENDVERTEX_CHI2/Y_ENDVERTEX_NDOF) < 6 & Y_MM<5280 & Y_DIRA_OWNPV>0.9995 & sin(Y_FlightDir_Zangle)*Y_FD_OWNPV < 7', r'$B^0 \rightarrow D^{*+} \mu$')
    ],
    'run2-data': [
        # Trigger
        Rule('muplus_L0Global_TIS & (Y_L0Global_TIS | Dst_2010_minus_L0HadronDecision_TOS)', key='L0'),
        Rule('Kplus_Hlt1Phys_Dec', key='Hlt1'),
        Rule('D0_Hlt2XcMuXForTauB2XcMuDecision_Dec', key='Hlt2'),
        # Newer step 2 cuts
        Rule('Kplus_PT > 800.0*MeV & !Kplus_isMuon & Kplus_IPCHI2_OWNPV > 45', r'Kaon'),
        Rule('piminus0_PT > 800.0*MeV & !piminus0_isMuon & piminus0_IPCHI2_OWNPV > 45', r'Pion'),
        Rule('D0_P > 2.0*GeV & D0_FDCHI2_OWNPV > 250 & ABS(D0_MM - PDG_M_D0) < 23.4 & (Kplus_PT > 1.7*GeV | piminus0_PT > 1.7*GeV) & log(D0_IP_OWNPV) > -3.5 & D0_IPCHI2_OWNPV > 9', r'$D^0 \\rightarrow K \\pi$'),
        Rule('muplus_isMuon & muplus_PIDmu > 2 & muplus_PIDe < 1 & muplus_P < 100.0*GeV & ETA(muplus_P,muplus_PZ)>1.7 & ETA(muplus_P,muplus_PZ)<5 & LOG10pp(muplus_PX, muplus_PY, muplus_PZ, Kplus_PX, Kplus_PY, Kplus_PZ)>-6.5 & LOG10pp(muplus_PX, muplus_PY, muplus_PZ, piminus0_PX, piminus0_PY, piminus0_PZ)>-6.5 & LOG10pp(muplus_PX, muplus_PY, muplus_PZ, piminus_PX, piminus_PY, piminus_PZ)>-6.5', r'$\mu$'),
        Rule('piminus_TRACK_GhostProb < 0.25 & Dst_2010_minus_ENDVERTEX_CHI2 / Dst_2010_minus_ENDVERTEX_NDOF < 10 & ABS(Dst_2010_minus_MM - D0_MM - 145.43) < 2', r'$D^{*+} \rightarrow D^0 \pi$'),
        Rule('Y_ISOLATION_BDT < 0.15 & (Y_ENDVERTEX_CHI2/Y_ENDVERTEX_NDOF) < 6 & Y_MM<5280 & Y_DIRA_OWNPV>0.9995 & sin(Y_FlightDir_Zangle)*Y_FD_OWNPV < 7', r'$B^0 \rightarrow D^{*+} \mu$')
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
    ntp = uproot.open(args.ntp)
    _, _, _, uniq_size, _ = extract_uid(ntp, args.tree)

    with open(args.input_yml) as f:
        result = safe_load(f)

    for cut, val in result.items():
        if cut in ALIASES:
            val['name'] = ALIASES[cut]
        if val['output'] is None:
            val['output'] = uniq_size

    cutflow_output_regulator = cutflow_uniq_events_outer(ntp, args.tree)

    result_addon = CutflowGen(
        args.ntp, args.tree, CUTFLOW[args.mode], uniq_size).do(
            output_regulator=cutflow_output_regulator)
    result.update(result_addon)

    with open(args.output_yml, 'w') as f:
        f.write(yaml_gen(result))

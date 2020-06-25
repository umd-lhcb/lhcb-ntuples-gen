#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Jun 24, 2020 at 09:26 PM +0800

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
    'SelMyD0': r'$D^0 \rightarrow K^- \pi^+$',
    'SelMyDst': r'$D^{*+} \rightarrow D^0 \pi^+$',
    'SelMyB0': r'$\bar{B}^0 \rightarrow D^{*+} \mu^-$',
    'SelMyRefitB02DstMu': r'Refit $\bar{B}^0$ decay tree',
}

CUTFLOW = {
    'run1-bare': [
        # Trigger
        Rule('mu_L0Global_TIS & (b0_L0Global_TIS | dst_L0HadronDecision_TOS)', key='L0'),
        Rule('k_Hlt1TrackAllL0Decision_TOS | pi_Hlt1TrackAllL0Decision_TOS', key='Hlt1'),
        Rule('d0_Hlt2CharmHadD02HH_D02KPiDecision_TOS', key='Hlt2'),
        # Stripping
        Rule('(mu_IPCHI2_OWNPV > 45.0) & (mu_TRACK_GhostProb < 0.5) & (mu_PIDmu > 2.0) & (mu_P > 3.0*GeV) & (mu_TRACK_CHI2NDOF < 3.0) & (k_PIDK > 4.0) & (k_IPCHI2_OWNPV > 45.0) & (k_P > 2.0*GeV) & (k_PT > 300.0*MeV) & (k_TRACK_GhostProb < 0.5) & (pi_P > 2.0*GeV) & (pi_PT > 300.0*MeV) & (pi_IPCHI2_OWNPV > 45.0) & (pi_PIDK < 2.0) & (pi_TRACK_GhostProb < 0.5) & (spi_IPCHI2_OWNPV > 0.0) & (spi_TRACK_CHI2NDOF < 3.0) & (spi_TRACK_GhostProb < 0.25) & (k_PT + pi_PT > 1400.0*MeV) & (ABS(d0_MM - PDG_M_D0) < 80.0*MeV) & (d0_ENDVERTEX_CHI2 / d0_ENDVERTEX_NDOF < 4.0) & (d0_FDCHI2_OWNPV > 250.0) & (d0_DIRA_OWNPV > 0.9998) & (ABS(dst_MM - PDG_M_Dst) < 125.0*MeV) & (dst_M - d0_M < 160.0*MeV) & (dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 100.0) & (0.0*GeV < b0_MM < 10.0*GeV) & (b0_ENDVERTEX_CHI2 / b0_ENDVERTEX_NDOF < 6.0) & (b0_DIRA_OWNPV > 0.9995)',
             key='Stripping (partial)'),
        # Newer step 2 cuts
        Rule('k_PT > 800.0*MeV & !k_isMuon & k_IPCHI2_OWNPV > 45', r'Kaon'),
        Rule('pi_PT > 800.0*MeV & !pi_isMuon & pi_IPCHI2_OWNPV > 45', r'Pion'),
        Rule('d0_P > 2.0*GeV & d0_FDCHI2_OWNPV > 250 & ABS(d0_MM - PDG_M_D0) < 23.4 & (k_PT > 1.7*GeV | pi_PT > 1.7*GeV)', r'$D^0 \\rightarrow K \\pi$'),
        Rule('mu_isMuon & mu_PIDmu > 2 & mu_PIDe < 1 & mu_P < 100.0*GeV', r'$\mu$'),
        Rule('spi_TRACK_GhostProb < 0.5', r'$\pi_{soft}$'),
        Rule('dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 10 & ABS(dst_MM - d0_MM - 145.43) < 2', r'$D^*$'),
        Rule('b0_ISOLATION_BDT < 0.15 & (b0_ENDVERTEX_CHI2/b0_ENDVERTEX_NDOF) < 6 & b0_MM<5280 & b0_DIRA_OWNPV>0.9995', r'$B^0$')
    ],
    'run2-bare': [
        # Trigger
        Rule('mu_L0Global_TIS & (b0_L0Global_TIS | dst_L0HadronDecision_TOS)', key='L0'),
        Rule('k_Hlt1TrackMVALooseDecision_TOS | pi_Hlt1TrackMVALooseDecision_TOS  | d0_Hlt1TwoTrackMVADecision_TOS', key='Hlt1'),
        Rule('d0_Hlt2XcMuXForTauB2XcMuDecision_Dec', key='Hlt2'),
        # Stripping
        Rule('(mu_IPCHI2_OWNPV > 16.0) & (mu_TRACK_GhostProb < 0.5) & (mu_PIDmu > -200.0) & (mu_P > 3.0*GeV) & (mu_TRACK_CHI2NDOF < 3.0) & (k_PIDK > 4.0) & (k_IPCHI2_OWNPV > 9.0) & (k_P > 2.0*GeV) & (k_PT > 300.0*MeV) & (k_TRACK_GhostProb < 0.5) & (pi_P > 2.0*GeV) & (pi_PT > 300.0*MeV) & (pi_IPCHI2_OWNPV > 9.0) & (pi_PIDK < 2.0) & (pi_TRACK_GhostProb < 0.5) & (spi_IPCHI2_OWNPV > 0.0) & (spi_TRACK_CHI2NDOF < 3.0) & (spi_TRACK_GhostProb < 0.25) & (k_PT + pi_PT > 2500.0*MeV) & (ABS(d0_MM - PDG_M_D0) < 80.0*MeV) & (d0_ENDVERTEX_CHI2 / d0_ENDVERTEX_NDOF < 4.0) & (d0_FDCHI2_OWNPV > 25.0) & (d0_DIRA_OWNPV > 0.999) & (ABS(dst_MM - PDG_M_Dst) < 125.0*MeV) & (dst_M - d0_M < 160.0*MeV) & (dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 100.0) & (0.0*GeV < b0_MM < 10.0*GeV) & (b0_ENDVERTEX_CHI2 / b0_ENDVERTEX_NDOF < 6.0) & (b0_DIRA_OWNPV > 0.999)',
             key='Stripping (partial)'),
        # Newer step 2 cuts
        Rule('k_PT > 800.0*MeV & !k_isMuon & k_IPCHI2_OWNPV > 45', r'Kaon'),
        Rule('pi_PT > 800.0*MeV & !pi_isMuon & pi_IPCHI2_OWNPV > 45', r'Pion'),
        Rule('d0_P > 2.0*GeV & d0_FDCHI2_OWNPV > 250 & ABS(d0_MM - PDG_M_D0) < 23.4 & (k_PT > 1.7*GeV | pi_PT > 1.7*GeV)', r'$D^0 \\rightarrow K \\pi$'),
        Rule('mu_isMuon & mu_PIDmu > 2 & mu_PIDe < 1 & mu_P < 100.0*GeV', r'$\mu$'),
        Rule('spi_TRACK_GhostProb < 0.5', r'$\pi_{soft}$'),
        Rule('dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 10 & ABS(dst_MM - d0_MM - 145.43) < 2', r'$D^*$'),
        Rule('b0_ISOLATION_BDT < 0.15 & (b0_ENDVERTEX_CHI2/b0_ENDVERTEX_NDOF) < 6 & b0_MM<5280 & b0_DIRA_OWNPV>0.9995', r'$B^0$')
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

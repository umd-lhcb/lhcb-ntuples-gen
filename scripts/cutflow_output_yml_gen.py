#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon May 24, 2021 at 03:10 AM +0200

import uproot

from yaml import safe_load
from argparse import ArgumentParser
from collections import OrderedDict as odict

from pyTuplingUtils.utils import extract_uid
from pyTuplingUtils.cutflow import CutflowGen, CutflowRule as Rule
from pyTuplingUtils.cutflow import cutflow_uniq_events_outer


ALIASES = {
    'run1-Dst-bare': {
        'SELECT:Phys/StdAllNoPIDsKaons': 'Total events',
        'SelMyB-': r'Relaxed $D^0 \mu$ cands',
        'SelMyDst': r'$D^{*+} \rightarrow D^0 \pi^+$',
        'SelMyB0': r'$\bar{B}^0 \rightarrow D^{*+} \mu^-$',
    }
}

CUTFLOW = {
    'run1-Dst-bare': [
        # Trigger
        Rule('mu_L0Global_TIS & (b0_L0Global_TIS | dst_L0HadronDecision_TOS)', key='L0'),
        Rule('k_Hlt1TrackAllL0Decision_TOS | pi_Hlt1TrackAllL0Decision_TOS', key='Hlt1'),
        Rule('d0_Hlt2CharmHadD02HH_D02KPiDecision_TOS', key='Hlt2'),
        # Stripping
        Rule('(mu_IPCHI2_OWNPV > 45.0) & (mu_TRACK_GhostProb < 0.5) & (mu_PIDmu > 2.0) & (mu_P > 3.0*GeV) & (mu_TRACK_CHI2NDOF < 3.0) & (k_PIDK > 4.0) & (k_IPCHI2_OWNPV > 45.0) & (k_P > 2.0*GeV) & (k_PT > 300.0*MeV) & (k_TRACK_GhostProb < 0.5) & (pi_P > 2.0*GeV) & (pi_PT > 300.0*MeV) & (pi_IPCHI2_OWNPV > 45.0) & (pi_PIDK < 2.0) & (pi_TRACK_GhostProb < 0.5) & (spi_IPCHI2_OWNPV > 0.0) & (spi_TRACK_CHI2NDOF < 3.0) & (spi_TRACK_GhostProb < 0.25) & (k_PT + pi_PT > 1400.0*MeV) & (abs(d0_MM - PDG_M_D0) < 80.0*MeV) & (d0_ENDVERTEX_CHI2 / d0_ENDVERTEX_NDOF < 4.0) & (d0_FDCHI2_OWNPV > 250.0) & (d0_DIRA_OWNPV > 0.9998) & (abs(dst_MM - PDG_M_Dst) < 125.0*MeV) & (dst_M - d0_M < 160.0*MeV) & (dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 100.0) & (0.0*GeV < b0_MM < 10.0*GeV) & (b0_ENDVERTEX_CHI2 / b0_ENDVERTEX_NDOF < 6.0) & (b0_DIRA_OWNPV > 0.9995)',
             key='Stripping (partial)'),
        # Newer step 2 cuts
        # Rule('k_PT > 800.0*MeV & !k_isMuon & k_IPCHI2_OWNPV > 45', r'Kaon'),
        # Rule('pi_PT > 800.0*MeV & !pi_isMuon & pi_IPCHI2_OWNPV > 45', r'Pion'),
        # Rule('d0_P > 2.0*GeV & d0_FDCHI2_OWNPV > 250 & abs(d0_MM - PDG_M_D0) < 23.4 & ((k_PT > 1.7*GeV & k_Hlt1TrackAllL0Decision_TOS) | (pi_PT > 1.7*GeV & pi_Hlt1TrackAllL0Decision_TOS)) & log(d0_IP_OWNPV) > -3.5 & d0_IPCHI2_OWNPV > 9', r'$D^0 \\rightarrow K \\pi$'),
        # Rule('mu_isMuon & mu_PIDmu > 2 & mu_PIDe < 1 & mu_P < 100.0*GeV & ETA(mu_P,mu_PZ)>1.7 & ETA(mu_P,mu_PZ)<5 & LOG10pp(mu_PX, mu_PY, mu_PZ, k_PX, k_PY, k_PZ)>-6.5 & LOG10pp(mu_PX, mu_PY, mu_PZ, pi_PX, pi_PY, pi_PZ)>-6.5 & LOG10pp(mu_PX, mu_PY, mu_PZ, pi_PX, pi_PY, pi_PZ)>-6.5', r'$\mu$'),
        # Rule('spi_TRACK_GhostProb < 0.25 & dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 10 & abs(dst_MM - d0_MM - 145.43) < 2', r'$D^{*+} \rightarrow D^0 \pi$'),
        # Rule('b0_ISOLATION_BDT < 0.15 & (b0_ENDVERTEX_CHI2/b0_ENDVERTEX_NDOF) < 6 & b0_MM<5280 & b0_DIRA_OWNPV>0.9995 & sin(b0_FlightDir_Zangle)*b0_FD_OWNPV < 7', r'$B^0 \rightarrow D^{*+} \mu$')
    ],
    'run2-bare': [
        # Trigger
        Rule('mu_L0Global_TIS & (b0_L0Global_TIS | dst_L0HadronDecision_TOS)', key='L0'),
        Rule('k_Hlt1TrackMVALooseDecision_TOS | pi_Hlt1TrackMVALooseDecision_TOS  | d0_Hlt1TwoTrackMVADecision_TOS', key='Hlt1'),
        Rule('d0_Hlt2XcMuXForTauB2XcMuDecision_Dec', key='Hlt2'),
        # Stripping
        Rule('(mu_IPCHI2_OWNPV > 16.0) & (mu_TRACK_GhostProb < 0.5) & (mu_PIDmu > -200.0) & (mu_P > 3.0*GeV) & (mu_TRACK_CHI2NDOF < 3.0) & (k_PIDK > 4.0) & (k_IPCHI2_OWNPV > 9.0) & (k_P > 2.0*GeV) & (k_PT > 300.0*MeV) & (k_TRACK_GhostProb < 0.5) & (pi_P > 2.0*GeV) & (pi_PT > 300.0*MeV) & (pi_IPCHI2_OWNPV > 9.0) & (pi_PIDK < 2.0) & (pi_TRACK_GhostProb < 0.5) & (spi_IPCHI2_OWNPV > 0.0) & (spi_TRACK_CHI2NDOF < 3.0) & (spi_TRACK_GhostProb < 0.25) & (k_PT + pi_PT > 2500.0*MeV) & (abs(d0_MM - PDG_M_D0) < 80.0*MeV) & (d0_ENDVERTEX_CHI2 / d0_ENDVERTEX_NDOF < 4.0) & (d0_FDCHI2_OWNPV > 25.0) & (d0_DIRA_OWNPV > 0.999) & (abs(dst_MM - PDG_M_Dst) < 125.0*MeV) & (dst_M - d0_M < 160.0*MeV) & (dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 100.0) & (0.0*GeV < b0_MM < 10.0*GeV) & (b0_ENDVERTEX_CHI2 / b0_ENDVERTEX_NDOF < 6.0) & (b0_DIRA_OWNPV > 0.999)',
             key='Stripping (partial)'),
        # Newer step 2 cuts
        Rule('k_PT > 800.0*MeV & !k_isMuon & k_IPCHI2_OWNPV > 45', r'Kaon'),
        Rule('pi_PT > 800.0*MeV & !pi_isMuon & pi_IPCHI2_OWNPV > 45', r'Pion'),
        Rule('d0_P > 2.0*GeV & d0_FDCHI2_OWNPV > 250 & abs(d0_MM - PDG_M_D0) < 23.4 & ((k_PT > 1.7*GeV & k_Hlt1TrackMVALooseDecision_TOS) | (pi_PT > 1.7*GeV & pi_Hlt1TrackMVALooseDecision_TOS)) & log(d0_IP_OWNPV) > -3.5 & d0_IPCHI2_OWNPV > 9', r'$D^0 \\rightarrow K \\pi$'),
        Rule('mu_isMuon & mu_PIDmu > 2 & mu_PIDe < 1 & mu_P < 100.0*GeV & ETA(mu_P,mu_PZ)>1.7 & ETA(mu_P,mu_PZ)<5 & LOG10pp(mu_PX, mu_PY, mu_PZ, k_PX, k_PY, k_PZ)>-6.5 & LOG10pp(mu_PX, mu_PY, mu_PZ, pi_PX, pi_PY, pi_PZ)>-6.5 & LOG10pp(mu_PX, mu_PY, mu_PZ, pi_PX, pi_PY, pi_PZ)>-6.5', r'$\mu$'),
        Rule('spi_TRACK_GhostProb < 0.25 & dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 10 & abs(dst_MM - d0_MM - 145.43) < 2', r'$D^{*+} \rightarrow D^0 \pi$'),
        Rule('b0_ISOLATION_BDT < 0.15 & (b0_ENDVERTEX_CHI2/b0_ENDVERTEX_NDOF) < 6 & b0_MM<5280 & b0_DIRA_OWNPV>0.9995 & sin(b0_FlightDir_Zangle)*b0_FD_OWNPV < 7', r'$B^0 \rightarrow D^{*+} \mu$')
    ]
}


################################
# Command line argument parser #
################################

def parse_input(descr='Generate cutflow output YAML based on input ntuple and YAML.'):
    parser = ArgumentParser(description=descr)

    parser.add_argument('ntps', nargs='+',
                        help='specify input ntuple paths.')

    parser.add_argument('-i', '--input_yml', required=True,
                        help='specify input YAML path.')

    parser.add_argument('-o', '--output_yml', required=True,
                        help='specify output YAML path.')

    parser.add_argument('-m', '--mode', required=True,
                        help='specify mode.')

    parser.add_argument('-t', '--tree',
                        default='TupleB0/DecayTree',
                        help='specify tree name in the input ntuple.'
                        )

    return parser.parse_args()


###########
# Helpers #
###########

# We need this naive YAML generator so that nothing is escaped
def yaml_gen(data, indent='', indent_increment=' '*4):
    result = ''
    for key, items in data.items():
        result += '{}{}:'.format(indent, key)
        if type(items) in [dict, odict]:
            result += '\n'
            result += yaml_gen(items, indent=indent+indent_increment)
        elif items is None:
            result += ' null\n'
        else:
            result += ' {}\n'.format(items)
    return result


if __name__ == '__main__':
    args = parse_input()
    aliases = ALIASES[args.mode]
    cuts = CUTFLOW[args.mode]
    cut_to_update = list(aliases.values())[-1]

    with open(args.input_yml) as f:
        raw = safe_load(f)

    result = dict()
    for cut, val in raw.items():
        if val['output'] is None:
            val['output'] = 0

        if cut in aliases:
            result[aliases[cut]] = val

    for ntp_path in args.ntps:
        ntp = uproot.open(ntp_path)
        _, _, _, uniq_size, _, _ = extract_uid(ntp, args.tree)

        # Update the total number after the DaVinci step
        result[cut_to_update]['output'] += uniq_size

        cutflow_output_regulator = cutflow_uniq_events_outer(ntp, args.tree)

        result_addon = CutflowGen(ntp_path, args.tree, cuts, uniq_size).do(
            output_regulator=cutflow_output_regulator)
        result.update(result_addon)

        with open(args.output_yml, 'w') as f:
            f.write(yaml_gen(result))

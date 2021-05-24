#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon May 24, 2021 at 10:10 PM +0200

import pathlib
import os
import sys

# Make ROOT aware of our custom header path
pwd = pathlib.Path(__file__).parent.absolute()
header_path = str((pwd / '../include').resolve())
os.environ['ROOT_INCLUDE_PATH'] = header_path

import uproot
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from yaml import safe_load
from argparse import ArgumentParser
from collections import OrderedDict as odict

import numpy as np
from numpy import vectorize, sqrt, log10
from numpy import logical_and as AND

from pyTuplingUtils.utils import extract_uid
from pyTuplingUtils.cutflow import CutflowGen, CutflowRule as Rule
from pyTuplingUtils.cutflow import cutflow_uniq_events_outer
from pyTuplingUtils.boolean.const import KNOWN_FUNC
from TrackerOnlyEmu.loader import load_cpp


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
        Rule('''flag_sel_run1_strip(mu_IPCHI2_OWNPV, mu_TRACK_GhostProb,
                                    mu_PIDmu, mu_P, mu_TRACK_CHI2NDOF,
                                    k_PIDK, k_IPCHI2_OWNPV, k_P, k_PT,
                                    k_TRACK_GhostProb,
                                    pi_PIDK, pi_IPCHI2_OWNPV, pi_P, pi_PT,
                                    pi_TRACK_GhostProb,
                                    d0_MM, d0_ENDVERTEX_CHI2,
                                    d0_ENDVERTEX_NDOF, d0_FDCHI2_OWNPV,
                                    d0_DIRA_OWNPV)''',
             key='Stripping'),
        Rule('''flag_sel_run1_dv(spi_IPCHI2_OWNPV, spi_TRACK_GhostProb,
                                 spi_TRACK_CHI2NDOF,
                                 d0_M,
                                 dst_MM, dst_M, dst_ENDVERTEX_CHI2,
                                 dst_ENDVERTEX_NDOF,
                                 b0_MM, b0_ENDVERTEX_CHI2, b0_ENDVERTEX_NDOF,
                                 b0_DIRA_OWNPV)''',
             key=r'DaVinci $D^* \mu$ cuts'),
        # Step 2 cuts
        Rule('''flag_sel_d0_run1(k_PIDK, pi_PIDK, k_isMuon, pi_isMuon,
                                 k_PT, pi_PT, k_P, pi_P,
                                 k_Hlt1TrackAllL0Decision_TOS,
                                 pi_Hlt1TrackAllL0Decision_TOS,
                                 k_IPCHI2_OWNPV, pi_IPCHI2_OWNPV,
                                 k_TRACK_GhostProb, pi_TRACK_GhostProb,
                                 d0_PT, d0_Hlt2CharmHadD02HH_D02KPiDecision_TOS,
                                 d0_ENDVERTEX_NDOF, d0_ENDVERTEX_CHI2,
                                 d0_IP_OWNPV, d0_IPCHI2_OWNPV,
                                 d0_DIRA_OWNPV, d0_FDCHI2_OWNPV, d0_M)''',
             key=r'Offline $D^0$ cuts'),
        Rule('''flag_sel_mu_run1(mu_PX, mu_PY, mu_PZ,
                                 k_PX, k_PY, k_PZ,
                                 pi_PX, pi_PY, pi_PZ,
                                 spi_PX, spi_PY, spi_PZ,
                                 mu_isMuon, mu_PIDmu, mu_PIDe,
                                 mu_P, mu_IPCHI2_OWNPV, mu_TRACK_GhostProb)''',
             key=r'Offline $\mu$ cuts'),
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


###################
# Known functions #
###################

load_cpp(header_path + '/functor/rdx/cut.h')
load_cpp(header_path + '/functor/rdx/kinematic.h')

flag_sel_d0_pid_ok_run1 = vectorize(ROOT.FLAG_SEL_D0_PID_OK_RUN1)
flag_sel_d0_run1_raw = vectorize(ROOT.FLAG_SEL_D0_RUN1)

flag_sel_mu_pid_ok_run1 = vectorize(ROOT.FLAG_SEL_MU_PID_OK_RUN1)
flag_sel_mu_run1_raw = vectorize(ROOT.FLAG_SEL_MU_RUN1)
kinematic_eta = vectorize(ROOT.ETA)


def flag_sel_d0_run1(k_pid_k, pi_pid_k, k_is_mu, pi_is_mu,
                     k_pt, pi_pt,
                     k_p, pi_p,
                     k_hlt1_tos, pi_hlt1_tos,
                     k_ip_chi2, pi_ip_chi2,
                     k_gh_prob, pi_gh_prob,
                     d0_pt,
                     d0_hlt2,
                     d0_endvtx_chi2, d0_endvtx_ndof,
                     d0_ip, d0_ip_chi2,
                     d0_dira, d0_fd_chi2, d0_m):
    d0_pid_ok = flag_sel_d0_pid_ok_run1(k_pid_k, pi_pid_k, k_is_mu,
                                             pi_is_mu)
    return flag_sel_d0_run1_raw(d0_pid_ok, k_pt, pi_pt, k_p, pi_p,
                                k_hlt1_tos, pi_hlt1_tos,
                                k_ip_chi2, pi_ip_chi2, k_gh_prob, pi_gh_prob,
                                d0_pt, d0_hlt2,
                                d0_endvtx_chi2, d0_endvtx_ndof,
                                d0_ip, d0_ip_chi2, d0_dira, d0_fd_chi2, d0_m)


# I decide to NOT use the C++ implementation here
def flag_sel_good_tracks(mu_px, mu_py, mu_pz, k_px, k_py, k_pz,
                         pi_px, pi_py, pi_pz, spi_px, spi_py, spi_pz):
    other_px = (k_px, pi_px, spi_px)
    other_py = (k_py, pi_py, spi_py)
    other_pz = (k_pz, pi_pz, spi_pz)
    flag = []

    for px, py, pz in zip(other_px, other_py, other_pz):
        inner_prod = mu_px*px + mu_py*py + mu_pz*pz
        magnitude = sqrt(mu_px*mu_px + mu_py*mu_py + mu_pz*mu_pz) * \
            sqrt(px*px + py*py + pz*pz)
        flag.append(log10(1 - inner_prod / magnitude) > -6.5)

    return AND(*flag)


def flag_sel_mu_run1(mu_px, mu_py, mu_pz,
                     k_px, k_py, k_pz,
                     pi_px, pi_py, pi_pz,
                     spi_px, spi_py, spi_pz,
                     mu_is_mu, mu_pid_mu, mu_pid_e,
                     mu_p, mu_ip_chi2, mu_gh_prob):
    good_tracks = flag_sel_good_tracks(mu_px, mu_py, mu_pz, k_px, k_py, k_pz,
                                       pi_px, pi_py, pi_pz, spi_px, spi_py,
                                       spi_pz)

    fake_mu_bdt_mu = np.full(mu_px.size, 0.4)
    mu_pid_ok = flag_sel_mu_pid_ok_run1(mu_is_mu, mu_pid_mu, mu_pid_e,
                                        fake_mu_bdt_mu)

    mu_eta = kinematic_eta(mu_p, mu_pz)
    # Need to do unit conversion here, since in C++ 'mu_p' is expected to be in
    # GeV
    mu_p = mu_p / 1000
    return flag_sel_mu_run1_raw(good_tracks, mu_pid_ok, mu_p, mu_eta,
                                mu_ip_chi2, mu_gh_prob)


KNOWN_FUNC['flag_sel_run1_strip'] = vectorize(ROOT.FLAG_SEL_RUN1_STRIP)
KNOWN_FUNC['flag_sel_run1_dv'] = vectorize(ROOT.FLAG_SEL_RUN1_DV)
KNOWN_FUNC['flag_sel_d0_run1'] = flag_sel_d0_run1
KNOWN_FUNC['flag_sel_mu_run1'] = flag_sel_mu_run1


########
# Main #
########

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
        cutflow_generator = CutflowGen(ntp_path, args.tree, cuts, uniq_size)

        result_addon = cutflow_generator.do(
            output_regulator=cutflow_output_regulator)

        for key, val in result_addon.items():
            if key not in result:
                result[key] = val
            else:
                result[key]['input'] += val['input']
                result[key]['output'] += val['output']

        with open(args.output_yml, 'w') as f:
            f.write(yaml_gen(result))

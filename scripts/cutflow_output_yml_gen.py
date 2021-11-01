#!/usr/bin/env python3
#
# Author: Yipeng Sun, Manual Franco Sevilla
# License: BSD 2-clause
# Last Change: Mon Nov 01, 2021 at 02:45 PM +0100

import pathlib
import os

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
from itertools import product

import numpy as np
from numpy import vectorize, sqrt, log10
from numpy import logical_and as AND

from pyTuplingUtils.utils import extract_uid
from pyTuplingUtils.cutflow import CutflowGen, CutflowRule as Rule
from pyTuplingUtils.cutflow import cutflow_uniq_events_outer
from pyTuplingUtils.boolean.const import KNOWN_FUNC
from TrackerOnlyEmu.loader import load_cpp

#################################
# DaVinci log selection aliases #
#################################

ALIASES = {
    'run1-Dst-bare': {
        'DaVinciEventSeq': 'Total events',
        'SelMyB-': r'Relaxed $D^0 \mu$ combo',
        'SelMyDst': r'$D^{*+} \rightarrow D^0 \pi^+$',
        'SelMyB0': r'$\bar{B}^0 \rightarrow D^{*+} \mu^-$',
    }
}

for mode in ['run2-Dst-bare',
             'run1-Dst-bare-nor', 'run1-Dst-bare-sig', 'run1-Dst-bare-dss',
             'run2-Dst-bare-nor', 'run2-Dst-bare-sig', 'run2-Dst-bare-dss']:
    ALIASES[mode] = ALIASES['run1-Dst-bare']


################
# Offline cuts #
################

CUTFLOW = {
    'run1-std': [
        # Trigger + stripping (already applied in data) + DaVinci
        Rule('''(mu_L0Global_TIS & (b0_L0Global_TIS | d0_L0HadronDecision_TOS)) &
        (k_Hlt1TrackAllL0Decision_TOS | pi_Hlt1TrackAllL0Decision_TOS) &
        d0_Hlt2CharmHadD02HH_D02KPiDecision_TOS &
        flag_sel_run1_strip(mu_IPCHI2_OWNPV, mu_TRACK_GhostProb,
                                    mu_PIDmu, mu_P, mu_TRACK_CHI2NDOF,
                                    k_PIDK, k_IPCHI2_OWNPV, k_P, k_PT,
                                    k_TRACK_GhostProb,
                                    pi_PIDK, pi_IPCHI2_OWNPV, pi_P, pi_PT,
                                    pi_TRACK_GhostProb,
                                    d0_MM, d0_ENDVERTEX_CHI2,
                                    d0_ENDVERTEX_NDOF, d0_FDCHI2_OWNPV,
                                    d0_DIRA_OWNPV)''',
             key=r'Trig. + Strip.'),
        # Step 2 cuts (currently same as in run 1)
        Rule('''flag_sel_d0_run1(k_PIDK, pi_PIDK, k_isMuon, pi_isMuon,
                                 k_PT, pi_PT,
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
        Rule('''flag_sel_b0dst_run1(spi_TRACK_GhostProb,
                                    dst_ENDVERTEX_CHI2, dst_ENDVERTEX_NDOF,
                                    dst_M, d0_M,
                                    b0_DISCARDMu_CHI2,
                                    b0_ENDVERTEX_CHI2, b0_ENDVERTEX_NDOF,
                                    b0_ENDVERTEX_X, b0_ENDVERTEX_Y,
                                    b0_OWNPV_X, b0_OWNPV_Y,
                                    b0_DIRA_OWNPV, b0_M) &
        flag_sel_run1_dv(spi_IPCHI2_OWNPV, spi_TRACK_GhostProb,
                                 spi_TRACK_CHI2NDOF,
                                 d0_M,
                                 dst_MM, dst_M, dst_ENDVERTEX_CHI2,
                                 dst_ENDVERTEX_NDOF,
                                 b0_MM, b0_ENDVERTEX_CHI2, b0_ENDVERTEX_NDOF,
                                 b0_DIRA_OWNPV)''',
             key=r'Offline $D^* \mu$ combo cuts'),
        Rule('b0_ISOLATION_BDT < 0.15', key=r'$BDT_{iso} < 0.15$'),
    ],
    'run2-std': [
        # Trigger + stripping (already applied in data) + DaVinci
        Rule('''(b0_L0Global_TIS | d0_L0HadronDecision_TOS) &
        (k_Hlt1TrackMVADecision_TOS | pi_Hlt1TrackMVADecision_TOS |
        d0_Hlt1TwoTrackMVADecision_TOS) & b0_Hlt2XcMuXForTauB2XcMuDecision_TOS &
        flag_sel_run2_strip(mu_IPCHI2_OWNPV, mu_TRACK_GhostProb,
                                    mu_PIDmu, mu_P, mu_TRACK_CHI2NDOF,
                                    k_PIDK, k_IPCHI2_OWNPV, k_P, k_PT,
                                    k_TRACK_GhostProb,
                                    pi_PIDK, pi_IPCHI2_OWNPV, pi_P, pi_PT,
                                    pi_TRACK_GhostProb,
                                    d0_MM, d0_ENDVERTEX_CHI2,
                                    d0_ENDVERTEX_NDOF, d0_FDCHI2_OWNPV,
                                    d0_DIRA_OWNPV)''',
             key=r'Trig. + Strip.'),
        # Step 2 cuts (currently same as in run 1)
        Rule('''flag_sel_d0_run1(k_PIDK, pi_PIDK, k_isMuon, pi_isMuon,
                                 k_PT, pi_PT,
                                 k_Hlt1TrackMVADecision_TOS,
                                 pi_Hlt1TrackMVADecision_TOS,
                                 k_IPCHI2_OWNPV, pi_IPCHI2_OWNPV,
                                 k_TRACK_GhostProb, pi_TRACK_GhostProb,
                                 d0_PT, true,
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
        Rule('''flag_sel_b0dst_run1(spi_TRACK_GhostProb,
                                    dst_ENDVERTEX_CHI2, dst_ENDVERTEX_NDOF,
                                    dst_M, d0_M,
                                    b0_DISCARDMu_CHI2,
                                    b0_ENDVERTEX_CHI2, b0_ENDVERTEX_NDOF,
                                    b0_ENDVERTEX_X, b0_ENDVERTEX_Y,
                                    b0_OWNPV_X, b0_OWNPV_Y,
                                    b0_DIRA_OWNPV, b0_M) &
        flag_sel_run2_dv(spi_IPCHI2_OWNPV, spi_TRACK_GhostProb,
                                 spi_TRACK_CHI2NDOF,
                                 d0_M,
                                 dst_MM, dst_M, dst_ENDVERTEX_CHI2,
                                 dst_ENDVERTEX_NDOF,
                                 b0_MM, b0_ENDVERTEX_CHI2, b0_ENDVERTEX_NDOF,
                                 b0_DIRA_OWNPV)''',
             key=r'Offline $D^* \mu$ combo cuts'),
        Rule('b0_ISOLATION_BDT < 0.15', key=r'$BDT_{iso} < 0.15$'),
    ],
    'run1-Dst-bare': [
        # Trigger
        Rule('mu_L0Global_TIS & (b0_L0Global_TIS | d0_L0HadronDecision_TOS)',
             key='L0'),
        Rule('k_Hlt1TrackAllL0Decision_TOS | pi_Hlt1TrackAllL0Decision_TOS',
             key='Hlt1'),
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
                                 k_PT, pi_PT,
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
        Rule('''flag_sel_b0dst_run1(spi_TRACK_GhostProb,
                                    dst_ENDVERTEX_CHI2, dst_ENDVERTEX_NDOF,
                                    dst_M, d0_M,
                                    b0_DISCARDMu_CHI2,
                                    b0_ENDVERTEX_CHI2, b0_ENDVERTEX_NDOF,
                                    b0_ENDVERTEX_X, b0_ENDVERTEX_Y,
                                    b0_OWNPV_X, b0_OWNPV_Y,
                                    b0_DIRA_OWNPV, b0_M)''',
             key=r'Offline $D^* \mu$ combo cuts'),
        Rule('b0_ISOLATION_BDT < 0.15', key=r'$BDT_{iso} < 0.15$'),
    ],
    'run2-Dst-bare': [
        # Trigger
        Rule('b0_L0Global_TIS | d0_L0HadronDecision_TOS', key='L0'),
        Rule('''k_Hlt1TrackMVADecision_TOS | pi_Hlt1TrackMVADecision_TOS |
                d0_Hlt1TwoTrackMVADecision_TOS''', key='Hlt1'),
        Rule('b0_Hlt2XcMuXForTauB2XcMuDecision_TOS', key='Hlt2'),
        # Stripping
        Rule('''flag_sel_run2_strip(mu_IPCHI2_OWNPV, mu_TRACK_GhostProb,
                                    mu_PIDmu, mu_P, mu_TRACK_CHI2NDOF,
                                    k_PIDK, k_IPCHI2_OWNPV, k_P, k_PT,
                                    k_TRACK_GhostProb,
                                    pi_PIDK, pi_IPCHI2_OWNPV, pi_P, pi_PT,
                                    pi_TRACK_GhostProb,
                                    d0_MM, d0_ENDVERTEX_CHI2,
                                    d0_ENDVERTEX_NDOF, d0_FDCHI2_OWNPV,
                                    d0_DIRA_OWNPV)''',
             key='Stripping'),
        Rule('''flag_sel_run2_dv(spi_IPCHI2_OWNPV, spi_TRACK_GhostProb,
                                 spi_TRACK_CHI2NDOF,
                                 d0_M,
                                 dst_MM, dst_M, dst_ENDVERTEX_CHI2,
                                 dst_ENDVERTEX_NDOF,
                                 b0_MM, b0_ENDVERTEX_CHI2, b0_ENDVERTEX_NDOF,
                                 b0_DIRA_OWNPV)''',
             key=r'DaVinci $D^* \mu$ cuts'),
        # Step 2 cuts (currently same as in run 1)
        Rule('''flag_sel_d0_run1(k_PIDK, pi_PIDK, k_isMuon, pi_isMuon,
                                 k_PT, pi_PT,
                                 k_Hlt1TrackMVADecision_TOS,
                                 pi_Hlt1TrackMVADecision_TOS,
                                 k_IPCHI2_OWNPV, pi_IPCHI2_OWNPV,
                                 k_TRACK_GhostProb, pi_TRACK_GhostProb,
                                 d0_PT, true,
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
        Rule('''flag_sel_b0dst_run1(spi_TRACK_GhostProb,
                                    dst_ENDVERTEX_CHI2, dst_ENDVERTEX_NDOF,
                                    dst_M, d0_M,
                                    b0_DISCARDMu_CHI2,
                                    b0_ENDVERTEX_CHI2, b0_ENDVERTEX_NDOF,
                                    b0_ENDVERTEX_X, b0_ENDVERTEX_Y,
                                    b0_OWNPV_X, b0_OWNPV_Y,
                                    b0_DIRA_OWNPV, b0_M)''',
             key=r'Offline $D^* \mu$ combo cuts'),
        Rule('b0_ISOLATION_BDT < 0.15', key=r'$BDT_{iso} < 0.15$'),
    ]
}

TRUTH_MATCHING = {
    'sig': Rule('''abs(mu_MC_MOTHER_ID) == 15 &
                   abs(d0_MC_MOTHER_ID) == 413 &
                   abs(d0_MC_GD_MOTHER_ID) == 511''',
                key='Signal truth-matching'),

    'nor': Rule('''abs(mu_MC_MOTHER_ID) == 511 &
                   abs(d0_MC_MOTHER_ID) == 413 &
                   abs(d0_MC_GD_MOTHER_ID) == 511''',
                key='Normalization truth-matching'),

    'dss': Rule('''(abs(mu_MC_MOTHER_ID) == 511 &
                    abs(d0_MC_MOTHER_ID) == 10411 &
                    abs(d0_MC_GD_MOTHER_ID) == 511) |
                   (abs(mu_MC_MOTHER_ID) == 511 &
                    abs(d0_MC_GD_MOTHER_ID) == 10413 &
                    abs(d0_MC_GD_GD_MOTHER_ID) == 511) |
                   (abs(mu_MC_MOTHER_ID) == 511 &
                    abs(d0_MC_GD_MOTHER_ID) == 20413 &
                    abs(d0_MC_GD_GD_MOTHER_ID) == 511) |
                   (abs(mu_MC_MOTHER_ID) == 511 &
                    (abs(d0_MC_MOTHER_ID) == 415 &
                     abs(d0_MC_GD_MOTHER_ID) == 511 |
                     abs(d0_MC_GD_MOTHER_ID) == 415 &
                     abs(d0_MC_GD_GD_MOTHER_ID) == 511))''',
                key='$D^{**}$ truth-matching'),
}

for run, decay_mode in product(['run1', 'run2'], TRUTH_MATCHING):
    orig_key = '{}-Dst-bare'.format(run)
    rules = [TRUTH_MATCHING[decay_mode]] + CUTFLOW[orig_key]
    key = '{}-{}'.format(orig_key, decay_mode)
    CUTFLOW[key] = rules

for run, decay_mode in product(['run1', 'run2'], TRUTH_MATCHING):
    orig_key = '{}-std'.format(run)
    rules = [TRUTH_MATCHING[decay_mode]] + CUTFLOW[orig_key]
    key = '{}-{}'.format(orig_key, decay_mode)
    CUTFLOW[key] = rules


################################
# Command line argument parser #
################################

def parse_input(descr='Generate cutflow output YAML based on input ntuple and YAML.'):
    parser = ArgumentParser(description=descr)

    parser.add_argument('ntps', nargs='+',
                        help='specify input ntuple paths.')

    parser.add_argument('-i', '--input_yml',
                        help='specify input YAML path.')

    parser.add_argument('-o', '--output_yml', required=True,
                        help='specify output YAML path.')

    parser.add_argument('-m', '--mode', required=True,
                        help='specify mode.')

    parser.add_argument('-s', '--silent',
                        action='store_true',
                        help='do no print output'
                        )

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

flag_sel_b0dst_run1_raw = vectorize(ROOT.FLAG_SEL_B0DST_RUN1)


def flag_sel_d0_run1(k_pid_k, pi_pid_k, k_is_mu, pi_is_mu,
                     k_pt, pi_pt,
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
    return flag_sel_d0_run1_raw(d0_pid_ok, k_pt, pi_pt,
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

    mu_pid_ok = flag_sel_mu_pid_ok_run1(mu_is_mu, mu_pid_mu, mu_pid_e)

    mu_eta = kinematic_eta(mu_p, mu_pz)
    return flag_sel_mu_run1_raw(good_tracks, mu_pid_ok, mu_p, mu_eta,
                                mu_ip_chi2, mu_gh_prob)


def vec_trans(x, y):
    return sqrt(x*x + y*y)


def flag_sel_b0dst_run1(spi_gh_prob,
                        dst_endvtx_chi2, dst_endvtx_ndof,
                        dst_m, d0_m,
                        b0_discard_mu_chi2,
                        b0_endvtx_chi2, b0_endvtx_ndof,
                        b0_endvtx_x, b0_endvtx_y,
                        b0_pv_x, b0_pv_y,
                        b0_dira, b0_m):
    fake_sel_d0 = np.full(spi_gh_prob.size, True)
    fake_sel_mu = fake_sel_d0
    b0_fd_trans = vec_trans(b0_endvtx_x - b0_pv_x, b0_endvtx_y - b0_pv_y)

    return flag_sel_b0dst_run1_raw(fake_sel_d0, fake_sel_mu,
                                   spi_gh_prob,
                                   dst_endvtx_chi2, dst_endvtx_ndof,
                                   dst_m, d0_m,
                                   b0_discard_mu_chi2,
                                   b0_endvtx_chi2, b0_endvtx_ndof,
                                   b0_fd_trans, b0_dira, b0_m)


KNOWN_FUNC['flag_sel_run1_strip'] = vectorize(ROOT.FLAG_SEL_RUN1_STRIP)
KNOWN_FUNC['flag_sel_run1_dv'] = vectorize(ROOT.FLAG_SEL_RUN1_DV)
KNOWN_FUNC['flag_sel_d0_run1'] = flag_sel_d0_run1
KNOWN_FUNC['flag_sel_mu_run1'] = flag_sel_mu_run1
KNOWN_FUNC['flag_sel_b0dst_run1'] = flag_sel_b0dst_run1

KNOWN_FUNC['flag_sel_run2_strip'] = vectorize(ROOT.FLAG_SEL_RUN2_STRIP)
KNOWN_FUNC['flag_sel_run2_dv'] = vectorize(ROOT.FLAG_SEL_RUN2_DV)


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()
    cuts = CUTFLOW[args.mode]

    result = dict()
    if args.input_yml is not None:
        aliases = ALIASES[args.mode]
        cut_to_update = list(aliases.values())[-1]
        with open(args.input_yml) as f:
            raw = safe_load(f)

        for cut, val in raw.items():
            if val['output'] is None:
                val['output'] = 0

            if cut in aliases:
                result[aliases[cut]] = val

    for ntp_path in args.ntps:
        ntp = uproot.open(ntp_path)
        _, _, _, uniq_size, _, _ = extract_uid(ntp, args.tree)

        # Update the total number after the DaVinci step
        if args.input_yml is None:
            key = 'Total events'
            if key not in result:
                val = dict()
                val['input'] = uniq_size
                val['output'] = uniq_size
                result['Total events'] = val
            else:
                result[key]['input'] += uniq_size
                result[key]['output'] += uniq_size
        else:
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
            if not args.silent:
                print(" cat  "+args.output_yml)

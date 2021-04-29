#!/usr/bin/env python
#
# Author: Manuel Franco Sevilla
# License: BSD 2-clause
# Last Change: Thu Apr 29, 2021 at 02:26 AM +0200

import uproot
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from yaml import safe_load
from argparse import ArgumentParser

from pyTuplingUtils.utils import extract_uid
from pyTuplingUtils.cutflow import CutflowGen, CutflowRule as Rule
from pyTuplingUtils.cutflow import cutflow_uniq_events_outer

from cutflow_output_yml_gen import yaml_gen


ALIASES = {
    'SeqMyB0': 'Total events',
    'StrippedBCands': r'Stripped $D^0 \mu^-$',
    'SelMyD0': r'$D^0 \rightarrow K^- \pi^+$',
    'SelMyDst': r'$D^{*+} \rightarrow D^0 \pi^+$',
    'SelMyB0': r'$\bar{B}^0 \rightarrow D^{*+} \mu^-$',
    'SelMyRefitB02DstMu': r'Refit $\bar{B}^0$ decay tree',
}

CUTFLOW = {
    'run1-sig': [
        Rule('abs(mu_MC_MOTHER_ID)==15 & abs(d0_MC_MOTHER_ID)==413 & abs(d0_MC_GD_MOTHER_ID)==511', key='Partial stripping'),
        # Trigger
        Rule('mu_L0Global_TIS & (b0_L0Global_TIS | dst_L0HadronDecision_TOS)', key='L0'),
        Rule('k_Hlt1TrackAllL0Decision_TOS | pi_Hlt1TrackAllL0Decision_TOS', key='Hlt1'),
        Rule('d0_Hlt2CharmHadD02HH_D02KPiDecision_TOS', key='Hlt2'),
        # Stripping
        Rule('(mu_IPCHI2_OWNPV > 16.0) & (mu_TRACK_GhostProb < 0.5) & (mu_PIDmu > -200.0) & (mu_P > 3.0*GeV) & (mu_TRACK_CHI2NDOF < 3.0) & (k_PIDK > 4.0) & (k_IPCHI2_OWNPV > 9.0) & (k_P > 2.0*GeV) & (k_PT > 300.0*MeV) & (k_TRACK_GhostProb < 0.5) & (pi_P > 2.0*GeV) & (pi_PT > 300.0*MeV) & (pi_IPCHI2_OWNPV > 9.0) & (pi_PIDK < 2.0) & (pi_TRACK_GhostProb < 0.5) & (spi_IPCHI2_OWNPV > 0.0) & (spi_TRACK_CHI2NDOF < 3.0) & (spi_TRACK_GhostProb < 0.25) & (k_PT + pi_PT > 2500.0*MeV) & (abs(d0_MM - PDG_M_D0) < 80.0*MeV) & (d0_ENDVERTEX_CHI2 / d0_ENDVERTEX_NDOF < 4.0) & (d0_FDCHI2_OWNPV > 25.0) & (d0_DIRA_OWNPV > 0.999) & (abs(dst_MM - PDG_M_Dst) < 125.0*MeV) & (dst_M - d0_M < 160.0*MeV) & (dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 100.0) & (0.0*GeV < b0_MM < 10.0*GeV) & (b0_ENDVERTEX_CHI2 / b0_ENDVERTEX_NDOF < 6.0) & (b0_DIRA_OWNPV > 0.999)',
             key='Full stripping'),
        # Step 2
        Rule('mu_isMuon & mu_PIDmu > 2 & mu_PIDe < 1 & mu_P < 100.0*GeV', r'$\mu$ PID'),
        Rule('b0_ISOLATION_BDT < 0.15', r'$\text{IsoBDT}_{B^0} < 0.15$'),
        Rule('b0_MM < 5280 & b0_DIRA_OWNPV > 0.9995', r'$B^0$ cuts'),
        # Newer step 2 cuts
        Rule('k_PT > 800.0*MeV & !k_isMuon & k_IPCHI2_OWNPV > 45', r'$K$ cuts'),
        Rule('pi_PT > 800.0*MeV & !pi_isMuon & pi_IPCHI2_OWNPV > 45', r'$\pi$ cuts'),
        Rule('spi_TRACK_GhostProb < 0.5', r'$\pi_{soft}$ cuts'),
        Rule('d0_P > 2.0*GeV & d0_FDCHI2_OWNPV > 250 & abs(d0_MM - PDG_M_D0) < 23.4 & (k_PT > 1.7*GeV | pi_PT > 1.7*GeV)', r'$D^0$ cuts'),
        Rule('dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 10 & abs(dst_MM - d0_MM - 145.43) < 2', r'$D^*$ cuts'),
    ],

    'run1-nor': [
        Rule('abs(mu_MC_MOTHER_ID)==511 & abs(d0_MC_MOTHER_ID)==413 & abs(d0_MC_GD_MOTHER_ID)==511', r'$D^{*+}\mu\nu$', key='Partial stripping'),
        # Trigger
        Rule('mu_L0Global_TIS & (b0_L0Global_TIS | dst_L0HadronDecision_TOS)', key='L0'),
        Rule('k_Hlt1TrackAllL0Decision_TOS | pi_Hlt1TrackAllL0Decision_TOS', key='Hlt1'),
        Rule('d0_Hlt2CharmHadD02HH_D02KPiDecision_TOS', key='Hlt2'),
        # Stripping
        Rule('(mu_IPCHI2_OWNPV > 16.0) & (mu_TRACK_GhostProb < 0.5) & (mu_PIDmu > -200.0) & (mu_P > 3.0*GeV) & (mu_TRACK_CHI2NDOF < 3.0) & (k_PIDK > 4.0) & (k_IPCHI2_OWNPV > 9.0) & (k_P > 2.0*GeV) & (k_PT > 300.0*MeV) & (k_TRACK_GhostProb < 0.5) & (pi_P > 2.0*GeV) & (pi_PT > 300.0*MeV) & (pi_IPCHI2_OWNPV > 9.0) & (pi_PIDK < 2.0) & (pi_TRACK_GhostProb < 0.5) & (spi_IPCHI2_OWNPV > 0.0) & (spi_TRACK_CHI2NDOF < 3.0) & (spi_TRACK_GhostProb < 0.25) & (k_PT + pi_PT > 2500.0*MeV) & (abs(d0_MM - PDG_M_D0) < 80.0*MeV) & (d0_ENDVERTEX_CHI2 / d0_ENDVERTEX_NDOF < 4.0) & (d0_FDCHI2_OWNPV > 25.0) & (d0_DIRA_OWNPV > 0.999) & (abs(dst_MM - PDG_M_Dst) < 125.0*MeV) & (dst_M - d0_M < 160.0*MeV) & (dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 100.0) & (0.0*GeV < b0_MM < 10.0*GeV) & (b0_ENDVERTEX_CHI2 / b0_ENDVERTEX_NDOF < 6.0) & (b0_DIRA_OWNPV > 0.999)',
             key='Full stripping'),
        # Step 2
        Rule('mu_isMuon & mu_PIDmu > 2 & mu_PIDe < 1 & mu_P < 100.0*GeV', r'$\mu$ PID'),
        Rule('b0_ISOLATION_BDT < 0.15', r'$\text{IsoBDT}_{B^0} < 0.15$'),
        Rule('b0_MM < 5280 & b0_DIRA_OWNPV > 0.9995', r'$B^0$ cuts'),
        # Newer step 2 cuts
        Rule('k_PT > 800.0*MeV & !k_isMuon & k_IPCHI2_OWNPV > 45', r'$K$ cuts'),
        Rule('pi_PT > 800.0*MeV & !pi_isMuon & pi_IPCHI2_OWNPV > 45', r'$\pi$ cuts'),
        Rule('spi_TRACK_GhostProb < 0.5', r'$\pi_{soft}$ cuts'),
        Rule('d0_P > 2.0*GeV & d0_FDCHI2_OWNPV > 250 & abs(d0_MM - PDG_M_D0) < 23.4 & (k_PT > 1.7*GeV | pi_PT > 1.7*GeV)', r'$D^0$ cuts'),
        Rule('dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 10 & abs(dst_MM - d0_MM - 145.43) < 2', r'$D^*$ cuts'),
    ],

    'run1-dss': [
        Rule('(abs(mu_MC_MOTHER_ID)==511 & abs(d0_MC_MOTHER_ID)==10411 & abs(d0_MC_GD_MOTHER_ID)==511) | (abs(mu_MC_MOTHER_ID)==511 & abs(d0_MC_GD_MOTHER_ID)==10413 & abs(d0_MC_GD_GD_MOTHER_ID)==511) | (abs(mu_MC_MOTHER_ID)==511 & abs(d0_MC_GD_MOTHER_ID)==20413 & abs(d0_MC_GD_GD_MOTHER_ID)==511) | (abs(mu_MC_MOTHER_ID)==511 & (abs(d0_MC_MOTHER_ID)==415 & abs(d0_MC_GD_MOTHER_ID)==511 | abs(d0_MC_GD_MOTHER_ID)==415 & abs(d0_MC_GD_GD_MOTHER_ID)==511))', r'$D^{**}$', key='Partial stripping'),
        # Trigger
        Rule('mu_L0Global_TIS & (b0_L0Global_TIS | dst_L0HadronDecision_TOS)', key='L0'),
        Rule('k_Hlt1TrackAllL0Decision_TOS | pi_Hlt1TrackAllL0Decision_TOS', key='Hlt1'),
        Rule('d0_Hlt2CharmHadD02HH_D02KPiDecision_TOS', key='Hlt2'),
        # Stripping
        Rule('(mu_IPCHI2_OWNPV > 16.0) & (mu_TRACK_GhostProb < 0.5) & (mu_PIDmu > -200.0) & (mu_P > 3.0*GeV) & (mu_TRACK_CHI2NDOF < 3.0) & (k_PIDK > 4.0) & (k_IPCHI2_OWNPV > 9.0) & (k_P > 2.0*GeV) & (k_PT > 300.0*MeV) & (k_TRACK_GhostProb < 0.5) & (pi_P > 2.0*GeV) & (pi_PT > 300.0*MeV) & (pi_IPCHI2_OWNPV > 9.0) & (pi_PIDK < 2.0) & (pi_TRACK_GhostProb < 0.5) & (spi_IPCHI2_OWNPV > 0.0) & (spi_TRACK_CHI2NDOF < 3.0) & (spi_TRACK_GhostProb < 0.25) & (k_PT + pi_PT > 2500.0*MeV) & (abs(d0_MM - PDG_M_D0) < 80.0*MeV) & (d0_ENDVERTEX_CHI2 / d0_ENDVERTEX_NDOF < 4.0) & (d0_FDCHI2_OWNPV > 25.0) & (d0_DIRA_OWNPV > 0.999) & (abs(dst_MM - PDG_M_Dst) < 125.0*MeV) & (dst_M - d0_M < 160.0*MeV) & (dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 100.0) & (0.0*GeV < b0_MM < 10.0*GeV) & (b0_ENDVERTEX_CHI2 / b0_ENDVERTEX_NDOF < 6.0) & (b0_DIRA_OWNPV > 0.999)',
             key='Full stripping'),
        # Step 2
        Rule('mu_isMuon & mu_PIDmu > 2 & mu_PIDe < 1 & mu_P < 100.0*GeV', r'$\mu$ PID'),
        Rule('b0_ISOLATION_BDT < 0.15', r'$\text{IsoBDT}_{B^0} < 0.15$'),
        Rule('b0_MM < 5280 & b0_DIRA_OWNPV > 0.9995', r'$B^0$ cuts'),
        # Newer step 2 cuts
        Rule('k_PT > 800.0*MeV & !k_isMuon & k_IPCHI2_OWNPV > 45', r'$K$ cuts'),
        Rule('pi_PT > 800.0*MeV & !pi_isMuon & pi_IPCHI2_OWNPV > 45', r'$\pi$ cuts'),
        Rule('spi_TRACK_GhostProb < 0.5', r'$\pi_{soft}$ cuts'),
        Rule('d0_P > 2.0*GeV & d0_FDCHI2_OWNPV > 250 & abs(d0_MM - PDG_M_D0) < 23.4 & (k_PT > 1.7*GeV | pi_PT > 1.7*GeV)', r'$D^0$ cuts'),
        Rule('dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 10 & abs(dst_MM - d0_MM - 145.43) < 2', r'$D^*$ cuts'),
    ],

    'run2-sig': [
        Rule('abs(mu_MC_MOTHER_ID)==15 & abs(d0_MC_MOTHER_ID)==413 & abs(d0_MC_GD_MOTHER_ID)==511', key='Partial stripping'),
        # Trigger
        Rule('mu_L0Global_TIS & (b0_L0Global_TIS | dst_L0HadronDecision_TOS)', key='L0'),
        Rule('k_Hlt1TrackMVALooseDecision_TOS | pi_Hlt1TrackMVALooseDecision_TOS  | d0_Hlt1TwoTrackMVADecision_TOS', key='Hlt1'),
        Rule('d0_Hlt2XcMuXForTauB2XcMuDecision_Dec', key='Hlt2'),
        # Stripping
        Rule('(mu_IPCHI2_OWNPV > 16.0) & (mu_TRACK_GhostProb < 0.5) & (mu_PIDmu > -200.0) & (mu_P > 3.0*GeV) & (mu_TRACK_CHI2NDOF < 3.0) & (k_PIDK > 4.0) & (k_IPCHI2_OWNPV > 9.0) & (k_P > 2.0*GeV) & (k_PT > 300.0*MeV) & (k_TRACK_GhostProb < 0.5) & (pi_P > 2.0*GeV) & (pi_PT > 300.0*MeV) & (pi_IPCHI2_OWNPV > 9.0) & (pi_PIDK < 2.0) & (pi_TRACK_GhostProb < 0.5) & (spi_IPCHI2_OWNPV > 0.0) & (spi_TRACK_CHI2NDOF < 3.0) & (spi_TRACK_GhostProb < 0.25) & (k_PT + pi_PT > 2500.0*MeV) & (abs(d0_MM - PDG_M_D0) < 80.0*MeV) & (d0_ENDVERTEX_CHI2 / d0_ENDVERTEX_NDOF < 4.0) & (d0_FDCHI2_OWNPV > 25.0) & (d0_DIRA_OWNPV > 0.999) & (abs(dst_MM - PDG_M_Dst) < 125.0*MeV) & (dst_M - d0_M < 160.0*MeV) & (dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 100.0) & (0.0*GeV < b0_MM < 10.0*GeV) & (b0_ENDVERTEX_CHI2 / b0_ENDVERTEX_NDOF < 6.0) & (b0_DIRA_OWNPV > 0.999)',
             key='Full stripping'),
        # Step 2
        Rule('mu_isMuon & mu_PIDmu > 2 & mu_PIDe < 1 & mu_P < 100.0*GeV', r'$\mu$ PID'),
        Rule('b0_ISOLATION_BDT < 0.15', r'$\text{IsoBDT}_{B^0} < 0.15$'),
        Rule('b0_MM < 5280 & b0_DIRA_OWNPV > 0.9995', r'$B^0$ cuts'),
        # Newer step 2 cuts
        Rule('k_PT > 800.0*MeV & !k_isMuon & k_IPCHI2_OWNPV > 45', r'$K$ cuts'),
        Rule('pi_PT > 800.0*MeV & !pi_isMuon & pi_IPCHI2_OWNPV > 45', r'$\pi$ cuts'),
        Rule('spi_TRACK_GhostProb < 0.5', r'$\pi_{soft}$ cuts'),
        Rule('d0_P > 2.0*GeV & d0_FDCHI2_OWNPV > 250 & abs(d0_MM - PDG_M_D0) < 23.4 & (k_PT > 1.7*GeV | pi_PT > 1.7*GeV)', r'$D^0$ cuts'),
        Rule('dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 10 & abs(dst_MM - d0_MM - 145.43) < 2', r'$D^*$ cuts'),
    ],

    'run2-nor': [
        Rule('abs(mu_MC_MOTHER_ID)==511 & abs(d0_MC_MOTHER_ID)==413 & abs(d0_MC_GD_MOTHER_ID)==511', r'$D^{*+}\mu\nu$', key='Partial stripping'),
        # Trigger
        Rule('mu_L0Global_TIS & (b0_L0Global_TIS | dst_L0HadronDecision_TOS)', key='L0'),
        Rule('k_Hlt1TrackMVALooseDecision_TOS | pi_Hlt1TrackMVALooseDecision_TOS  | d0_Hlt1TwoTrackMVADecision_TOS', key='Hlt1'),
        Rule('d0_Hlt2XcMuXForTauB2XcMuDecision_Dec', key='Hlt2'),
        # Stripping
        Rule('(mu_IPCHI2_OWNPV > 16.0) & (mu_TRACK_GhostProb < 0.5) & (mu_PIDmu > -200.0) & (mu_P > 3.0*GeV) & (mu_TRACK_CHI2NDOF < 3.0) & (k_PIDK > 4.0) & (k_IPCHI2_OWNPV > 9.0) & (k_P > 2.0*GeV) & (k_PT > 300.0*MeV) & (k_TRACK_GhostProb < 0.5) & (pi_P > 2.0*GeV) & (pi_PT > 300.0*MeV) & (pi_IPCHI2_OWNPV > 9.0) & (pi_PIDK < 2.0) & (pi_TRACK_GhostProb < 0.5) & (spi_IPCHI2_OWNPV > 0.0) & (spi_TRACK_CHI2NDOF < 3.0) & (spi_TRACK_GhostProb < 0.25) & (k_PT + pi_PT > 2500.0*MeV) & (abs(d0_MM - PDG_M_D0) < 80.0*MeV) & (d0_ENDVERTEX_CHI2 / d0_ENDVERTEX_NDOF < 4.0) & (d0_FDCHI2_OWNPV > 25.0) & (d0_DIRA_OWNPV > 0.999) & (abs(dst_MM - PDG_M_Dst) < 125.0*MeV) & (dst_M - d0_M < 160.0*MeV) & (dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 100.0) & (0.0*GeV < b0_MM < 10.0*GeV) & (b0_ENDVERTEX_CHI2 / b0_ENDVERTEX_NDOF < 6.0) & (b0_DIRA_OWNPV > 0.999)',
             key='Full stripping'),
        # Step 2
        Rule('mu_isMuon & mu_PIDmu > 2 & mu_PIDe < 1 & mu_P < 100.0*GeV', r'$\mu$ PID'),
        Rule('b0_ISOLATION_BDT < 0.15', r'$\text{IsoBDT}_{B^0} < 0.15$'),
        Rule('b0_MM < 5280 & b0_DIRA_OWNPV > 0.9995', r'$B^0$ cuts'),
        # Newer step 2 cuts
        Rule('k_PT > 800.0*MeV & !k_isMuon & k_IPCHI2_OWNPV > 45', r'$K$ cuts'),
        Rule('pi_PT > 800.0*MeV & !pi_isMuon & pi_IPCHI2_OWNPV > 45', r'$\pi$ cuts'),
        Rule('spi_TRACK_GhostProb < 0.5', r'$\pi_{soft}$ cuts'),
        Rule('d0_P > 2.0*GeV & d0_FDCHI2_OWNPV > 250 & abs(d0_MM - PDG_M_D0) < 23.4 & (k_PT > 1.7*GeV | pi_PT > 1.7*GeV)', r'$D^0$ cuts'),
        Rule('dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 10 & abs(dst_MM - d0_MM - 145.43) < 2', r'$D^*$ cuts'),
    ],

    'run2-dss': [
        Rule('(abs(mu_MC_MOTHER_ID)==511 & abs(d0_MC_MOTHER_ID)==10411 & abs(d0_MC_GD_MOTHER_ID)==511) | (abs(mu_MC_MOTHER_ID)==511 & abs(d0_MC_GD_MOTHER_ID)==10413 & abs(d0_MC_GD_GD_MOTHER_ID)==511) | (abs(mu_MC_MOTHER_ID)==511 & abs(d0_MC_GD_MOTHER_ID)==20413 & abs(d0_MC_GD_GD_MOTHER_ID)==511) | (abs(mu_MC_MOTHER_ID)==511 & (abs(d0_MC_MOTHER_ID)==415 & abs(d0_MC_GD_MOTHER_ID)==511 | abs(d0_MC_GD_MOTHER_ID)==415 & abs(d0_MC_GD_GD_MOTHER_ID)==511))', r'$D^{**}$', key='Partial stripping'),
        # Trigger
        Rule('mu_L0Global_TIS & (b0_L0Global_TIS | dst_L0HadronDecision_TOS)', key='L0'),
        Rule('k_Hlt1TrackMVALooseDecision_TOS | pi_Hlt1TrackMVALooseDecision_TOS  | d0_Hlt1TwoTrackMVADecision_TOS', key='Hlt1'),
        Rule('d0_Hlt2XcMuXForTauB2XcMuDecision_Dec', key='Hlt2'),
        # Stripping
        Rule('(mu_IPCHI2_OWNPV > 16.0) & (mu_TRACK_GhostProb < 0.5) & (mu_PIDmu > -200.0) & (mu_P > 3.0*GeV) & (mu_TRACK_CHI2NDOF < 3.0) & (k_PIDK > 4.0) & (k_IPCHI2_OWNPV > 9.0) & (k_P > 2.0*GeV) & (k_PT > 300.0*MeV) & (k_TRACK_GhostProb < 0.5) & (pi_P > 2.0*GeV) & (pi_PT > 300.0*MeV) & (pi_IPCHI2_OWNPV > 9.0) & (pi_PIDK < 2.0) & (pi_TRACK_GhostProb < 0.5) & (spi_IPCHI2_OWNPV > 0.0) & (spi_TRACK_CHI2NDOF < 3.0) & (spi_TRACK_GhostProb < 0.25) & (k_PT + pi_PT > 2500.0*MeV) & (abs(d0_MM - PDG_M_D0) < 80.0*MeV) & (d0_ENDVERTEX_CHI2 / d0_ENDVERTEX_NDOF < 4.0) & (d0_FDCHI2_OWNPV > 25.0) & (d0_DIRA_OWNPV > 0.999) & (abs(dst_MM - PDG_M_Dst) < 125.0*MeV) & (dst_M - d0_M < 160.0*MeV) & (dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 100.0) & (0.0*GeV < b0_MM < 10.0*GeV) & (b0_ENDVERTEX_CHI2 / b0_ENDVERTEX_NDOF < 6.0) & (b0_DIRA_OWNPV > 0.999)',
             key='Full stripping'),
        # Step 2
        Rule('mu_isMuon & mu_PIDmu > 2 & mu_PIDe < 1 & mu_P < 100.0*GeV', r'$\mu$ PID'),
        Rule('b0_ISOLATION_BDT < 0.15', r'$\text{IsoBDT}_{B^0} < 0.15$'),
        Rule('b0_MM < 5280 & b0_DIRA_OWNPV > 0.9995', r'$B^0$ cuts'),
        # Newer step 2 cuts
        Rule('k_PT > 800.0*MeV & !k_isMuon & k_IPCHI2_OWNPV > 45', r'$K$ cuts'),
        Rule('pi_PT > 800.0*MeV & !pi_isMuon & pi_IPCHI2_OWNPV > 45', r'$\pi$ cuts'),
        Rule('spi_TRACK_GhostProb < 0.5', r'$\pi_{soft}$ cuts'),
        Rule('d0_P > 2.0*GeV & d0_FDCHI2_OWNPV > 250 & abs(d0_MM - PDG_M_D0) < 23.4 & (k_PT > 1.7*GeV | pi_PT > 1.7*GeV)', r'$D^0$ cuts'),
        Rule('dst_ENDVERTEX_CHI2 / dst_ENDVERTEX_NDOF < 10 & abs(dst_MM - d0_MM - 145.43) < 2', r'$D^*$ cuts'),
    ]
}


################################
# Command line argument parser #
################################

def parse_input(descr='Generate cutflow output YAML based on input ntuple and YAML.'):
    parser = ArgumentParser(description=descr)

    parser.add_argument('ntp',
                        help='specify input ntuple path.')

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

    cutflow_output_regulator = cutflow_uniq_events_outer(ntp, args.tree)

    result = CutflowGen(
        args.ntp, args.tree, CUTFLOW[args.mode], uniq_size).do(
            output_regulator=cutflow_output_regulator)

    with open(args.output_yml, 'w') as f:
        f.write(yaml_gen(result))

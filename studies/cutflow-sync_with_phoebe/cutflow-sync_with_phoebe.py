#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Nov 29, 2021 at 08:08 PM +0100
# Note: Here we use Phoebe's latest ntuple

import sys
import pathlib
import os

# Make ROOT aware of our custom header path
pwd = pathlib.Path(__file__).parent.absolute()
header_path = str((pwd / '../../include').resolve())
os.environ['ROOT_INCLUDE_PATH'] = header_path

import ROOT
from ROOT import RDataFrame
from pyBabyMaker.base import TermColor as TC

# Load C++ headers
ROOT.gInterpreter.Declare('#include "functor/rdx/skims.h"')


#################
# Configurables #
#################

DST_CUTS = [
    'isData > 0 && DstIDprod > 0 && IDprod > 0 && muPID > 0 && '  # redoHistos_Dst.C, LN 3651
    'm_nu1 >= -2.0 && m_nu1 <= 10.9 && '
    'El >= 0.1e3 && El <= 2.65e3 && '
    'q2 >= -0.4e6 && q2 <= 12.6e6',  # Generic global cuts on fit variables
    'L0 && (YTIS || YTOS) && Hlt1 && Hlt2 && '
    '((Hlt1TAL0K && K_PT > 1700.0) || (Hlt1TAL0pi && pi_PT > 1700.0))',  # trigger
    '!muVeto && DLLe < 1.0 && BDTmu > 0.25 && '
    'mu_P > 3.0e3 && mu_P < 100.0e3 && mu_ETA > 1.7 && mu_ETA < 5.0',  # Mu
    'dxy < 7.0 && Y_M < 5280.0',  # D*Mu combo
    'abs(Dst_M-D0_M-145.454) < 2.0',  # D*
    '!(reweighting_69_gen3_pt2 < 0.01 || reweighting_89_gen3_pt2 < 0.01)',  # Derived from some MC weight
    # 'piminus_TRACK_Type == 3',  # Ineffective
    # 'muIPCHI2 > 45.0',  # Mu, ineffective
    # 'abs(Dst_M-D0_M-145.454-9) < 2.0 || abs(Dst_M-D0_M-145.454) < 2.0',  # D*Mu combo, keeping side-band
    # 'Y_DISCARDMu_CHI2 < 6.0 && Y_ENDVERTEX_CHI2 < 24.0 && '
    # 'Y_DIRA_OWNPV > 0.9995 && pislow_GhostProb < 0.25',  # D*Mu combo, ineffective
    # 'abs(D0_M-1865.49) < 23.4',  # D0, ineffective
    # 'KIPCHI2 > 45.0 && piIPCHI2 > 45.0',  # D0, ineffective
    # 'D0_DIRA_OWNPV > 0.9998 && D0IPCHI2 > 9.0',  # D0, ineffective
    # 'K_P > 2000.0 && pi_P > 2000.0 && '
    # 'K_PT > 500.0 && pi_PT > 500.0 && K_PT+pi_PT > 1400.0 && D0_PT > 2000.0',  # D0, ineffective
]

D0_CUTS = [
    'isData > 0 && muPID > 0 && '  # redoHistos_D0.C, LN 2059
    'm_nu1 >= -2.0e6 && m_nu1 <= 10.9e6 && '
    'El >= 0.1e3 && El <= 2.65e3 && '
    'q2 >= -0.4e6 && q2 <= 12.6e6',  # Generic global cuts on fit variables, m_nu1 in MeV^2
    '(YTIS || YTOS) && '
    '((Hlt1TAL0K && K_PT > 1700.0) || (Hlt1TAL0pi && pi_PT > 1700.0))',  # trigger
    '!muVeto && DLLe < 1.0 && BDTmu > 0.25 && '
    'mu_P > 3.0e3 && mu_P < 100.0e3 && mu_ETA > 1.7 && mu_ETA < 5.0',  # Mu
    'dxy < 7.0 && Y_M < 5200.0',  # D0Mu combo
    'Mmu2pi - D0_M - 145.454 > 4.0 && '
    'Mmu2pi - D0_M > 165.0',  # D0 mass hypothesis test
    '!(reweighting_69_gen3_pt2 < 0.01 || reweighting_89_gen3_pt2 < 0.01)',  # Derived from some MC weight
]

# NOTE: We decided to not apply single candidate selection cuts
#       Because Phoebe had a bug in her code s.t. the cut was not applied in her
#       fit templates.
# DST_SKIM_CUTS = {
#     'ISO': 'FLAG_ISO(ISOnum == 0, iso_BDT)',
#     '1OS': '''
#            FLAG_1OS(
#            AntiISOnum == 0,
#            iso_BDT, iso_BDT2,
#            TO_TYPE(iso_Type, 1),
#            GEV(iso_P), GEV(iso_PT),
#            TO_TYPE(iso_CHARGE, 1),
#            iso_NNk,
#            Dst_ID, GEV(iso_DeltaM)
#            )
#            ''',
#     '2OS': '''
#            FLAG_2OS(
#            AntiISOnum == 0,
#            iso_BDT, iso_BDT2, iso_BDT3,
#            TO_TYPE(iso_Type, 1), TO_TYPE(iso_Type2, 1),
#            GEV(iso_P), GEV(iso_P2),
#            GEV(iso_PT), GEV(iso_PT2),
#            TO_TYPE(iso_CHARGE, 1), TO_TYPE(iso_CHARGE2, 1),
#            iso_NNk, iso_NNk2
#            )
#            ''',
#     'DD': '''
#           FLAG_DD(
#           AntiISOnum == 0,
#           iso_BDT, iso_BDT2, iso_BDT3,
#           TO_TYPE(iso_Type, 1), TO_TYPE(iso_Type2, 1), TO_TYPE(iso_Type3, 1),
#           GEV(iso_P), GEV(iso_P2), GEV(iso_P3),
#           GEV(iso_PT), GEV(iso_PT2), GEV(iso_PT3),
#           iso_NNk, iso_NNk2, iso_NNk3
#           )
#           ''',
# }

DST_SKIM_CUTS = {
    'ISO': 'FLAG_ISO(true, iso_BDT)',
    '1OS': '''
           FLAG_1OS(
           true,
           iso_BDT, iso_BDT2,
           TO_TYPE(iso_Type, 1),
           GEV(iso_P), GEV(iso_PT),
           TO_TYPE(iso_CHARGE, 1),
           iso_NNk,
           Dst_ID, GEV(iso_DeltaM)
           )
           ''',
    '2OS': '''
           FLAG_2OS(
           true,
           iso_BDT, iso_BDT2, iso_BDT3,
           TO_TYPE(iso_Type, 1), TO_TYPE(iso_Type2, 1),
           GEV(iso_P), GEV(iso_P2),
           GEV(iso_PT), GEV(iso_PT2),
           TO_TYPE(iso_CHARGE, 1), TO_TYPE(iso_CHARGE2, 1),
           iso_NNk, iso_NNk2
           )
           ''',
    'DD': '''
          FLAG_DD(
          true,
          iso_BDT, iso_BDT2, iso_BDT3,
          TO_TYPE(iso_Type, 1), TO_TYPE(iso_Type2, 1), TO_TYPE(iso_Type3, 1),
          GEV(iso_P), GEV(iso_P2), GEV(iso_P3),
          GEV(iso_PT), GEV(iso_PT2), GEV(iso_PT3),
          iso_NNk, iso_NNk2, iso_NNk3
          )
          ''',
}

D0_SKIM_CUTS = {
    'ISO': 'FLAG_ISO(true, iso_BDT)',
    '1OS': '''
           FLAG_1OS(
           true,
           iso_BDT, iso_BDT2,
           TO_TYPE(iso_Type, 1),
           GEV(iso_P), GEV(iso_PT),
           TO_TYPE(iso_CHARGE, 1),
           iso_NNk,
           D0_ID
           )
           ''',
    '2OS': '''
           FLAG_2OS(
           true,
           iso_BDT, iso_BDT2, iso_BDT3,
           TO_TYPE(iso_Type, 1), TO_TYPE(iso_Type2, 1),
           GEV(iso_P), GEV(iso_P2),
           GEV(iso_PT), GEV(iso_PT2),
           TO_TYPE(iso_CHARGE, 1), TO_TYPE(iso_CHARGE2, 1),
           iso_NNk, iso_NNk2
           )
           ''',
    'DD': '''
          FLAG_DD(
          true,
          iso_BDT, iso_BDT2, iso_BDT3,
          TO_TYPE(iso_Type, 1), TO_TYPE(iso_Type2, 1), TO_TYPE(iso_Type3, 1),
          GEV(iso_P), GEV(iso_P2), GEV(iso_P3),
          GEV(iso_PT), GEV(iso_PT2), GEV(iso_PT3),
          iso_NNk, iso_NNk2, iso_NNk3
          )
          ''',
}

DST_REF_NUMS = {
    'ISO': 420646,
    '1OS': 19666,
    '2OS': 8389,
    'DD': 30918,
}

D0_REF_NUMS = {
    'ISO': 1731149,
    '1OS': 168767,
    '2OS': 42508,
    'DD': 188384,
}


###########
# Helpers #
###########

def apply_skim_cuts(frame, skim_cuts, ref):
    for name, cut in skim_cuts.items():
        cut_frame = frame.Filter(cut)
        num = cut_frame.Count().GetValue()
        num_diff = num - ref[name]
        print('    After applying {}{:>3}{} skim cut: {}{:,} ({:+,}, {:+.1%}){}'.format(
            TC.BOLD+TC.GREEN, name, TC.END, TC.UNDERLINE, num,
            num_diff, num_diff/num, TC.END))


def apply_cuts(frame, cuts, skim_cuts, ref):
    print('Cuts we are about to apply:')
    print('    '+' && '.join(cuts))

    print('The reference templates have the following entries:')
    for name, num in ref.items():
        print('    {:>3}: {:,}'.format(name, num))

    frames = [frame]
    if len(frames) == 1:
        print('{}Before applying any cut: {}{:,}{}'.format(
            TC.BOLD, TC.UNDERLINE, frames[-1].Count().GetValue(), TC.END))

    for c in cuts:
        frm = frames[-1]
        new_frm = frm.Filter(c)
        num = new_frm.Count().GetValue()
        print('{}After applying {}{}{}: {}{:,}{}'.format(
            TC.BOLD, TC.YELLOW, c, TC.END+TC.BOLD, TC.UNDERLINE, num, TC.END))
        frames.append(new_frm)

        apply_skim_cuts(new_frm, skim_cuts, ref)


########
# Main #
########

if __name__ == '__main__':
    ntp_dst = '../../ntuples/ref-rdx-run1/Dst-mix/Dst--21_10_21--mix--all--2011-2012--md-mu--phoebe.root'
    ntp_d0 = '../../ntuples/ref-rdx-run1/D0-mix/D0--21_10_21--mix--all--2011-2012--md-mu--phoebe.root'

    if len(sys.argv) == 1 or sys.argv[1].lower() == 'dst':
        print('Working on Dst...')
        frame_dst = RDataFrame('ntp1', ntp_dst)
        apply_cuts(frame_dst, DST_CUTS, DST_SKIM_CUTS, DST_REF_NUMS)
    elif sys.argv[1].lower() == 'd0':
        print('Working on D0...')
        frame_d0 = RDataFrame('ntp1', ntp_d0)
        apply_cuts(frame_d0, D0_CUTS, D0_SKIM_CUTS, D0_REF_NUMS)
    else:
        print(f'Unknown mode: {sys.argv[1]}')
        sys.exit(255)

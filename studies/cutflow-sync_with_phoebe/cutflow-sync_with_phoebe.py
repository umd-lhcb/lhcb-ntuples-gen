#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sat Oct 23, 2021 at 01:07 AM +0200
# Note: Here we use Phoebe's latest ntuple

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
    # '(selcounter & (4096 * 64 - 1)) == (4096 * 64 - 1)',  # No event removed
    'isData && DstIDprod > 0 && IDprod > 0 && '
    'IN_RANGE(m_nu1, -2.0, 10.9, true) && '
    'IN_RANGE(GEV(El), 0.1, 2.65, true) && '
    'IN_RANGE(GEV2(q2), -0.4, 12.6, true)',  # Generic global cuts on fit variables
    # 'piminus_TRACK_Type == 3',  # No event removed
    'L0 && (YTIS || YTOS) && Hlt1 && Hlt2',  # trigger
    '(Hlt1TAL0K && K_PT > 1700.0) || (Hlt1TAL0pi && pi_PT > 1700.0)',  # trigger
    '!muVeto && muPID > 0 && DLLe < 1.0 && BDTmu > 0.25 && '
    'mu_P > 3.0e3 && mu_P < 100.0e3 && mu_ETA > 1.7 && mu_ETA < 5.0 && '
    'GhostProb < 0.5 && muIPCHI2 > 45.0',  # Mu
    'dxy < 7.0 && Y_DISCARDMu_CHI2 < 6.0 && Y_ENDVERTEX_CHI2 < 24.0 && '
    'Y_DIRA_OWNPV > 0.9995 && pislow_GhostProb < 0.25',  # D*Mu combo
    'Y_M < 5280.0',  # D*Mu combo
    # 'ABS(Dst_M-D0_M-145.454) < 2.0',  # D*Mu combo, this cut is too narrow
    # 'IN_RANGE(Dst_M-D0_M, 143.0, 147.0)',  # D*Mu combo, again too tight
    'ABS(Dst_M-D0_M-145.454-9) < 2.0 || ABS(Dst_M-D0_M-145.454) < 2.0',  # D*Mu combo, keeping side-band
    'ABS(D0_M-1865.49) < 23.4',  # FIXME: Different from below!
    'IN_RANGE(D0_M, 1845.0, 1890.0)',  # FIXME: Missing in our cuts.
    # 'KIPCHI2 > 45.0 && piIPCHI2 > 45.0',  # D0, no event removed
    # 'D0_DIRA_OWNPV > 0.9998 && D0IPCHI2 > 9.0',  # D0, no event removed
    # 'ABS(D0_M-1865.49) < 23.4 && '
    # 'K_P > 2000.0 && pi_P > 2000.0 && '
    # 'K_PT > 500.0 && pi_PT > 500.0 && K_PT+pi_PT > 1400.0 && D0_PT > 2000.0',  # D0, doesn't remove any event
]

DST_SKIM_CUTS = {
    'ISO': 'FLAG_ISO(ISOnum == 0, iso_BDT)',
    '1OS': '''
           FLAG_1OS(
           AntiISOnum == 0,
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
           AntiISOnum == 0,
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
          AntiISOnum == 0,
          iso_BDT, iso_BDT2, iso_BDT3,
          TO_TYPE(iso_Type, 1), TO_TYPE(iso_Type2, 1), TO_TYPE(iso_Type3, 1),
          GEV(iso_P), GEV(iso_P2), GEV(iso_P3),
          GEV(iso_PT), GEV(iso_PT2), GEV(iso_PT3),
          iso_NNk, iso_NNk2, iso_NNk3
          )
          ''',
}


###########
# Helpers #
###########

def apply_skim_cuts(frame, cuts=DST_SKIM_CUTS):
    for name, cut in cuts.items():
        cut_frame = frame.Filter(cut)
        num = cut_frame.Count().GetValue()
        print('    After applying {}{}{} skim cut: {}{:,}{}'.format(
            TC.BOLD+TC.GREEN, name, TC.END, TC.UNDERLINE, num, TC.END))


########
# Main #
########

if __name__ == '__main__':
    # D*
    ntp_dst = '../../ntuples/ref-rdx-run1/Dst-mix/Dst--21_10_21--mix--all--2011-2012--md-mu--phoebe.root'
    frames_dst = [RDataFrame('ntp1', ntp_dst)]

    for c in DST_CUTS:
        if len(frames_dst) == 1:
            print('{}Before applying any cut: {}{:,}{}'.format(
                TC.BOLD, TC.UNDERLINE, frames_dst[-1].Count().GetValue(),
                TC.END))

        frm = frames_dst[-1]
        new_frm = frm.Filter(c)
        num = new_frm.Count().GetValue()
        print('{}After applying {}{}{}: {}{:,}{}'.format(
            TC.BOLD, TC.YELLOW, c, TC.END+TC.BOLD, TC.UNDERLINE, num, TC.END))
        frames_dst.append(new_frm)

        apply_skim_cuts(new_frm)

#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri Oct 22, 2021 at 03:48 AM +0200
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
    '(selcounter & (4096 * 64 - 1)) == (4096 * 64 - 1)',
    'isData && DstIDprod > 0 && IDprod > 0',
    '!muVeto',
    'dxy < 7.0',
    '(Hlt1TAL0K && K_PT > 1700.0) || (Hlt1TAL0pi && pi_PT > 1700.0)',
    'muPID && DLLe < 1.0 && BDTmu > 0.25'
]

DST_SKIM_CUTS = {
    'ISO': 'FLAG_ISO(ISOnum == 0, iso_BDT)'
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

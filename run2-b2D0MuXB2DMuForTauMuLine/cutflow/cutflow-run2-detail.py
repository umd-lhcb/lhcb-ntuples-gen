#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Apr 29, 2020 at 10:16 PM +0800

import uproot
import sys
import yaml

sys.path.insert(0, '../../utils')

from numpy import logical_and as AND, logical_or as OR
from numpy import sum
from tab_gen import TAB
from pyTuplingUtils.io import read_branch
from pyTuplingUtils.utils import extract_uid


###########
# Helpers #
###########

def total_num(ntp, tree, branch='runNumber'):
    return read_branch(ntp, tree, branch).size


def simplify_line(line, remove='Decision'):
    return line.replace(remove, '')


def remove_from(lst, remove=None):
    return [i for i in lst if i != remove]


def comb_cut(ntp, tree, basename, base_result, line,
             particle='Y', tistos='TIS', particle_print=r'$\upsilon(4s)$'):
    add_branch = read_branch(ntp, tree,
                             '{}_{}_{}'.format(particle, line, tistos))
    result = AND(add_branch, base_result)
    return [basename+'+{} {} {}'.format(
        particle_print, simplify_line(line), tistos), sum(result)], result


####################################
# LL/HLT efficiencies from n-tuple #
####################################

L0_lines = [
    'L0DiMuonDecision',
    'L0ElectronDecision',
    'L0HadronDecision',
    'L0JetElDecision',
    'L0JetPhDecision',
    'L0MuonDecision',
    'L0MuonEWDecision',
    'L0PhotonDecision',
    'L0Global',
]

Hlt1_lines = [
    'Hlt1TwoTrackMVADecision',
    'Hlt1TrackMVALooseDecision',
    'Hlt1TwoTrackMVALooseDecision',
    'Hlt1TrackMuonDecision',
    'Hlt1TrackMuonMVADecision',
    'Hlt1SingleMuonHighPTDecision',
]


def tab_marginal_impact(ntp, tree):
    result = [['name', 'number of B']]

    result.append(['DaVinci cuts (DV)', total_num(ntp, tree)])

    row, base_result = comb_cut(ntp, tree, 'DV', True, 'L0HadronDecision',
                                particle='Dst_2010_minus',
                                particle_print=r'$D^*$',
                                tistos='TOS')
    result.append(row)
    basename = row[0]

    for line in L0_lines:
        row, L0_add_result = comb_cut(ntp, tree, basename, base_result, line)
        result.append(row)
        rest_of_L0 = remove_from(L0_lines, line)
        L0_add_name = row[0]

        if line != 'L0Global':
            for lline in rest_of_L0:
                row, _ = comb_cut(ntp, tree, L0_add_name, L0_add_result, lline)
                result.append(row)

    return result


if __name__ == '__main__':
    ntp_path = sys.argv[1]

    ntp = uproot.open(ntp_path)
    tree = 'TupleB0/DecayTree'

    table = tab_marginal_impact(ntp, tree)

    print(TAB.tabulate(table, headers='firstrow'))

#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Mar 23, 2020 at 08:10 PM +0800

import uproot
import sys
import yaml

sys.path.insert(0, '../../utils')

from davinci_log_parser import yaml_gen
from pyTuplingUtils.io import read_branch
from pyTuplingUtils.utils import extract_uid
from numpy import logical_and, logical_or
from numpy import sum


###########
# Helpers #
###########

def total_num(ntp, tree, branch='runNumber'):
    return read_branch(ntp, tree, branch).size


def total_num_dedupl(ntp, tree):
    _, _, _, uniq_size, _ = extract_uid(ntp, tree)
    return uniq_size


####################################
# LL/HLT efficiencies from n-tuple #
####################################

# L0Cuts: muplus_L0Global_TIS && (Y_L0Global_TIS || Dst_L0HadronDecision_TOS)
def L0_cuts(ntp, tree):
    muplus_L0Global_TIS = read_branch(ntp, tree, 'muplus_L0Global_TIS')
    Y_L0Global_TIS = read_branch(ntp, tree, 'Y_L0Global_TIS')
    Dst_L0HadronDecision_TOS = read_branch(
        ntp, tree, 'Dst_2010_minus_L0HadronDecision_TOS')

    result = logical_and(muplus_L0Global_TIS,
                         logical_and(Y_L0Global_TIS, Dst_L0HadronDecision_TOS))
    return sum(result), result


# Hlt1Cuts (run 1): (K_Hlt1TrackAllL0Decision_TOS || pi_Hlt1TrackAllL0Decision_TOS) (pi from D0)
# Hlt1Cuts (run 2): (K_Hlt1Phys_Dec || pi_Hlt1Phys_Dec) (pi from D0)
def Hlt1_cuts(ntp, tree):
    K_Hlt1Phys_Dec = read_branch(ntp, tree, 'Kplus_Hlt1Phys_Dec')
    pi_Hlt1Phys_Dec = read_branch(ntp, tree, 'piminus0_Hlt1Phys_Dec')

    result = logical_or(K_Hlt1Phys_Dec, pi_Hlt1Phys_Dec)
    return sum(result), result


# Hlt2Cuts (run 1): D0_Hlt2CharmHadD02HH_D02KPiDecision_TOS
# Hlt2Cuts (run 2): D0_Hlt2XcMuXForTauB2XcMuDecision_Dec
def Hlt2_cuts(ntp, tree):
    result = read_branch(ntp, tree, 'D0_Hlt2XcMuXForTauB2XcMuDecision_Dec')
    return sum(result), result


# TriggerCuts: L0Cuts && Hlt1Cuts && Hlt2Cuts


if __name__ == '__main__':
    ntp = uproot.open('../ntuples/mc/BCands-yipeng-mc-mag_down-py8-sim09b-Bd2D0XMuNu-D0_cocktail.root')
    tree = 'TupleB0/DecayTree'
    size = total_num(ntp, tree)
    uniq_size = total_num_dedupl(ntp, tree)

    input_yml = 'input-run2.yml'
    output_yml = 'output-run2.yml'

    L0_eff, L0_result = L0_cuts(ntp, tree)
    Hlt1_eff, Hlt1_result = Hlt1_cuts(ntp, tree)
    Hlt2_eff, Hlt2_result = Hlt2_cuts(ntp, tree)

    L0_Hlt1_eff = sum(logical_and(L0_result, Hlt1_result))
    trigger_eff = sum(logical_and(L0_result,
                                  logical_and(Hlt1_result, Hlt2_result)))

    with open(input_yml) as f:
        result = yaml.safe_load(f)

    # Update the output of the final DaVinci cut
    for k, v in result.items():
        if v['output'] == 'None':
            v['output'] = uniq_size  # Here we are only considering events passing the refitting procedure
        result[k] = v

    # Update the L0/Hlt cuts
    result['L0'] = {'input': size, 'output': L0_eff}
    result['Hlt1'] = {'input': L0_eff, 'output': L0_Hlt1_eff}
    result['Hlt2'] = {'input': L0_Hlt1_eff, 'output': trigger_eff}

    with open(output_yml, 'w') as f:
        f.write(yaml_gen(result))

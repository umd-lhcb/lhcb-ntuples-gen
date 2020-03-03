#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Mar 03, 2020 at 09:46 PM +0800

import uproot
import sys
import yaml

sys.path.insert(0, '../../utils')

from davinci_log_parser import yaml_gen
from pyTuplingUtils.io import read_branch
from numpy import logical_and, logical_or
from numpy import sum


###########
# Helpers #
###########

def total_num(ntp, tree, branch='Y_ISOLATION_Type'):
    return read_branch(ntp, tree, branch).size


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


# Hlt1Cuts: (K_Hlt1TrackAllL0Decision_TOS || pi_Hlt1TrackAllL0Decision_TOS) (pi from D0)
def Hlt1_cuts(ntp, tree):
    K_Hlt1TrackAllL0Decision_TOS = read_branch(
        ntp, tree, 'Kplus_Hlt1TrackAllL0Decision_TOS')
    pi_Hlt1TrackAllL0Decision_TOS = read_branch(
        ntp, tree, 'piminus0_Hlt1TrackAllL0Decision_TOS')

    result = logical_or(K_Hlt1TrackAllL0Decision_TOS,
                        pi_Hlt1TrackAllL0Decision_TOS)
    return sum(result), result


# Hlt2Cuts (run 1): D0_Hlt2CharmHadD02HH_D02KPiDecision_TOS
# Hlt2Cuts (run 2): D0_Hlt2XcMuXForTauB2XcMuDecision_TOS
def Hlt2_cuts(ntp, tree):
    result = read_branch(ntp, tree, 'D0_Hlt2XcMuXForTauB2XcMuDecision_TOS')
    return sum(result), result


# TriggerCuts: L0Cuts && Hlt1Cuts && Hlt2Cuts


if __name__ == '__main__':
    ntp = uproot.open('../ntuples/mc/BCands-yipeng-mc-mag_down-py8-sim09b-Bd2D0XMuMu-D0_cocktail.root')
    tree = 'TupleB0/DecayTree'
    size = total_num(ntp, tree)

    input_yml = 'input-mc-mag_down-py8-sim09b-Bd2D0XMuMu-D0_cocktail.yml'
    output_yml = 'output-mc-mag_down-py8-sim09b-Bd2D0XMuMu-D0_cocktail.yml'

    L0_eff, L0_result = L0_cuts(ntp, tree)
    Hlt1_eff, Hlt1_result = Hlt1_cuts(ntp, tree)
    Hlt2_eff, Hlt2_result = Hlt2_cuts(ntp, tree)

    trigger_eff = sum(logical_and(L0_result,
                                  logical_and(Hlt1_result, Hlt2_result)))

    with open(input_yml) as f:
        result = yaml.safe_load(f)

    # Update the output of the final DaVinci cut
    for k, v in result.items():
        if v['output'] == 'None':
            v['output'] = size
        result[k] = v

    # Update the L0/Hlt cuts
    result['L0'] = {'input': size, 'output': L0_eff}
    result['Hlt1'] = {'input': size, 'output': Hlt1_eff}
    result['Hlt2'] = {'input': size, 'output': Hlt2_eff}
    result['Trigger'] = {'input': size, 'output': trigger_eff}

    with open(output_yml, 'w') as f:
        f.write(yaml_gen(result))

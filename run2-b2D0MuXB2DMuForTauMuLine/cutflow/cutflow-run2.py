#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Apr 06, 2020 at 09:05 PM +0800

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


def alt_name(dct):
    rename = {
        'SeqMyB0': 'Total events',
        'StrippedBCands': r'Stripped $D^0 \mu^-$',
        'SelMyD0': r'$D^0 \rightarrow K^- \pi^+$ (tigter $K \pi$)',
        'SelMyDst': r'$D^{*+} \rightarrow D^0 \pi^+$',
        'SelMyB0': r'$\bar{B}^0 \rightarrow D^{*+} \mu^-$',
        'SelMyRefitB02DstMu': r'Refit $\bar{B}^0$ decay tree',
        'Mu_pid': r'$\mu$ PID',
        'Y_isolation': r'$\text{IsoBDT}_{\Upsilon(\text{4s})} < 0.15$',
        'Y_mass': r'$m_{\Upsilon(\text{4s})} < 5280$'
    }

    for key, val in dct.items():
        if key in rename.keys():
            val['name'] = rename[key]


#######################
# Cuts made in step 2 #
#######################

def Mu_pid(ntp, tree):
    muplus_isMuon = read_branch(ntp, tree, 'muplus_isMuon')
    muplus_PIDmu = read_branch(ntp, tree, 'muplus_PIDmu')
    muplus_PIDmu_bool = muplus_PIDmu > 2

    result = logical_and(muplus_isMuon, muplus_PIDmu_bool)
    return sum(result), result


def Y_isolation_cut(ntp, tree):
    Y_ISOLATION_BDT = read_branch(ntp, tree, 'Y_ISOLATION_BDT')
    result = Y_ISOLATION_BDT < 0.15
    return sum(result), result


def Y_mass_cut(ntp, tree):
    Y_M = read_branch(ntp, tree, 'Y_M')
    result = Y_M < 5280
    return sum(result), result


####################################
# LL/HLT efficiencies from n-tuple #
####################################

# L0Cuts: muplus_L0Global_TIS && (Y_L0Global_TIS || Dst_L0HadronDecision_TOS)
# NOTE: We also made this cut for step 2 ntuple.
def L0_cuts(ntp, tree):
    muplus_L0Global_TIS = read_branch(ntp, tree, 'muplus_L0Global_TIS')
    Y_L0Global_TIS = read_branch(ntp, tree, 'Y_L0Global_TIS')
    Dst_L0HadronDecision_TOS = read_branch(
        ntp, tree, 'Dst_2010_minus_L0HadronDecision_TOS')

    result = logical_and(muplus_L0Global_TIS,
                         logical_or(Y_L0Global_TIS, Dst_L0HadronDecision_TOS))
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
    ntp_path, input_yml, output_yml = sys.argv[1:]

    ntp = uproot.open(ntp_path)
    tree = 'TupleB0/DecayTree'
    size = total_num(ntp, tree)
    uniq_size = total_num_dedupl(ntp, tree)

    # Trigger cuts #############################################################
    L0_eff, L0_result = L0_cuts(ntp, tree)
    Hlt1_eff, Hlt1_result = Hlt1_cuts(ntp, tree)
    Hlt2_eff, Hlt2_result = Hlt2_cuts(ntp, tree)

    # HLT 1 on top of L0
    Hlt1_L0_result = logical_and(L0_result, Hlt1_result)
    Hlt1_L0_eff = sum(Hlt1_L0_result)

    # HLT 2 on top of HLT 1 (a.k.a: trigger cuts)
    trigger_result = logical_and(Hlt1_L0_result, Hlt2_result)
    trigger_eff = sum(trigger_result)

    # Step 2 cuts ##############################################################
    Mu_pid_eff, Mu_pid_result = Mu_pid(ntp, tree)
    Y_isolation_cut_eff, Y_isolation_cut_result = Y_isolation_cut(ntp, tree)
    Y_mass_cut_eff, Y_mass_cut_result = Y_mass_cut(ntp, tree)

    # Muon PID cuts on top of trigger cuts
    Mu_pid_trigger_result = logical_and(trigger_result, Mu_pid_result)
    Mu_pid_trigger_eff = sum(Mu_pid_trigger_result)

    # Y isolation cut on top of Muon PID
    Y_isolation_cut_Mu_pid_result = logical_and(Mu_pid_trigger_result,
                                                Y_isolation_cut_result)
    Y_isolation_cut_Mu_pid_eff = sum(Y_isolation_cut_Mu_pid_result)

    # Y mass cut on top of Y isolation (a.k.a: step 2 cuts)
    step2_result = logical_and(Y_isolation_cut_Mu_pid_result, Y_mass_cut_result)
    step2_eff = sum(step2_result)

    with open(input_yml) as f:
        result = yaml.safe_load(f)

    # Update the output of the final DaVinci cut
    for k, v in result.items():
        if v['output'] == 'None':
            v['output'] = uniq_size  # Here we are only considering events passing the refitting procedure
        result[k] = v

    # Update the L0/Hlt cuts
    result['L0'] = {'input': size, 'output': L0_eff}
    result['Hlt1'] = {'input': L0_eff, 'output': Hlt1_L0_eff}
    result['Hlt2'] = {'input': Hlt1_L0_eff, 'output': trigger_eff}

    # Update step-2 cuts
    result['Mu_pid'] = {'input': trigger_eff, 'output': Mu_pid_trigger_eff}
    result['Y_isolation'] = {'input': Mu_pid_trigger_eff,
                             'output': Y_isolation_cut_Mu_pid_eff}
    result['Y_mass'] = {'input': Y_isolation_cut_Mu_pid_eff,
                        'output': step2_eff}

    alt_name(result)

    with open(output_yml, 'w') as f:
        f.write(yaml_gen(result))

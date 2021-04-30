#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri Apr 30, 2021 at 04:42 AM +0200

import pathlib
import os

pwd = pathlib.Path(__file__).parent.absolute()
header_path = (pwd / '../../include').resolve()
os.environ['ROOT_INCLUDE_PATH'] = str(header_path)

from argparse import ArgumentParser
from ROOT import RDataFrame

from TrackerOnlyEmu.executor import ExecDirective as EXEC
from TrackerOnlyEmu.executor import process_directives
from TrackerOnlyEmu.loader import load_cpp


#################
# Configurables #
#################

TREES = [
    'TupleB0/DecayTree'
]


#################################
# Command line arguments parser #
#################################

def parse_input():
    parser = ArgumentParser(
        description='Find selection efficiencies for RDX run 2.')

    parser.add_argument('input', help='''
specify input ntuple file.''')

    parser.add_argument('-o', '--output-dir',
                        default=None, help='''
optionally specify output ntuple file.''')

    return parser.parse_args()


###########
# Helpers #
###########

load_cpp('<functor/rdx/flag.h>', current_file_path=str(header_path / 'dummy'))


def normalize_tree_name(tree_name):
    return tree_name.replace('/', '_').lower()


##############
# Selections #
##############

sel_d0 = [
    EXEC('Define', 'k_pt', 'k_PT / 1e3', True),
    EXEC('Define', 'pi_pt', 'pi_PT / 1e3', True),
    EXEC('Define', 'k_p', 'k_P / 1e3', True),
    EXEC('Define', 'pi_p', 'pi_P / 1e3', True),

    # Trigger is a bit different than what we plan to use
    EXEC('Define', 'k_hlt1_tos',
         'k_Hlt1TwoTrackMVADecision_TOS || k_Hlt1TrackMVALooseDecision_TOS',
         True),
    EXEC('Define', 'pi_hlt1_tos',
         'pi_Hlt1TwoTrackMVADecision_TOS || pi_Hlt1TrackMVALooseDecision_TOS',
         True),

    EXEC('Define', 'k_ip_chi2', 'k_IPCHI2_OWNPV', True),
    EXEC('Define', 'pi_ip_chi2', 'pi_IPCHI2_OWNPV', True),

    # Dummy PID variables to make sure everything is true
    EXEC('Define', 'k_pid_k', '6.0', True),
    EXEC('Define', 'pi_pid_k', '0.0', True),
    EXEC('Define', 'mu_veto', 'false', True),

    EXEC('Define', 'k_gh_prob', 'k_TRACK_GhostProb', True),
    EXEC('Define', 'pi_gh_prob', 'pi_TRACK_GhostProb', True),

    EXEC('Define', 'd0_pt', 'd0_PT / 1e3', True),
    EXEC('Define', 'd0_hlt2', 'd0_Hlt2XcMuXForTauB2XcMuDecision_TOS', True),
    EXEC('Define', 'd0_endvtx_chi2', 'd0_ENDVERTEX_CHI2', True),
    EXEC('Define', 'd0_endvtx_ndof', 'd0_ENDVERTEX_NDOF', True),
    EXEC('Define', 'd0_ip', 'd0_IP_OWNPV', True),
    EXEC('Define', 'd0_ip_chi2', 'd0_IPCHI2_OWNPV', True),
    EXEC('Define', 'd0_dira', 'd0_DIRA_OWNPV', True),
    EXEC('Define', 'd0_fd_chi2', 'd0_FDCHI2_OWNPV', True),
    EXEC('Define', 'd0_m', 'd0_M', True),

    EXEC('Define', 'sel_d0', '''
FLAG_SEL_D0_RUN1(k_pt, pi_pt,
                 k_p, pi_p,
                 k_hlt1_tos, pi_hlt1_tos,
                 k_ip_chi2, pi_ip_chi2,
                 k_pid_k, pi_pid_k,
                 k_gh_prob, pi_gh_prob,
                 mu_veto,
                 d0_pt,
                 d0_hlt2,
                 d0_endvtx_chi2, d0_endvtx_ndof,
                 d0_ip, d0_ip_chi2,
                 d0_dira,
                 d0_fd_chi2,
                 d0_m)
         ''', True),
]


if __name__ == '__main__':
    args = parse_input()

    for tree in TREES:
        init_frame = RDataFrame(tree, args.input)
        dfs, output_br_names = process_directives(sel_d0, init_frame)

        # Debug only
        if args.output_dir:
            output_ntp = args.output_dir + '/' + normalize_tree_name(tree) + \
                '.root'
            dfs[-1].Snapshot(tree, output_ntp, output_br_names)

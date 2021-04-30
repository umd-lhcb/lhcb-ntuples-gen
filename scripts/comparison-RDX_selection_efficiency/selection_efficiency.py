#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri Apr 30, 2021 at 03:07 PM +0200

import pathlib
import os

pwd = pathlib.Path(__file__).parent.absolute()
header_path = (pwd / '../../include').resolve()
os.environ['ROOT_INCLUDE_PATH'] = str(header_path)

from argparse import ArgumentParser
from ROOT import RDataFrame

from TrackerOnlyEmu.executor import ExecDirective as EXEC
from TrackerOnlyEmu.executor import process_directives
from TrackerOnlyEmu.executor import merge_vectors
from TrackerOnlyEmu.loader import load_cpp


#################
# Configurables #
#################

TREES = {
    'TupleB0/DecayTree': [
        EXEC('Filter', instruct='b0_L0Global_TIS || d0_L0HadronDecision_TOS'),
        EXEC('Filter', instruct='d0_Hlt1TrackMVALooseDecision_TOS || d0_Hlt1TwoTrackMVADecision_TOS'),
        EXEC('Filter', instruct='b0_Hlt2XcMuXForTauB2XcMuDecision_TOS'),
    ]
}


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
load_cpp('<functor/rdx/kinematic.h>',
         current_file_path=str(header_path / 'dummy'))


def normalize_tree_name(tree_name):
    return tree_name.replace('/', '_').lower()


def other_trks_gen(particles):
    v3 = ['{' + ', '.join([p+'_'+br for br in ['PX', 'PY', 'PZ']]) + '}'
          for p in particles]
    return 'std::vector<TVector3> {' + ', '.join(v3) + '}'


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
    EXEC('Define', 'k_pid_k', '6.0'),
    EXEC('Define', 'pi_pid_k', '0.0'),
    EXEC('Define', 'mu_veto', 'false'),

    EXEC('Define', 'k_gh_prob', 'k_TRACK_GhostProb', True),
    EXEC('Define', 'pi_gh_prob', 'pi_TRACK_GhostProb', True),

    EXEC('Define', 'd0_pt', 'd0_PT / 1e3', True),
    EXEC('Define', 'd0_hlt2', 'true', True),  # For run 2, our HLT2 is triggered on B
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

sel_mu = [
    EXEC('Define', 'mu_p', 'mu_P / 1e3', True),
    EXEC('Define', 'mu_eta', 'ETA(mu_P, mu_PZ)', True),

    # Dummy PID variables
    EXEC('Define', 'mu_is_mu', 'true'),
    EXEC('Define', 'mu_pid_mu', '10'),
    EXEC('Define', 'mu_pid_e', '0'),
    EXEC('Define', 'mu_bdt_mu', '0.5'),

    # NOTE: The 'mu_good_trks' are undefined here; it needs to be defined in the
    # actual loop because it depends on the mode we are looking at
    EXEC('Define', 'sel_mu', '''
FLAG_SEL_MU_RUN1(mu_p,
                 mu_eta,
                 mu_is_mu, mu_pid_mu, mu_pid_e, mu_bdt_mu,
                 mu_good_trks)''', True),
]


if __name__ == '__main__':
    args = parse_input()

    for tree, init_dir in TREES.items():
        init_frame = RDataFrame(tree, args.input)
        n_tot = init_frame.Count().GetValue()

        # Filter on trigger first
        dfs_fltr, _ = process_directives(init_dir, init_frame)
        n_fltr = dfs_fltr[-1].Count().GetValue()

        # Filter on D0 selection
        dfs_d0, output_br_names_d0 = process_directives(sel_d0, dfs_fltr[-1])
        df_d0_sel = dfs_d0[-1].Filter('sel_d0')
        n_d0 = df_d0_sel.Count().GetValue()

        # Filter on Mu
        if 'B0' in tree:
            sel_mu_tmp = [
                EXEC('Define', 'v3_mu', 'TVector3(mu_PX, mu_PY, mu_PZ)'),
                EXEC('Define', 'v3_other_trks',
                     other_trks_gen(['k', 'pi', 'spi'])),
                EXEC('Define', 'mu_good_trks',
                     'FLAG_SEL_GOOD_TRACKS(v3_mu, v3_other_trks)', True),
            ]
        elif 'Bminus' in tree:
            sel_mu_tmp = [
                EXEC('Define', 'v3_mu', 'TVector3(mu_PX, mu_PY, mu_PZ)'),
                EXEC('Define', 'v3_other_trks', other_trks_gen(['k', 'pi'])),
                EXEC('Define', 'mu_good_trks',
                     'FLAG_SEL_GOOD_TRACKS(v3_mu, v3_other_trks)'),
            ]

        sel_mu_tmp += sel_mu
        dfs_mu, output_br_names_mu = process_directives(sel_mu_tmp, df_d0_sel)
        df_mu_sel = dfs_mu[-1].Filter('sel_mu')
        n_mu = df_mu_sel.Count().GetValue()

        # Debug only
        if args.output_dir:
            output_br_names = merge_vectors(
                output_br_names_d0, output_br_names_mu)

            final_frame = dfs_mu[-1]
            output_ntp = args.output_dir + '/' + normalize_tree_name(tree) + \
                '.root'
            final_frame.Snapshot(tree, output_ntp, output_br_names)

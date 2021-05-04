#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue May 04, 2021 at 07:02 PM +0200

import pathlib
import os
import sys

# Make ROOT aware of our custom header path
pwd = pathlib.Path(__file__).parent.absolute()
header_path = (pwd / '../../include').resolve()
os.environ['ROOT_INCLUDE_PATH'] = str(header_path)

from argparse import ArgumentParser
from glob import glob
from re import search
from csv import DictReader
from collections import defaultdict

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  # Don't hijack my --help flag!

from ROOT import RDataFrame, gInterpreter

from TrackerOnlyEmu.executor import ExecDirective as EXEC
from TrackerOnlyEmu.executor import process_directives
from TrackerOnlyEmu.executor import merge_vectors


#################
# Configurables #
#################

TREES = {
    'TupleB0/DecayTree': [
        EXEC('Filter', instruct='b0_L0Global_TIS || d0_L0HadronDecision_TOS'),
        EXEC('Filter', instruct='d0_Hlt1TrackMVALooseDecision_TOS || d0_Hlt1TwoTrackMVADecision_TOS'),
        EXEC('Filter', instruct='b0_Hlt2XcMuXForTauB2XcMuDecision_TOS'),
    ],
    'TupleBminus/DecayTree': [
        EXEC('Filter', instruct='b_L0Global_TIS || d0_L0HadronDecision_TOS'),
        EXEC('Filter', instruct='d0_Hlt1TrackMVALooseDecision_TOS || d0_Hlt1TwoTrackMVADecision_TOS'),
        EXEC('Filter', instruct='b_Hlt2XcMuXForTauB2XcMuDecision_TOS'),
    ]
}


#################################
# Command line arguments parser #
#################################

def parse_input():
    parser = ArgumentParser(
        description='Find selection efficiencies for RDX run 2.')

    parser.add_argument('input',
                        nargs='+', help='''
specify input ntuple files and folders.''')

    parser.add_argument('-o', '--output-dir',
                        default=None, help='''
optionally specify output ntuple file.''')

    parser.add_argument('-b', '--blocked-kw',
                        default=['2012', 'TrackerOnly'],
                        help='''
specify blocked keywords in ntuple filenames''')

    parser.add_argument('-c', '--csv',
                        default='sel_eff.csv', help='''
specify output CSV.''')

    parser.add_argument('-r', '--ref-csv',
                        default=None, help='''
specify optional input CSV.''')

    parser.add_argument('-H', '--headers',
                        nargs='+', default=None, help='''
specify ntuple IDs in the generated CSV.''')

    parser.add_argument('-O', '--ordering',
                        default=None, nargs='+', help='''
specify an ordering for MC ntuples.
''')

    return parser.parse_args()


###########
# Helpers #
###########

gInterpreter.Declare('#include "functor/rdx/cut.h"')
gInterpreter.Declare('#include "functor/rdx/kinematic.h"')


def normalize_tree_name(tree_name):
    return tree_name.replace('/', '_').lower()


def other_trks_gen(particles):
    v3 = ['{' + ', '.join([p+'_'+br for br in ['PX', 'PY', 'PZ']]) + '}'
          for p in particles]
    return 'std::vector<TVector3> {' + ', '.join(v3) + '}'


def glob_ntuples(paths, blocked_kw=[]):
    raw = [m for p in paths for m in glob(p)]
    return [m for m in raw if True not in [k in m for k in blocked_kw]]


def find_ntp_id(ntp_name):
    if result := search(r'\d{8}', ntp_name):
        return result.group(0)
    return False


def stat_gen(tree_name, *numbers,
             raw_keys=['DaVinci', 'trigger', 'D0', 'Mu'],
             raw_subkeys=['ISO']):
    if 'B0' in tree_name:
        keys = ['B0 '+k for k in raw_keys]
        keys.append('B0')
        keys += ['B0 '+k for k in raw_subkeys]
    if 'Bminus' in tree_name:
        keys = ['B '+k for k in raw_keys]
        keys.append('B')
        keys += ['B '+k for k in raw_subkeys]

    return dict(zip(keys, numbers))


def csv_read(csv_file, key_row='mode'):
    result = dict()

    with open(csv_file) as f:
        for line in DictReader(f):
            result[line[key_row]] = {k: v for k, v in line.items()
                                     if k != key_row}

    return result


def csv_gen(modes):
    rows = []
    max_header_len = 0

    for mode, attr in modes.items():
        if len(tmp_headers := ['mode'] + list(attr.keys())) > max_header_len:
            headers = tmp_headers
            max_header_len = len(tmp_headers)

        row = [mode] + [str(i) for i in attr.values()]
        rows.append(row)

    return [headers] + rows


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
         'd0_Hlt1TwoTrackMVADecision_TOS || k_Hlt1TrackMVALooseDecision_TOS',
         True),
    EXEC('Define', 'pi_hlt1_tos',
         'd0_Hlt1TwoTrackMVADecision_TOS || pi_Hlt1TrackMVALooseDecision_TOS',
         True),

    EXEC('Define', 'k_ip_chi2', 'k_IPCHI2_OWNPV', True),
    EXEC('Define', 'pi_ip_chi2', 'pi_IPCHI2_OWNPV', True),

    # Dummy PID
    EXEC('Define', 'd0_pid_ok', 'true'),

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
FLAG_SEL_D0_RUN1(d0_pid_ok,
                 k_pt, pi_pt,
                 k_p, pi_p,
                 k_hlt1_tos, pi_hlt1_tos,
                 k_ip_chi2, pi_ip_chi2,
                 k_gh_prob, pi_gh_prob,
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

    EXEC('Define', 'mu_ip_chi2', 'mu_IPCHI2_OWNPV', True),
    EXEC('Define', 'mu_gh_prob', 'mu_TRACK_GhostProb', True),

    # Dummy PID
    EXEC('Define', 'mu_pid_ok', 'true'),

    # NOTE: The 'mu_good_trks' are undefined here; it needs to be defined in the
    # actual loop because it depends on the mode we are looking at
    EXEC('Define', 'sel_mu', '''
FLAG_SEL_MU_RUN1(mu_good_trks, mu_pid_ok,
                 mu_p,
                 mu_eta,
                 mu_ip_chi2, mu_gh_prob)''', True),
]

sel_b0 = [
    EXEC('Define', 'spi_gh_prob', 'spi_TRACK_GhostProb', True),

    EXEC('Define', 'dst_endvtx_chi2', 'dst_ENDVERTEX_CHI2', True),
    EXEC('Define', 'dst_endvtx_ndof', 'dst_ENDVERTEX_NDOF', True),
    EXEC('Define', 'dst_m', 'dst_M', True),

    EXEC('Define', 'b0_discard_mu_chi2', 'b0_DISCARDMu_CHI2', True),
    EXEC('Define', 'b0_endvtx_chi2', 'b0_ENDVERTEX_CHI2', True),
    EXEC('Define', 'b0_endvtx_ndof', 'b0_ENDVERTEX_NDOF', True),
    EXEC('Define', 'v3_b0_flight', '''
TVector3(b0_ENDVERTEX_X - b0_OWNPV_X,
         b0_ENDVERTEX_Y - b0_OWNPV_Y,
         b0_ENDVERTEX_Z - b0_OWNPV_Z
         )'''),
    EXEC('Define', 'b0_fd_trans', 'v3_b0_flight.Perp()', True),
    EXEC('Define', 'b0_dira', 'b0_DIRA_OWNPV', True),
    EXEC('Define', 'b0_m', 'b0_M', True),

    EXEC('Define', 'sel_b', '''
FLAG_SEL_B0DST_RUN1(sel_d0, sel_mu,
                    spi_gh_prob,
                    dst_endvtx_chi2, dst_endvtx_ndof,
                    dst_m, d0_m,
                    b0_discard_mu_chi2,
                    b0_endvtx_chi2, b0_endvtx_ndof,
                    b0_fd_trans,
                    b0_dira,
                    b0_m)''', True),

    EXEC('Define', 'iso_bdt', 'b0_ISOLATION_BDT'),
]

sel_bminus = [
    EXEC('Define', 'b_endvtx_chi2', 'b_ENDVERTEX_CHI2', True),
    EXEC('Define', 'b_endvtx_ndof', 'b_ENDVERTEX_NDOF', True),
    EXEC('Define', 'v3_b_flight', '''
TVector3(b_ENDVERTEX_X - b_OWNPV_X,
         b_ENDVERTEX_Y - b_OWNPV_Y,
         b_ENDVERTEX_Z - b_OWNPV_Z
         )'''),
    EXEC('Define', 'b_fd_trans', 'v3_b_flight.Perp()', True),
    EXEC('Define', 'b_dira', 'b_DIRA_OWNPV', True),
    EXEC('Define', 'b_m', 'b_M', True),

    EXEC('Define', 'mu_px', 'mu_PX'),  # These need to be in MeV
    EXEC('Define', 'mu_py', 'mu_PY'),  # These need to be in MeV
    EXEC('Define', 'mu_pz', 'mu_PZ'),  # These need to be in MeV
    EXEC('Define', 'd0_px', 'd0_PX'),
    EXEC('Define', 'd0_py', 'd0_PY'),
    EXEC('Define', 'd0_pz', 'd0_PZ'),

    EXEC('Define', 'sel_b', '''
FLAG_SEL_BMINUSD0_RUN1(sel_d0, sel_mu,
                       b_endvtx_chi2, b_endvtx_ndof,
                       b_fd_trans,
                       b_dira,
                       b_m,
                       mu_px, mu_py, mu_pz,
                       d0_px, d0_py, d0_pz,
                       d0_m)''', True),

    EXEC('Define', 'iso_bdt', 'b_ISOLATION_BDT'),
]


if __name__ == '__main__':
    args = parse_input()
    ntps = glob_ntuples(args.input, args.blocked_kw)

    if args.ordering:
        ntps_ord = {find_ntp_id(n): n for n in ntps}
        ntps = [ntps_ord[i] for i in args.ordering]

    if not ntps:
        print('No input ntuple retained after filtering on blocked keywords.')
        sys.exit(1)

    ids = args.headers if args.headers else list(range(0, len(ntps)))

    if args.ref_csv:
        all_modes = csv_read(args.ref_csv)
    else:
        all_modes = defaultdict(dict)

    for ntp, alt_id in zip(ntps, ids):
        ntp_id = find_ntp_id(ntp)  # This works for MC only

        if not ntp_id:
            print('Use ID specified in cli: {}'.format(alt_id))
            ntp_id = alt_id

        for tree, init_dir in TREES.items():
            init_frame = RDataFrame(tree, ntp)
            n_tot = init_frame.Count().GetValue()

            # Filter on trigger first
            dfs_fltr, _ = process_directives(init_dir, init_frame)
            n_fltr = dfs_fltr[-1].Count().GetValue()

            # Filter on D0 selection
            dfs_d0, output_br_names_d0 = process_directives(
                sel_d0, dfs_fltr[-1])
            df_d0_sel = dfs_d0[-1].Filter('sel_d0')
            n_d0 = df_d0_sel.Count().GetValue()

            if 'B0' in tree:
                sel_mu_tmp = [
                    EXEC('Define', 'v3_mu', 'TVector3(mu_PX, mu_PY, mu_PZ)'),
                    EXEC('Define', 'v3_other_trks',
                         other_trks_gen(['k', 'pi', 'spi'])),
                    EXEC('Define', 'mu_good_trks',
                         'FLAG_SEL_GOOD_TRACKS(v3_mu, v3_other_trks)', True),
                ]
                sel_b = sel_b0
            elif 'Bminus' in tree:
                sel_mu_tmp = [
                    EXEC('Define', 'v3_mu', 'TVector3(mu_PX, mu_PY, mu_PZ)'),
                    EXEC('Define', 'v3_other_trks',
                         other_trks_gen(['k', 'pi'])),
                    EXEC('Define', 'mu_good_trks',
                         'FLAG_SEL_GOOD_TRACKS(v3_mu, v3_other_trks)'),
                ]
                sel_b = sel_bminus

            # Filter on Mu
            sel_mu_tmp += sel_mu
            dfs_mu, output_br_names_mu = process_directives(
                sel_mu_tmp, df_d0_sel)
            df_mu_sel = dfs_mu[-1].Filter('sel_mu')
            n_mu = df_mu_sel.Count().GetValue()

            # Filter on reconstructed B (D meson + Muon combo)
            dfs_b, output_br_names_b = process_directives(sel_b, df_mu_sel)
            df_b_sel = dfs_b[-1].Filter('sel_b')
            n_b = df_b_sel.Count().GetValue()

            # Filter on isolation BDT
            df_iso_sel = df_b_sel.Filter('iso_bdt < 0.15')
            n_iso = df_iso_sel.Count().GetValue()

            all_modes[ntp_id].update(stat_gen(
                tree, n_tot, n_fltr, n_d0, n_mu, n_b, n_iso))

            # Debug only
            if args.output_dir:
                output_br_names = merge_vectors(
                    output_br_names_d0, output_br_names_mu, output_br_names_b)

                final_frame = dfs_b[-1]
                output_ntp = args.output_dir + '/' + \
                    normalize_tree_name(tree) + '.root'
                final_frame.Snapshot(tree, output_ntp, output_br_names)

    with open(args.csv, 'w') as f:
        for row in csv_gen(all_modes):
            f.write(','.join(row)+'\n')

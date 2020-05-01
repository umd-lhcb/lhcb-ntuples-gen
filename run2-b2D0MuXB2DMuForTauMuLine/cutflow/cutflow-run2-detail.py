#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri May 01, 2020 at 08:34 PM +0800

import uproot
import sys

from argparse import ArgumentParser
from pyTuplingUtils.io import yaml_gen
from pyTuplingUtils.utils import extract_uid, tabl as TAB
from pyTuplingUtils.cutflow import CutflowGen, CutflowRule as Rule


L0 = [
    'L0DiMuonDecision',
    'L0ElectronDecision',
    'L0HadronDecision',
    'L0JetElDecision',
    'L0JetPhDecision',
    'L0MuonDecision',
    'L0MuonEWDecision',
    'L0PhotonDecision',
    'L0Global',  # This needs to be placed to the last
]

HLT1 = [
    'Hlt1TwoTrackMVADecision',
    'Hlt1TrackMVALooseDecision',
    'Hlt1TwoTrackMVALooseDecision',
    'Hlt1TrackMuonDecision',
    'Hlt1TrackMuonMVADecision',
    'Hlt1SingleMuonHighPTDecision',
    'Hlt1Phys'  # This needs to be placed to the last
]


###########
# Helpers #
###########

def simplify_line(line, remove='Decision'):
    return line.replace(remove, '')


def remove_from(lst, remove=None):
    return [i for i in lst if i != remove]


def cut_gen(line, particle='Y', tistos='TIS', particle_name=r'$\Upsilon(4s)$'):
    cut = '_'.join([particle, line, tistos])
    name = '{} {} {}'.format(particle_name, simplify_line(line), tistos)
    return cut, name


def cut_comb(prev_cut, prev_name, *args, **kwargs):
    cut, name = cut_gen(*args, **kwargs)
    return prev_cut+' & ({})'.format(cut), prev_name+'+{}'.format(name)


def cutflow_rule_gen(l0lines=L0, hlt1lines=HLT1, marginal=True):
    basecut, basename = cut_gen(
        'L0HadronDecision', 'Dst_2010_minus', 'TOS', r'$D^*$')
    cutflows = [Rule(basecut, basename)]

    if not marginal:
        for l0 in l0lines:
            cut, name = cut_gen(l0)
            cutflows.append(Rule(cut, name, -1, True))

    for l0 in l0lines:
        l0cut, l0name = cut_comb(basecut, basename, l0)
        cutflows.append(Rule(l0cut, l0name, 0, True))
        ref_idx = len(cutflows) - 1

        if marginal and l0 != 'L0Global':
            for ll0 in remove_from(l0lines, l0):
                ll0cut, ll0name = cut_comb(l0cut, l0name, ll0)
                cutflows.append(Rule(ll0cut, ll0name, 0, True))

    for hlt1 in hlt1lines:
        hlt1cut, hlt1name = cut_comb(l0cut, l0name, hlt1)
        cutflows.append(Rule(hlt1cut, hlt1name, ref_idx, True))

        if marginal and hlt1 != 'Hlt1Phys':
            for hhlt1 in remove_from(hlt1lines, hlt1):
                hhlt1cut, hhlt1name = cut_comb(hlt1cut, hlt1name, hhlt1)
                cutflows.append(Rule(hhlt1cut, hhlt1name, ref_idx, True))

    return cutflows


################################
# Command line argument parser #
################################

def parse_input(descr='Generate cut flow CSV from YAML files.'):
    parser = ArgumentParser(description=descr)

    parser.add_argument('ntp',
                        help='specify ntuple path.')

    parser.add_argument('yaml',
                        help='specify output YAML path.')

    parser.add_argument('-t', '--tree',
                        default='TupleB0/DecayTree',
                        help='specify tree name in the ntuple.'
                        )

    parser.add_argument('-f', '--format',
                        nargs='?',
                        choices=['latex',
                                 'simple',
                                 'github',
                                 'latex_booktabs',
                                 'latex_booktabs_raw',
                                 'latex_raw'],
                        default='github',
                        help='specify the output table format.'
                        )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_input()
    _, _, size, _, _ = extract_uid(uproot.open(args.ntp), args.tree)
    result_marginal = {'DV': {'input': size, 'output': size}}
    result_individual = {'DV': {'input': size, 'output': size}}

    rules_individual = cutflow_rule_gen(marginal=False)
    result_individual_addon = CutflowGen(
        args.ntp, args.tree, rules_individual, size).do()
    result_individual.update(result_individual_addon)

    # print(TAB.tabulate(tab_marginal, headers='firstrow', tablefmt=fmt))
    # print(TAB.tabulate(tab_individual, headers='firstrow', tablefmt=fmt))
    with open(args.yaml, 'w') as f:
        f.write(yaml_gen(result_individual))

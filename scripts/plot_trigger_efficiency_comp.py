#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Tue Apr 13, 2021 at 07:40 PM +0200

import uproot

from argparse import Action
from numpy import logical_and as AND
from numpy import nan_to_num

from pyTuplingUtils.parse import single_ntuple_parser_no_output
from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.io import read_branches, read_branch
from pyTuplingUtils.plot import plot_style, plot_two_histos, ax_add_args_simple


#################################
# Command line arguments parser #
#################################

class DataRangeAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) % 2 != 0:
            raise ValueError('Odd number of min, max pairs!')

        values = [float(v) for v in values]
        min_max_pairs = self.divide_list_in_chunk(values)
        setattr(namespace, self.dest, min_max_pairs)

    @staticmethod
    def divide_list_in_chunk(lst, chunk_size=2):
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


DESCR = '''
generate trigger efficiency comparison plots
'''


def parse_input(descr=DESCR):
    parser = single_ntuple_parser_no_output(descr)

    parser.add_argument('-o', '--output-prefix',
                        required=True,
                        help='''
specify prefix to all output files.
''')

    parser.add_argument('-k', '--kinematic-vars',
                        nargs='+',
                        default=['q2', 'mmiss2', 'el'],
                        help='''
specify efficiency regarding which kinematic variables.
''')

    parser.add_argument('-T', '--triggers',
                        nargs='+',
                        required=True,
                        help='''
specify trigger branches that will be used for efficiency comparison.
''')

    parser.add_argument('-c', '--cuts',
                        nargs='+',
                        default=['d0_l0_global_dec'],
                        help='''
specify triggers to be required True before evaluating efficiency.
''')

    parser.add_argument('-D', '--data-range',
                        nargs='+',
                        default=[(-10, 10), (-10, 8), (0, 3)],
                        action=DataRangeAction,
                        help='''
specify plotting range for the kinematic variables.
''')

    parser.add_argument('--xlabel',
                        nargs='+',
                        default=['$q^2$', '$m_{miss}^2$', '$E_l$'])

    return parser


########
# Main #
########

if __name__ == '__main__':
    args = parse_input().parse_args()

    plot_style(text_usetex=True, font_family='Times')

    ntp = uproot.open(args.ref)

    # Load trigger branches that we cut on
    cut = read_branches(ntp, args.ref_tree, args.cuts)
    if len(cut) > 1:
        cut = AND(cut)
    else:
        cut = cut[0]

    # Load trigger branches that will be used for efficiency comparison
    eff_branches = []
    for br in args.triggers:
        raw = read_branch(ntp, args.ref_tree, br)
        filtered = raw[cut]
        eff_branches.append(filtered)

    # Now generate efficiency plots regarding some kinematic variables
    for br, data_range, xlabel in zip(args.kinematic_vars, args.data_range,
                                      args.xlabel):
        raw = read_branch(ntp, args.ref_tree, br)
        filtered = raw[cut]
        histos = []
        legends = []

        for tr_br in eff_branches:
            histo_orig, bins = gen_histo(
                filtered, bins=25, data_range=data_range)
            histo_weighted, bins = gen_histo(
                filtered, bins=25, data_range=data_range,
                weights=tr_br.astype(int))

            # Replace NaN with 0
            histos.append(nan_to_num(histo_weighted / histo_orig))
            legends.append(dict())

        filename = '_'.join([args.output_prefix, br])

        plot_two_histos(
            histos[0], bins, histos[1], bins,
            dict(), dict(), output=filename, ylabel='Efficiency', xlabel=xlabel)

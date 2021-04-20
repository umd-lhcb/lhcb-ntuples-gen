#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Tue Apr 20, 2021 at 07:19 PM +0200

import uproot
import numpy as np

from argparse import Action
from numpy import logical_and as AND
from numpy import nan_to_num
from statsmodels.stats.proportion import proportion_confint

from pyTuplingUtils.parse import single_ntuple_parser_no_output
from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.io import read_branches, read_branch
from pyTuplingUtils.plot import plot_style, plot_two_errorbar


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
                        default=['q2',
                                 'mmiss2',
                                 'el',
                                 'k_p', 'k_pt',
                                 'pi_p', 'pi_pt',
                                 'k_chi2ndof', 'k_ipchi2', 'k_ghost',
                                 'pi_chi2ndof', 'pi_ipchi2', 'pi_ghost',
                                 ],
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
                        nargs='*',
                        default=['d0_l0_global_dec'],
                        help='''
specify triggers to be required True before evaluating efficiency.
''')

    parser.add_argument('-D', '--data-range',
                        nargs='+',
                        default=[
                            (-10, 10),
                            (-10, 8),
                            (0, 3),
                            (0, 200), (0, 15),
                            (0, 200), (0, 15),
                            (0, 4), (0, 10000), (0, 0.4),
                            (0, 4), (0, 10000), (0, 0.4),
                        ],
                        action=DataRangeAction,
                        help='''
specify plotting range for the kinematic variables.
''')

    parser.add_argument('--xlabel',
                        nargs='+',
                        default=[
                            '$q^2$ [GeV$^2$]',
                            '$m_{miss}^2$ [GeV$^2$]',
                            '$E_l$ [GeV]',
                            '$K$ $p$ [GeV]', '$K$ $p_T$ [GeV]',
                            '$\\pi$ $p$ [GeV]', '$\\pi$ $p_T$ [GeV]',
                            '$K$ $\\chi^2/DOF$', '$K$ IP$\\chi^2$', '$K$ Ghost Prob',
                            '$\\pi$ $\\chi^2/DOF$', '$\\pi$ IP$\\chi^2$', '$\\pi$ Ghost Prob',
                        ],
                        help='''
specify the x axis label.
''')

    parser.add_argument('--legends',
                        nargs='+',
                        default=['Real response', 'Emulated'],
                        help='''
specify legend labels.
''')

    parser.add_argument('--title',
                        help='''
specify title of the plot.
''')

    parser.add_argument('--colors',
                        nargs='+',
                        default=['red', 'blue'],
                        help='''
specify plot colors.
''')

    parser.add_argument('--ext',
                        nargs='+',
                        default=['pdf', 'png'],
                        help='''
specify output filetypes.
''')

    return parser


########
# Main #
########

def errorbar_style(label, color, yerr=None):
    return {
        'label': label,
        'ls': 'none',
        'color': color,
        'marker': 'o',
        'markeredgecolor': 'none',
        'yerr': yerr,
    }


def div_with_confint(num, denom):
    ratio = num / denom
    intv = proportion_confint(num, denom, method='beta', alpha=0.05)
    err = np.abs(intv - ratio)  # Errors are allowed to be asymmetrical

    return nan_to_num(ratio), nan_to_num(err)


if __name__ == '__main__':
    args = parse_input().parse_args()

    plot_style(text_usetex=True, font_family='Times')

    ntp = uproot.open(args.ref)

    # Load trigger branches that we cut on
    if args.cuts:
        cut = read_branches(ntp, args.ref_tree, args.cuts)
        if len(cut) > 1:
            cut = AND(cut)
        else:
            cut = cut[0]
    else:
        evt_num = read_branch(ntp, args.ref_tree, 'runNumber')
        cut = np.array([True]*evt_num.size)

    # Load trigger branches that will be used for efficiency comparison
    eff_branches = []
    for br in args.triggers:
        raw = read_branch(ntp, args.ref_tree, br)
        filtered = raw[cut]
        eff_branches.append(filtered)

    # Now generate efficiency plots regarding some kinematic variables
    for br, data_range, xlabel in zip(
            args.kinematic_vars, args.data_range, args.xlabel):
        raw = read_branch(ntp, args.ref_tree, br)
        filtered = raw[cut]
        histos = []
        styles = []

        for tr_br, color, legend in zip(
                eff_branches, args.colors, args.legends):
            histo_orig, bins = gen_histo(
                filtered, bins=25, data_range=data_range)
            histo_weighted, bins = gen_histo(
                filtered, bins=25, data_range=data_range,
                weights=tr_br.astype(np.double))

            histo, error = div_with_confint(histo_weighted, histo_orig)
            histos.append(histo)
            styles.append(errorbar_style(legend, color, yerr=error))

        for ext in args.ext:
            filename = '_'.join([
                args.output_prefix, args.title.replace(' ', '_'), br]) + \
                '.' + ext

            plot_two_errorbar(
                bins, histos[0], bins, histos[1], *styles,
                output=filename,
                ylabel='Efficiency', xlabel=xlabel,
                title=args.title
            )

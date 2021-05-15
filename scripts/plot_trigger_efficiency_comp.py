#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Sat May 15, 2021 at 02:29 AM +0200

import uproot
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep

from argparse import Action
from numpy import logical_and as AND
from numpy import nan_to_num
from statsmodels.stats.proportion import proportion_confint

from pyTuplingUtils.parse import single_ntuple_parser_no_output
from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.io import read_branches, read_branch
from pyTuplingUtils.plot import plot_style, plot_top_errorbar_bot_errorbar
from pyTuplingUtils.plot import ax_add_args_errorbar as errorbar_style


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
                        default=['q2', 'mmiss2', 'el',
                                 'k_p', 'k_pt',
                                 'pi_p', 'pi_pt',
                                 'mu_p', 'mu_pt',
                                 'k_chi2ndof', 'k_ipchi2', 'k_ghost',
                                 'pi_chi2ndof', 'pi_ipchi2', 'pi_ghost',
                                 'mu_chi2ndof', 'mu_ipchi2', 'mu_ghost',
                                 'k_theta', 'pi_theta', 'mu_theta',
                                 'k_phi', 'pi_phi', 'mu_phi',
                                 'nspd_hits',
                                 'mva_score_1_2', 'mva_score_1_3',
                                 'mva_score_1_4', 'mva_score_2_3',
                                 'mva_score_2_4', 'mva_score_3_4',
                                 'k_pi_apt',
                                 'mva_doca_1_2', 'mva_doca_1_3',
                                 'mva_doca_1_4', 'mva_doca_2_3',
                                 'mva_doca_2_4', 'mva_doca_3_4',
                                 'mva_dira_1_2', 'mva_dira_1_3',
                                 'mva_dira_1_4', 'mva_dira_2_3',
                                 'mva_dira_2_4', 'mva_dira_3_4',
                                 'mva_eta_1_2', 'mva_eta_1_3',
                                 'mva_eta_1_4', 'mva_eta_2_3',
                                 'mva_eta_2_4', 'mva_eta_3_4',
                                 'mva_vertex_chi2_1_2', 'mva_vertex_chi2_1_3',
                                 'mva_vertex_chi2_1_4', 'mva_vertex_chi2_2_3',
                                 'mva_vertex_chi2_2_4', 'mva_vertex_chi2_3_4',
                                 'mva_mcorr_1_2', 'mva_mcorr_1_3',
                                 'mva_mcorr_1_4', 'mva_mcorr_2_3',
                                 'mva_mcorr_2_4', 'mva_mcorr_3_4',
                                 ],
                        help='''
specify efficiency regarding which kinematic variables.
''')

    parser.add_argument('--xlabel',
                        nargs='+',
                        default=[
                            '$q^2$ [GeV$^2$]', '$m_{miss}^2$ [GeV$^2$]', '$E_l$ [GeV]',
                            '$K$ $p$ [GeV]', '$K$ $p_T$ [GeV]',
                            '$\\pi$ $p$ [GeV]', '$\\pi$ $p_T$ [GeV]',
                            '$\\mu$ $p$ [GeV]', '$\\mu$ $p_T$ [GeV]',
                            '$K$ $\\chi^2/DOF$', '$K$ IP$\\chi^2$', '$K$ Ghost Prob',
                            '$\\pi$ $\\chi^2/DOF$', '$\\pi$ IP$\\chi^2$', '$\\pi$ Ghost Prob',
                            '$\\mu$ $\\chi^2/DOF$', '$\\mu$ IP$\\chi^2$', '$\\mu$ Ghost Prob',
                            '$K$ $\\theta$', '$\\pi$ $\\theta$', '$\\mu$ $\\theta$',
                            '$K$ $\\phi$', '$\\pi$ $\\phi$', '$\\mu$ $\\phi$',
                            'Number of SPD hits',
                            'MVA score 1,2', 'MVA score 1,3',
                            'MVA score 1,4', 'MVA score 2,3',
                            'MVA score 2,4', 'MVA score 3,4',
                            '$K-\\pi$ Sum $P_T$ [GeV]',
                            'MVA DOCA 1,2', 'MVA DOCA 1,3',
                            'MVA DOCA 1,4', 'MVA DOCA 2,3',
                            'MVA DOCA 2,4', 'MVA DOCA 3,4',
                            'MVA DIRA 1,2', 'MVA DIRA 1,3',
                            'MVA DIRA 1,4', 'MVA DIRA 2,3',
                            'MVA DIRA 2,4', 'MVA DIRA 3,4',
                            'MVA $\\eta$ 1,2', 'MVA $\\eta$ 1,3',
                            'MVA $\\eta$ 1,4', 'MVA $\\eta$ 2,3',
                            'MVA $\\eta$ 2,4', 'MVA $\\eta$ 3,4',
                            'MVA Vertex$\\chi^2$ 1,2', 'MVA Vertex$\\chi^2$ 1,3',
                            'MVA Vertex$\\chi^2$ 1,4', 'MVA Vertex$\\chi^2$ 2,3',
                            'MVA Vertex$\\chi^2$ 2,4', 'MVA Vertex$\\chi^2$ 3,4',
                            'MVA MCORR 1,2', 'MVA MCORR 1,3',
                            'MVA MCORR 1,4', 'MVA MCORR 2,3',
                            'MVA MCORR 2,4', 'MVA MCORR 3,4',
                        ],
                        help='''
specify the x axis label.
''')

    parser.add_argument('-D', '--data-range',
                        nargs='+',
                        default=[
                            (-5, 15), (-6, 12), (0, 4),
                            (0, 150), (0, 15),
                            (0, 150), (0, 15),
                            (0, 150), (0, 15),
                            (0, 4), (0, 10000), (0, 0.4),
                            (0, 4), (0, 10000), (0, 0.4),
                            (0, 4), (0, 10000), (0, 0.4),
                            (0, 0.35), (0, 0.35), (0, 0.35),
                            (-1.6, 1.6), (-1.6, 1.6), (-1.6, 1.6),
                            (0, 500),
                            (0.9, 1), (0.9, 1),
                            (0.9, 1), (0.9, 1),
                            (0.9, 1), (0.9, 1),
                            (10, 30),
                            (-5, 15), (-5, 15),
                            (-5, 15), (-5, 15),
                            (-5, 15), (-5, 15),
                            (-1, 1), (-1, 1),
                            (-1, 1), (-1, 1),
                            (-1, 1), (-1, 1),
                            (2, 5), (2, 5),
                            (2, 5), (2, 5),
                            (2, 5), (2, 5),
                            (0, 12), (0, 12),
                            (0, 12), (0, 12),
                            (0, 12), (0, 12),
                            (80, 1.1e10), (80, 1.1e10),
                            (80, 1.1e10), (80, 1.1e10),
                            (80, 1.1e10), (80, 1.1e10),
                        ],
                        action=DataRangeAction,
                        help='''
specify plotting range for the kinematic variables.
''')

    parser.add_argument('--triggers',
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

    parser.add_argument('--ax2-ylabel',
                        default='Emulated / Real',
                        help='''
specify y label for the ratio plot.
''')

    parser.add_argument('--bins',
                        default=25,
                        type=int,
                        help='''
specify number of bins.
''')

    return parser


###########
# Helpers #
###########

def div_with_confint(num, denom):
    ratio = num / denom
    intv = proportion_confint(num, denom, method='beta', alpha=0.05)
    err = np.abs(intv - ratio)  # Errors are allowed to be asymmetrical

    return nan_to_num(ratio), nan_to_num(err)


########
# Main #
########

if __name__ == '__main__':
    args = parse_input().parse_args()
    hep.set_style('LHCb2')

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
                filtered, bins=args.bins, data_range=data_range)
            histo_weighted, bins = gen_histo(
                filtered, bins=args.bins, data_range=data_range,
                weights=tr_br.astype(np.double))

            histo, error = div_with_confint(histo_weighted, histo_orig)
            histos.append(histo)
            styles.append(errorbar_style(legend, color, yerr=error))

        # Compute the ratio
        ratio = histos[1] / histos[0]

        for ext in args.ext:
            filename = '_'.join([
                args.output_prefix, args.title.replace(' ', '_'), br]) + \
                '.' + ext

            plot_top_errorbar_bot_errorbar(
                bins, histos[0], bins, histos[1], bins, ratio,
                styles[0], styles[1],
                output=filename,
                title=args.title,
                xlabel=xlabel,
                ax1_ylabel='Efficiency', ax2_ylabel=args.ax2_ylabel,
                hline_pos=1,
                xlim=data_range
            )

            # Clear plot in memory
            plt.close('all')

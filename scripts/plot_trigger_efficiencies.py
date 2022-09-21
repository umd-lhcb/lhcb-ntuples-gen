#!/usr/bin/env python3
#
# Author: Yipeng Sun
# Last Change: Tue Sep 20, 2022 at 11:50 PM -0400

import sys
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep

from numpy import nan_to_num
from statsmodels.stats.proportion import proportion_confint

from pyTuplingUtils.argparse import (
    single_branch_parser_no_output, DataRangeAction, split_ntp_tree)
from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.plot import (
    plot_errorbar, plot_step, plot_fill, plot_top, plot_top_bot,
    ax_add_args_errorbar, ax_add_args_step, ax_add_args_fill
)
from pyTuplingUtils.boolean.eval import BooleanEvaluator


#################################
# Command line arguments parser #
#################################

def parse_input(descr='generate trigger efficiency comparison plots'):
    parser = single_branch_parser_no_output(descr)

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
                        help='specify efficiency regarding which kinematic variables.')

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
                        help='specify the x-axis label.')

    parser.add_argument('-D', '--data-range',
                        nargs='+',
                        default=[
                            (-3, 11), (-6, 12), (0, 4),
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
                        help='specify plotting range for the kinematic variables.')

    parser.add_argument('-Y', '--yrange',
                        nargs='+',
                        default=None,
                        action=DataRangeAction,
                        help='specify y plotting range.'
                        )

    parser.add_argument('-o', '--output-prefix',
                        required=True,
                        help='specify prefix to all output files.')

    parser.add_argument('--ax1-ylabel',
                        default='Efficiency',
                        help='specify y-axis label for the top plot.')

    parser.add_argument('--ax2-ylabel',
                        default='Emulated / Real',
                        help='specify y-axis label for the bottom plot.')

    parser.add_argument('--ax1-yscale',
                        default='linear',
                        choices=['linear', 'log'],
                        help='specify y-axis scale for the top plot.')

    parser.add_argument('--ratio-plot',
                        action='store_true',
                        help='show the bottom ratio plot.')

    parser.add_argument('--errorbar-plot',
                        action='store_true',
                        help='Use error-bar plots instead of step plots.')

    parser.add_argument('--title',
                        default=None,
                        help='specify title of the plot.')

    parser.add_argument('--ext',
                        nargs='+',
                        default=['pdf', 'png'],
                        help='specify output filetypes.')

    parser.add_argument('-c', '--cuts',
                        nargs='+',
                        action='append',
                        default=None,
                        help='specify triggers to be required True before evaluating efficiency.')

    parser.add_argument('--default-cut',
                        default='true',
                        help='default cut to fill for cuts')

    parser.add_argument('-l', '--legends',
                        nargs='+',
                        action='append',
                        default=None,
                        help='specify legend labels.')

    parser.add_argument('--colors',
                        nargs='+',
                        action='append',
                        default=None,
                        help='specify plot colors.')

    return parser.parse_args()


###########
# Helpers #
###########

def div_with_confint(num, denom):
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = num / denom
        intv = proportion_confint(num, denom, method='beta', alpha=0.05)
        err = np.abs(intv - ratio)  # Errors are allowed to be asymmetrical

    return nan_to_num(ratio), nan_to_num(err), nan_to_num(intv)


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()
    hep.style.use('LHCb2')

    top_plotters = dict()
    bot_plotters = dict()
    ref_histos = dict()

    if not args.colors:
        good_colors = ['black', 'crimson', 'mediumblue', 'darkgoldenrod']
        good_colors.reverse()
        try:
            args.colors = [[good_colors.pop() for _ in br]
                           for br in args.ref_branch]
        except IndexError:
            print('No color specified and we are running out of default colors.')
            print('Please specify plot colors manually.')
            sys.exit(255)

    if not args.legends:
        default_legends = [
            'Real response', 'Emulated', 'BDT']
        default_legends.reverse()

        try:
            args.legends = [[default_legends.pop() for _ in br]
                            for br in args.ref_branch]
        except IndexError:
            print('No legend specified and we are running out of default legends.')
            print('Please specify plot legends manually.')
            sys.exit(255)

    if not args.cuts:
        args.cuts = [[args.default_cut]*len(br) for br in args.ref_branch]

    for ntp_tree, trigger_branches, colors, legends, cuts in zip(
            args.ref, args.ref_branch, args.colors, args.legends, args.cuts):
        ntp_name, tree = split_ntp_tree(ntp_tree)
        cutter = BooleanEvaluator(ntp_name, tree)

        for k_br_name, d_range in zip(args.kinematic_vars, args.data_range):
            for tr_br_name, cut, clr, lbl in zip(
                    trigger_branches, cuts, colors, legends):
                tr_br = cutter.eval(tr_br_name)[cutter.eval(cut)]
                k_br = cutter.eval(k_br_name)[cutter.eval(cut)]

                histo_orig, bins = gen_histo(
                    k_br, bins=args.bins, data_range=d_range)
                histo_weighted, _ = gen_histo(
                    k_br, bins=args.bins, data_range=d_range,
                    weights=tr_br.astype(np.double))

                histo, err, intv = div_with_confint(histo_weighted, histo_orig)

                first_plot = k_br_name not in top_plotters
                if first_plot:
                    top_plotters[k_br_name] = []
                    bot_plotters[k_br_name] = []
                    ref_histos[k_br_name] = histo

                    pts_args = ax_add_args_errorbar(lbl, clr, yerr=err)
                    top_plotters[k_br_name].append(
                        lambda fig, ax, b=bins, h=histo, add=pts_args:
                        plot_errorbar(b, h, add, figure=fig, axis=ax,
                                      show_legend=False))

                elif args.errorbar_plot:
                    pts_args = ax_add_args_errorbar(lbl, clr, yerr=err)
                    top_plotters[k_br_name].append(
                        lambda fig, ax, b=bins, h=histo, add=pts_args:
                        plot_errorbar(b, h, add, figure=fig, axis=ax,
                                      show_legend=False))

                else:
                    step_args = ax_add_args_step(lbl, clr)
                    top_plotters[k_br_name].append(
                        lambda fig, ax, b=bins, h=histo, add=step_args:
                        plot_step(b, h, add, figure=fig, axis=ax,
                                  show_legend=False))
                    fill_args = ax_add_args_fill(clr, alpha=0.4)
                    top_plotters[k_br_name].append(
                        lambda fig, ax, b=bins, y=intv, add=fill_args:
                        plot_fill(b, y, add, figure=fig, axis=ax,
                                  show_legend=False))

                default_val = 1. if first_plot else 0.
                with np.errstate(divide='ignore', invalid='ignore'):
                    ratio_histo =  histo / ref_histos[k_br_name]
                    ratio_histo[ratio_histo == np.inf] = default_val
                    ratio_histo[np.isnan(ratio_histo)] = default_val

                # Bottom will always be a series of step plots
                bot_args = ax_add_args_step(lbl, clr)
                bot_plotters[k_br_name].append(
                    lambda fig, ax, b=bins, h=ratio_histo, add=bot_args:
                    plot_step(b, h, add, figure=fig, axis=ax,
                              show_legend=False))

    # Now do the actual plot
    yrange = args.yrange if args.yrange else [None]*len(args.xlabel)
    for k_br_name, xlabel, ylim in zip(top_plotters, args.xlabel, yrange):
        if args.ratio_plot:
            fig, ax1, ax2 = plot_top_bot(
                top_plotters[k_br_name], bot_plotters[k_br_name],
                title=args.title, xlabel=xlabel,
                ax1_ylabel=args.ax1_ylabel, ax2_ylabel=args.ax2_ylabel,
                ax1_yscale=args.ax1_yscale)
        else:
            fig, ax1, ax2 = plot_top(
                top_plotters[k_br_name],
                title=args.title,
                xlabel=xlabel, ylabel=args.ax1_ylabel,
                yscale=args.ax1_yscale)

        if ylim:
            ax1.set_ylim(ylim)

        for ext in args.ext:
            filename = '_'.join([
                args.output_prefix, args.title.replace(' ', '_'),
                k_br_name]) + '.' + ext

            fig.savefig(filename)

        # Clear plot in memory
        plt.close('all')

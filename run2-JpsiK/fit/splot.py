#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Feb 23, 2022 at 04:44 PM -0500

import sys
import zfit
import mplhep
import os.path as op

sys.path.insert(0, op.dirname(op.abspath(__file__)))

from argparse import ArgumentParser

from pyTuplingUtils.io import read_branches_dict
from pyTuplingUtils.plot import plot_top, plot_errorbar, plot_histo
from pyTuplingUtils.plot import ax_add_args_errorbar, ax_add_args_histo
from pyTuplingUtils.utils import gen_histo

from fit_and_sweight import gen_histo_from_pdf, fit_model_sig, fit_model_bkg
from fit_and_sweight import load_params
from fit_and_sweight import MODEL_BDY


##########
# Config #
##########

MODELS = {
    'sig': fit_model_sig,
    'bkg': fit_model_bkg,
}


#######################
# Command line parser #
#######################

def parse_input():
    parser = ArgumentParser(description='make sPlots from J/psi K fit output.')

    parser.add_argument('-i', '--input', required=True,
                        help='specify input ntuple, which must contains sWeight branches.')

    parser.add_argument('-o', '--output', required=True,
                        help='specify path to output plot.')

    parser.add_argument('-p', '--params', required=True,
                        help='specify fitted parameters, in YAML.')

    parser.add_argument('-b', '--branch', default='b_m',
                        help='specify the branch as the plotting variable.')

    parser.add_argument('-m', '--model', default='sig',
                        help='specify the model to plot.')

    parser.add_argument('-t', '--tree', default='tree',
                        help='specify the tree name in the input ntuple.')

    parser.add_argument('--xLabel', default=r'$m_B$ [MeV]',
                        help='specify xlabel.')

    parser.add_argument('--yLabel', default=r'Number of events',
                        help='specify ylabel.')

    parser.add_argument('--dataLabel', default='2016 data',
                        help='specify data label in the plots.')

    parser.add_argument('--modelLabel', default='sig.',
                        help='specify model label in the plots.')

    parser.add_argument('--bins', default=50,
                        help='specify the binning in the plot.')

    return parser.parse_args()


############
# Plotting #
############


def plot_splot(fit_var, fit_model, fit_sweight,
               bins=30, data_range=None, output=None,
               data_lbl='Data', model_lbl='Model',
               model_color='cornflowerblue',
               **kwargs):
    plotters = []

    # Data plot
    h_data, h_bins = gen_histo(
        fit_var, bins=bins, data_range=data_range, weights=fit_sweight)
    h_data_args = ax_add_args_errorbar(
        data_lbl, 'black', marker='.', markersize=10)
    plotters.append(
        lambda fig, ax, b=h_bins, h=h_data, add=h_data_args: plot_errorbar(
            b, h, add, figure=fig, axis=ax, show_legend=False))

    # Model plot
    h_model = gen_histo_from_pdf(fit_model, h_bins)
    h_model_args = ax_add_args_histo(model_lbl, model_color)
    plotters.append(
        lambda fig, ax, b=h_bins, h=h_model, add=h_model_args: plot_histo(
            b, h, add, figure=fig, axis=ax, show_legend=False))

    # Do the actual plot
    fig, ax = plot_top(plotters, **kwargs)

    # Tweaks on legend
    try:
        ax.ticklabel_format(style='sci', scilimits=[-4, 3], axis='y')
    except:
        pass

    fig.savefig(output)


if __name__ == '__main__':
    mplhep.style.use('LHCb2')
    args = parse_input()

    branches = read_branches_dict(
        args.input, args.tree, [args.branch, f'sw_{args.model}'])
    fit_params = load_params(args.params)
    obs = zfit.Space('x', limits=MODEL_BDY)

    # Create a scaling factor based on total yields
    fit_var = branches[args.branch]
    sweight = branches[f'sw_{args.model}']
    fit_param_yld = zfit.ComposedParameter(
        'yld',
        lambda raw: fit_var.size * raw,
        {'raw': fit_params[f'yld_{args.model}_ratio']}
    )

    fit_model_validate = MODELS[args.model](
        obs, fit_param_yld, fit_params)
    plot_splot(
        fit_var, fit_model_validate, sweight,
        output=args.output, data_range=MODEL_BDY,
        xlabel=args.xLabel, ylabel=args.yLabel,
        data_lbl=args.dataLabel, model_lbl=args.modelLabel,
        bins=args.bins
    )

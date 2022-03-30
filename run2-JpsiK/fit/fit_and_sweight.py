#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Mar 30, 2022 at 12:47 PM -0400
# NOTE: This is inspired by Greg Ciezarek's run 1 J/psi K fit

import zfit
import yaml
import time
import sys
import mplhep
import numpy as np

from argparse import ArgumentParser
from os import makedirs
from pathlib import Path
from uproot import concatenate, recreate
from hepstats.splot import compute_sweights

from pyTuplingUtils.utils import gen_histo, gen_histo_stacked_baseline
from pyTuplingUtils.plot import (
    plot_top_bot, plot_errorbar, plot_histo, plot_hlines,
    ax_add_args_errorbar, ax_add_args_histo, ax_add_args_hlines,
    ensure_no_majortick_on_topmost
)


##########
# Config #
##########

MODEL_BDY = (5150, 5350)


#######################
# Command line parser #
#######################

def parse_input():
    parser = ArgumentParser(description='simple fit and sWeight to J/psi K.')

    parser.add_argument('-i', '--input', nargs='+', required=True,
                        help='specify input ntuples and trees of uproot spec.')

    parser.add_argument('-p', '--params', required=True,
                        help='specify fit initial parameters.')

    parser.add_argument('-o', '--output', default='fit_results',
                        help='specify output folder.')

    parser.add_argument('-O', '--outputNtp', default=None,
                        help='specify path to output ntuple.')

    parser.add_argument('-b', '--branch', default='b_m',
                        help='specify the branch as the fit variable.')

    parser.add_argument('--noFit', action='store_true',
                        help='just plot the model before fit.')

    parser.add_argument('-I', '--outputPlotInit', default=None,
                        help='specify path to initial plot.')

    parser.add_argument('--dataLabel', default='2016 data',
                        help='specify data label in the plots.')

    parser.add_argument('--xLabel', default=r'$m_B$ [MeV]',
                        help='specify xlabel.')

    parser.add_argument('--yLabel', default=r'# events',
                        help='specify ylabel.')

    parser.add_argument('--bins', default=80, type=int,
                        help='specify the binning in the plot.')

    parser.add_argument('-e', '--extraBranches',
                        default=[
                            'runNumber',
                            'eventNumber',
                            'b_ownpv_ndof',
                            'ntracks',
                            'b_p',
                            'b_pt',
                            'b_eta',
                        ],
                        help='specify extra branches to save in output ntuple.')

    return parser.parse_args()


###########
# Helpers #
###########

# This controls output of a single parameter
def filter_dict(dct):
    value = dct['value']
    return {
        'value': value,
        'lower': value + dct['minuit_minos']['lower'],
        'upper': value + dct['minuit_minos']['upper'],
    }


def gen_ylds(num_of_evt, fit_params, names=['bkg', 'sig']):
    for n in names:
        yld_param = zfit.ComposedParameter(
            f'yld_{n}',
            lambda raw: num_of_evt*raw,
            {'raw': fit_params[f'yld_{n}_ratio']}
        )
        fit_params[f'yld_{n}'] = yld_param
    return [fit_params[f'yld_{i}'] for i in names]


def load_params(yml):
    with open(yml, 'r') as f:
        params_to_load = yaml.safe_load(f)

    params = dict()
    for var, spec in params_to_load.items():
        lower, upper = spec['lower'], spec['upper']
        value = (upper+lower) / 2 if 'value' not in spec else spec['value']
        params[var] = zfit.Parameter(var, value, lower, upper)

    return params


def ensure_dir(path, is_file=True):
    if is_file:
        makedirs(Path(path).parent, exist_ok=True)
    else:
        makedirs(Path(path), exist_ok=True)


############
# Plotting #
############

def gen_histo_from_pdf(pdf, bin_bdy):
    histo = []
    for left_bdy, right_bdy in zip(bin_bdy[:-1], bin_bdy[1:]):
        histo.append(pdf.ext_integrate([left_bdy, right_bdy])[0])
    return np.array(histo)


def plot(fit_var, fit_models,
         bins=30, data_range=None, output=None,
         data_lbl='Data', title='Fit',
         fit_model_lbls=['bkg.', 'sig.'],
         fit_model_colors=['crimson', 'cornflowerblue', 'darkgoldenrod'],
         ax1_ylabel='',
         **kwargs):
    top_plotters = []
    bot_plotters = []

    # Data plot
    h_data, h_bins = gen_histo(fit_var, bins=bins, data_range=data_range)
    h_data_args = ax_add_args_errorbar(
        data_lbl, 'black', yerr=np.sqrt(h_data), marker='.', markersize=10)
    top_plotters.append(
        lambda fig, ax, b=h_bins, h=h_data, add=h_data_args: plot_errorbar(
            b, h, add, figure=fig, axis=ax, show_legend=False))

    # Fit pdf plot (manually binned)
    h_models = [gen_histo_from_pdf(pdf, h_bins) for pdf in fit_models]
    y_baselines = gen_histo_stacked_baseline(h_models)

    for hist, bot, lbl, clr in zip(
            h_models, y_baselines, fit_model_lbls, fit_model_colors):
        h_models_args = ax_add_args_histo(lbl, clr, baseline=bot)
        top_plotters.append(
            lambda fig, ax, b=h_bins, h=hist+bot, add=h_models_args: plot_histo(
                b, h, add, figure=fig, axis=ax, show_legend=False))

    # Plot horizontal line at y=0 for pull plot as a reference
    bin_padding = 10
    plot_range = [h_bins[0]-bin_padding, h_bins[-1]+bin_padding]

    hline_ref_args = ax_add_args_hlines('ref', 'gray')
    bot_plotters.append(
        lambda fig, ax, b=plot_range, h=[0.0], add=hline_ref_args:
        plot_hlines(b, h, add, figure=fig, axis=ax, show_legend=False))

    hrect_ref_args = ax_add_args_histo('ref', 'gray', alpha=0.4)
    bot_plotters.append(
        lambda fig, ax, b=plot_range, h=[2.0], add=hrect_ref_args:
        plot_histo(b, h, add, figure=fig, axis=ax, show_legend=False))
    bot_plotters.append(
        lambda fig, ax, b=plot_range, h=[-2.0], add=hrect_ref_args:
        plot_histo(b, h, add, figure=fig, axis=ax, show_legend=False))

    # Pull plot
    h_model_tot_yld = np.add.reduce(h_models)
    h_resid = h_data - h_model_tot_yld
    h_err = np.sqrt(h_data)
    h_pull = h_resid / h_err

    h_pull_args = ax_add_args_hlines('pull', 'black', linewidth=3)
    bot_plotters.append(
        lambda fig, ax, b=h_bins, h=h_pull, add=h_pull_args: plot_hlines(
            b, h, add, figure=fig, axis=ax, show_legend=False))

    # Do the actual plot
    ax1_ylabel = ax1_ylabel + f' / {(MODEL_BDY[1]-MODEL_BDY[0])/args.bins:.1f} MeV'
    fig, ax1, ax2 = plot_top_bot(
        top_plotters, bot_plotters, title=title, ax2_ylabel='Pulls',
        legend_add_args={'numpoints': 1, 'loc': 'best', 'frameon': 'true'},
        ax1_ylabel=ax1_ylabel, **kwargs)

    # Tweaks on legend
    try:
        ax1.ticklabel_format(style='sci', scilimits=[-4, 3], axis='y')
    except:
        pass
    ensure_no_majortick_on_topmost(ax2, 'linear', thresh=0.75, ratio=0.5,
                                   verbose=True)

    # Manually fix plot range
    ax1.set_xlim(plot_range)
    ax2.set_xlim(plot_range)

    fig.savefig(output)


#######
# Fit #
#######

def fit_model_sig(obs, yld, fit_params):
    # It's a composition between a Gaussian and a CB
    peak = fit_params['peak']

    # Unlike RooFit, an initial value has to be provided
    # NOTE: By default RooFit use the center of the range
    #       My definition should be equivalent to Greg's
    width_cb = fit_params['width_cb']
    alpha = fit_params['alpha']
    n_cb = fit_params['n_cb']
    pdf_sig_cb = zfit.pdf.CrystalBall(
        obs=obs, mu=peak, sigma=width_cb, alpha=alpha, n=n_cb)

    width_g_sig = fit_params['width_g_sig']
    pdf_sig_g = zfit.pdf.Gauss(obs=obs, mu=peak, sigma=width_g_sig)

    width_g2_sig = fit_params['width_g2_sig']
    pdf_sig_g2 = zfit.pdf.Gauss(obs=obs, mu=peak, sigma=width_g2_sig)

    # Composite the 3 distributions
    pdf = zfit.pdf.SumPDF(
        pdfs=[
            pdf_sig_cb, pdf_sig_g, pdf_sig_g2
        ],
        fracs=[
            fit_params['frac_sig_cb'],
            fit_params['frac_sig_g'],
        ],
        name='sumpdf_sig')
    return pdf.create_extended(yld)


def fit_model_bkg(obs, yld, fit_params):
    expc = fit_params['expc']

    pdf = zfit.pdf.Exponential(obs=obs, lam=expc)
    return pdf.create_extended(yld)


def fit_model_tail(obs, yld, fit_params):
    peak_tail = fit_params['peak_tail']
    width_g_tail = fit_params['width_g_tail']

    pdf = zfit.pdf.Gauss(obs=obs, mu=peak_tail, sigma=width_g_tail)
    return pdf.create_extended(yld)


def fit_model_overall(obs, fit_var, fit_params):
    fit_component_builders = [fit_model_bkg, fit_model_sig]
    fit_yields = gen_ylds(fit_var.size, fit_params, names=['bkg', 'sig'])
    fit_components = [
        m(obs, yld, fit_params)
        for m, yld in zip(fit_component_builders, fit_yields)]

    return zfit.pdf.SumPDF(pdfs=fit_components, name='sumpdf_overall'), \
        fit_components, fit_yields


def fit(obs, fit_var, fit_model):
    # Load data
    data = zfit.data.Data.from_numpy(obs=obs, array=fit_var)

    # Fit
    print('Start to fit...')
    time_start = time.time()

    nll = zfit.loss.ExtendedUnbinnedNLL(model=fit_model, data=data)
    minimizer = zfit.minimize.Minuit()
    result = minimizer.minimize(loss=nll)

    print('Compute errors...')
    result.errors(method='minuit_minos')

    print(f'Fit & error computation took a total of {time.time() - time_start:.2f} sec.')
    return result, nll


if __name__ == '__main__':
    mplhep.style.use('LHCb2')
    args = parse_input()
    fit_params = load_params(args.params)

    ntp_brs = concatenate(
        args.input, [args.branch]+args.extraBranches, library='np')
    fit_var = ntp_brs[args.branch]
    print(f'Total events in data: {fit_var.size}')

    print('Initialize fit model...')
    obs = zfit.Space('x', limits=MODEL_BDY)
    fit_model, fit_components, _ = fit_model_overall(obs, fit_var, fit_params)

    output_plot_init = args.output + '/fit_init.pdf' \
        if not args.outputPlotInit else args.outputPlotInit
    ensure_dir(output_plot_init)
    # Always plot the initial condition
    plot(
        fit_var, fit_components, output=output_plot_init, data_range=MODEL_BDY,
        xlabel=args.xLabel, ax1_ylabel=args.yLabel, data_lbl=args.dataLabel,
        title='Before fit', bins=args.bins
    )

    if args.noFit:
        sys.exit(0)

    # Now do the fit
    fit_result, fit_nll = fit(obs, fit_var, fit_model)
    print('Fit result:\n', fit_result, sep='')

    # Compute sWeights
    print('Compute sWeights...')
    sweights = compute_sweights(fit_model, fit_var)

    # Dump result
    print('Dump result...')
    ensure_dir(args.output, is_file=False)

    ntp_path = f'{args.output}/fit.root' if not args.outputNtp \
        else args.outputNtp
    ntp = recreate(ntp_path)
    ntp_brs['sw_sig'] = sweights[fit_params['yld_sig']]
    ntp_brs['sw_bkg'] = sweights[fit_params['yld_bkg']]
    ntp['tree'] = ntp_brs

    with open(f'{args.output}/params.yml', 'w') as f:
        params_formatted = {k.name: filter_dict(v)
                            for k, v in fit_result.params.items()}
        yaml.dump(params_formatted, f)

    # Fit plots
    print('Plot fitting results...')
    plot(
        fit_var, fit_components, output=args.output+'/fit_final.pdf',
        data_range=MODEL_BDY,
        xlabel=args.xLabel, ax1_ylabel=args.yLabel, data_lbl=args.dataLabel,
        title=r'$J\psi K$ aux. fit', bins=args.bins
    )
    plot(
        fit_var, fit_components, output=args.output+'/fit_final_log_scale.pdf',
        data_range=MODEL_BDY,
        xlabel=args.xLabel, ax1_ylabel=args.yLabel, data_lbl=args.dataLabel,
        title=r'$J/\psi K$ aux. fit', ax1_yscale='log', bins=args.bins
    )

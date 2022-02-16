#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Feb 16, 2022 at 03:56 AM -0500
# NOTE: This is inspired by Greg Ciezarek's run 1 J/psi K fit

import zfit
import yaml
import time
import mplhep
import numpy as np
import matplotlib.pyplot as plt

from argparse import ArgumentParser
from uproot import concatenate, recreate
from os import makedirs

from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.plot import (
    plot_top, plot_errorbar, plot_histo,
    ax_add_args_errorbar, ax_add_args_histo
)


##########
# Config #
##########

MODEL_BDY = (5200, 5360)


#######################
# Command line parser #
#######################

def parse_input():
    parser = ArgumentParser(description='Simple fit and sWeight to J/psi K.')

    parser.add_argument('-i', '--input', nargs='+', required=True,
                        help='specify input ntuples and trees of uproot spec.')

    parser.add_argument('-o', '--output', default='fit_results',
                        help='specify output folder.')

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

    parser.add_argument('--yLabel', default=r'Number of events',
                        help='specify ylabel.')

    return parser.parse_args()


###########
# Helpers #
###########

# This controls output of a single parameter
def filter_dict(dct):
    return {
        'value': dct['value'],
        'err_lower': dct['minuit_minos']['lower'],
        'err_upper': dct['minuit_minos']['upper'],
    }


def gen_ylds(num_of_evt, names=['sig', 'bkg', 'tail'],
             ratios=[0.95, 0.14, 0.07], nominal_fac=0.75):
    ylds = []
    for n, r in zip(names, ratios):
        ylds.append(zfit.Parameter(
            f'yld_{n}', num_of_evt*r*nominal_fac, 0, num_of_evt*r))
    return ylds


############
# Plotting #
############

def gen_histo_from_pdf(pdf, bin_bdy):
    histo = []
    for left_bdy, right_bdy in zip(bin_bdy[:-1], bin_bdy[1:]):
        histo.append(pdf.ext_integrate([left_bdy, right_bdy])[0])
    return np.array(histo)


def gen_histo_stacked_baseline(histos):
    result = [np.zeros(histos[0].size)]
    for idx in range(0, len(histos)-1):
        result.append(result[idx]+histos[idx])
    return result


def plot(fit_var, fit_models, bins=30, data_lbl='Data', title='Fit',
         data_range=None, output=None,
         fit_model_lbls=['sig.', 'bkg.', 'tail'],
         fit_model_colors=['cornflowerblue', 'crimson', 'darkgoldenrod'],
         **kwargs):
    plotters = []

    h_data, h_bins = gen_histo(fit_var, bins=bins, data_range=data_range)
    h_data_args = ax_add_args_errorbar(
        data_lbl, 'black', yerr=np.sqrt(h_data), marker='.')
    plotters.append(
        lambda fig, ax, b=h_bins, h=h_data, add=h_data_args: plot_errorbar(
            b, h, add, figure=fig, axis=ax, show_legend=False))

    h_models = [gen_histo_from_pdf(pdf, h_bins) for pdf in fit_models]
    y_baselines = gen_histo_stacked_baseline(h_models)

    for hist, baseline, lbl, clr in zip(
            h_models, y_baselines, fit_model_lbls, fit_model_colors):
        h_models_args = ax_add_args_histo(lbl, clr, bottom=baseline)
        plotters.append(
            lambda fig, ax, b=h_bins, h=hist, add=h_models_args: plot_histo(
                b, h, add, figure=fig, axis=ax, show_legend=False))

    fig, ax = plot_top(
        plotters, output=None, title=title,
        legend_add_args={
            'numpoints': 1, 'loc': 'best', 'fontsize': 'medium',
            'frameon': 'true'
        }, **kwargs)
    ax.ticklabel_format(style='sci', scilimits=[-4, 3], axis='y')
    plt.tight_layout(pad=0)
    fig.savefig(output)
    plt.close(fig)


#######
# Fit #
#######

def fit_model_sig(obs, yld):
    # It's a composition between a Gaussian and a CB
    peak = zfit.Parameter('peak', 5280, 5270, 5290)

    # Unlike RooFit, an initial value has to be provided
    # NOTE: By default RooFit use the center of the range
    #       My definition should be equivalent to Greg's
    width_cb = zfit.Parameter('width_cb', 22.5, 15, 30)
    alpha = zfit.Parameter('alpha', 1.25, 0.5, 2)
    n_cb = zfit.Parameter('n_cb', 76.5, 3, 150)

    width_g_sig = zfit.Parameter('width_g_sig', 7.5, 0, 15)

    pdf_sig_cb = zfit.pdf.CrystalBall(
        obs=obs, mu=peak, sigma=width_cb, alpha=alpha, n=n_cb)
    pdf_sig_g = zfit.pdf.Gauss(obs=obs, mu=peak, sigma=width_g_sig)

    # Composite the 2 distributions
    frac_sig_cb_g = zfit.Parameter('frac_sig_cb_g', 0.6, 0, 1)
    pdf = zfit.pdf.SumPDF(
        pdfs=[pdf_sig_cb, pdf_sig_g], fracs=frac_sig_cb_g, name='sumpdf_sig')
    pdf.set_yield(yld)
    return pdf


def fit_model_bkg(obs, yld):
    expc = zfit.Parameter('expc', -0.025, -0.05, 0)

    pdf = zfit.pdf.Exponential(obs=obs, lam=expc)
    pdf.set_yield(yld)
    return pdf


def fit_model_tail(obs, yld):
    peak_tail = zfit.Parameter('peak_tail', 5145, 5120, 5170)
    width_g_tail = zfit.Parameter('width_g_tail', 35, 20, 50)

    pdf = zfit.pdf.Gauss(obs=obs, mu=peak_tail, sigma=width_g_tail)
    pdf.set_yield(yld)
    return pdf


def fit_model_overall(obs, fit_var):
    fit_component_builders = [fit_model_sig, fit_model_bkg, fit_model_tail]
    fit_yields = gen_ylds(fit_var.size)
    fit_components = [
        m(obs, yld) for m, yld in zip(fit_component_builders, fit_yields)]

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

    print(f'Fit took a total of {time.time() - time_start} sec.')
    return result


if __name__ == '__main__':
    mplhep.style.use('LHCb2')
    args = parse_input()

    ntp_brs = concatenate(
        args.input, [args.branch, 'runNumber', 'eventNumber'], library='np')
    fit_var = ntp_brs[args.branch]
    print(f'Total events in data: {fit_var.size}')

    print('Initialize fit model...')
    obs = zfit.Space('x', limits=MODEL_BDY)
    fit_model, fit_components, _ = fit_model_overall(obs, fit_var)

    output_plot_init = args.output + '/fit_init.pdf' \
        if not args.outputPlotInit else args.outputPlotInit
    plot(
        fit_var, fit_components, output=output_plot_init, data_range=MODEL_BDY,
        xlabel=args.xLabel, ylabel=args.yLabel, data_lbl=args.dataLabel,
        title='Before fit'
    )

    if not args.noFit:
        fit_result = fit(obs, fit_var, fit_model)
        print('Fit result:\n', fit_result, sep='')

        # Dump result
        makedirs(args.output, exist_ok=True)

        ntp = recreate(f'{args.output}/in_out.root')
        out_brs = ntp_brs
        ntp['tree'] = out_brs

        with open(f'{args.output}/params.yml', 'w') as f:
            params_formatted = {k.name: filter_dict(v)
                                for k, v in fit_result.params.items()}
            yaml.dump(params_formatted, f)

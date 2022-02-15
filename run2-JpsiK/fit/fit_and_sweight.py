#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Feb 15, 2022 at 05:30 AM -0500
# NOTE: This is inspired by Greg Ciezarek's run 1 J/psi K fit

import zfit
import yaml

from argparse import ArgumentParser
from uproot import concatenate
from os import makedirs


#######################
# Command line parser #
#######################

def parse_input():
    parser = ArgumentParser(description='Simple fit and sWeight to J/psi K.')

    parser.add_argument('-i', '--input', nargs='+',
                        help='specify input ntuples and trees of uproot spec.')

    parser.add_argument('-o', '--output',
                        help='specify output folder.')

    parser.add_argument('-b', '--branch', default='b_m',
                        help='specify the branch as the fit variable.')

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


def fit(fit_var):
    obs = zfit.Space('x', limits=(5150, 5350))

    # Load models
    fit_components = [fit_model_sig, fit_model_bkg, fit_model_tail]
    fit_yields = [
        zfit.Parameter('yld_sig', 1.5e6/2, 0, 1.5e6),
        zfit.Parameter('yld_bkg', 2e5/2, 0, 2e5),
        zfit.Parameter('yld_tail', 10e3/2, 0, 10e3)
    ]
    fit_model = zfit.pdf.SumPDF(
        pdfs=[m(obs, yld) for m, yld in zip(fit_components, fit_yields)],
        name='sumpdf_overall')

    # Load data
    data = zfit.data.Data.from_numpy(obs=obs, array=fit_var)

    # Fit
    print('Start to fit...')
    nll = zfit.loss.ExtendedUnbinnedNLL(model=fit_model, data=data)
    minimizer = zfit.minimize.Minuit()
    minima = minimizer.minimize(loss=nll)
    print('Compute errors...')
    minima.errors(method='minuit_minos')

    return minima


if __name__ == '__main__':
    args = parse_input()

    fit_var = concatenate(args.input, [args.branch], library='np')[args.branch]
    print(f'Total events in data: {fit_var.size}')

    fit_result = fit(fit_var)
    print('Fit result:\n', fit_result, sep='')

    # Dump result
    makedirs(args.output, exist_ok=True)

    with open(f'{args.output}/params.yml', 'w') as f:
        params_formatted = {k.name: filter_dict(v)
                            for k, v in fit_result.params.items()}
        yaml.dump(params_formatted, f)

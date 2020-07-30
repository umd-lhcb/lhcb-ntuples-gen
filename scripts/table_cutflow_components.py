#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Jul 30, 2020 at 07:58 PM +0800

from yaml import safe_load
from argparse import ArgumentParser
from uncertainties import ufloat, UFloat
from statsmodels.stats.proportion import proportion_confint


#######################
# Uncertainty-related #
#######################

def div_with_confint(num, denom):
    ratio = num / denom
    intv = proportion_confint(num, denom, method='beta', alpha=0.32)  # Clopper-Pearson
    # Use the larger error bar and pretend its a Gaussian
    err_bar = max([abs(x - ratio) for x in intv])
    return ufloat(ratio, err_bar)


def div(num, denom):
    if type(num) == type(denom):
        result = num / denom*100.
    else:
        result = 'naN'

    return result


###############
# CSV-related #
###############

CSV_HEADERS = ['cut name', 'Signal', 'Normaliz.', 'D**',
               'Sig eff', 'Nor eff', 'D** eff']


def list_gen(sig_descr, nor_descr, dss_descr, header=CSV_HEADERS):
    result = [CSV_HEADERS]
    sig_total_input = None
    nor_total_input = None
    dss_total_input = None

    for key, val in sig_descr.items():
        if key in nor_descr.keys() and key in dss_descr.keys():
            row = []
            nor_row = nor_descr[key]
            dss_row = dss_descr[key]

            try:
                cut_name = val['name']
            except KeyError:
                cut_name = key
            row.append(cut_name)

            sig_yield = val['output']
            nor_yield = nor_row['output']
            dss_yield = dss_row['output']

            # Store total number of events in the raw data.
            if key == 'Full stripping':
                sig_total_input = sig_yield
                nor_total_input = nor_yield
                dss_total_input = dss_yield

            if len(result) > 1:
                sig_eff = div(val['output'], val['input'])
                nor_eff = div(nor_row['output'], nor_row['input'])
                dss_eff = div(dss_row['output'], dss_row['input'])
            else:  # Approx numbers from .dec file
                sig_eff = div(val['output'], 21800)
                nor_eff = div(nor_row['output'], 336000)
                dss_eff = div(dss_row['output'], 162000)

            row += [sig_yield, nor_yield, dss_yield, sig_eff, nor_eff, dss_eff]
            result.append(row)

    # Append the total ratio
    sig_total_eff = div(sig_yield, sig_total_input)
    nor_total_eff = div(nor_yield, nor_total_input)
    dss_total_eff = div(dss_yield, dss_total_input)
    result.append(['Total ratio'] + ['-']*(len(header)-4) +
                  [sig_total_eff, nor_total_eff, dss_total_eff])
    return result


def csv_gen(lst, latex_wrapper=True):
    for row in lst:
        formatted = []

        for elem in row:
            if isinstance(elem, float):
                formatted.append('{:.1f}'.format(elem))
            else:
                formatted.append(str(elem))

        print(','.join(formatted))


################################
# Command line argument parser #
################################

def parse_input(descr='Generate cut flow CSV from YAML files.'):
    parser = ArgumentParser(description=descr)

    parser.add_argument('-s', '--signal',
                        required=True,
                        help='specify the signal cutflow YAML file.'
                        )

    parser.add_argument('-n', '--normalization',
                        required=True,
                        help='specify the normalization cutflow YAML file.'
                        )

    parser.add_argument('-d', '--dss',
                        required=True,
                        help='specify the D** cutflow YAML file.'
                        )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_input()

    with open(args.signal) as f:
        sig_descr = safe_load(f)

    with open(args.normalization) as f:
        nor_descr = safe_load(f)

    with open(args.dss) as f:
        dss_descr = safe_load(f)

    tab = list_gen(sig_descr, nor_descr, dss_descr)
    csv_gen(tab, False)

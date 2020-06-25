#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri May 01, 2020 at 10:11 PM +0800

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
        if isinstance(num, UFloat):
            result = num / denom

        elif isinstance(num, (int, float)):
            try:
                result = div_with_confint(num, denom)
            except ZeroDivisionError:
                result = 'naN'

        else:
            result = 'naN'
    else:
        result = 'naN'

    return result


###############
# CSV-related #
###############

CSV_HEADERS = ['cut name', 'run 1 yield', 'run 2 yield',
               'run 1 efficiency', 'run 2 efficiency', 'double ratio']


def list_gen(run1_descr, run2_descr, header=CSV_HEADERS):
    result = [CSV_HEADERS]
    run1_total_input = None
    run2_total_input = None

    for key, val in run1_descr.items():
        if key in run2_descr.keys():
            row = []
            run2_row = run2_descr[key]

            try:
                cut_name = val['name']
            except KeyError:
                try:
                    cut_name = run2_row['name']
                except Exception:
                    cut_name = key
            row.append(cut_name)

            run1_yield = val['output']
            run2_yield = run2_row['output']

            # Store total number of events in the raw data.
            if not run1_total_input:
                run1_total_input = run1_yield
            if not run2_total_input:
                run2_total_input = run2_yield

            if len(result) > 1:
                run1_eff = div(val['output'], val['input'])
                run2_eff = div(run2_row['output'], run2_row['input'])

                double_ratio = div(run2_eff, run1_eff)

            else:  # Don't calculate ratios for the total number of candidates
                run1_eff = run2_eff = double_ratio = '-'

            row += [run1_yield, run2_yield, run1_eff, run2_eff, double_ratio]
            result.append(row)

    # Append the total ratio
    run1_total_eff = div(run1_yield, run1_total_input)
    run2_total_eff = div(run2_yield, run2_total_input)
    result.append(['Total ratio'] + ['-']*(len(header)-4) +
                  [run1_total_eff, run2_total_eff,
                   run2_total_eff / run1_total_eff])

    return result


def csv_gen(lst, latex_wrapper=True):
    for row in lst:
        formatted = []

        for elem in row:
            if isinstance(elem, float):
                formatted.append('{:.2f}'.format(elem))
            elif isinstance(elem, UFloat):
                if latex_wrapper:
                    formatted.append('${:.3f}$'.format(elem))
                else:
                    formatted.append('{:.3f}'.format(elem))
            else:
                formatted.append(str(elem))

        print(','.join(formatted))


################################
# Command line argument parser #
################################

def parse_input(descr='Generate cut flow CSV from YAML files.'):
    parser = ArgumentParser(description=descr)

    parser.add_argument('-o', '--runOne',
                        required=True,
                        help='specify the run 1 cutflow YAML file.'
                        )

    parser.add_argument('-t', '--runTwo',
                        required=True,
                        help='specify the run 2 cutflow YAML file.'
                        )

    parser.add_argument('-n', '--noLaTeX',
                        action='store_true',
                        help='disable LaTeX wrapping.'
                        )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_input()

    with open(args.runOne) as f:
        run1_descr = safe_load(f)

    with open(args.runTwo) as f:
        run2_descr = safe_load(f)

    tab = list_gen(run1_descr, run2_descr)
    csv_gen(tab, not args.noLaTeX)

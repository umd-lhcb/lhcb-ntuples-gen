#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Mar 23, 2020 at 10:20 PM +0800

from yaml import safe_load
from argparse import ArgumentParser
from uncertainties import ufloat, UFloat
from statsmodels.stats.proportion import proportion_confint


###############
# CSV-related #
###############

CSV_HEADERS = ['cut name', 'run 1 yield', 'run 2 yield',
               'run 1 efficiency', 'run 2 efficiency', 'double ratio']


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


def list_gen(run1_descr, run2_descr, header=CSV_HEADERS):
    result = [CSV_HEADERS]
    total_ratio = 1

    for key, val in run1_descr.items():
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

        run1_eff = div(val['output'], val['input'])
        run2_eff = div(run2_row['output'], run2_row['input'])

        double_ratio = div(run2_eff, run1_eff)
        total_ratio = total_ratio * double_ratio

        row += [run1_yield, run2_yield, run1_eff, run2_eff, double_ratio]
        result.append(row)

    # Append the total ratio
    result.append(['Total ratio (run 2/run 1)'] + ['-']*(len(header)-2) +
                  [total_ratio])

    return result


def csv_gen(lst, latex_wrapper=True):
    for row in lst:
        formatted = []

        for elem in row:
            if isinstance(elem, float):
                formatted.append('{:.3f}'.format(elem))
            elif isinstance(elem, UFloat):
                if latex_wrapper:
                    formatted.append('${:.3uL}$'.format(elem))
                else:
                    formatted.append('{:.3uP}'.format(elem))
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
                        help='specify the output table format.'
                        )

    parser.add_argument('-t', '--runTwo',
                        required=True,
                        help='specify the alignment for each column (right, center, left).'
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

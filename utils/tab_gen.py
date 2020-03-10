#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Mar 10, 2020 at 10:46 PM +0800

import fileinput

from argparse import ArgumentParser
from tabulate import tabulate


################################
# Command line argument parser #
################################

def parse_input(descr='table generator taking stdin as input.'):
    parser = ArgumentParser(description=descr)

    parser.add_argument('-f', '--format',
                        nargs='?',
                        choices=['latex', 'simple', 'github', 'latex_booktabs'],
                        default='latex_booktabs',
                        help='specify the output table format.'
                        )

    parser.add_argument('-n', '--no-math-env',
                        action='store_false',
                        help="Don't wrap content of each cell with $ sign."
                        )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_input()

    output = []
    for l in fileinput.input():
        output.append(l.rstrip().split(','))

    print(tabulate(output, headers='firstrow', tablefmt=args.format))

#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Mar 10, 2020 at 11:04 PM +0800

import fileinput

from argparse import ArgumentParser, Action
from tabulate import tabulate


################################
# Command line argument parser #
################################

class ColAlignmentAct(Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if ',' not in value:
            setattr(namespace, self.dest, [value])
        else:
            setattr(namespace, self.dest, value.split(','))


def parse_input(descr='table generator taking stdin as input.'):
    parser = ArgumentParser(description=descr)

    parser.add_argument('-f', '--format',
                        nargs='?',
                        choices=['latex',
                                 'simple',
                                 'github',
                                 'latex_booktabs',
                                 'latex_raw'],
                        default='latex_raw',
                        help='specify the output table format.'
                        )

    parser.add_argument('-a', '--alignment',
                        action=ColAlignmentAct,
                        default=None,
                        help='specify the alignment for each column (right, center, left).')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_input()

    output = []
    for l in fileinput.input(files=('-',)):
        row = l.rstrip().split(',')
        # Strip out head and tail whitespace unconditionally
        row = [x.strip() for x in row]
        output.append(row)

    if args.alignment is not None:
        print(tabulate(output, headers='firstrow', tablefmt=args.format,
                       colalign=args.alignment))
    else:
        print(tabulate(output, headers='firstrow', tablefmt=args.format))

#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Apr 27, 2021 at 03:08 AM +0200

from argparse import ArgumentParser

from ROOT import RDataFrame


################################
# Command line argument parser #
################################

def parse_input():
    parser = ArgumentParser(
        description='find retention rates for various trigger paths.')

    parser.add_argument('ntp', help='specify ntuple path.')

    parser.add_argument('tree', help='specify tree name.')

    parser.add_argument('-t', '--trigger-paths',
                        nargs='?',
                        help='specify trigger paths.')

    return parser.parse_args()


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    init_frame = RDataFrame(args.tree, args.ntp)
    for tp in args.trigger_paths:
        init_frame.Filter(tp, tp)

    init_frame.Report().Print()

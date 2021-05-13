#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu May 13, 2021 at 07:10 PM +0200

import uproot

from pyTuplingUtils.utils import find_common_uid, extract_uid
from pyTuplingUtils.parse import double_ntuple_parser_no_output
from sys import exit


#################################
# Command line arguments parser #
#################################

DESCR = '''
compare if the two ntuples have the identical reconstructed candidates inside.
'''


def parse_input(descr=DESCR):
    parser = double_ntuple_parser_no_output(descr)

    parser.add_argument('--runNumber',
                        nargs='?',
                        default='runNumber',
                        help='''
branch name contains runNumber.''')

    parser.add_argument('--eventNumber',
                        nargs='?',
                        default='eventNumber',
                        help='''
branch name contains eventNumber.''')

    return parser


if __name__ == '__main__':
    args = parse_input(DESCR).parse_args()
    ntp1 = uproot.open(args.ref)
    ntp2 = uproot.open(args.comp)

    _, _, *stat1 = extract_uid(ntp1, args.ref_tree, args.runNumber,
                               args.eventNumber)
    _, _, *stat2 = extract_uid(ntp2, args.comp_tree, args.runNumber,
                               args.eventNumber)
    uniq_common, _, _ = find_common_uid(ntp1, ntp2,
                                        args.ref_tree, args.comp_tree,
                                        run_branch=args.runNumber,
                                        event_branch=args.eventNumber)

    # Here we check both ntuples have same number of events, same number of IDs,
    # same number of duplicated IDs and same number of duplicated events
    badness = sum([abs(x-y) for x, y in zip(stat1, stat2)])

    if not badness:
        print('The two ntuples agree: {} unique cands, {} duplicate cands.'.format(
            stat1[1], stat1[-1]
        ))
    else:
        print('The two ntuples disagree.')
        print('{} has {} unique cands, {} duplicate cands.'.format(
            args.ref, stat1[1], stat1[-1]
        ))
        print('{} has {} unique cands, {} duplicate cands.'.format(
            args.comp, stat2[1], stat2[-1]
        ))
        print('They have {} common cands.'.format(uniq_common.size))

    exit(badness)

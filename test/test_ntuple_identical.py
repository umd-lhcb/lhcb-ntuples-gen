#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Jun 09, 2020 at 12:59 AM +0800

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

    _, _, _, uniq1, dupl1 = extract_uid(ntp1, args.ref_tree,
                                        args.runNumber, args.eventNumber)
    _, _, _, uniq2, dupl2 = extract_uid(ntp2, args.comp_tree,
                                        args.runNumber, args.eventNumber)
    uniq_common, _, _ = find_common_uid(ntp1, ntp2,
                                        args.ref_tree, args.comp_tree,
                                        run_branch=args.runNumber,
                                        event_branch=args.eventNumber)
    uniq_common = len(uniq_common)

    uniq_diff = abs(uniq1-uniq2)
    dupl_diff = abs(dupl1-dupl2)

    uniq_common_diff = abs(uniq_common-uniq1) + abs(uniq_common-uniq2)

    badness = uniq_diff + dupl_diff + uniq_common_diff

    if not badness:
        print('The two ntuples agree: {} unique cands, {} duplicate cands.'.format(
            uniq1, dupl1
        ))
    else:
        print('The two ntuples disagree.')
        print('{} has {} unique cands, {} duplicate cands.'.format(
            args.ref, uniq1, dupl1
        ))
        print('{} has {} unique cands, {} duplicate cands.'.format(
            args.comp, uniq2, dupl2
        ))
        print('They have {} common cands.'.format(uniq_common))

    exit(badness)

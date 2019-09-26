#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Sep 25, 2019 at 11:14 PM -0400

import uproot
import numpy as np


def extract_uid(filename, tree,
                runBranch='runNumber', eventBranch='eventNumber'):
    ntp = uproot.open(filename)
    run = np.char.mod('%d', ntp[tree].array(runBranch))
    event = np.char.mod('%d', ntp[tree].array(eventBranch))

    run = np.char.add(run, '-')
    mid = np.char.add(run, event)

    uid, idx, count = np.unique(mid, return_index=True, return_counts=True)
    uid_idx = idx[count == 1]

    total_size = mid.size
    uniq_size = uid.size
    dupl_size = total_size - uniq_size

    return (uid, uid_idx, total_size, uniq_size, dupl_size)


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    tree = sys.argv[2]

    _, _, total_size, _, dupl_size = extract_uid(filename, tree)
    print('Total # of event: {}, duplicate: {}'.format(total_size, dupl_size))

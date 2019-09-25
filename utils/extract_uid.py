#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Sep 25, 2019 at 05:28 PM -0400

import uproot
import numpy as np


def get_unique_id(filename, tree,
                  runBranch='runNumber', eventBranch='eventNumber'):
    ntp = uproot.open(filename)
    run = np.char.mod('%d', ntp[tree].array(runBranch))
    event = np.char.mod('%d', ntp[tree].array(eventBranch))

    run = np.char.add(run, '-')
    mid = np.char.add(run, event)

    _, idx, count = np.unique(mid, return_index=True, return_counts=True)
    uniq = idx[count == 1]

    total_size = mid.size
    uniq_size = uniq.size
    dup_size = total_size - uniq_size

    return (uniq, total_size, uniq_size, dup_size)


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    tree = sys.argv[2]

    _, total_size, _, dup_size = get_unique_id(filename, tree)
    print('Total # of event: {}, duplicate: {}'.format(total_size, dup_size))

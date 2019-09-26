#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Sep 26, 2019 at 12:11 AM -0400

import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from extract_uid import extract_uid


def find_common_uid(filename1, filename2, tree1, tree2, **kwargs):
    uid1, idx1, _, _, _ = extract_uid(filename1, tree1, **kwargs)
    uid2, idx2, _, _, _ = extract_uid(filename2, tree2, **kwargs)
    uid_comm, uid_comm_idx1, uid_comm_idx2 = np.intersect1d(
        uid1, uid2, assume_unique=True, return_indices=True)

    return uid_comm, idx1[uid_comm_idx1], idx2[uid_comm_idx2]


if __name__ == '__main__':
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    tree1 = sys.argv[3]
    tree2 = sys.argv[4]

    uid_comm, idx1, idx2 = find_common_uid(filename1, filename2, tree1, tree2)
    print('Total # of common UIDs: {}'.format(uid_comm.size))

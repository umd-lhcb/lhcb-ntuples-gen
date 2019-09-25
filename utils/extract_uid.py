#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Sep 25, 2019 at 03:33 PM -0400

import uproot
import numpy as np


def get_unique_id(filename, tree,
                  runBranch='runNumber', eventBranch='eventNumber'):
    ntp = uproot.open(filename)
    run = np.char.mod('%d', ntp[tree].array(runBranch))
    event = np.char.mod('%d', ntp[tree].array(eventBranch))

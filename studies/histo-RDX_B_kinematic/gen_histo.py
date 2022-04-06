#!/usr/bin/env python

import uproot
import numpy as np

# b_pt, b_eta
BINNING = ([20, 9], [[0, 25e3], [2, 5]])
NTPS = '../../ntuples/0.9.6-2016_production/Dst_D0-mc-tracker_only/Dst_D0--22_02_24--mc--tracker_only--MC_2016_Beam6500GeV-2016-MagDown-TrackerOnly-Nu1.6-25ns-Pythia8_Sim09k_Reco16_Filtered_12773410_D0TAUNU.SAFESTRIPTRIG.DST/*-dv.root:TupleBminus/DecayTree'


branches = uproot.concatenate(
    NTPS, ['b_PT', 'b_P', 'b_PZ'], library='np')

brPT, brP, brPZ = branches['b_PT'], branches['b_P'], branches['b_PZ']
brETA = 0.5 * np.log((brP + brPZ) / (brP - brPZ))

histo = np.histogram2d(brPT, brETA, *BINNING)

ntpOut = uproot.recreate('histo.root')
ntpOut['histo'] = histo

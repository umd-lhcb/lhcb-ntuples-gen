# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sun Jul 14, 2019 at 01:05 AM -0400

from argparse import ArgumentParser

j = Job(name='First ganga job')
myApp = GaudiExec()
myApp.directory = "./DaVinciDev_v44r6"
j.application = myApp
j.application.options = ['ntuple_options.py']
bkPath = '/MC/2016/Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8/Sim09c/Trig0x6138160F/Reco16/Turbo03/Stripping28r1NoPrescalingFlagged/27163002/ALLSTREAMS.DST'
data  = BKQuery(bkPath, dqflag=['OK']).getDataset()
j.inputdata = data[0:2]
j.backend = Dirac()
j.splitter = SplitByFiles(filesPerJob=1)
j.outputfiles = [LocalFile('DVntuple.root')]
j.submit()

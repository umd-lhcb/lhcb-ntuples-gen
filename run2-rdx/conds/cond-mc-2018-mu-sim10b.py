from Configurables import DaVinci

DaVinci().DataType = '2018'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'
# DaVinci().HistogramFile = 'mc-histo.root'

# Additional global flags
#DaVinci().MoniSequence += ['TRACKER_ONLY']


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20201113-8-vc-mu100-Sim10"
LHCbApp().DDDBtag = "dddb-20210528-8"


#from GaudiConf import IOHelper

# # Lambda background
#IOHelper().inputFiles([
#    './data/Lb2Lc2860_MuNu-2016-mu-py8-sim10b-fullsim/00173824_00000065_7.AllStreams.dst',
#    './data/Lb2Lc2860_MuNu-2016-mu-py8-sim10b-fullsim/00173824_00000128_7.AllStreams.dst',
#    './data/Lb2Lc2860_MuNu-2016-mu-py8-sim10b-fullsim/00173824_00000157_7.AllStreams.dst',
#], clear=True)

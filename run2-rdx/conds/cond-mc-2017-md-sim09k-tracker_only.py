from Configurables import DaVinci

DaVinci().DataType = '2017'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'
# DaVinci().HistogramFile = 'mc-histo.root'

# Additional global flags
DaVinci().MoniSequence += ['TRACKER_ONLY']


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20190430-1-vc-md100"
LHCbApp().DDDBtag = "dddb-20170721-3"

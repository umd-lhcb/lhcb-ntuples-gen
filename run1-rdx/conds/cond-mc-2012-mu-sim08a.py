from Configurables import DaVinci

DaVinci().DataType = '2012'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'
# DaVinci().HistogramFile = 'mc-histo.root'


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20130503-1-vc-mu100"
LHCbApp().DDDBtag = "dddb-20130503-1"

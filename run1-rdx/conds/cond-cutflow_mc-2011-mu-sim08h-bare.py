from Configurables import DaVinci

DaVinci().DataType = '2011'
DaVinci().Simulation = True

DaVinci().TupleFile = 'cutflow_mc-bare.root'

# Additional global flags
DaVinci().MoniSequence += ['CUTFLOW', 'BARE']


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20130522-vc-mu100"
LHCbApp().DDDBtag = "dddb-20130929"

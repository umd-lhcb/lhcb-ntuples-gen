from Configurables import DaVinci

DaVinci().DataType = '2018'
DaVinci().Simulation = True

DaVinci().TupleFile = 'mc.root'

# Additional global flags
DaVinci().MoniSequence += ['TRACKER_ONLY']


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20201113-8-vc-md100-Sim10"
LHCbApp().DDDBtag = "dddb-20220927-2018"
from Configurables import DaVinci

DaVinci().DataType = '2011'
DaVinci().Simulation = True

DaVinci().TupleFile = 'cutflow_mc-bare.root'

# Additional global flags
DaVinci().MoniSequence += ['CUTFLOW', 'BARE']


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20130522-vc-md100"
LHCbApp().DDDBtag = "dddb-20130929"


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/Bd2D0XMuNu_D0_cocktail-2011-md-py8-sim08h/00046784_00000003_2.AllStreams.dst',
    './data/Bd2D0XMuNu_D0_cocktail-2011-md-py8-sim08h/00046785_00000016_2.AllStreams.dst',
], clear=True)

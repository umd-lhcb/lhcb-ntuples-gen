from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'Dst-mc.root'

# Additional global flags
DaVinci().MoniSequence += ['CUTFLOW', 'BARE']


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20130522-vc-md100"
LHCbApp().DDDBtag = "dddb-20130929"


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/mc-mag_down-py8-sim08h-Bd2D0XMuNu-D0_cocktail/00046785_00000003_2.AllStreams.dst',
    './data/mc-mag_down-py8-sim08h-Bd2D0XMuNu-D0_cocktail/00046785_00000016_2.AllStreams.dst',
], clear=True)

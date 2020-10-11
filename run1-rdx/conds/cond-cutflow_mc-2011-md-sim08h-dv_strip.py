from Configurables import DaVinci

DaVinci().DataType = '2011'
DaVinci().Simulation = True

DaVinci().TupleFile = 'cutflow_mc-dv_strip.root'

# Additional global flags
DaVinci().MoniSequence += ['CUTFLOW', 'DV_STRIP', 'NO_SMEAR']


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20130522-vc-md100"
LHCbApp().DDDBtag = "dddb-20130929"


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/Bd2D0XMuNu_D0_cocktail-2011-md-py8-sim08h/00046785_00000003_2.AllStreams.dst',
    './data/Bd2D0XMuNu_D0_cocktail-2011-md-py8-sim08h/00046785_00000016_2.AllStreams.dst',
], clear=True)

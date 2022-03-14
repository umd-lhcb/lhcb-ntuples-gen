from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True
DaVinci().InputType = "MDST"

DaVinci().TupleFile = 'ghost1.root'

# Additional global flags
DaVinci().MoniSequence += ['MU_MISID', 'GHOST']


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20160614-1-vc-md100"
LHCbApp().DDDBtag = "dddb-20170721-1"


from GaudiConf import IOHelper
from glob import glob

IOHelper().inputFiles(glob('../data/Bd2DstX_cocktail_D0Pi-2016-md-py8-sim09i/*.mdst'),
                      clear=True)

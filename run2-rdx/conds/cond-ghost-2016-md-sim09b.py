from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = True

DaVinci().TupleFile = 'ghost.root'

# Additional global flags
DaVinci().MoniSequence += ['GHOST']


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20161124-2-vc-md100"
LHCbApp().DDDBtag = "dddb-20150724"


from GaudiConf import IOHelper
from glob import glob

# 12875420 (Bu_D0Xmunu,D0=cocktail,LHCbAcceptance)
IOHelper().inputFiles(glob('./data/Bu2D0XMuNu_D0_cocktail-2016-md-py8-sim09b/*.dst'),
                      clear=True)

# 11876060 (Bd_D0Xmunu,D0=cocktail,LHCbAcceptance_buggy)
# IOHelper().inputFiles(glob('./data/Bd2D0XMuNu_D0_cocktail-2016-md-py8-sim09b/*.dst'),
#                       clear=True)

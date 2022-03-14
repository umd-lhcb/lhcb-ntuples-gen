from Configurables import DaVinci

DaVinci().DataType = '2012'
DaVinci().Simulation = True

DaVinci().TupleFile = 'ghost.root'


from Configurables import LHCbApp

LHCbApp().CondDBtag = "sim-20150703-vc-md100"
LHCbApp().DDDBtag = "dddb-20150703"


# Additional global flags
DaVinci().MoniSequence += ['MU_MISID', 'GHOST']


from GaudiConf import IOHelper
from glob import glob

IOHelper().inputFiles(glob('./data/Dst2D0Pi_FromB-2012-md-py8-sim08h/*.dst'),
                      clear=True)

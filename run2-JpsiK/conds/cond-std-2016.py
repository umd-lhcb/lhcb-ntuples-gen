from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = False

DaVinci().TupleFile = 'std.root'
# DaVinci().HistogramFile = 'std-histo.root'


from GaudiConf import IOHelper
from glob import glob

# Stripping v28r2
IOHelper().inputFiles(glob('./data/data-2016-md/*.dst'), clear=True)

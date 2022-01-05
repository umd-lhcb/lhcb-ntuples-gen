from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = False

DaVinci().TupleFile = 'std.root'
# DaVinci().HistogramFile = 'std-histo.root'


from GaudiConf import IOHelper

# Stripping v28r2p1
IOHelper().inputFiles([
    './data/data-2016-md/00151979_00000281_1.dimuon.dst',
    './data/data-2016-md/00151979_00000290_1.dimuon.dst',
    './data/data-2016-md/00151979_00000312_1.dimuon.dst',
], clear=True)

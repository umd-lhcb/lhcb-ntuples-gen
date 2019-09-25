from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = False

DaVinci().TupleFile = 'BCands_Dst-validation.root'
# DaVinci().HistogramFile = 'BCands_Dst_histo-data.root'


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/validation-stripping28v2/00095518_00000063_1.semileptonic.dst',
], clear=True)

from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = False

DaVinci().TupleFile = 'cutflow_data.root'
# DaVinci().HistogramFile = 'cutflow_data-histo.root'

# Additional global flags
DaVinci().MoniSequence += ['CUTFLOW']


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/data-2016-md/00069529_00017556_1.semileptonic.dst',  # 1.2 GB
    './data/data-2016-md/00069527_00003141_1.semileptonic.dst',  # 3.5 GB
], clear=True)

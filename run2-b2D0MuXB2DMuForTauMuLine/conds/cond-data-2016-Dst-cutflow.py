from Configurables import DaVinci

DaVinci().DataType = '2016'
DaVinci().Simulation = False

DaVinci().TupleFile = 'BCands_Dst-data.root'
# DaVinci().HistogramFile = 'BCands_Dst_histo-data.root'

# Additional global flags
DaVinci().MoniSequence += ['CUTFLOW']


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/data-2016-mag_down/00069529_00017556_1.semileptonic.dst',  # 1.2 GB
    './data/data-2016-mag_down/00069527_00003141_1.semileptonic.dst',  # 3.5 GB
], clear=True)

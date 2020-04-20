from Configurables import DaVinci

DaVinci().DataType = '2012'
DaVinci().Simulation = False

DaVinci().TupleFile = 'BCands_Dst-data.root'
# DaVinci().HistogramFile = 'BCands_Dst_histo-data.root'

# Specify tags
# DaVinci().DDDBtag = 'dddb-20130929-1'
# DaVinci().CondDBtag = 'cond-20141007'

# Additional global flags
DaVinci().MoniSequence += ['CUTFLOW']


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/data-2012-mag_down/00041836_00006100_1.semileptonic.dst',  # 95 MB
    './data/data-2012-mag_down/00041836_00011435_1.semileptonic.dst',  # 1.3 GB
    './data/data-2012-mag_down/00041836_00013110_1.semileptonic.dst',  # 2.9 GB
], clear=True)

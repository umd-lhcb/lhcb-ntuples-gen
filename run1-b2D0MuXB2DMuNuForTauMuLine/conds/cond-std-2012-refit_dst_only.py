from Configurables import DaVinci

DaVinci().DataType = '2012'
DaVinci().Simulation = False

DaVinci().TupleFile = 'std-refit_dst_only.root'
# DaVinci().HistogramFile = 'std-histo.root'

DaVinci().MoniSequence += ['REFIT_DST_ONLY']

# Specify tags
# DaVinci().DDDBtag = 'dddb-20130929-1'
# DaVinci().CondDBtag = 'cond-20141007'


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/data-2012-md/00041836_00006100_1.semileptonic.dst',  # 95 MB
    './data/data-2012-md/00041836_00011435_1.semileptonic.dst',  # 1.3 GB
    './data/data-2012-md/00041836_00013110_1.semileptonic.dst',  # 2.9 GB
], clear=True)

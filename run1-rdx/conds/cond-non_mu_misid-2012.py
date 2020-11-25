from Configurables import DaVinci

DaVinci().DataType = '2012'
DaVinci().Simulation = False

DaVinci().TupleFile = 'non_mu_misid.root'

# Additional global flags
DaVinci().MoniSequence += ['NON_MU_MISID']


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/data-2012-md/00041836_00006100_1.semileptonic.dst',  # 95 MB
    './data/data-2012-md/00041836_00011435_1.semileptonic.dst',  # 1.3 GB
    './data/data-2012-md/00041836_00013110_1.semileptonic.dst',  # 2.9 GB
], clear=True)

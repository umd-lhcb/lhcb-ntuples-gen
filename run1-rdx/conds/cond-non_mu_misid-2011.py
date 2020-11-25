from Configurables import DaVinci

DaVinci().DataType = '2011'
DaVinci().Simulation = False

DaVinci().TupleFile = 'non_mu_misid.root'

# Additional global flags
DaVinci().MoniSequence += ['NON_MU_MISID']

# Specify tags
# DaVinci().DDDBtag = 'dddb-20130929-1'
# DaVinci().CondDBtag = 'cond-20141007'


from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/data-2011-md/00041840_00046559_1.semileptonic.dst',  # 3.8 GB
], clear=True)

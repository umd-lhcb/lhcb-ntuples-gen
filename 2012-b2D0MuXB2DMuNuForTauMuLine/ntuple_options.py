# License: BSD 2-clause
# Last Change: Thu Dec 20, 2018 at 03:09 PM -0500

#####################
# Configure DaVinci #
#####################

from Configurables import DaVinci

DaVinci().InputType = 'DST'
DaVinci().DataType = '2012'
DaVinci().EvtMax = -1
DaVinci().SkipEvents = 0
DaVinci().Simulation = False

DaVinci().PrintFreq = 100

# Output filename
DaVinci().TupleFile = 'DVntuple.root'

# Only ask for luminosity information when not using simulated data
DaVinci().Lumi = not DaVinci().Simulation


##########################
# Define stripping lines #
##########################

line_data = 'b2D0MuXB2DMuNuForTauMuLine'


############################################
# Stream and stripping line we want to use #
############################################

from Configurables import DecayTreeTuple
from DecayTreeTuple.Configuration import *

stream = 'Semileptonic'

# Create an ntuple to capture semileptonic B decays from the stripping line
dtt = DecayTreeTuple('LFUv')
dtt.Inputs = ['/Event/{0}/Phys/{1}/Particles'.format(stream, line_data)]
#dtt.Decay = '[B~0 -> ^(D*(2010)+ -> ^(D0 -> ^K- ^pi+) ^pi+) ^mu-]CC'  ## Decay from Phoebe's script
dtt.Decay = '[B+ ->  ^(D~0 -> ^K+ ^pi-) ^mu+]CC'   ## The D* is not reconstructed by the stripping line

# dtt.addBranches({
#     "Y" : "^([B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) mu+]CC)",
#     "Dst_2010_minus" : "[B0 -> ^(D*(2010)- -> (D~0 -> K+ pi-) pi-) mu+]CC",
#     "D0" : "[B0 -> (D*(2010)- -> ^(D~0 -> K+ pi-) pi-) mu+]CC",
#     "piminus" : "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) ^pi-) mu+]CC",
#     "piminus0" : "[B0 -> (D*(2010)- -> (D~0 -> K+ ^pi-) pi-) mu+]CC",
#     "Kplus" : "[B0 -> (D*(2010)- -> (D~0 -> ^K+ pi-) pi-) mu+]CC",
#     "muplus" : "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) ^mu+]CC"})

DaVinci().UserAlgorithms += [dtt]


##################
# Define filters #
##################

from PhysConf.Filters import LoKi_Filters



# fltrs = LoKi_Filters(
#   STRIP_Code="HLT_PASS_RE('StrippingD2hhPromptDst2D2KKLineDecision')"
# )
# 
# DaVinci().EventPreFilters = fltrs.filters('Filters')


####################
# Local input file #
####################

from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/mag_down/00041836_00006100_1.semileptonic.dst'
    #'./data/mag_down/00041836_00011435_1.semileptonic.dst'
], clear=True)

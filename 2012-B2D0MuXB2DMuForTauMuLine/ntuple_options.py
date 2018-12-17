# Author: Yipeng Sun <syp at umd dot edu>
# Last Change: Mon Dec 17, 2018 at 01:40 AM -0500

############################################
# Stream and stripping line we want to use #
############################################

from Configurables import DecayTreeTuple
from DecayTreeTuple.Configuration import *

stream = 'AllStreams'
line = 'Strippingb2D0MuXB2DMuForTauMuLine'

# Create an ntuple to capture semileptonic B decays from the stripping line
dtt = DecayTreeTuple('TupleDstToD*Mu+Nu(NuNu)')
dtt.Inputs = ['/Event/{0}/Phys/{1}/Particles'.format(stream, line)]
dtt.Decay = '[D*(2010)+ -> (D0 -> K- K+) pi+]CC'


#####################
# Configure DaVinci #
#####################

from Configurables import DaVinci
from PhysConf.Filters import LoKi_Filters

DaVinci().UserAlgorithms += [dtt]
DaVinci().InputType = 'DST'
DaVinci().TupleFile = 'DVntuple.root'
DaVinci().PrintFreq = 1000
DaVinci().DataType = '2012'
DaVinci().Simulation = False

# Only ask for luminosity information when not using simulated data
DaVinci().Lumi = not DaVinci().Simulation

# DaVinci().EvtMax = 10

# fltrs = LoKi_Filters(
    # STRIP_Code="HLT_PASS_RE('StrippingD2hhPromptDst2D2KKLineDecision')"
# )

# DaVinci().EventPreFilters = fltrs.filters('Filters')


####################
# Local input file #
####################

from GaudiConf import IOHelper

IOHelper().inputFiles([
    './00062514_00000001_7.AllStreams.dst'
], clear=True)

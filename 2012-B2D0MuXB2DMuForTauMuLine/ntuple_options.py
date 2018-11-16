############################################
# Stream and stripping line we want to use #
############################################

from Configurables import DecayTreeTuple
from DecayTreeTuple.Configuration import *

stream = 'AllStreams'
line = 'D2hhPromptDst2D2KKLine'

# Create an ntuple to capture D*+ decays from the StrippingLine line
dtt = DecayTreeTuple('TupleDstToD0pi_D0ToKK')
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
DaVinci().DataType = '2016'
DaVinci().Simulation = True

# Only ask for luminosity information when not using simulated data
DaVinci().Lumi = not DaVinci().Simulation

# DaVinci().EvtMax = 10

# Specify tags for MC data only
DaVinci().CondDBtag = 'sim-20161124-2-vc-md100'
DaVinci().DDDBtag = 'dddb-20150724'

fltrs = LoKi_Filters(
    STRIP_Code="HLT_PASS_RE('StrippingD2hhPromptDst2D2KKLineDecision')"
)

DaVinci().EventPreFilters = fltrs.filters('Filters')


####################
# Local input file #
####################

from GaudiConf import IOHelper

IOHelper().inputFiles([
    './00062514_00000001_7.AllStreams.dst'
], clear=True)

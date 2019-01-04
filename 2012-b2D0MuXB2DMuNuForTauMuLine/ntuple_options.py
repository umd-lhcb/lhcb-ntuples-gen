# License: BSD 2-clause
# Last Change: Fri Jan 04, 2019 at 01:28 PM -0500

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

# Output filenames
DaVinci().TupleFile = './gen/DVntuple.root'
DaVinci().HistogramFile = './gen/DVHisto.root'

# Only ask for luminosity information when not using simulated data
DaVinci().Lumi = not DaVinci().Simulation


###############################
# Define stripping lines, etc #
###############################

line_strip = 'b2D0MuXB2DMuNuForTauMuLine'
line_hlt = 'Hlt2CharmHadD0HH_D02KPi'


###################################
# Customize DaVinci main sequence #
###################################
# These algorithms are executed before any of the selection algorithms.
#
# algorithms defined here will set up stuffs that will be available for all
# selection algorithms.

from Configurables import ChargedProtoParticleMaker

veloprotos = ChargedProtoParticleMaker(name='myProtoPMaker')
veloprotos.Inputs = ['Rec/Track/Best']
veloprotos.Output = 'Rec/ProtoP/myProtoPMaker/ProtoParticles'  # This TES location will be accessible for all selection algorithms

DaVinci().appendToMainSequence([veloprotos])


######################
# Define pre-filters #
######################
# These filters are executed *before* the main selection algorithms to ignore
# obviously uninteresting events.
#
# This should speed up the execution time.

from Configurables import LoKi__HDRFilter as HDRFilter

# Differences between 'HLT_PASS' and 'HLT_PASS_RE':
#   'HLT_PASS' matches the line *exactly*
#   'HLT_PASS_RE' (which was used in the starter kit) use regular expression to
#   check if line given is a part of the lines of the events.
fltr_strip = HDRFilter('StrippedBCands',
                       Code="HLT_PASS('Stripping{0}Decision')".format(
                           line_strip))

fltr_trig = HDRFilter('TriggeredD0',
                      Code="HLT_PASS('{0}Decision')".format(line_hlt))

# DaVinci().EventPreFilters = fltrs.filters('Filters')


###############
# Define cuts #
###############


#####################
# Define selections #
#####################

from Configurables import DecayTreeTuple
# from DecayTreeTuple.Configuration import *

stream = 'Semileptonic'

# Create an ntuple to capture semileptonic B decays from the stripping line
dtt = DecayTreeTuple('LFUv')
dtt.Inputs = ['/Event/{0}/Phys/{1}/Particles'.format(stream, line_strip)]
# dtt.Decay = '[B~0 -> ^(D*(2010)+ -> ^(D0 -> ^K- ^pi+) ^pi+) ^mu-]CC'  # Decay from Phoebe's script
dtt.Decay = '[B+ ->  ^(D~0 -> ^K+ ^pi-) ^mu+]CC'  # The D* is not reconstructed by the stripping line

# dtt.addBranches({
#     "Y" : "^([B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) mu+]CC)",
#     "Dst_2010_minus" : "[B0 -> ^(D*(2010)- -> (D~0 -> K+ pi-) pi-) mu+]CC",
#     "D0" : "[B0 -> (D*(2010)- -> ^(D~0 -> K+ pi-) pi-) mu+]CC",
#     "piminus" : "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) ^pi-) mu+]CC",
#     "piminus0" : "[B0 -> (D*(2010)- -> (D~0 -> K+ ^pi-) pi-) mu+]CC",
#     "Kplus" : "[B0 -> (D*(2010)- -> (D~0 -> ^K+ pi-) pi-) mu+]CC",
#     "muplus" : "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) ^mu+]CC"})

DaVinci().UserAlgorithms += [dtt]


####################
# Local input file #
####################

from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/mag_down/00041836_00006100_1.semileptonic.dst',
    './data/mag_down/00041836_00011435_1.semileptonic.dst'
], clear=True)

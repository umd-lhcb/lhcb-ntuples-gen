# License: BSD 2-clause
# Last Change: Fri Jan 04, 2019 at 04:40 PM -0500

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
from Configurables import TrackScaleState as TrkSS

# Provide required information for Greg's TupleTool.
ms_veloprotos = ChargedProtoParticleMaker(name='myProtoPMaker')
ms_veloprotos.Inputs = ['Rec/Track/Best']
ms_veloprotos.Output = 'Rec/ProtoP/myProtoPMaker/ProtoParticles'  # This TES location will be accessible for all selection algorithms


# According to the source code (available in 'Analysis/Phys/DaVinciTrackScaling/src/TrackScaleState.cpp'):
# Scale the state. Use on DST to scale the track states *before* your user
# algorithms sequence.
# FIXME: don't understand
ms_scaler = TrkSS('StateScale')

DaVinci().appendToMainSequence([ms_veloprotos, ms_scaler])


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
fltr_strip = HDRFilter(
    'StrippedBCands',
    Code="HLT_PASS('Stripping{0}Decision')".format(line_strip))

fltr_hlt = HDRFilter(
    'TriggeredD0',
    Code="HLT_PASS('{0}Decision')".format(line_hlt))


#######################
# Particle references #
#######################

# It seems that 'DataOnDemand' is a misnomer of 'AutomaticData'
from PhysSelPython.Wrappers import AutomaticData

pr_stripped = AutomaticData(
    Location='/Event/Semileptonic/Phys/{0}/Particles'.format(line_strip))

pr_all_pi = AutomaticData(Location='Phys/StdAllLoosePions/Particles')

# standard NoPIDs upstream pions
pr_up_pi = AutomaticData(Location='Phys/StdNoPIDsUpPions/Particles')


############################
# Define simple selections #
############################
# 'simple' means that algorithms for these selections are effectively one-
# liners.

from PhysSelPython.Wrappers import Selection
from Configurables import FilterDesktop, FilterInTrees

sel_stripped_filtered = Selection(
    'SelMyStrippedFiltered',
    Algorithm=FilterDesktop(
        'MyStrippedFiltered',
        Code="INTREE((ABSID == 'mu+') & (TIS('L0.*', 'L0TriggerTisTos')))"
    ),
    RequiredSelections=[pr_stripped]
)

# NOTE: 'charged' means +/-.
sel_charged_K = Selection(
    'SelMyChargedK',
    Algorithm=FilterInTrees('MyChargedK', Code="(ABSID == 'K+')"),
    RequiredSelections=[sel_stripped_filtered]
)

sel_charged_pi = Selection(
    'SelMyChargedPi',
    Algorithm=FilterInTrees('MyChargedPi', Code="(ABSID == 'pi+')"),
    RequiredSelections=[sel_stripped_filtered]
)

sel_charged_mu = Selection(
    'SelMyChargedMu',
    Algorithm=FilterInTrees('MyChargedMu', Code="(ABSID == 'mu+')"),
    RequiredSelections=[sel_stripped_filtered]
)


#####################
# Define algorithms #
#####################

from Configurables import CombineParticles

# D0 ###########################################################################
algo_D0 = CombineParticles('MyD0')
algo_D0.DecayDescriptor = '[D0 -> K- pi+]CC'

algo_D0.DaughtersCuts = {
    # PT: transverse momentum
    # MIPCHI2DV: minimum IP-chi^2
    # TRCHI2DOF: chi^2 per degree of freedom of the track fit
    # PIDK: combined delta-log-likelihood for the given hypothesis (wrt the
    #       pion)
    # TRGHOSTPROB: track ghost probability
    'K+': '(PT > 300*MeV) & (MIPCHI2DV(PRIMARY) > 45.0) &' + \
          '(TRCHI2DOF < 4) & (PIDK > 4) & (TRGHOSTPROB < 0.5)',
    'pi-': '(PT > 300*MeV) & (MIPCHI2DV(PRIMARY) > 45.0) &' + \
           '(TRCHI2DOF < 4) & (PIDK < 2) & (TRGHOSTPROB < 0.5)'
}

# ADAMASS: the absolute mass difference to the PDG reference value
algo_D0.CombinationCut = "(ADAMASS('D0') < 200*MeV)"

# ADMASS: the absolute mass difference to the reference value
# VFASPF: vertex function as particle function
#         Allow to apply vertex functors to the particle's `endVertex()`
# VCHI2: vertex chi^2
# VDOF: vertex fit number of degree of freedom
algo_D0.MotherCut = "(ADMASS('D0') < 100*MeV) & (VFASPF(VCHI2/VDOF) < 100)"

# This is the default setting now, and should be no longer needed
# algo_D0.ParticleCombiners.update({'': 'LoKi::VertexFitter'})

# Dstar ########################################################################
algo_Dst = CombineParticles("MyDstar")
algo_Dst.DecayDescriptor = '[D*(2010)+ -> D0 pi+]CC'

algo_Dst.DaughtersCuts = {
    'pi+': '(MIPCHI2DV(PRIMARY) > 0.0) & (TRCHI2DOF < 3) & (TRGHOSTPROB < 0.25)'
}

algo_Dst.MotherCut = "(ADMASS('D*(2010)+') < 220*MeV)"

# Bd ###########################################################################
algo_Bd = CombineParticles("MyBd")
algo_Bd.DecayDescriptor = "[B~0 -> D*(2010)+ mu-]CC"

# ALL: trivial select all
algo_Bd.DaughtersCuts = {
    "mu-": "ALL"
}

# AM: mass of the combination
#     Return sqrt(E^2 - p^2)
algo_Bd.CombinationCut = '(AM < 10200*MeV)'

# BPVDIRA: direction angle
#          Compute the cosine of the angle between the momentum of the particle
#          and the direction to flight from the best PV to the decay vertex.
algo_Bd.MotherCut = "(M < 10000*MeV) & (BPVDIRA > 0.9995) &" + \
                    "(VFASPF(VCHI2/VDOF)<6.0)"


#####################
# Define selections #
#####################

from Configurables import FitDecayTrees

sel_D0 = Selection(
    'SelMyD0',
    Algorithm=algo_D0,
    RequiredSelections=[sel_charged_K, sel_charged_pi]
)

sel_Dst = Selection(
    'SelMyDst',
    Algorithm=algo_Dst,
    RequiredSelections=[sel_D0, pr_all_pi, pr_up_pi]
)

sel_Bd = Selection(
    'SelMyWSBd',
    Algorithm=algo_Bd,
    RequiredSelections=[sel_Dst, sel_charged_mu]
)

sel_refit_b2DstMu = Selection(
    'SelMyYDTF',
    Algorithm=FitDecayTrees(
        'MyRefitb2DstMu',
        Code="DECTREE('[B~0 -> (D*(2010)+ -> (D0->K- pi+) pi+) mu-]CC')",
        UsePVConstraint=False,
        Inputs=[sel_Bd.outputLocation()]
    ),
    RequiredSelections=[sel_Bd]
)


##############################
# Define selection sequences #
##############################

from PhysSelPython.Wrappers import SelectionSequence

selseq_y_maker = SelectionSequence(
    'SelSeqMyYMaker',
    EventPreSelector=[fltr_hlt, fltr_strip],
    TopSelection=sel_refit_b2DstMu
)


DaVinci().UserAlgorithms += [selseq_y_maker.sequence()]


###################
# Define n-tuples #
###################

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

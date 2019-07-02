# Author: Phoebe Hamilton, Manuel Franco Sevilla, Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Jul 02, 2019 at 05:48 PM -0400

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
DaVinci().TupleFile = './gen/YCands.root'
# DaVinci().HistogramFile = './gen/YCands_hist.root'

# Only ask for luminosity information when not using simulated data
DaVinci().Lumi = not DaVinci().Simulation


###################################
# Customize DaVinci main sequence #
###################################
# These algorithms are executed before any of the selection algorithms.
#
# algorithms defined here will set up stuffs that will be available for all
# selection algorithms.

from Configurables import ChargedProtoParticleMaker
from Configurables import NoPIDsParticleMaker
from Configurables import TrackScaleState as TrkSS

# Provide required information for Greg's TupleTool.
ms_velo_protos = ChargedProtoParticleMaker(name='MyProtoPMaker')
ms_velo_protos.Inputs = ['Rec/Track/Best']
ms_velo_protos.Output = 'Rec/ProtoP/MyProtoPMaker/ProtoParticles'  # This TES location will be accessible for all selection algorithms

# VELO pions for Greg's isolation tool.
ms_velo_pions = NoPIDsParticleMaker('StdNoPIDsVeloPions', Particle='pion')
ms_velo_pions.Input = 'Rec/ProtoP/MyProtoPMaker/ProtoParticles'

# According to the source code (available in 'Analysis/Phys/DaVinciTrackScaling/src/TrackScaleState.cpp'):
# Scale the state. Use on DST to scale the track states *before* your user
# algorithms sequence.
ms_scaler = TrkSS('StateScale')


DaVinci().appendToMainSequence([ms_velo_protos, ms_velo_pions, ms_scaler])


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
line_strip = 'b2D0MuXB2DMuNuForTauMuLine'
fltr_strip = HDRFilter(
    'StrippedBCands',
    Code="HLT_PASS('Stripping{0}Decision')".format(line_strip))

line_hlt = 'Hlt2CharmHadD02HH_D02KPi'
fltr_hlt = HDRFilter(
    'Hlt2TriggeredD0',
    Code="HLT_PASS('{0}Decision')".format(line_hlt))


#######################
# Particle references #
#######################

# It seems that 'DataOnDemand' is a misnomer of 'AutomaticData'
from PhysSelPython.Wrappers import AutomaticData

pr_stripped = AutomaticData(
    Location='/Event/Semileptonic/Phys/{0}/Particles'.format(line_strip))

pr_all_pi = AutomaticData(Location='Phys/StdAllLoosePions/Particles')

# standard NoPIDs upstream pions (VELO + TT hits, no T-layers).
# They only added 10% with terrible mass resolution, so they didn't use them in
# the end.
# pr_up_pi = AutomaticData(Location='Phys/StdNoPIDsUpPions/Particles')


############################
# Define simple selections #
############################
# 'simple' means that algorithms for these selections are effectively one-
# liners.

from PhysSelPython.Wrappers import Selection
from Configurables import FilterDesktop, FilterInTrees

# This selects events that have a muon and was triggered regardless of the muon
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

sel_charged_Pi = Selection(
    'SelMyChargedPi',
    Algorithm=FilterInTrees('MyChargedPi', Code="(ABSID == 'pi+')"),
    RequiredSelections=[sel_stripped_filtered]
)

sel_charged_Mu = Selection(
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
algo_D0.DecayDescriptor = '[D0 -> K- pi+]cc'

# These cuts are imposed by the stripping line
# http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping21/semileptonic/strippingb2d0muxb2dmunufortaumuline.html
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

# ADAMASS: the absolute mass difference to the PDG reference value, this functor
#          takes an array as input, unlike ADMASS, which takes a scaler.
# .CombinationCut are cuts made before the vertex fit, so it saves time
algo_D0.CombinationCut = "(ADAMASS('D0') < 200*MeV)"

# ADMASS: the absolute mass difference to the PDG reference value, but it is
#         used after the vertex fit
# VFASPF: vertex function as particle function
#         Allow to apply vertex functors to the particle's `endVertex()`
# VCHI2: vertex chi^2
# VDOF: vertex fit number of degree of freedom
# .MotherCut are cuts after the vertex fit, that's why the mass cut is tighter
algo_D0.MotherCut = "(ADMASS('D0') < 100*MeV) & (VFASPF(VCHI2/VDOF) < 100)"

# This is the default setting now, and should be no longer needed
# algo_D0.ParticleCombiners.update({'': 'LoKi::VertexFitter'})


# Dstar ########################################################################
algo_Dst = CombineParticles('MyDstar')
algo_Dst.DecayDescriptor = '[D*(2010)+ -> D0 pi+]cc'

algo_Dst.DaughtersCuts = {
    'pi+': '(MIPCHI2DV(PRIMARY) > 0.0) & (TRCHI2DOF < 3) & (TRGHOSTPROB < 0.25)'
}

algo_Dst.CombinationCut = "(ADAMASS('D*(2010)+') < 220*MeV)"
algo_Dst.MotherCut = "(ADMASS('D*(2010)+') < 125*MeV) &" + \
    "(M-MAXTREE(ABSID=='D0', M) < 160*MeV) &" + \
    "(VFASPF(VCHI2/VDOF) < 100)"


# DstarWS ######################################################################
algo_Dst_ws = CombineParticles('MyDstarWS')
algo_Dst_ws.DecayDescriptor = '[D*(2010)- -> D0 pi-]cc'

algo_Dst_ws.DaughtersCuts = algo_Dst.DaughtersCuts
algo_Dst_ws.CombinationCut = algo_Dst.CombinationCut
algo_Dst_ws.MotherCut = algo_Dst.MotherCut


# Bd ###########################################################################
algo_Bd = CombineParticles('MyBd')
algo_Bd.DecayDescriptor = "[B~0 -> D*(2010)+ mu-]cc"

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
                    "(VFASPF(VCHI2/VDOF) < 6.0)"


# BdWSMu #######################################################################
algo_Bd_ws_Mu = CombineParticles('MyBdWSMu')
algo_Bd_ws_Mu.DecayDescriptor = "[B~0 -> D*(2010)+ mu+]cc"

algo_Bd_ws_Mu.DaughtersCuts = {
    "mu+": "ALL"
}

algo_Bd_ws_Mu.CombinationCut = algo_Bd.CombinationCut
algo_Bd_ws_Mu.MotherCut = algo_Bd.MotherCut


# BdWSPi #######################################################################
algo_Bd_ws_Pi = CombineParticles('MyBdWSPi')
algo_Bd_ws_Pi.DecayDescriptor = "[B0 -> D*(2010)+ mu+]cc"

algo_Bd_ws_Pi.DaughtersCuts = algo_Bd_ws_Mu.DaughtersCuts
algo_Bd_ws_Pi.CombinationCut = algo_Bd.CombinationCut
algo_Bd_ws_Pi.MotherCut = algo_Bd.MotherCut


#####################
# Define selections #
#####################

from Configurables import FitDecayTrees

# For SeqMyYMaker ##############################################################

# RequiredSelections takes a union of supplied selections, thus orderless.
sel_D0 = Selection(
    'SelMyD0',
    Algorithm=algo_D0,
    RequiredSelections=[sel_charged_K, sel_charged_Pi]
)

# Removed the upstream pions, which were not used by Greg/Phoebe
sel_Dst = Selection(
    'SelMyDst',
    Algorithm=algo_Dst,
    RequiredSelections=[sel_D0, pr_all_pi]
)

sel_Bd = Selection(
    'SelMyBd',
    Algorithm=algo_Bd,
    RequiredSelections=[sel_Dst, sel_charged_Mu]
)

sel_refit_b2DstMu = Selection(
    'SelMyRefitb2DstMu',
    Algorithm=FitDecayTrees(
        'MyRefitb2DstMu',
        Code="DECTREE('[B~0 -> (D*(2010)+ -> (D0->K- pi+) pi+) mu-]CC')",
        UsePVConstraint=False,
        Inputs=[sel_Bd.outputLocation()]
    ),
    RequiredSelections=[sel_Bd]
)


# For SeqMyYMakerWSMu ##########################################################
sel_Bd_ws_Mu = Selection(
    'SelMyBdWSMu',
    Algorithm=algo_Bd_ws_Mu,
    RequiredSelections=[sel_Dst, sel_charged_Mu]
)

sel_refit_b2DstMu_ws_Mu = Selection(
    'SelMyRefitb2DstMuWSMu',
    Algorithm=FitDecayTrees(
        'MyRefitb2DstMuWSMu',
        Code="DECTREE('[B~0 -> (D*(2010)+ -> (D0->K- pi+) pi+) mu+]CC')",
        UsePVConstraint=False,
        Inputs=[sel_Bd_ws_Mu.outputLocation()]
    ),
    RequiredSelections=[sel_Bd_ws_Mu]
)

# For SeqMyYMakerWSPi ##########################################################
sel_Dst_ws = Selection(
    'SelMyDstWS',
    Algorithm=algo_Dst_ws,
    RequiredSelections=[sel_D0, pr_all_pi]
)

sel_Bd_ws_Pi = Selection(
    'SelMyBdWSPi',
    Algorithm=algo_Bd_ws_Pi,
    RequiredSelections=[sel_Dst_ws, sel_charged_Mu]
)

sel_refit_b2DstMu_ws_Pi = Selection(
    'SelMyRefitb2DstMuWSPi',
    Algorithm=FitDecayTrees(
        'MyRefitb2DstMuWSPi',
        Code="DECTREE('[B~0 -> (D*(2010)- -> (D0->K- pi+) pi-) mu-]CC')",
        UsePVConstraint=False,
        Inputs=[sel_Bd_ws_Pi.outputLocation()]
    ),
    RequiredSelections=[sel_Bd_ws_Pi]
)


##############################
# Define selection sequences #
##############################

from PhysSelPython.Wrappers import SelectionSequence

seq_Y = SelectionSequence(
    'SeqMyY',
    EventPreSelector=[fltr_hlt, fltr_strip],
    TopSelection=sel_refit_b2DstMu
)

seq_Y_ws_Mu = SelectionSequence(
    'SeqMyYWSMu',
    EventPreSelector=[fltr_hlt, fltr_strip],
    TopSelection=sel_refit_b2DstMu_ws_Mu
)

seq_Y_ws_Pi = SelectionSequence(
    'SeqMyYWSPi',
    EventPreSelector=[fltr_hlt, fltr_strip],
    TopSelection=sel_refit_b2DstMu_ws_Pi
)


DaVinci().UserAlgorithms += [seq_Y.sequence(),
                             seq_Y_ws_Mu.sequence(),
                             seq_Y_ws_Pi.sequence()]


###################
# Define n-tuples #
###################

from Configurables import DecayTreeTuple
from Configurables import TupleToolApplyIsolation
from Configurables import TupleToolTagDiscardDstMu
from Configurables import TupleToolANNPIDTraining
from Configurables import TupleToolTauMuDiscrVars
from DecayTreeTuple.Configuration import *  # for addTupleTool


def tuple_initializer(name, sel_seq, decay):
    tp = DecayTreeTuple(name)
    tp.addTupleTool('TupleToolTrackInfo')  # For addBranches
    tp.Inputs = [sel_seq.outputLocation()]
    tp.Decay = decay
    return tp


def tuple_postpocess(tp, weights='./weights_soft.xml'):
    tp.Y.addTool(TupleToolTagDiscardDstMu, name='TupleMyDiscardDstMu')
    tp.Y.ToolList += ['TupleToolTagDiscardDstMu/TupleMyDiscardDstMu']

    tp.Y.addTool(TupleToolApplyIsolation, name='TupleMyApplyIso')
    tp.Y.TupleMyApplyIso.WeightsFile = weights
    tp.Y.ToolList += ['TupleToolApplyIsolation/TupleMyApplyIso']

    tp.Y.addTool(TupleToolTauMuDiscrVars, name='TupleMyRFA')
    tp.Y.ToolList += ['TupleToolTauMuDiscrVars/TupleMyRFA']

    tp.muplus.ToolList += ['TupleToolANNPIDTraining']


# Y ############################################################################
tp_Y = tuple_initializer(
    'TupleY',
    seq_Y,
    '[B~0 -> ^(D*(2010)+ -> ^(D0 -> ^K- ^pi+) ^pi+) ^mu-]CC'
)

tp_Y.addBranches({
    "Y": "^([B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) mu+]CC)",
    "Dst_2010_minus": "[B0 -> ^(D*(2010)- -> (D~0 -> K+ pi-) pi-) mu+]CC",
    "D0": "[B0 -> (D*(2010)- -> ^(D~0 -> K+ pi-) pi-) mu+]CC",
    "piminus": "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) ^pi-) mu+]CC",
    "piminus0": "[B0 -> (D*(2010)- -> (D~0 -> K+ ^pi-) pi-) mu+]CC",
    "Kplus": "[B0 -> (D*(2010)- -> (D~0 -> ^K+ pi-) pi-) mu+]CC",
    "muplus": "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) ^mu+]CC"})

tuple_postpocess(tp_Y)


# Y_ws_Mu ######################################################################
tp_Y_ws_Mu = tuple_initializer(
    'TupleYWSMu',
    seq_Y_ws_Mu,
    '[B~0 -> ^(D*(2010)+ -> ^(D0 -> ^K- ^pi+) ^pi+) ^mu+]CC'
)

tp_Y_ws_Mu.addBranches({
    "Y": "^([B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) mu-]CC)",
    "Dst_2010_minus": "[B0 -> ^(D*(2010)- -> (D~0 -> K+ pi-) pi-) mu-]CC",
    "D0": "[B0 -> (D*(2010)- -> ^(D~0 -> K+ pi-) pi-) mu-]CC",
    "piminus": "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) ^pi-) mu-]CC",
    "piminus0": "[B0 -> (D*(2010)- -> (D~0 -> K+ ^pi-) pi-) mu-]CC",
    "Kplus": "[B0 -> (D*(2010)- -> (D~0 -> ^K+ pi-) pi-) mu-]CC",
    "muplus": "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) ^mu-]CC"})

tuple_postpocess(tp_Y_ws_Mu)


# Y_ws_Pi ######################################################################
tp_Y_ws_Pi = tuple_initializer(
    'TupleYWSPi',
    seq_Y_ws_Pi,
    '[B~0 -> ^(D*(2010)- -> ^(D0 -> ^K- ^pi+) ^pi-) ^mu-]CC'
)

tp_Y_ws_Pi.addBranches({
    "Y": "^([B0 -> (D*(2010)+ -> (D~0 -> K+ pi-) pi+) mu+]CC)",
    "Dst_2010_minus": "[B0 -> ^(D*(2010)+ -> (D~0 -> K+ pi-) pi+) mu+]CC",
    "D0": "[B0 -> (D*(2010)+ -> ^(D~0 -> K+ pi-) pi+) mu+]CC",
    "piminus": "[B0 -> (D*(2010)+ -> (D~0 -> K+ pi-) ^pi+) mu+]CC",
    "piminus0": "[B0 -> (D*(2010)+ -> (D~0 -> K+ ^pi-) pi+) mu+]CC",
    "Kplus": "[B0 -> (D*(2010)+ -> (D~0 -> ^K+ pi-) pi+) mu+]CC",
    "muplus": "[B0 -> (D*(2010)+ -> (D~0 -> K+ pi-) pi+) ^mu+]CC"})

tuple_postpocess(tp_Y_ws_Pi)


DaVinci().UserAlgorithms += [tp_Y, tp_Y_ws_Mu, tp_Y_ws_Pi]


####################
# Local input file #
####################

from GaudiConf import IOHelper

IOHelper().inputFiles([
    './data/mag_down/00041836_00006100_1.semileptonic.dst',  # 95 MB
    './data/mag_down/00041836_00011435_1.semileptonic.dst',  # 1.3 GB
    './data/mag_down/00041836_00013110_1.semileptonic.dst',  # 2.9 GB
], clear=True)

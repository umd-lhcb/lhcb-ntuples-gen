# Author: Phoebe Hamilton, Manuel Franco Sevilla, Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Apr 15, 2020 at 02:05 AM +0800
#
# Description: Definitions of selection and reconstruction procedures for run 1,
#              With thorough comments.


################################################################################
# General helper                                                               #
################################################################################


################################################################################
# Dst                                                                          #
################################################################################

###################################
# Customize DaVinci main sequence #
###################################
# These algorithms are executed before any of the selection algorithms.
#
# algorithms defined here will set up locations that will be available for all
# selection algorithms.

from Configurables import ChargedProtoParticleMaker
from Configurables import NoPIDsParticleMaker
from Configurables import TrackScaleState
from Configurables import TrackSmearState

# Provide required information for VELO pions.
ms_all_protos = ChargedProtoParticleMaker(name='MyProtoPMaker')
ms_all_protos.Inputs = ['Rec/Track/Best']
ms_all_protos.Output = 'Rec/ProtoP/MyProtoPMaker/ProtoParticles'  # This TES location will be accessible for all selection algorithms

# VELO pions for Greg's isolation tool.
# NOTE: The name 'StdNoPIDsVeloPions' is hard-coded in the tuple tool, so the
#       name should not be changed.
ms_velo_pions = NoPIDsParticleMaker('StdNoPIDsVeloPions', Particle='pion')
ms_velo_pions.Input = ms_all_protos.Output

# According to the source code (available in 'Analysis/Phys/DaVinciTrackScaling/src/TrackScaleState.cpp'):
# Scale the state. Use on DST to scale the track states *before* your user
# algorithms sequence.
ms_scale = TrackScaleState('StateScale')

# Smear the momentum of MC particles, because the resolution is too good.
ms_smear = TrackSmearState('StateSmear')


######################
# Define pre-filters #
######################
# These filters are executed *before* the main selection algorithms to ignore
# obviously uninteresting events.
#
# Applying these filters should speed up the execution time.

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
# These references let us use *all* particles of a particular kind in an event,
# instead of just particles that pass the stripping condition.

from PhysSelPython.Wrappers import AutomaticData

# Events tagged with our stripping line
pr_stripped = AutomaticData(
    Location='/Event/Semileptonic/Phys/{0}/Particles'.format(line_strip))

pr_charged_K = AutomaticData(Location='Phys/StdAllNoPIDsKaons/Particles')

pr_charged_Pi = AutomaticData(Location='Phys/StdAllNoPIDsPions/Particles')
pr_all_Pi = AutomaticData(Location='Phys/StdAllLoosePions/Particles')
# standard NoPIDs upstream pions (VELO + TT hits, no T-layers).
# They only added 10% with terrible mass resolution, so they didn't use them in
# the end.
# pr_up_Pi = AutomaticData(Location='Phys/StdNoPIDsUpPions/Particles')

pr_Mu = AutomaticData(Location='Phys/StdAllNoPIDsMuons/Particles')


############################
# Define simple selections #
############################
# 'simple' means that algorithms for these selections are effectively one-
# liners.

from PhysSelPython.Wrappers import Selection
from Configurables import FilterDesktop, FilterInTrees
from Configurables import TisTosParticleTagger

# NOTE: 'stripped' selections require the existence of a stripping line, which
#       only exists in data, not MC.

# This selects events that have a muon and was triggered regardless of the muon
sel_stripped_filtered = Selection(
    'SelMyStrippedFiltered',
    Algorithm=FilterDesktop(
        'MyStrippedFiltered',
        Code="INTREE((ABSID == 'mu+') & (TIS('L0.*', 'L0TriggerTisTos')))"
    ),
    RequiredSelections=[pr_stripped]
)

sel_stripped_charged_K = Selection(
    'SelMyStrippedChargedK',
    Algorithm=FilterInTrees('MyChargedK', Code="(ABSID == 'K+')"),
    RequiredSelections=[sel_stripped_filtered]
)

sel_stripped_charged_Pi = Selection(
    'SelMyStrippedChargedPi',
    Algorithm=FilterInTrees('MyChargedPi', Code="(ABSID == 'pi+')"),
    RequiredSelections=[sel_stripped_filtered]
)

sel_stripped_Mu = Selection(
    'SelMyStrippedMu',
    Algorithm=FilterInTrees('MyMu', Code="(ABSID == 'mu+')"),
    RequiredSelections=[sel_stripped_filtered]
)

# We build our own Muons, instead of using stripping line Muons.
# See https://github.com/umd-lhcb/lhcb-ntuples-gen/issues/25 for an explanation.
sel_unstripped_tis_filtered_Mu = Selection(
    'SelMyUnstrippedMu',
    Algorithm=TisTosParticleTagger(
        'MyMuTisTagger',
        Inputs=['Phys/StdAllNoPIDsMuons/Particles'],
        TisTosSpecs={'L0Global%TIS': 0}),
    RequiredSelections=[pr_Mu]
)


#####################
# Define algorithms #
#####################

from Configurables import CombineParticles

algo_mc_match_preambulo = [
    'from LoKiMC.functions import *',
    'from LoKiPhysMC.decorators import *',
    'from LoKiPhysMC.functions import *'
]

# D0 ###########################################################################
algo_D0 = CombineParticles('MyD0')
algo_D0.DecayDescriptor = '[D0 -> K- pi+]cc'

# These cuts are imposed by the stripping line
# http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping21/semileptonic/strippingb2d0muxb2dmunufortaumuline.html

# PT: transverse momentum
# MIPCHI2DV: minimum IP-chi^2
# TRCHI2DOF: chi^2 per degree of freedom of the track fit
# PIDK: combined delta-log-likelihood for the given hypothesis (wrt the
#       pion)
# TRGHOSTPROB: track ghost probability
algo_D0.DaughtersCuts = {
    'K+': '(PT > 300*MeV) & (MIPCHI2DV(PRIMARY) > 45.0) &' +
          '(PIDK > 4) & (TRGHOSTPROB < 0.5)',
          # '(TRCHI2DOF < 4) & (PIDK > 4) & (TRGHOSTPROB < 0.5)',
    'pi-': '(PT > 300*MeV) & (MIPCHI2DV(PRIMARY) > 45.0) &' +
           '(PIDK < 2) & (TRGHOSTPROB < 0.5)'
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


# Dst ##########################################################################
algo_Dst = CombineParticles('MyDst')
algo_Dst.DecayDescriptor = '[D*(2010)+ -> D0 pi+]cc'

algo_Dst.DaughtersCuts = {
    'pi+': '(MIPCHI2DV(PRIMARY) > 0.0) & (TRCHI2DOF < 3) & (TRGHOSTPROB < 0.25)'
}

algo_Dst.CombinationCut = "(ADAMASS('D*(2010)+') < 220*MeV)"
algo_Dst.MotherCut = "(ADMASS('D*(2010)+') < 125*MeV) &" + \
                     "(M-MAXTREE(ABSID=='D0', M) < 160*MeV) &" + \
                     "(VFASPF(VCHI2/VDOF) < 100)"


# DstWS ########################################################################
# 'WS' stands for 'wrong sign'
algo_Dst_ws = CombineParticles('MyDstWS')
algo_Dst_ws.DecayDescriptor = '[D*(2010)- -> D0 pi-]cc'

algo_Dst_ws.DaughtersCuts = algo_Dst.DaughtersCuts
algo_Dst_ws.CombinationCut = algo_Dst.CombinationCut
algo_Dst_ws.MotherCut = algo_Dst.MotherCut


# B0 ###########################################################################
algo_B0 = CombineParticles('MyB0')
algo_B0.DecayDescriptor = "[B~0 -> D*(2010)+ mu-]cc"  # B~0 is the CC of B0

# ALL: trivial select all
algo_B0.DaughtersCuts = {
    "mu-": "ALL"
}

# AM: mass of the combination
#     Return sqrt(E^2 - p^2)
algo_B0.CombinationCut = '(AM < 10200*MeV)'

# BPVDIRA: direction angle
#          Compute the cosine of the angle between the momentum of the particle
#          and the direction to flight from the best PV to the decay vertex.
algo_B0.MotherCut = "(M < 10000*MeV) & (BPVDIRA > 0.9995) &" + \
                    "(VFASPF(VCHI2/VDOF) < 6.0)"


# B0WSMu #######################################################################
# Here the muon has the wrong sign---charge not conserved.
algo_B0_ws_Mu = CombineParticles('MyB0WSMu')
algo_B0_ws_Mu.DecayDescriptor = "[B~0 -> D*(2010)+ mu+]cc"

algo_B0_ws_Mu.DaughtersCuts = {
    "mu+": "ALL"
}

algo_B0_ws_Mu.CombinationCut = algo_B0.CombinationCut
algo_B0_ws_Mu.MotherCut = algo_B0.MotherCut


# B0WSPi #######################################################################
# Here, due to the wrong quark content of B0, instead of B~0, the pion (not
# listed here) will have wrong sign.
# In other words, this time, D* has the wrong sign.
algo_B0_ws_Pi = CombineParticles('MyB0WSPi')
algo_B0_ws_Pi.DecayDescriptor = "[B0 -> D*(2010)+ mu+]cc"

algo_B0_ws_Pi.DaughtersCuts = algo_B0_ws_Mu.DaughtersCuts
algo_B0_ws_Pi.CombinationCut = algo_B0.CombinationCut
algo_B0_ws_Pi.MotherCut = algo_B0.MotherCut


#####################
# Define selections #
#####################

from Configurables import FitDecayTrees

# For SeqMyB0 ###################################################################

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
    RequiredSelections=[sel_D0, pr_all_Pi]
)

sel_B0 = Selection(
    'SelMyB0',
    Algorithm=algo_B0,
    RequiredSelections=[sel_Dst, sel_Mu]
)

sel_refit_B02DstMu = Selection(
    'SelMyRefitB02DstMu',
    Algorithm=FitDecayTrees(
        'MyRefitB02DstMu',
        Code="DECTREE('[B~0 -> (D*(2010)+ -> (D0->K- pi+) pi+) mu-]CC')",
        UsePVConstraint=False,
        Inputs=[sel_B0.outputLocation()]
    ),
    RequiredSelections=[sel_B0]
)


# For SeqMyB0WSMu ###############################################################
sel_B0_ws_Mu = Selection(
    'SelMyB0WSMu',
    Algorithm=algo_B0_ws_Mu,
    RequiredSelections=[sel_Dst, sel_Mu]
)

sel_refit_B02DstMu_ws_Mu = Selection(
    'SelMyRefitB02DstMuWSMu',
    Algorithm=FitDecayTrees(
        'MyRefitB02DstMuwsMu',
        Code="DECTREE('[B~0 -> (D*(2010)+ -> (D0->K- pi+) pi+) mu+]CC')",
        UsePVConstraint=False,
        Inputs=[sel_B0_ws_Mu.outputLocation()]
    ),
    RequiredSelections=[sel_B0_ws_Mu]
)

# For SeqMyB0WSPi ###############################################################
sel_Dst_ws = Selection(
    'SelMyDstWS',
    Algorithm=algo_Dst_ws,
    RequiredSelections=[sel_D0, pr_all_Pi]
)

sel_B0_ws_Pi = Selection(
    'SelMyB0WSPi',
    Algorithm=algo_B0_ws_Pi,
    RequiredSelections=[sel_Dst_ws, sel_Mu]
)

sel_refit_B02DstMu_ws_Pi = Selection(
    'SelMyRefitB02DstMuWSPi',
    Algorithm=FitDecayTrees(
        'MyRefitB02DstMuWSPi',
        Code="DECTREE('[B~0 -> (D*(2010)- -> (D0->K- pi+) pi-) mu-]CC')",
        UsePVConstraint=False,
        Inputs=[sel_B0_ws_Pi.outputLocation()]
    ),
    RequiredSelections=[sel_B0_ws_Pi]
)


##############################
# Define selection sequences #
##############################

from PhysSelPython.Wrappers import SelectionSequence

seq_B0 = SelectionSequence(
    'SeqMyB0',
    EventPreSelector=event_pre_selectors,
    TopSelection=sel_refit_B02DstMu
)

seq_B0_ws_Mu = SelectionSequence(
    'SeqMyB0WSMu',
    EventPreSelector=event_pre_selectors,
    TopSelection=sel_refit_B02DstMu_ws_Mu
)

seq_B0_ws_Pi = SelectionSequence(
    'SeqMyB0WSPi',
    EventPreSelector=event_pre_selectors,
    TopSelection=sel_refit_B02DstMu_ws_Pi
)


###################
# Define n-tuples #
###################

# Tools for data
from Configurables import DecayTreeTuple
from Configurables import TupleToolApplyIsolation
from Configurables import TupleToolTagDiscardDstMu
from Configurables import TupleToolANNPIDTraining
from Configurables import TupleToolTauMuDiscrVars
from DecayTreeTuple.Configuration import *  # for addTupleTool

# Additional tools for MC
from Configurables import TupleToolMCTruth
from Configurables import TupleToolMCBackgroundInfo
from Configurables import TupleToolKinematic
from Configurables import BackgroundCategory
from Configurables import LoKi__Hybrid__EvtTupleTool as LokiEvtTool
from Configurables import TupleToolTrigger
from Configurables import TupleToolTISTOS


def tuple_initialize_data(name, sel_seq, decay):
    tp = DecayTreeTuple(name)
    tp.addTupleTool('TupleToolTrackInfo')  # For addBranches
    tp.Inputs = [sel_seq.outputLocation()]
    tp.Decay = decay

    tp.ToolList += [
        'TupleToolKinematic',
        'TupleToolAngles',
        'TupleToolPid',  # This one produces 'PIDmu', and other PID variables
        'TupleToolMuonPid',  # This write out NN mu inputs
        'TupleToolL0Calo',
    ]

    # Save trigger decisions.
    tt_tistos = tp.addTupleTool('TupleToolTISTOS')
    tt_tistos.TriggerList = [
        'L0MuonDecision',
        'L0HadronDecision',
        'Hlt1TrackAllL0Decision',
        'Hlt2CharmHadD02HH_D02KPiDecision'
    ]
    tt_tistos.VerboseL0 = True
    tt_tistos.VerboseHlt1 = True
    tt_tistos.VerboseHlt2 = True

    # Add event-level information.
    tt_loki_evt = tp.addTupleTool(LokiEvtTool, "TupleMyLokiEvtTool")
    tt_loki_evt.Preambulo += ['from LoKiCore.functions import *']
    tt_loki_evt.VOID_Variables = {
        'nTracks': "CONTAINS('Rec/Track/Best')",
        'nSPDhits': "CONTAINS('Raw/Spd/Digits')",
    }

    return tp


def tuple_initialize_mc(name, sel_seq, decay):
    tp = tuple_initialize_data(name, sel_seq, decay)

    tt_mcbi = tp.addTupleTool('TupleToolMCBackgroundInfo')
    tt_mcbi.addTool(BackgroundCategory, name="BackgroundCategory")
    tt_mcbi.BackgroundCategory.SemileptonicDecay = True
    tt_mcbi.BackgroundCategory.NumNeutrinos = 3

    tt_truth = tp.addTupleTool('TupleToolMCTruth')
    tt_truth.ToolList = [
        'MCTupleToolKinematic',
        'MCTupleToolHierarchy'
    ]

    return tp


def tuple_postpocess_data(tp, weights='./weights_soft.xml'):
    tp.Y.addTool(TupleToolTagDiscardDstMu, name='TupleMyDiscardDstMu')
    tp.Y.ToolList += ['TupleToolTagDiscardDstMu/TupleMyDiscardDstMu']

    tp.Y.addTool(TupleToolApplyIsolation, name='TupleMyApplyIso')
    tp.Y.TupleMyApplyIso.WeightsFile = weights
    tp.Y.ToolList += ['TupleToolApplyIsolation/TupleMyApplyIso']

    tp.Y.addTool(TupleToolTauMuDiscrVars, name='TupleMyRFA')
    tp.Y.ToolList += ['TupleToolTauMuDiscrVars/TupleMyRFA']

    tp.muplus.ToolList += ['TupleToolANNPIDTraining']


def tuple_postpocess_mc(tp, weights='./weights_soft.xml'):
    tuple_postpocess_data(tp, weights)


# B0 ###########################################################################
tp_B0 = tuple_initialize(
    'TupleB0',
    seq_B0,
    '[B~0 -> ^(D*(2010)+ -> ^(D0 -> ^K- ^pi+) ^pi+) ^mu-]CC'
)

tp_B0.addBranches({
    "Y": "^([B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) mu+]CC)",
    "Dst_2010_minus": "[B0 -> ^(D*(2010)- -> (D~0 -> K+ pi-) pi-) mu+]CC",
    "D0": "[B0 -> (D*(2010)- -> ^(D~0 -> K+ pi-) pi-) mu+]CC",
    "piminus": "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) ^pi-) mu+]CC",
    "piminus0": "[B0 -> (D*(2010)- -> (D~0 -> K+ ^pi-) pi-) mu+]CC",
    "Kplus": "[B0 -> (D*(2010)- -> (D~0 -> ^K+ pi-) pi-) mu+]CC",
    "muplus": "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) ^mu+]CC"})

tuple_postpocess(tp_B0)


# B0_ws_Mu #####################################################################
tp_B0_ws_Mu = tuple_initialize(
    'TupleB0WSMu',
    seq_B0_ws_Mu,
    '[B~0 -> ^(D*(2010)+ -> ^(D0 -> ^K- ^pi+) ^pi+) ^mu+]CC'
)

tp_B0_ws_Mu.addBranches({
    "Y": "^([B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) mu-]CC)",
    "Dst_2010_minus": "[B0 -> ^(D*(2010)- -> (D~0 -> K+ pi-) pi-) mu-]CC",
    "D0": "[B0 -> (D*(2010)- -> ^(D~0 -> K+ pi-) pi-) mu-]CC",
    "piminus": "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) ^pi-) mu-]CC",
    "piminus0": "[B0 -> (D*(2010)- -> (D~0 -> K+ ^pi-) pi-) mu-]CC",
    "Kplus": "[B0 -> (D*(2010)- -> (D~0 -> ^K+ pi-) pi-) mu-]CC",
    "muplus": "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) ^mu-]CC"})

tuple_postpocess(tp_B0_ws_Mu)


# B0_ws_Pi #####################################################################
tp_B0_ws_Pi = tuple_initialize(
    'TupleB0WSPi',
    seq_B0_ws_Pi,
    '[B~0 -> ^(D*(2010)- -> ^(D0 -> ^K- ^pi+) ^pi-) ^mu-]CC'
)

tp_B0_ws_Pi.addBranches({
    "Y": "^([B0 -> (D*(2010)+ -> (D~0 -> K+ pi-) pi+) mu+]CC)",
    "Dst_2010_minus": "[B0 -> ^(D*(2010)+ -> (D~0 -> K+ pi-) pi+) mu+]CC",
    "D0": "[B0 -> (D*(2010)+ -> ^(D~0 -> K+ pi-) pi+) mu+]CC",
    "piminus": "[B0 -> (D*(2010)+ -> (D~0 -> K+ pi-) ^pi+) mu+]CC",
    "piminus0": "[B0 -> (D*(2010)+ -> (D~0 -> K+ ^pi-) pi+) mu+]CC",
    "Kplus": "[B0 -> (D*(2010)+ -> (D~0 -> ^K+ pi-) pi+) mu+]CC",
    "muplus": "[B0 -> (D*(2010)+ -> (D~0 -> K+ pi-) pi+) ^mu+]CC"})

tuple_postpocess(tp_B0_ws_Pi)

# Author: Phoebe Hamilton, Manuel Franco Sevilla, Yipeng Sun
# License: BSD 2-clause
# Last Change: Sat May 30, 2020 at 02:52 AM +0800
#
# Description: Definitions of selection and reconstruction procedures for Dst in
#              run 2. For more thorough comments, take a look at:
#                run1-b2D0MuXB2DMuNuForTauMuLine/reco_Dst.py


#########################################
# Load user-defined configuration flags #
#########################################

from Configurables import DaVinci

# NOTE: We *abuse* DaVinci's MoniSequence to pass additional flags
user_config = DaVinci().MoniSequence
DaVinci().MoniSequence = []  # Nothing should be in the sequence after all!


def has_flag(flg):
    return True if flg in user_config else False


#####################
# Configure DaVinci #
#####################

from Gaudi.Configuration import *

# Debug options
# DaVinci().EvtMax = 300
# MessageSvc().OutputLevel = DEBUG
DaVinci().EvtMax = -1

DaVinci().InputType = 'DST'
DaVinci().SkipEvents = 0
DaVinci().PrintFreq = 100

# Only ask for luminosity information when not using simulated data
DaVinci().Lumi = not DaVinci().Simulation


###################################
# Customize DaVinci main sequence #
###################################

from Configurables import ChargedProtoParticleMaker
from Configurables import NoPIDsParticleMaker
from Configurables import TrackScaleState
from Configurables import TrackSmearState
from CommonParticles.Utils import trackSelector, updateDoD

# Provide required information for VELO pions.
ms_all_protos = ChargedProtoParticleMaker(name='MyProtoPMaker')
ms_all_protos.Inputs = ['Rec/Track/Best']
ms_all_protos.Output = 'Rec/ProtoP/MyProtoPMaker/ProtoParticles'  # This TES location will be accessible for all selection algorithms

# VELO pions for Greg's isolation tool.
# NOTE: The name 'StdNoPIDsVeloPions' is hard-coded in the tuple tool, so the
#       name should not be changed.
ms_velo_pions = NoPIDsParticleMaker('StdNoPIDsVeloPions', Particle='pion')
ms_velo_pions.Input = ms_all_protos.Output

# NOTE: These two lines are needed to select particles in VELO only.
# NOTE: DARK MAGIC.
trackSelector(ms_velo_pions, trackTypes=['Velo'])
updateDoD(ms_velo_pions)

# According to the source code (available in 'Analysis/Phys/DaVinciTrackScaling/src/TrackScaleState.cpp'):
# Scale the state. Use on DST to scale the track states *before* your user
# algorithms sequence.
ms_scale = TrackScaleState('StateScale')

# Smear the momentum of MC particles, because the resolution is too good.
ms_smear = TrackSmearState('StateSmear')


if not DaVinci().Simulation:
    DaVinci().appendToMainSequence([ms_scale])
else:
    DaVinci().appendToMainSequence([ms_smear])


DaVinci().appendToMainSequence([ms_all_protos, ms_velo_pions])


######################
# Define pre-filters #
######################
# The run 2 stripping line definition can be found at:
#  http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping28r2/semileptonic/strippingb2d0muxb2dmufortaumuline.html

from Configurables import LoKi__HDRFilter as HDRFilter

line_strip = 'b2D0MuXB2DMuForTauMuLine'
fltr_strip = HDRFilter(
    'StrippedBCands',
    Code="HLT_PASS('Stripping{0}Decision')".format(line_strip))


if has_flag('CUTFLOW') and has_flag('BARE'):
    pass
elif not DaVinci().Simulation or has_flag('CUTFLOW'):
    DaVinci().EventPreFilters = [fltr_strip]


#######################
# Particle references #
#######################

from PhysSelPython.Wrappers import AutomaticData


if DaVinci().Simulation and has_flag('CUTFLOW'):
    pr_stripped = AutomaticData(
        Location='AllStreams/Phys/{0}/Particles'.format(line_strip))
else:
    pr_stripped = AutomaticData(
        Location='/Event/Semileptonic/Phys/{0}/Particles'.format(line_strip))


pr_charged_K = AutomaticData(Location='Phys/StdAllNoPIDsKaons/Particles')

pr_charged_Pi = AutomaticData(Location='Phys/StdAllNoPIDsPions/Particles')
pr_all_Pi = AutomaticData(Location='Phys/StdAllLoosePions/Particles')
# pr_up_Pi = AutomaticData(Location='Phys/StdNoPIDsUpPions/Particles')

pr_Mu = AutomaticData(Location='Phys/StdAllNoPIDsMuons/Particles')


############################
# Define simple selections #
############################

from PhysSelPython.Wrappers import Selection
from Configurables import FilterDesktop, FilterInTrees
from Configurables import TisTosParticleTagger

sel_stripped_Mu_filtered_evt = Selection(
    'SelMyStrippedMuFilteredEvent',
    Algorithm=FilterDesktop(
        'MyStrippedFiltered',
        Code="INTREE((ABSID == 'mu+') & (TIS('L0.*', 'L0TriggerTisTos')))"
    ),
    RequiredSelections=[pr_stripped]
)

# We build our own Muons, instead of using stripping line Muons for MC.
# See https://github.com/umd-lhcb/lhcb-ntuples-gen/issues/25 for an explanation.
sel_unstripped_tis_filtered_Mu = Selection(
    'SelMyUnstrippedFilteredMu',
    Algorithm=TisTosParticleTagger(
        'MyMuTisTagger',
        Inputs=['Phys/StdAllNoPIDsMuons/Particles'],
        TisTosSpecs={'L0Global%TIS': 0}),
    RequiredSelections=[pr_Mu]
)

# NOTE: 'stripped' selections require the existence of a stripping line, which
#       only exists in data, not MC.
sel_stripped_charged_K = Selection(
    'SelMyStrippedChargedK',
    Algorithm=FilterInTrees('MyChargedK', Code="(ABSID == 'K+')"),
    RequiredSelections=[pr_stripped]
)

sel_stripped_charged_Pi = Selection(
    'SelMyStrippedChargedPi',
    Algorithm=FilterInTrees('MyChargedPi', Code="(ABSID == 'pi+')"),
    RequiredSelections=[pr_stripped]
)

sel_stripped_Mu = Selection(
    'SelMyStrippedMu',
    Algorithm=FilterInTrees('MyMu', Code="(ABSID == 'mu+')"),
    RequiredSelections=[pr_stripped]
)


# For run 2, use unstripped Muon and don't put additional cut on Muons yet.
# We can always do TIS-filtering in step 2.
if has_flag('BARE') or DaVinci().Simulation and not has_flag('CUTFLOW'):
    sel_charged_K = pr_charged_K
    sel_charged_Pi = pr_charged_Pi
    sel_Mu = pr_Mu
else:
    sel_charged_K = sel_stripped_charged_K
    sel_charged_Pi = sel_stripped_charged_Pi
    sel_Mu = sel_stripped_Mu


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


if not has_flag('BARE'):
    algo_D0.DaughtersCuts = {
        'K+': '(PT > 300*MeV) & (MIPCHI2DV(PRIMARY) > 9.0) &' +
              '(PIDK > 4) & (TRGHOSTPROB < 0.5)',
        'pi-': '(PT > 300*MeV) & (MIPCHI2DV(PRIMARY) > 9.0) &' +
               '(PIDK < 2) & (TRGHOSTPROB < 0.5)'
    }

    algo_D0.CombinationCut = "(ADAMASS('D0') < 100*MeV) &" + \
        "(ACHILD(PT, 1) + ACHILD(PT, 2) > 2500*MeV)"
    algo_D0.MotherCut = "(ADMASS('D0') < 80*MeV) & (VFASPF(VCHI2/VDOF) < 4) &" + \
        "(SUMTREE(PT, ISBASIC) > 2500*MeV) & (BPVVDCHI2 > 25.0) &" + \
        "(BPVDIRA > 0.999)"


if DaVinci().Simulation and has_flag('BARE'):
    algo_D0.Preambulo += algo_mc_match_preambulo

    algo_D0.DaughtersCuts = {
        'K+': '(MIPCHI2DV(PRIMARY) > 9.0) &' +
              '(PIDK > 4) & (TRGHOSTPROB < 0.5)',
        'pi-': '(MIPCHI2DV(PRIMARY) > 9.0) &' +
               '(PIDK < 2) & (TRGHOSTPROB < 0.5)'
    }

    algo_D0.CombinationCut = 'AALL'
    algo_D0.MotherCut = "(VFASPF(VCHI2/VDOF) < 4) &" + \
        "(BPVVDCHI2 > 25.0) & (BPVDIRA > 0.999)"

elif DaVinci().Simulation:
    algo_D0.Preambulo += algo_mc_match_preambulo

    algo_D0.DaughtersCuts['K+'] = \
        "(mcMatch('[^K+]CC')) & (P > 2.0*GeV) &" + \
        "(MCSELMATCH(MCNINANCESTORS(BEAUTY) > 0)) &" + \
        algo_D0.DaughtersCuts['K+']

    algo_D0.DaughtersCuts['pi-'] = \
        '(P > 2.0*GeV) &' + \
        '(MCSELMATCH(MCNINANCESTORS(BEAUTY) > 0)) &' + \
        algo_D0.DaughtersCuts['pi-']

    algo_D0.MotherCut = \
        "(mcMatch('[Charm -> K- pi+ {gamma}{gamma}{gamma}]CC')) &" + \
        algo_D0.MotherCut


# Dst ##########################################################################
algo_Dst = CombineParticles('MyDst')
algo_Dst.DecayDescriptor = '[D*(2010)+ -> D0 pi+]cc'


if not has_flag('BARE'):
    algo_Dst.DaughtersCuts = {
        'pi+': '(MIPCHI2DV(PRIMARY) > 0.0) & (TRCHI2DOF < 3) &' +
               '(TRGHOSTPROB < 0.25)'
    }

    algo_Dst.CombinationCut = "(ADAMASS('D*(2010)+') < 220*MeV)"
    algo_Dst.MotherCut = "(ADMASS('D*(2010)+') < 125*MeV) &" + \
                         "(M-MAXTREE(ABSID=='D0', M) < 160*MeV) &" + \
                         "(VFASPF(VCHI2/VDOF) < 100)"

else:
    algo_Dst.DaughtersCuts = {
        'pi+': '(MIPCHI2DV(PRIMARY) > 0.0) & (TRCHI2DOF < 3) &' +
               '(TRGHOSTPROB < 0.25)'
    }

    algo_Dst.CombinationCut = "AALL"
    algo_Dst.MotherCut = "(VFASPF(VCHI2/VDOF) < 100)"


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


if not has_flag('BARE'):
    algo_B0.DaughtersCuts = {"mu-": "ALL"}
    algo_B0.CombinationCut = '(AM < 10200*MeV)'
    algo_B0.MotherCut = "(M < 10000*MeV) & (BPVDIRA > 0.9995) &" + \
                        "(VFASPF(VCHI2/VDOF) < 6.0)"


if DaVinci().Simulation and has_flag('BARE'):
    algo_B0.Preambulo += algo_mc_match_preambulo

    algo_B0.DaughtersCuts = {
        "mu-": "(mcMatch('[^mu+]CC')) & (TRGHOSTPROB < 0.5) &" +
               "(MIPCHI2DV(PRIMARY)>45) & (TRCHI2DOF < 3.0)"
    }
    algo_B0.CombinationCut = 'AALL'
    algo_B0.MotherCut = "(BPVDIRA > 0.9995) & (VFASPF(VCHI2/VDOF) < 6.0)"

elif DaVinci().Simulation:
    algo_B0.Preambulo += algo_mc_match_preambulo

    algo_B0.DaughtersCuts['mu-'] = \
        "(mcMatch('[^mu+]CC')) & (TRGHOSTPROB < 0.5) &" + \
        "(MIPCHI2DV(PRIMARY)>45) & (TRCHI2DOF < 3.0)"

    # algo_Bd.HistoProduce = True
    # algo_Bd.addTool(PlotTool("MotherPlots"))
    # algo_Bd.MotherPlots.Histos = {
    #    "AMAXDOCA(FLATTEN((ABSID=='D0') | (ABSID=='mu-')))" : ("DOCA",0,2)}


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
    TopSelection=sel_refit_B02DstMu
)

seq_B0_ws_Mu = SelectionSequence(
    'SeqMyB0WSMu',
    TopSelection=sel_refit_B02DstMu_ws_Mu
)

seq_B0_ws_Pi = SelectionSequence(
    'SeqMyB0WSPi',
    TopSelection=sel_refit_B02DstMu_ws_Pi
)


if DaVinci().Simulation or has_flag('CUTFLOW'):
    DaVinci().UserAlgorithms += [seq_B0.sequence()]
else:
    DaVinci().UserAlgorithms += [seq_B0.sequence(),
                                 seq_B0_ws_Mu.sequence(),
                                 seq_B0_ws_Pi.sequence()]


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
        'TupleToolPid',
        'TupleToolMuonPid',
        'TupleToolL0Calo',
    ]

    # Add event-level information.
    tt_loki_evt = tp.addTupleTool(LokiEvtTool, "TupleMyLokiEvtTool")
    tt_loki_evt.Preambulo += ['from LoKiCore.functions import *']
    tt_loki_evt.VOID_Variables = {
        'nTracks': "CONTAINS('Rec/Track/Best')",
        'nSPDhits': "CONTAINS('Raw/Spd/Digits')",
    }

    return tp


def tuple_initialize_mc(*args):
    tp = tuple_initialize_data(*args)

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


def tuple_postpocess_data(tp,
                          weights='./weights_soft.xml',
                          trigger_list_global=[
                              # L0
                              'L0HadronDecision',
                              'L0DiMuonDecision',
                              'L0ElectronDecision',
                              'L0JetElDecision',
                              'L0JetPhDecision',
                              'L0MuonDecision',
                              'L0MuonEWDecision',
                              'L0PhotonDecision',
                              # HLT 1
                              'Hlt1TrackAllL0Decision',
                              'Hlt1TwoTrackMVADecision',
                              'Hlt1TrackMVALooseDecision',
                              'Hlt1TwoTrackMVALooseDecision',
                              'Hlt1TrackMuonDecision',
                              'Hlt1TrackMuonMVADecision',
                              'Hlt1SingleMuonHighPTDecision',
                              # HLT 2
                              'Hlt2XcMuXForTauB2XcMuDecision'
                          ],
                          # NOTE: This is is unused for run 2
                          trigger_list_B0=[
                              # L0
                              'L0HadronDecision',
                              'L0DiMuonDecision',
                              'L0ElectronDecision',
                              'L0JetElDecision',
                              'L0JetPhDecision',
                              'L0MuonDecision',
                              'L0MuonEWDecision',
                              'L0PhotonDecision',
                              # HLT 1
                              'Hlt1TrackAllL0Decision',
                              'Hlt1TwoTrackMVADecision',
                              'Hlt1TrackMVALooseDecision',
                              'Hlt1TwoTrackMVALooseDecision',
                              'Hlt1TrackMuonDecision',
                              'Hlt1TrackMuonMVADecision',
                              'Hlt1SingleMuonHighPTDecision',
                          ]
                          ):
    tp.b0.addTool(TupleToolTagDiscardDstMu, name='TupleMyDiscardDstMu')
    tp.b0.ToolList += ['TupleToolTagDiscardDstMu/TupleMyDiscardDstMu']

    tp.b0.addTool(TupleToolApplyIsolation, name='TupleMyApplyIso')
    tp.b0.TupleMyApplyIso.WeightsFile = weights
    tp.b0.ToolList += ['TupleToolApplyIsolation/TupleMyApplyIso']

    tp.b0.addTool(TupleToolTauMuDiscrVars, name='TupleMyRFA')
    tp.b0.ToolList += ['TupleToolTauMuDiscrVars/TupleMyRFA']

    tp.mu.ToolList += ['TupleToolANNPIDTraining']

    tt_trigger = tp.addTupleTool('TupleToolTrigger')
    tt_trigger.Verbose = True
    tt_trigger.TriggerList = trigger_list_global

    tt_tistos = tp.addTupleTool('TupleToolTISTOS')
    tt_tistos.Verbose = True
    tt_tistos.TriggerList = trigger_list_global

    # NOTE: This has to be disabled, otherwise the TupleToolTrigger will NOT
    # act on B0
    # Trigger decisions to be saved for
    # tt_tistos_b0 = tp.b0.addTupleTool('TupleToolTISTOS')
    # tt_tistos_b0.Verbose = True
    # tt_tistos_b0.TriggerList += trigger_list_B0


def tuple_postpocess_mc(*args, **kwargs):
    tuple_postpocess_data(*args, **kwargs)


if not DaVinci().Simulation:
    tuple_initialize = tuple_initialize_data
    tuple_postpocess = tuple_postpocess_data
else:
    tuple_initialize = tuple_initialize_mc
    tuple_postpocess = tuple_postpocess_mc


# B0 ###########################################################################
tp_B0 = tuple_initialize(
    'TupleB0',
    seq_B0,
    '[B~0 -> ^(D*(2010)+ -> ^(D0 -> ^K- ^pi+) ^pi+) ^mu-]CC'
)

tp_B0.addBranches({
    "b0": "^([B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) mu+]CC)",
    "dst": "[B0 -> ^(D*(2010)- -> (D~0 -> K+ pi-) pi-) mu+]CC",
    "d0": "[B0 -> (D*(2010)- -> ^(D~0 -> K+ pi-) pi-) mu+]CC",
    "spi": "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) ^pi-) mu+]CC",
    "pi": "[B0 -> (D*(2010)- -> (D~0 -> K+ ^pi-) pi-) mu+]CC",
    "k": "[B0 -> (D*(2010)- -> (D~0 -> ^K+ pi-) pi-) mu+]CC",
    "mu": "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) ^mu+]CC"})

tuple_postpocess(tp_B0)


# B0_ws_Mu #####################################################################
tp_B0_ws_Mu = tuple_initialize(
    'TupleB0WSMu',
    seq_B0_ws_Mu,
    '[B~0 -> ^(D*(2010)+ -> ^(D0 -> ^K- ^pi+) ^pi+) ^mu+]CC'
)

tp_B0_ws_Mu.addBranches({
    "b0": "^([B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) mu-]CC)",
    "dst": "[B0 -> ^(D*(2010)- -> (D~0 -> K+ pi-) pi-) mu-]CC",
    "d0": "[B0 -> (D*(2010)- -> ^(D~0 -> K+ pi-) pi-) mu-]CC",
    "spi": "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) ^pi-) mu-]CC",
    "pi": "[B0 -> (D*(2010)- -> (D~0 -> K+ ^pi-) pi-) mu-]CC",
    "k": "[B0 -> (D*(2010)- -> (D~0 -> ^K+ pi-) pi-) mu-]CC",
    "mu": "[B0 -> (D*(2010)- -> (D~0 -> K+ pi-) pi-) ^mu-]CC"})

tuple_postpocess(tp_B0_ws_Mu)


# B0_ws_Pi #####################################################################
tp_B0_ws_Pi = tuple_initialize(
    'TupleB0WSPi',
    seq_B0_ws_Pi,
    '[B~0 -> ^(D*(2010)- -> ^(D0 -> ^K- ^pi+) ^pi-) ^mu-]CC'
)

tp_B0_ws_Pi.addBranches({
    "b0": "^([B0 -> (D*(2010)+ -> (D~0 -> K+ pi-) pi+) mu+]CC)",
    "dst": "[B0 -> ^(D*(2010)+ -> (D~0 -> K+ pi-) pi+) mu+]CC",
    "d0": "[B0 -> (D*(2010)+ -> ^(D~0 -> K+ pi-) pi+) mu+]CC",
    "spi": "[B0 -> (D*(2010)+ -> (D~0 -> K+ pi-) ^pi+) mu+]CC",
    "pi": "[B0 -> (D*(2010)+ -> (D~0 -> K+ ^pi-) pi+) mu+]CC",
    "k": "[B0 -> (D*(2010)+ -> (D~0 -> ^K+ pi-) pi+) mu+]CC",
    "mu": "[B0 -> (D*(2010)+ -> (D~0 -> K+ pi-) pi+) ^mu+]CC"})

tuple_postpocess(tp_B0_ws_Pi)


if DaVinci().Simulation or has_flag('CUTFLOW'):
    DaVinci().UserAlgorithms += [tp_B0]
else:
    DaVinci().UserAlgorithms += [tp_B0, tp_B0_ws_Mu, tp_B0_ws_Pi]

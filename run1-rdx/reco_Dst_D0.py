# Author: Phoebe Hamilton, Manuel Franco Sevilla, Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Mar 15, 2021 at 01:21 AM +0100
#
# Description: Definitions of selection and reconstruction procedures for run 1
#              R(D(*)), with thorough comments.
#
# Meanings for flags:
# NOTE: The CUTFLOW, BARE, and DV_STRIP flags are all used for cutflow studies
#
#   CUTFLOW:
#     Use stripping line and stripping line only. Don't apply additional HLT
#     cuts.
#
#   BARE:
#     Apply way less and way looser cuts compared to the stripping line. This
#     implies that we don't use stripping line at all.
#
#     This is for cutflow studies without biasing the trigger efficiencies from
#     the trigger cuts in the stripping line.
#
#   DV_STRIP:
#     Apply all stripping line cuts in DaVinci, but don't use stripping line.
#     This is used to show that applying cuts later is very similar to applying
#     cuts in the official stripping production (with admittedly minor
#     differences).
#
#   NON_MU_MISID:
#     Don't apply Muon PID cuts for Muon, and use the dedicated Fake stripping
#     line instead of the regular one. The misID sample is used in fit.


#########################################
# Load user-defined configuration flags #
#########################################

from Configurables import DaVinci

# NOTE: We *abuse* DaVinci's MoniSequence to pass additional flags
user_config = DaVinci().MoniSequence
DaVinci().MoniSequence = []  # Nothing should be in the sequence after all!


def has_flag(flg):
    return flg in user_config


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
# These algorithms are executed before any of the selection algorithms.
#
# algorithms defined here will set up locations that will be available for all
# selection algorithms.

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
elif not has_flag('NO_SMEAR'):
    DaVinci().appendToMainSequence([ms_smear])


DaVinci().appendToMainSequence([ms_all_protos, ms_velo_pions])


######################
# Define pre-filters #
######################
# These filters are executed *before* the main selection algorithms to ignore
# obviously uninteresting events.
#
# Applying these filters should speed up the execution time.
#
# The run 1 stripping line definition can be found at:
#  http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping21/semileptonic/strippingb2d0muxb2dmunufortaumuline.html
# The older stripping line has a different name, but the cuts are the same:
#  http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping20r1/semileptonic/strippingb2d0muxb2dmufortaumuline.html

from Configurables import LoKi__HDRFilter as HDRFilter


if DaVinci().Simulation and has_flag('CUTFLOW'):
    line_strip = 'b2D0MuXB2DMuForTauMuLine'  # Name of the stripping line back in 2011.
elif has_flag('NON_MU_MISID'):
    line_strip = 'b2D0MuXFakeB2DMuNuForTauMuLine'
else:
    line_strip = 'b2D0MuXB2DMuNuForTauMuLine'


# Differences between 'HLT_PASS' and 'HLT_PASS_RE':
#   'HLT_PASS' matches the line *exactly*
#   'HLT_PASS_RE' (which was used in the starter kit) use regular expression to
#   check if line given is a part of the lines of the events.
fltr_strip = HDRFilter(
    'StrippedBCands',
    Code="HLT_PASS('Stripping{0}Decision')".format(line_strip))

line_hlt = 'Hlt2CharmHadD02HH_D02KPi'
fltr_hlt = HDRFilter(
    'Hlt2TriggeredD0',
    Code="HLT_PASS('{0}Decision')".format(line_hlt))


if has_flag('BARE') or has_flag('DV_STRIP'):
    pass
elif has_flag('CUTFLOW'):
    DaVinci().EventPreFilters = [fltr_strip]
elif not DaVinci().Simulation:
    DaVinci().EventPreFilters = [fltr_strip, fltr_hlt]


#######################
# Particle references #
#######################
# Definitions of these particle references can be found at:
#   https://gitlab.cern.ch/lhcb/Phys/-/tree/master/Phys/CommonParticles/python/CommonParticles

# 'DataOnDemand' == 'AutomaticData'
from PhysSelPython.Wrappers import AutomaticData


# Events tagged with our stripping line
if line_strip == 'b2D0MuXB2DMuForTauMuLine':
    pr_stripped = AutomaticData(
        Location='AllStreams/Phys/{0}/Particles'.format(line_strip))
else:
    pr_stripped = AutomaticData(
        Location='/Event/Semileptonic/Phys/{0}/Particles'.format(line_strip))


pr_all_nopid_K = AutomaticData(Location='Phys/StdAllNoPIDsKaons/Particles')
pr_loose_K = AutomaticData(Location='Phys/StdLooseKaons/Particles')

pr_all_nopid_Pi = AutomaticData(Location='Phys/StdAllNoPIDsPions/Particles')
pr_loose_Pi = AutomaticData(Location='Phys/StdLoosePions/Particles')
pr_all_loose_Pi = AutomaticData(Location='Phys/StdAllLoosePions/Particles')
# Standard NoPIDs upstream pions (VELO + TT hits, no T-layers).
# They only added 10% with terrible mass resolution, so they didn't use them in
# the end.
# pr_nopid_up_Pi = AutomaticData(Location='Phys/StdNoPIDsUpPions/Particles')

pr_all_nopid_Mu = AutomaticData(Location='Phys/StdAllNoPIDsMuons/Particles')
pr_all_loose_Mu = AutomaticData(Location='Phys/StdAllLooseMuons/Particles')


##############################
# Stable particle selections #
##############################
# Stable particles don't decay inside the detector, and these selections are
# relatively simple.

from PhysSelPython.Wrappers import Selection
from Configurables import FilterDesktop, FilterInTrees
from Configurables import TisTosParticleTagger

# This selects events that have a Muon satisfying stripping requirements and was
# triggered regardless of the muon.
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
    RequiredSelections=[pr_all_nopid_Mu]
)

# NOTE: 'stripped' selections require the existence of a stripping line, which
#       only exists in data, and flagged MC, NOT filtered MC.
#
#       This is because typically MC is either flagged or filtered, but not
#       both.
# NOTE: We decide to do Muon TIS-filtering for run 1 as well for consistency.
sel_stripped_charged_K = Selection(
    'SelMyStrippedChargedK',
    Algorithm=FilterInTrees('MyChargedK', Code="(ABSID == 'K+')"),
    RequiredSelections=[sel_stripped_Mu_filtered_evt]
)

sel_stripped_charged_Pi = Selection(
    'SelMyStrippedChargedPi',
    Algorithm=FilterInTrees('MyChargedPi', Code="(ABSID == 'pi+')"),
    RequiredSelections=[sel_stripped_Mu_filtered_evt]
)

sel_stripped_Mu = Selection(
    'SelMyStrippedMu',
    Algorithm=FilterInTrees('MyMu', Code="(ABSID == 'mu+')"),
    RequiredSelections=[sel_stripped_Mu_filtered_evt]
)


# For run 1:
#   Build Muon from scratch for MC because semileptonic production MC doesn't
#   have stripping lines
#
#   For data, we always have a stripping line, so all events contains *some*
#   Muons that pass the stripping criteria.
#
# NOTE: Muons that do not pass stripping still get saved *but we don't want
#       to use them*.
if has_flag('BARE') or has_flag('DV_STRIP'):
    sel_charged_K = pr_loose_K
    sel_charged_Pi = pr_loose_Pi
    sel_Mu = pr_all_loose_Mu
    sel_soft_Pi = pr_all_loose_Pi
elif not DaVinci().Simulation or has_flag('CUTFLOW'):
    sel_charged_K = sel_stripped_charged_K
    sel_charged_Pi = sel_stripped_charged_Pi
    sel_Mu = sel_stripped_Mu
    sel_soft_Pi = pr_all_loose_Pi
else:
    sel_charged_K = pr_all_nopid_K
    sel_charged_Pi = pr_all_nopid_Pi
    sel_Mu = sel_unstripped_tis_filtered_Mu
    sel_soft_Pi = pr_all_nopid_Pi


#########################
# B- -> D0 Mu selection #
#########################
# Use this LoKi functor page to find the meaning of various functors:
#  https://twiki.cern.ch/twiki/bin/view/LHCb/LoKiHybridFilters

from Configurables import CombineParticles
from Configurables import FitDecayTrees
from PhysSelPython.Wrappers import SelectionSequence

algo_mc_match_preambulo = [
    'from LoKiMC.functions import *',
    'from LoKiPhysMC.decorators import *',
    'from LoKiPhysMC.functions import *'
]

# D0 ###########################################################################
# NOTE:
#   .CombinationCut are cuts made before the vertex fit, so it saves time
#   .MotherCut are cuts after the vertex fit, that's why the mass cut is tighter
algo_D0 = CombineParticles('MyD0')
algo_D0.DecayDescriptor = '[D0 -> K- pi+]cc'

algo_D0.DaughtersCuts = {
    'K+': '(MIPCHI2DV(PRIMARY) > 45.0) &'
          '(P > 2.0*GeV) & (PT > 300.0*MeV) &'
          '(TRGHOSTPROB < 0.5)',
    'pi-': '(P > 2.0*GeV) & (PT > 300.0*MeV) &'
           '(MIPCHI2DV(PRIMARY) > 45.0) &'
           '(TRGHOSTPROB < 0.5)'
}

algo_D0.CombinationCut = \
    "(ADAMASS('D0') < 100.0*MeV) &" \
    "(ACHILD(PT,1) + ACHILD(PT,2) > 1400.0*MeV)"
algo_D0.MotherCut = \
    "(SUMTREE(PT,ISBASIC) > 1400.0*MeV) & (ADMASS('D0') < 80.0*MeV) &" \
    "(VFASPF(VCHI2/VDOF) < 4.0) & (BPVVDCHI2 > 250.0) & (BPVDIRA> 0.9998)"


if has_flag('BARE'):
    algo_D0.DaughtersCuts = {
        'K+': '(PIDK > 2.0) & (MIPCHI2DV(PRIMARY) > 4.5) &'
              '(TRGHOSTPROB < 1.0)',
        'pi-': '(MIPCHI2DV(PRIMARY) > 4.5) &'
               '(PIDK < 4.0) & (TRGHOSTPROB < 1.0)'
    }

    algo_D0.CombinationCut = 'ATRUE'
    algo_D0.MotherCut = \
        "(VFASPF(VCHI2/VDOF) < 8.0) & (BPVVDCHI2 > 12.5) & (BPVDIRA> 0.998)"


# PID for real data/cutflow only
if not DaVinci().Simulation or has_flag('CUTFLOW'):
    algo_D0.DaughtersCuts['K+'] = \
        '(PIDK > 4.0) &' + \
        algo_D0.DaughtersCuts['K+']

    algo_D0.DaughtersCuts['pi-'] = \
        '(PIDK < 2.0) &' + \
        algo_D0.DaughtersCuts['pi-']


if DaVinci().Simulation:
    algo_D0.Preambulo += algo_mc_match_preambulo

    algo_D0.DaughtersCuts['K+'] = \
        "(mcMatch('[^K+]CC')) &" \
        "(MCSELMATCH(MCNINANCESTORS(BEAUTY) > 0)) &" + \
        algo_D0.DaughtersCuts['K+']

    algo_D0.DaughtersCuts['pi-'] = \
        '(MCSELMATCH(MCNINANCESTORS(BEAUTY) > 0)) &' + \
        algo_D0.DaughtersCuts['pi-']

    algo_D0.MotherCut = \
        "(mcMatch('[Charm -> K- pi+ {gamma}{gamma}{gamma}]CC')) &" + \
        algo_D0.MotherCut


# RequiredSelections takes a union of supplied selections, thus orderless.
sel_D0 = Selection(
    'SelMyD0',
    Algorithm=algo_D0,
    RequiredSelections=[sel_charged_K, sel_charged_Pi]
)

# B- ###########################################################################
# This corresponds to the B-meson cuts defined in the stripping line
algo_Bminus = CombineParticles('MyB-')
algo_Bminus.DecayDescriptor = '[B- -> D0 mu-]cc'
# algo_Bminus.DecayDescriptors = ['[B- -> D0 mu-]cc', '[B+ -> D0 mu+]cc']

algo_Bminus.DaughtersCuts = {
    'mu-': '(MIPCHI2DV(PRIMARY) > 45.0) & (TRGHOSTPROB < 0.5) &'
           '(P > 3.0*GeV)'  # NOTE: Mu PID is added later
}

algo_Bminus.CombinationCut = '(AM < 10.2*GeV)'
algo_Bminus.MotherCut = \
    '(MM < 10.0*GeV) & (MM > 0.0*GeV) &' \
    '(VFASPF(VCHI2/VDOF) < 6.0) & (BPVDIRA > 0.9995)'


# NOTE: For all but Non-Mu MisID reco, we add Muon PID requirement.
if not (has_flag('NON_MU_MISID') or DaVinci().Simulation) or \
        has_flag('CUTFLOW'):
    algo_Bminus.DaughtersCuts['mu-'] = \
        '(PIDmu > 2.0) &' + algo_Bminus.DaughtersCuts['mu-']


if has_flag('BARE'):
    algo_Bminus.DaughtersCuts['mu-'] = \
        '(MIPCHI2DV(PRIMARY) > 8.0) & (TRGHOSTPROB < 1.0) &' \
        '(PIDmu > -400.0)'

    algo_Bminus.CombinationCut = 'ATRUE'
    algo_Bminus.MotherCut = '(VFASPF(VCHI2/VDOF) < 12.0) & (BPVDIRA > 0.998)'


if DaVinci().Simulation:
    algo_Bminus.Preambulo += algo_mc_match_preambulo

    if has_flag('BARE'):
        algo_Bminus.DaughtersCuts['mu-'] = \
            "(mcMatch('[^mu+]CC')) & (TRCHI2DOF < 6.0) &" + \
            algo_Bminus.DaughtersCuts['mu-']
    else:
        algo_Bminus.DaughtersCuts['mu-'] = \
            "(mcMatch('[^mu+]CC')) & (TRCHI2DOF < 3.0) &" + \
            algo_Bminus.DaughtersCuts['mu-']


sel_Bminus = Selection(
    'SelMyB-',
    Algorithm=algo_Bminus,
    RequiredSelections=[sel_D0, sel_Mu]
)

sel_refit_Bminus2D0Mu = Selection(
    'SelMyRefitB-2D0Mu',
    Algorithm=FitDecayTrees(
        'MyRefitB-2D0Mu',
        Code="DECTREE('[B- -> (D0->K- pi+) mu-]CC')",
        UsePVConstraint=False,
    ),
    RequiredSelections=[sel_Bminus]
)

seq_Bminus = SelectionSequence('SeqMyB-', TopSelection=sel_refit_Bminus2D0Mu)

# B-_ws ########################################################################
# 'WS' means wrong-sign.
algo_Bminus_ws = CombineParticles('MyB-WS')
algo_Bminus_ws.DecayDescriptor = '[B+ -> D0 mu+]cc'  # D0 is WS, D~0 is correct.

algo_Bminus_ws.Preambulo = algo_Bminus.Preambulo
algo_Bminus_ws.DaughtersCuts = algo_Bminus.DaughtersCuts
algo_Bminus_ws.CombinationCut = algo_Bminus.CombinationCut
algo_Bminus_ws.MotherCut = algo_Bminus.MotherCut

sel_Bminus_ws = Selection(
    'SelMyB-WS',
    Algorithm=algo_Bminus_ws,
    RequiredSelections=[sel_D0, sel_Mu]
)

sel_refit_Bminus2D0Mu_ws = Selection(
    'SelMyRefitB-2D0MuWS',
    Algorithm=FitDecayTrees(
        'MyRefitB-2D0MuWS',
        Code="DECTREE('[B+ -> (D0->K- pi+) mu+]CC')",
        UsePVConstraint=False,
    ),
    RequiredSelections=[sel_Bminus_ws]
)

seq_Bminus_ws = SelectionSequence('SeqMyB-WS',
                                  TopSelection=sel_refit_Bminus2D0Mu_ws)

# Filtered D0 and Mu from the D0 Mu combo ######################################
# These particles pass the stripping line selection, and can be reused to build
# other particles.
sel_D0_combo = Selection(
    'SelMyComboD0',
    Algorithm=FilterInTrees('MyComboD0', Code="(ABSID == 'D0')"),
    RequiredSelections=[sel_Bminus]
)

sel_Mu_combo = Selection(
    'SelMyComboMu',
    Algorithm=FilterInTrees('MyComboMu', Code="(ABSID == 'mu+')"),
    RequiredSelections=[sel_Bminus]
)

sel_D0_ws_combo = Selection(
    'SelMyComboD0WS',
    Algorithm=FilterInTrees('MyComboMuWS', Code="(ABSID == 'D0')"),
    RequiredSelections=[sel_Bminus_ws]
)

sel_Mu_ws_combo = Selection(
    'SelMyComboMuWS',
    Algorithm=FilterInTrees('MyComboMuWS', Code="(ABSID == 'mu+')"),
    RequiredSelections=[sel_Bminus_ws]
)


##########################
# B0 -> Dst Mu selection #
##########################

# Dst ##########################################################################
algo_Dst = CombineParticles('MyDst')
algo_Dst.DecayDescriptor = '[D*(2010)+ -> D0 pi+]cc'

algo_Dst.DaughtersCuts = {
    'pi+': '(MIPCHI2DV(PRIMARY) > 0.0) & (TRCHI2DOF < 3.0) &'
           '(TRGHOSTPROB < 0.25)'
}

algo_Dst.CombinationCut = "(ADAMASS('D*(2010)+') < 220.0*MeV)"
algo_Dst.MotherCut = \
    "(ADMASS('D*(2010)+') < 125.0*MeV) &" \
    "(M-MAXTREE(ABSID=='D0',M) < 160.0*MeV) &" \
    "(VFASPF(VCHI2/VDOF) < 100.0)"


if has_flag('BARE'):
    algo_Dst.DaughtersCuts = {
        'pi+': '(MIPCHI2DV(PRIMARY) > 0.0) & (TRCHI2DOF < 6.0) &'
               '(TRGHOSTPROB < 0.5)'
    }

    algo_Dst.CombinationCut = 'ATRUE'
    algo_Dst.MotherCut = "(VFASPF(VCHI2/VDOF) < 200.0)"


if DaVinci().Simulation:
    algo_Dst.Preambulo += algo_mc_match_preambulo

    algo_Dst.DaughtersCuts['pi+'] = \
        '(MCSELMATCH(MCNINANCESTORS(BEAUTY) > 0)) &' + \
        algo_Dst.DaughtersCuts['pi+']


sel_Dst = Selection(
    'SelMyDst',
    Algorithm=algo_Dst,
    RequiredSelections=[sel_D0_combo, sel_soft_Pi]
)

sel_refit_Dst2D0Pi = Selection(
    'SelMyRefitDst2D0Pi',
    Algorithm=FitDecayTrees(
        'MyRefitDst2D0Pi',
        Code="DECTREE('[D*(2010)+ -> D0 pi+]CC')",
        UsePVConstraint=False,
    ),
    RequiredSelections=[sel_Dst]
)

# Dst_ws_Mu ####################################################################
# 'WS' stands for 'wrong sign'
algo_Dst_ws_Mu = CombineParticles('MyDstWSMu')
algo_Dst_ws_Mu.DecayDescriptor = '[D*(2010)+ -> D0 pi+]cc'

algo_Dst_ws_Mu.DaughtersCuts = algo_Dst.DaughtersCuts
algo_Dst_ws_Mu.CombinationCut = algo_Dst.CombinationCut
algo_Dst_ws_Mu.MotherCut = algo_Dst.MotherCut

sel_Dst_ws_Mu = Selection(
    'SelMyDstWSMu',
    Algorithm=algo_Dst_ws_Mu,
    RequiredSelections=[sel_D0_ws_combo, sel_soft_Pi]
)

sel_refit_Dst2D0Pi_ws_Mu = Selection(
    'SelMyRefitDst2D0PiWSMu',
    Algorithm=FitDecayTrees(
        'MyRefitDst2D0PiWSMu',
        Code="DECTREE('[D*(2010)+ -> D0 pi+]CC')",
        UsePVConstraint=False,
    ),
    RequiredSelections=[sel_Dst_ws_Mu]
)

# Dst_ws_Pi ####################################################################
algo_Dst_ws_Pi = CombineParticles('MyDstWSPi')
algo_Dst_ws_Pi.DecayDescriptor = '[D*(2010)- -> D0 pi-]cc'

algo_Dst_ws_Pi.DaughtersCuts = algo_Dst.DaughtersCuts
algo_Dst_ws_Pi.CombinationCut = algo_Dst.CombinationCut
algo_Dst_ws_Pi.MotherCut = algo_Dst.MotherCut

sel_Dst_ws_Pi = Selection(
    'SelMyDstWSPi',
    Algorithm=algo_Dst_ws_Pi,
    RequiredSelections=[sel_D0_combo, sel_soft_Pi]
)

sel_refit_Dst2D0Pi_ws_Pi = Selection(
    'SelMyRefitDst2D0PiWSPi',
    Algorithm=FitDecayTrees(
        'MyRefitDst2D0PiWSPi',
        Code="DECTREE('[D*(2010)- -> D0 pi-]CC')",
        UsePVConstraint=False,
    ),
    RequiredSelections=[sel_Dst_ws_Pi]
)

# Define Dst stubs depending if we have 'FULL_REFIT' flag ######################

if has_flag('FULL_REFIT'):
    sel_Dst_stub = sel_Dst
    sel_Dst_ws_Mu_stub = sel_Dst_ws_Mu
    sel_Dst_ws_Pi_stub = sel_Dst_ws_Pi
else:
    sel_Dst_stub = sel_refit_Dst2D0Pi
    sel_Dst_ws_Mu_stub = sel_refit_Dst2D0Pi_ws_Mu
    sel_Dst_ws_Pi_stub = sel_refit_Dst2D0Pi_ws_Pi


# B0 ###########################################################################
algo_B0 = CombineParticles('MyB0')
algo_B0.DecayDescriptor = "[B~0 -> D*(2010)+ mu-]cc"  # B~0 is the CC of B0

# Don't apply D0 Mu combo cuts to Dst Mu!
algo_B0.CombinationCut = 'ATRUE'
algo_B0.MotherCut = "(VFASPF(VCHI2/VDOF) < 100.0)"  # Loose cuts here

# algo_B0.HistoProduce = True
# algo_B0.addTool(PlotTool("MotherPlots"))
# algo_B0.MotherPlots.Histos = {
#    "AMAXDOCA(FLATTEN((ABSID=='D0') | (ABSID=='mu-')))" : ("DOCA",0,2)}

sel_B0 = Selection(
    'SelMyB0',
    Algorithm=algo_B0,
    RequiredSelections=[sel_Dst_stub, sel_Mu_combo]
)

sel_refit_B02DstMu = Selection(
    'SelMyRefitB02DstMu',
    Algorithm=FitDecayTrees(
        'MyRefitB02DstMu',
        Code="DECTREE('[B~0 -> (D*(2010)+ -> (D0->K- pi+) pi+) mu-]CC')",
        UsePVConstraint=False
    ),
    RequiredSelections=[sel_B0]
)

# B0_ws_Mu #####################################################################
# Here the muon has the wrong sign---charge not conserved.
algo_B0_ws_Mu = CombineParticles('MyB0WSMu')
algo_B0_ws_Mu.DecayDescriptor = "[B~0 -> D*(2010)+ mu+]cc"

algo_B0_ws_Mu.CombinationCut = algo_B0.CombinationCut
algo_B0_ws_Mu.MotherCut = algo_B0.MotherCut

sel_B0_ws_Mu = Selection(
    'SelMyB0WSMu',
    Algorithm=algo_B0_ws_Mu,
    RequiredSelections=[sel_Dst_ws_Mu_stub, sel_Mu_ws_combo]
)

sel_refit_B02DstMu_ws_Mu = Selection(
    'SelMyRefitB02DstMuWSMu',
    Algorithm=FitDecayTrees(
        'MyRefitB02DstMuwsMu',
        Code="DECTREE('[B~0 -> (D*(2010)+ -> (D0->K- pi+) pi+) mu+]CC')",
        UsePVConstraint=False
    ),
    RequiredSelections=[sel_B0_ws_Mu]
)

# B0_ws_Pi #####################################################################
# Here, due to the wrong quark content of B0, instead of B~0, the pion (not
# listed here) will have wrong sign.
# In other words, this time, D* has the wrong sign.
algo_B0_ws_Pi = CombineParticles('MyB0WSPi')
algo_B0_ws_Pi.DecayDescriptor = "[B0 -> D*(2010)+ mu+]cc"

algo_B0_ws_Pi.CombinationCut = algo_B0.CombinationCut
algo_B0_ws_Pi.MotherCut = algo_B0.MotherCut

sel_B0_ws_Pi = Selection(
    'SelMyB0WSPi',
    Algorithm=algo_B0_ws_Pi,
    RequiredSelections=[sel_Dst_ws_Pi_stub, sel_Mu_combo]
)

sel_refit_B02DstMu_ws_Pi = Selection(
    'SelMyRefitB02DstMuWSPi',
    Algorithm=FitDecayTrees(
        'MyRefitB02DstMuWSPi',
        Code="DECTREE('[B~0 -> (D*(2010)- -> (D0->K- pi+) pi-) mu-]CC')",
        UsePVConstraint=False
    ),
    RequiredSelections=[sel_B0_ws_Pi]
)

# Define B0 stubs depending if we have 'FULL_REFIT' flag #######################

if has_flag('FULL_REFIT'):
    seq_B0 = SelectionSequence('SeqMyB0', TopSelection=sel_refit_B02DstMu)
    seq_B0_ws_Mu = SelectionSequence('SeqMyB0WSMu',
                                     TopSelection=sel_refit_B02DstMu_ws_Mu)
    seq_B0_ws_Pi = SelectionSequence('SeqMyB0WSPi',
                                     TopSelection=sel_refit_B02DstMu_ws_Pi)
else:
    seq_B0 = SelectionSequence('SeqMyB0', TopSelection=sel_B0)
    seq_B0_ws_Mu = SelectionSequence('SeqMyB0WSMu',
                                     TopSelection=sel_B0_ws_Mu)
    seq_B0_ws_Pi = SelectionSequence('SeqMyB0WSPi',
                                     TopSelection=sel_B0_ws_Pi)


##########################
# Non-Mu MisID selection #
##########################
# NOTE: These are not used in fitter. Kept for archival purposes.

# B*_0+ -> B0 Pi+ ##############################################################
algo_BstPlus = CombineParticles('MyB*_0+')
algo_BstPlus.DecayDescriptor = '[B*_0+ -> B0 pi+]cc'
algo_BstPlus.DaughtersCuts = {
    'pi+': '(TRGHOSTPROB < 0.5) & (MIPCHI2DV(PRIMARY) > 4)'
}
algo_BstPlus.CombinationCut = '(AM < 5700*MeV) & (AM > 4800*MeV)'
algo_BstPlus.MotherCut = \
    '(M < 5500*MeV) & (M > 5000*MeV) &' \
    '(BPVDIRA > 0.9995) & (VFASPF(VCHI2/VDOF) < 9)'

sel_BstPlus = Selection(
    'SelMyB*_0+',
    Algorithm=algo_BstPlus,
    RequiredSelections=[sel_B0, sel_charged_Pi]
)

seq_BstPlus = SelectionSequence(
    'SeqMyB*_0+',
    TopSelection=sel_BstPlus)

# B*_00 -> B0 Pi+ Pi- ##########################################################
algo_Bst0 = CombineParticles('MyB*_00')
algo_Bst0.DecayDescriptor = '[B*_00 -> B0 pi+ pi-]cc'
algo_Bst0.DaughtersCuts = algo_BstPlus.DaughtersCuts
algo_Bst0.CombinationCut = algo_BstPlus.CombinationCut
algo_Bst0.MotherCut = algo_BstPlus.MotherCut

sel_Bst0 = Selection(
    'SelMyB*_00',
    Algorithm=algo_Bst0,
    RequiredSelections=[sel_B0, sel_charged_Pi]
)

seq_Bst0 = SelectionSequence(
    'SeqMyB*_00',
    TopSelection=sel_Bst0)


##################
# Define ntuples #
##################

from Configurables import DecayTreeTuple, MCDecayTreeTuple
from DecayTreeTuple.Configuration import *  # to use addTupleTool

# Additional TupleTool for addTool only
from Configurables import BackgroundCategory


# Helper function to really add TupleTool. This will remove existing tool before
# re-adding it.
def really_add_tool(tp, tool_name):
    try:
        tp.ToolList.remove(tool_name)
    except (ValueError, AttributeError):
        pass
    finally:
        tool = tp.addTupleTool(tool_name)
    return tool


def tuple_initialize_common(name, sel_seq, template, tuple_builder):
    tp = tuple_builder(name)
    if sel_seq:
        tp.Inputs = [sel_seq.outputLocation()]
    tp.setDescriptorTemplate(template)
    return tp


def tuple_initialize_data(name, sel_seq, template):
    tp = tuple_initialize_common(name, sel_seq, template, DecayTreeTuple)
    tp.ToolList += [
        'TupleToolAngles',
        'TupleToolMuonPid',  # This write out NN Mu inputs
        'TupleToolL0Calo',
        'TupleToolTrackInfo',
    ]

    tt_pid = really_add_tool(tp, 'TupleToolPid')
    tt_pid.Verbose = True

    # Add event-level information.
    tt_loki_evt = really_add_tool(
        tp, 'LoKi::Hybrid::EvtTupleTool/LoKi__Hybrid__EvtTupleTool')
    tt_loki_evt.Preambulo += ['from LoKiCore.functions import *']
    tt_loki_evt.VOID_Variables = {
        'nTracks': "CONTAINS('Rec/Track/Best')"
    }

    return tp


def tuple_initialize_mc(*args, **kwargs):
    tp = tuple_initialize_data(*args, **kwargs)

    tt_mcbi = really_add_tool(tp, 'TupleToolMCBackgroundInfo')
    tt_mcbi.addTool(BackgroundCategory)
    tt_mcbi.BackgroundCategory.SemileptonicDecay = True
    tt_mcbi.BackgroundCategory.NumNeutrinos = 3

    tt_truth = really_add_tool(tp, 'TupleToolMCTruth')
    tt_truth.ToolList = [
        'MCTupleToolKinematic',
        'MCTupleToolHierarchyExt'
    ]

    return tp


def tuple_initialize_aux(name, template):
    tp = tuple_initialize_common(name, None, template, MCDecayTreeTuple)

    tp.ToolList += [
        'MCTupleToolPID'
    ]

    return tp


def tuple_postpocess_data(tp, B_meson='b0', Mu='mu',
                          weights='./weights_soft.xml',
                          trigger_list_global=[
                              # L0
                              'L0HadronDecision',
                              # HLT 1
                              'Hlt1TrackAllL0Decision',
                              # HLT 2
                              'Hlt2CharmHadD02HH_D02KPiDecision'
                          ],
                          trigger_list_B=[
                              # L0
                              'L0HadronDecision',  # Hadron decision needed everywhere.
                              'L0DiMuonDecision',
                              'L0ElectronDecision',
                              'L0ElectronHiDecision',
                              'L0HighSumETJetDecision',
                              'L0MuonDecision',
                              'L0NoPVFlagDecision',
                              'L0PhotonDecision',
                              'L0PhotonHiDecision'
                          ]
                          ):
    # Trigger decisions to be saved for every particle
    tt_trigger = tp.addTupleTool('TupleToolTrigger')
    tt_trigger.Verbose = True
    tt_trigger.TriggerList = trigger_list_global

    tt_tistos = tp.addTupleTool('TupleToolTISTOS')
    tt_tistos.Verbose = True
    tt_tistos.TriggerList = trigger_list_global

    # Trigger decisions to be saved for B meson
    tt_tistos_B = getattr(tp, B_meson).addTupleTool('TupleToolTISTOS')
    tt_tistos_B.Verbose = True
    tt_tistos_B.TriggerList = trigger_list_B

    getattr(tp, B_meson).ToolList += [
        'TupleToolTagDiscardDstMu',
        'TupleToolTauMuDiscrVars',
    ]

    tt_app_iso = getattr(tp, B_meson).addTupleTool('TupleToolApplyIsolation')
    tt_app_iso.WeightsFile = weights

    getattr(tp, Mu).ToolList += ['TupleToolANNPIDTraining']


def tuple_postpocess_mc(*args, **kwargs):
    tuple_postpocess_data(*args, **kwargs)


if not DaVinci().Simulation:
    tuple_initialize = tuple_initialize_data
    tuple_postpocess = tuple_postpocess_data
else:
    tuple_initialize = tuple_initialize_mc
    tuple_postpocess = tuple_postpocess_mc


# B- ###########################################################################
tp_Bminus = tuple_initialize(
    'TupleBminus',
    seq_Bminus,
    '${b}[B- -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${mu}mu-]CC'
)
tuple_postpocess(tp_Bminus, B_meson='b')

# B- wrong-sign ################################################################
tp_Bminus_ws = tuple_initialize(
    'TupleBminusWS',
    seq_Bminus_ws,
    '${b}[B+ -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${mu}mu+]CC'
)
tuple_postpocess(tp_Bminus_ws, B_meson='b')

# B- MC ########################################################################
tp_Bminus_mc_Tau = tuple_initialize_aux(
    'MCTupleBminusTau',
    '${b}[B- => ${d0}(D0 => ${k}K- ${pi}pi+) ${tau}(tau- => ${mu}mu- ${amu_mu}nu_mu~ ${nu_tau}nu_tau) ${anu_tau}nu_tau~]CC'
)

tp_Bminus_mc_Mu = tuple_initialize_aux(
    'MCTupleBminusMu',
    '${b}[B- => ${d0}(D0 => ${k}K- ${pi}pi+) ${mu}mu- ${anu_mu}nu_mu~]CC'
)

# B0 ###########################################################################
tp_B0 = tuple_initialize(
    'TupleB0',
    seq_B0,
    '${b0}[B~0 -> ${dst}(D*(2010)+ -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi+) ${mu}mu-]CC'
)
tuple_postpocess(tp_B0)

# B0 wrong-sign ################################################################
tp_B0_ws_Mu = tuple_initialize(
    'TupleB0WSMu',
    seq_B0_ws_Mu,
    '${b0}[B~0 -> ${dst}(D*(2010)+ -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi+) ${mu}mu+]CC'
)
tuple_postpocess(tp_B0_ws_Mu)

tp_B0_ws_Pi = tuple_initialize(
    'TupleB0WSPi',
    seq_B0_ws_Pi,
    '${b0}[B~0 -> ${dst}(D*(2010)- -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi-) ${mu}mu-]CC'
)
tuple_postpocess(tp_B0_ws_Pi)

# B0 MC ########################################################################
tp_B0_mc_Tau = tuple_initialize_aux(
    'MCTupleB0Tau',
    '('
    '${b0}[B~0 => ${dst}(D*(2010)+ => ${d0}(D0 => ${k}K- ${pi}pi+) ${spi}pi+) ${tau}(tau- => ${mu}mu- ${anu_mu}nu_mu~ ${nu_tau}nu_tau) ${anu_tau}nu_tau~]CC'
    '||'
    '${b0}[B0 => ${dst}(D*(2010)+ => ${d0}(D0 => ${k}K- ${pi}pi+) ${spi}pi+) ${tau}(tau- => ${mu}mu- ${anu_mu}nu_mu~ ${nu_tau}nu_tau) ${anu_tau}nu_tau~]CC'
    ')'
)

tp_B0_mc_Mu = tuple_initialize_aux(
    'MCTupleB0Mu',
    '('
    '${b0}[B~0 => ${dst}(D*(2010)+ => ${d0}(D0 => ${k}K- ${pi}pi+) ${spi}pi+) ${mu}mu- ${anu_mu}nu_mu~]CC'
    '||'
    '${b0}[B0 => ${dst}(D*(2010)+ => ${d0}(D0 => ${k}K- ${pi}pi+) ${spi}pi+) ${mu}mu- ${anu_mu}nu_mu~]CC'
    ')'
)

# B*_0+ -> B0 Pi+ ##############################################################
tp_BstPlus = tuple_initialize(
    'TupleBstPlus',
    seq_BstPlus,
    '[${bst}B*_0- -> ${b0}(B~0 -> ${dst}(D*(2010)- -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi-) ${mu}mu-) ${bpi}pi-]CC'
)

# B*_00 -> B0 Pi+ Pi- ##########################################################
tp_Bst0 = tuple_initialize(
    'TupleBst0',
    seq_Bst0,
    '[${bst0}B*_0~0 -> ${b0}(B~0 -> ${dst}(D*(2010)- -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi-) ${mu}mu-) ${bpi1}pi+ ${bpi2}pi-]CC'
)


################################################
# Add selection & tupling sequences to DaVinci #
################################################

if has_flag('CUTFLOW') or has_flag('NON_MU_MISID'):
    DaVinci().UserAlgorithms += [seq_Bminus.sequence(),
                                 seq_B0.sequence(),
                                 # ntuples
                                 tp_Bminus, tp_B0]
elif DaVinci().Simulation:
    DaVinci().UserAlgorithms += [seq_Bminus.sequence(),
                                 seq_B0.sequence(),
                                 # ntuples
                                 tp_Bminus, tp_B0,
                                 # auxiliary ntuples
                                 tp_Bminus_mc_Tau, tp_Bminus_mc_Mu,
                                 tp_B0_mc_Tau, tp_B0_mc_Mu]
else:
    DaVinci().UserAlgorithms += [seq_Bminus.sequence(),
                                 seq_Bminus_ws.sequence(),
                                 seq_B0.sequence(),
                                 seq_B0_ws_Mu.sequence(),
                                 seq_B0_ws_Pi.sequence(),
                                 # ntuples
                                 tp_Bminus, tp_Bminus_ws,
                                 tp_B0, tp_B0_ws_Mu, tp_B0_ws_Pi]

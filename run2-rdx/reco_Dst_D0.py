# Author: Phoebe Hamilton, Manuel Franco Sevilla, Yipeng Sun
# License: BSD 2-clause
# Last Change: Sun Apr 11, 2021 at 05:58 PM +0200
#
# Description: Definitions of selection and reconstruction procedures for run 2
#              R(D(*)). For more thorough comments, take a look at:
#                  run1-rdx/reco_Dst_D0.py


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

from Configurables import MessageSvc

DaVinci().InputType = 'DST'
DaVinci().SkipEvents = 0
DaVinci().PrintFreq = 100

DaVinci().Lumi = not DaVinci().Simulation

# Debug options
# DaVinci().EvtMax = 300
DaVinci().EvtMax = -1


if has_flag('TRACKER_ONLY'):
    MessageSvc().OutputLevel = 6  # Suppress L0 error output


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
ms_all_protos.Output = 'Rec/ProtoP/MyProtoPMaker/ProtoParticles'

# NOTE: The name 'StdNoPIDsVeloPions' is hard-coded in the tuple tool, so the
#       name should not be changed.
ms_velo_pions = NoPIDsParticleMaker('StdNoPIDsVeloPions', Particle='pion')
ms_velo_pions.Input = ms_all_protos.Output

trackSelector(ms_velo_pions, trackTypes=['Velo'])
updateDoD(ms_velo_pions)

ms_scale = TrackScaleState('StateScale')
ms_smear = TrackSmearState('StateSmear')


if not DaVinci().Simulation:
    DaVinci().appendToMainSequence([ms_scale])
elif not has_flag('NO_SMEAR'):
    DaVinci().appendToMainSequence([ms_smear])


DaVinci().appendToMainSequence([ms_all_protos, ms_velo_pions])


######################
# Define pre-filters #
######################
# The run 2 stripping line definition can be found at:
#  http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping28r2/semileptonic/strippingb2d0muxb2dmufortaumuline.html

from Configurables import LoKi__HDRFilter as HDRFilter


if has_flag('NON_MU_MISID'):
    line_strip = 'b2D0MuXFakeB2DMuForTauMuLine'
else:
    line_strip = 'b2D0MuXB2DMuForTauMuLine'


fltr_strip = HDRFilter(
    'StrippedBCands',
    Code="HLT_PASS('Stripping{0}Decision')".format(line_strip))

# NOTE: Run 2 stripping contains a HLT2 filter, so this is only needed for
#       'DV_STRIP' flag.
line_hlt = 'Hlt2XcMuXForTauB2XcMu'
fltr_hlt = HDRFilter(
    'Hlt2StrippingLine',
    Code="HLT_PASS('{0}Decision')".format(line_hlt))


if has_flag('BARE'):
    pass
elif has_flag('DV_STRIP'):
    DaVinci().EventPreFilters = [fltr_hlt]
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


pr_all_nopid_K = AutomaticData(Location='Phys/StdAllNoPIDsKaons/Particles')
pr_loose_K = AutomaticData(Location='Phys/StdLooseKaons/Particles')

pr_all_nopid_Pi = AutomaticData(Location='Phys/StdAllNoPIDsPions/Particles')
pr_loose_Pi = AutomaticData(Location='Phys/StdLoosePions/Particles')
pr_all_loose_Pi = AutomaticData(Location='Phys/StdAllLoosePions/Particles')

pr_all_nopid_Mu = AutomaticData(Location='Phys/StdAllNoPIDsMuons/Particles')
pr_all_loose_Mu = AutomaticData(Location='Phys/StdAllLooseMuons/Particles')


##############################
# Stable particle selections #
##############################

from PhysSelPython.Wrappers import Selection
from Configurables import FilterDesktop, FilterInTrees
from Configurables import TisTosParticleTagger

# We don't plan to filtering on Muon with global TIS for run 2, for now.
sel_stripped_Mu_filtered_evt = Selection(
    'SelMyStrippedMuFilteredEvent',
    Algorithm=FilterDesktop(
        'MyStrippedFiltered',
        Code="INTREE((ABSID == 'mu+') & (TIS('L0.*', 'L0TriggerTisTos')))"
    ),
    RequiredSelections=[pr_stripped]
)

# NOTE: 'stripped' selections require the existence of a stripping line, which
#       only exists in data, not MC.
# NOTE: We need to do TIS-filtering for real data because unfiltered real data
#       tuples are too large.
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


# For run 2, use unstripped Muon and don't put additional cut on Muons yet.
# We can always do TIS-filtering in step 2.
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
    sel_Mu = pr_all_nopid_Mu
    sel_soft_Pi = pr_all_nopid_Pi


#########################
# B- -> D0 Mu selection #
#########################

from Configurables import CombineParticles
from Configurables import FitDecayTrees
from PhysSelPython.Wrappers import SelectionSequence

algo_mc_match_preambulo = [
    'from LoKiMC.functions import *',
    'from LoKiPhysMC.decorators import *',
    'from LoKiPhysMC.functions import *'
]

# D0 ###########################################################################
algo_D0 = CombineParticles('MyD0')
algo_D0.DecayDescriptor = '[D0 -> K- pi+]cc'

algo_D0.DaughtersCuts = {
    'K+': '(MIPCHI2DV(PRIMARY) > 9.0) &'
          '(P > 2.0*GeV) & (PT > 300.0*MeV) &'
          '(TRGHOSTPROB < 0.5)',
    'pi-': '(P > 2.0*GeV) & (PT > 300.0*MeV) &'
           '(MIPCHI2DV(PRIMARY) > 9.0) &'
           '(TRGHOSTPROB < 0.5)'
}

algo_D0.CombinationCut = \
    "(ADAMASS('D0') < 100.0*MeV) &" \
    "(ACHILD(PT,1) + ACHILD(PT,2) > 2500.0*MeV)"
algo_D0.MotherCut = \
    "(SUMTREE(PT,ISBASIC) > 2500.0*MeV) & (ADMASS('D0') < 80.0*MeV) &" \
    "(VFASPF(VCHI2/VDOF) < 4.0) & (BPVVDCHI2 > 25.0) & (BPVDIRA > 0.999)"


if has_flag('BARE'):
    algo_D0.DaughtersCuts = {
        'K+': '(PIDK > 2.0) & (MIPCHI2DV(PRIMARY) > 4.5) &'
              '(TRGHOSTPROB < 1.0)',
        'pi-': '(MIPCHI2DV(PRIMARY) > 4.5) &'
               '(PIDK < 4.0) & (TRGHOSTPROB < 1.0)'
    }

    algo_D0.CombinationCut = "ATRUE"
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


sel_D0 = Selection(
    'SelMyD0',
    Algorithm=algo_D0,
    RequiredSelections=[sel_charged_K, sel_charged_Pi]
)

# B- ###########################################################################
algo_Bminus = CombineParticles('MyB-')
algo_Bminus.DecayDescriptor = '[B- -> D0 mu-]cc'

algo_Bminus.DaughtersCuts = {
    'mu-': '(MIPCHI2DV(PRIMARY)> 16.0) & (TRGHOSTPROB < 0.5) &'
           '(P > 3.0*GeV)'  # NOTE: Mu PID is added later
}


if not (has_flag('NON_MU_MISID') or DaVinci().Simulation) or \
        has_flag('CUTFLOW'):
    algo_Bminus.DaughtersCuts['mu-'] = \
        '(PIDmu > -200.0) &' + algo_Bminus.DaughtersCuts['mu-']


algo_Bminus.CombinationCut = '(AM < 10.2*GeV)'
algo_Bminus.MotherCut = \
    "(MM < 10.0*GeV) & (MM > 0.0*GeV) &" \
    "(VFASPF(VCHI2/VDOF) < 6.0) & (BPVDIRA > 0.999)"


if has_flag('BARE'):
    algo_Bminus.DaughtersCuts['mu-'] = \
        "(MIPCHI2DV(PRIMARY) > 8.0) & (TRGHOSTPROB < 1.0) &" \
        "(PIDmu > -400.0)"

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
algo_Bminus_ws = CombineParticles('MyB-WS')
algo_Bminus_ws.DecayDescriptor = '[B+ -> D0 mu+]cc'

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
# NOTE: We are using the same made-up cuts for Dst, for now.
algo_Dst = CombineParticles('MyDst')
algo_Dst.DecayDescriptor = '[D*(2010)+ -> D0 pi+]cc'

algo_Dst.DaughtersCuts = {
    'pi+': '(MIPCHI2DV(PRIMARY) > 0.0) & (TRCHI2DOF < 3.0) &'
           '(TRGHOSTPROB < 0.25)'
}

algo_Dst.CombinationCut = "(ADAMASS('D*(2010)+') < 220.0*MeV)"
algo_Dst.MotherCut = \
    "(ADMASS('D*(2010)+') < 125.0*MeV) &" \
    "(M-MAXTREE(ABSID=='D0', M) < 160.0*MeV) &" \
    "(VFASPF(VCHI2/VDOF) < 100.0)"


if has_flag('BARE'):
    algo_Dst.DaughtersCuts = {
        'pi+': '(MIPCHI2DV(PRIMARY) > 0.0) & (TRCHI2DOF < 6.0) &'
               '(TRGHOSTPROB < 0.5)'
    }

    algo_Dst.CombinationCut = "ATRUE"
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

algo_B0.CombinationCut = 'ATRUE'
algo_B0.MotherCut = "(VFASPF(VCHI2/VDOF) < 100.0)"  # Loose cuts here

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
        UsePVConstraint=False,
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
        UsePVConstraint=False,
        Inputs=[sel_B0_ws_Mu.outputLocation()]
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
        UsePVConstraint=False,
        Inputs=[sel_B0_ws_Pi.outputLocation()]
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


##################
# HLT1 emulation #
##################

from Configurables import AddRelatedInfo, RelInfoHLT1Emulation


def hlt1_get_var_gen(output_loc, keys, vals):
    def get_var(i, j):
        comb = '{}_{}'.format(i, j)
        return {key: 'RELINFO("{}", "{}_{}", 0)'.format(output_loc, val, comb)
                for key, val in zip(keys, vals)}

    return get_var


def add_hlt1_info(sel_seq):
    relinfo = AddRelatedInfo('RelInfo_HLT1_' + sel_seq.name())
    relinfo.addTool(RelInfoHLT1Emulation, 'RelInfoHLT1Emulation')
    relinfo.Tool = "RelInfoHLT1Emulation"
    relinfo.Location = 'HLT1Emulation'
    relinfo.Inputs = [sel_seq.outputLocation()]

    dt_hlt1_emu = getattr(relinfo, 'RelInfoHLT1Emulation')
    dt_hlt1_emu.Variables = []
    dt_hlt1_emu.nltValue = int(DaVinci().DataType[2:])  # figure out the year by yourself, DaVinci!

    return relinfo


##################
# Define ntuples #
##################

from Configurables import DecayTreeTuple, MCDecayTreeTuple
from DecayTreeTuple.Configuration import *  # for addTupleTool

# Additional TupleTool for addTool only
from Configurables import BackgroundCategory

# HLT1 emulation
from itertools import combinations
from MVADictHelpers import addMatrixnetclassifierTuple


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
    ]

    tt_track_info = really_add_tool(tp, 'TupleToolTrackInfo')
    tt_track_info.Verbose = True  # for 'TRACK_nTTHits'

    tt_pid = really_add_tool(tp, 'TupleToolPid')
    tt_pid.Verbose = True

    # L0Calo variables
    tt_l0_calo = really_add_tool(tp, 'TupleToolL0Calo')
    tt_l0_calo.WhichCalo = "HCAL"
    tt_l0_calo.TriggerClusterLocation = "/Event/Trig/L0/Calo"
    tt_l0_calo.FillTriggerEt = True

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
                              'Hlt1TrackMVADecision',
                              'Hlt1TwoTrackMVADecision',
                              # HLT 2
                              'Hlt2XcMuXForTauB2XcMuDecision'
                          ]
                          ):
    tt_trigger = tp.addTupleTool('TupleToolTrigger')
    tt_trigger.Verbose = True
    tt_trigger.TriggerList = trigger_list_global

    tt_tistos = tp.addTupleTool('TupleToolTISTOS')
    tt_tistos.Verbose = True
    tt_tistos.TriggerList = trigger_list_global

    # NOTE: This has to be disabled, otherwise the TupleToolTrigger will NOT
    # act on B mesons
    # Trigger decisions to be saved for B meson
    # tt_tistos_B = getattr(tp, B_meson).addTupleTool('TupleToolTISTOS')
    # tt_tistos_B.Verbose = True
    # tt_tistos_B.TriggerList = trigger_list_B

    getattr(tp, B_meson).ToolList += [
        'TupleToolTagDiscardDstMu',
        'TupleToolTauMuDiscrVars',
    ]

    tt_app_iso = getattr(tp, B_meson).addTupleTool('TupleToolApplyIsolation')
    tt_app_iso.WeightsFile = weights

    getattr(tp, Mu).ToolList += ['TupleToolANNPIDTraining']


def tuple_postpocess_mc(tp,
                        B_meson='b0',
                        emu_hlt1_lines=[
                            'Hlt1TwoTrackMVA'
                        ],
                        # extra_hlt1_vars=[
                        #     'PT_DAU',
                        #     'P_DAU',
                        #     'IPCHI2_OWNPV_DAU',
                        #     'IPCHI2_MINIPPV_DAU',
                        #     'TRACK_GHOSTPROB_DAU',
                        #     'TRACK_CHI2_DAU',
                        #     'TRACK_NDOF_DAU'
                        # ],
                        extra_hlt1_vars=[],
                        extra_hlt1_vars_combo=[
                            'VERTEX_CHI2_COMB',
                            'VERTEX_NDOF_COMB',
                            'ETA_COMB',
                            'MCORR_OWNPV_COMB',
                            # 'MCORR_MINIPPV_COMB',
                            'SUMPT_COMB',
                            'DIRA_OWNPV_COMB',
                            # 'DIRA_MINIPPV',
                            'DOCA_COMB',
                            'VDCHI2_OWNPV_COMB',
                            # 'VDCHI2_MINIPPV_COMB',
                            'IPCHI2_OWNPV_COMB',
                            # 'IPCHI2_MINIPPV_COMB',
                            # 'NLT_MINIPPV_COMB',
                            # 'NLT_OWNPV_COMB',
                            'PT_COMB',
                            'P_COMB'
                        ],
                        **kwargs):
    tuple_postpocess_data(tp, B_meson=B_meson, **kwargs)

    # Always add L0 and HLT1 emulation variables for MC
    relinfo_output = tp.Inputs[0].replace('Particles', 'HLT1Emulation')

    # Add variables like 'k_X'. This is used for L0 trigger emulation
    tp.ToolList.append('TupleToolTrackPosition')

    get_var = hlt1_get_var_gen(
        relinfo_output,
        keys=['chi2', 'fdchi2', 'sumpt', 'nlt'],
        vals=[
            'VERTEX_CHI2_COMB',
            'VDCHI2_MINIPPV_COMB',
            'SUMPT_COMB',
            'NLT_MINIPPV_COMB'
        ])
    get_var_wrong_ip = hlt1_get_var_gen(
        relinfo_output,
        keys=['wrong_ip_chi2', 'wrong_ip_fdchi2', 'wrong_ip_sumpt',
              'wrong_ip_nlt'],
        vals=[
            'VERTEX_CHI2_COMB',
            'VDCHI2_MINIPPV_COMB',
            'SUMPT_COMB',
            'NLT_OWNPV_COMB'
        ])

    # HLT1 emulation
    for hlt in emu_hlt1_lines:
        for i, j in combinations(range(1, 5), 2):
            addMatrixnetclassifierTuple(
                getattr(tp, B_meson),
                '$PARAMFILESROOT/data/{}.mx'.format(hlt),
                get_var(i, j),
                '{}Emulations_{}_{}'.format(hlt, i, j),
                True
            )
            addMatrixnetclassifierTuple(
                getattr(tp, B_meson),
                '$PARAMFILESROOT/data/{}.mx'.format(hlt),
                get_var_wrong_ip(i, j),
                '{}Emulations_WrongIP_{}_{}'.format(hlt, i, j),
                True
            )

    # Additional HLT1 variables
    tt_hlt1_emu = getattr(tp, B_meson).addTupleTool(
        'LoKi::Hybrid::TupleTool/Hlt1TwoTrackMVAEmulation')
    tt_hlt1_emu.Preambulo = []

    for var in extra_hlt1_vars:
        for i in range(1, 5):
            key = '{}_{}'.format(var, i)
            tt_hlt1_emu.Variables[key] = \
                'RELINFO("{}", "{}", 0)'.format(relinfo_output, key)

    for var in extra_hlt1_vars_combo:
        for i, j in combinations(range(1, 5), 2):
            key = '{}_{}_{}'.format(var, i, j)
            tt_hlt1_emu.Variables[key] = \
                'RELINFO("{}", "{}", 0)'.format(relinfo_output, key)


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


################################################
# Add selection & tupling sequences to DaVinci #
################################################

if has_flag('CUTFLOW') or has_flag('NON_MU_MISID'):
    DaVinci().UserAlgorithms += [seq_Bminus.sequence(),
                                 seq_B0.sequence(),
                                 # ntuples
                                 tp_Bminus, tp_B0]
elif DaVinci().Simulation:
    DaVinci().UserAlgorithms += [seq_Bminus.sequence(), seq_B0.sequence()]

    # For trigger emulation
    DaVinci().UserAlgorithms += [add_hlt1_info(x)
                                 for x in (seq_Bminus, seq_B0)]

    DaVinci().UserAlgorithms += [tp_Bminus, tp_B0,
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

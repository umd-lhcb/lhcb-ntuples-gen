# Author: Lucas Meyer Garcia
# License: BSD 2-clause
#
# Description: Definitions of selection and reconstruction procedures for
#              [D*+ -> D0 pi+]cc samples needed for misid studies in run 2 R(D(*)).
#              Based on run2-rdx/reco_Dst_D0.py.
#
# Flags for run 2:
#   KMUNU:   Configure truth-matching for D0 -> K- mu+ nu sample
#   PIMUNU:  Configure truth-matching for D0 -> pi- mu+ nu sample
#   PIPI:    Configure truth-matching for D0 -> pi+ pi- sample
#   PIPIPI0: Configure truth-matching for D0 -> pi+ pi- pi0 sample
#   Absence of flags configures truth-matching D0 -> K- pi+ sample


#########################################
# Load user-defined configuration flags #
#########################################

from Configurables import DaVinci

# NOTE: We *abuse* DaVinci's MoniSequence to pass additional flags
user_config = DaVinci().MoniSequence
DaVinci().MoniSequence = []  # Nothing should be in the sequence after all!

no_flags = (len(user_config) == 0)

def has_flag(*flg):
    for f in flg:
        if f in user_config:
            return True
    return False


#####################
# Configure DaVinci #
#####################

from Configurables import (DecayTreeTuple, CombineParticles, FilterDesktop,
                           BackgroundCategory, TrackSmearState,
                           TupleToolMCDaughters)
from DecayTreeTuple.Configuration import *
from PhysSelPython.Wrappers import Selection, SelectionSequence
from StandardParticles import (StdAllNoPIDsKaons, StdAllNoPIDsPions,
                               StdAllNoPIDsMuons)

ms_smear = TrackSmearState('StateSmear')
DaVinci().appendToMainSequence([ms_smear])

DaVinci().InputType = 'DST'
DaVinci().PrintFreq = 10000
DaVinci().SkipEvents = 0
DaVinci().Lumi = not DaVinci().Simulation
DaVinci().EvtMax = -1

mc_match_preambulo = [
    'from LoKiMC.functions import *',
    'from LoKiPhysMC.functions import *'
]

# Define truth-matching requirements
fromSignal = 'MCSELMATCH( MCFROMSIGNAL )'
fromDecay  = 'MCSELMATCH( MCFROMDECAYS )'
fromD0     = 'MCSELMATCH( MCINANCESTORS( MCABSID == "D0" ) )'
fromDst    = 'MCSELMATCH( MCINANCESTORS( MCABSID == "D*(2010)+" ) )'
fromPi     = 'MCSELMATCH( MCINANCESTORS( MCABSID == "pi+" ) )'
fromK      = 'MCSELMATCH( MCINANCESTORS( MCABSID == "K+" ) )'
notFromD0  = f'(NINTREE( {fromD0} ) < 1)'
isD0       = 'mcMatch("[D0]cc")'
isDst      = 'mcMatch("[D*(2010)+]cc")'
isK        = 'mcMatch("[K+]cc")'
isPi       = 'mcMatch("[pi+]cc")'
isP        = 'mcMatch("[p+]cc")'
isE        = 'mcMatch("[e-]cc")'
isMu       = 'mcMatch("[mu-]cc")'
isEorGhost = f'(NINTREE( {isK} | {isPi} | {isP} | {isMu} ) < 1)'
isKLoose   = f'( {isK}  | ({isMu} & {fromK} ) )'
isPiLoose  = f'( {isPi} | ({isMu} & {fromPi}) )'

# Define trigger list for TupleToolTISTOS
# Should really only need L0
trig_list = [
    'L0HadronDecision',
    'L0MuonDecision',
    'Hlt1TrackMVADecision',
    'Hlt1TwoTrackMVADecision',
    'Hlt2XcMuXForTauB2XcMuDecision',
    'Hlt2XcMuXForTauB2XcFakeMuDecision'
]

#################################################################
# D* -> D0(-> K pi) pi ntuples for study K/pi misid corrections #
#################################################################


cutK  = f'ISLONG & {fromSignal} & {fromDst} & {fromD0}'
cutPi = f'ISLONG & {fromSignal} & {fromDst} & {fromD0}'
if no_flags:
    cutK  += f' & {isKLoose}'
    cutPi += f' & {isPiLoose}'

cutD0  = f'{isD0}'
cutDst = f'{isDst}'
if not no_flags:
    cutD0  += ' & in_range(1735, M, 2000)'
    cutDst += ' & ((M - CHILD(M, 1)) < 168)'

filterK = FilterDesktop(
    'FilterK',
    Code=cutK,
    Preambulo=mc_match_preambulo)
filterPi = FilterDesktop(
    'FilterPi',
    Code=cutPi,
    Preambulo=mc_match_preambulo)
filterPiSoft = FilterDesktop(
    'FilterPiSoft',
    Code=f'ISLONG & {fromSignal} & {fromDst} & {notFromD0} & {isPiLoose}',
    Preambulo=mc_match_preambulo)

selectionK = Selection('SelK',
                       Algorithm=filterK,
                       RequiredSelections=[StdAllNoPIDsKaons])
selectionPi = Selection('SelPi',
                        Algorithm=filterPi,
                        RequiredSelections=[StdAllNoPIDsPions])
selectionPiSoft = Selection('SelPiSoft',
                            Algorithm=filterPiSoft,
                            RequiredSelections=[StdAllNoPIDsPions])

# define D0 -> K pi decay
D02KPiDauCuts = {'K-': 'ALL', 'pi+': 'ALL'}
D02KPiComCuts = 'AHASCHILD( (TRGHOSTPROB < 0.5) & HASMUON & in_range(3000, P, 100000) )'
D02KPiMotCuts = cutD0
D02KPiCombination = CombineParticles('CombD02KPi',
                                     DecayDescriptor='[D0 -> K- pi+]cc',
                                     MotherCut=D02KPiMotCuts,
                                     DaughtersCuts=D02KPiDauCuts,
                                     CombinationCut=D02KPiComCuts)
D02KPi = Selection('SelD02KPi',
                   Algorithm=D02KPiCombination,
                   RequiredSelections=[selectionK, selectionPi])

# define D* -> D0 pi decay
Dst2D0PiDauCuts = {'D0': 'ALL', 'pi+': 'ALL'}
Dst2D0PiComCuts = 'AALL'
Dst2D0PiMotCuts = cutDst
Dst2D0PiCombination = CombineParticles(
    'CombDst2D0Pi',
    DecayDescriptor='[D*(2010)+ -> D0 pi+]cc',
    MotherCut=Dst2D0PiMotCuts,
    DaughtersCuts=Dst2D0PiDauCuts,
    CombinationCut=Dst2D0PiComCuts)
Dst2D0Pi = Selection('SelDst2D0Pi',
                     Algorithm=Dst2D0PiCombination,
                     RequiredSelections=[D02KPi, selectionPiSoft])

# Define decay tree tuple with uBDT input for K candidate
dttDstK = DecayTreeTuple('TupleDstANNK')
dttDstK.setDescriptorTemplate(
    '${dst}[(D*(2010)+ -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi+)]CC')
dttDstK.Inputs = [Dst2D0Pi.outputLocation()]
dttDstK.k.addTupleTool('TupleToolPid')
dttDstK.k.TupleToolPid.Verbose = True
dttDstK.addTupleTool('TupleToolTISTOS')
dttDstK.TupleToolTISTOS.Verbose = True
dttDstK.TupleToolTISTOS.TriggerList = trig_list
dttDstK.addTupleTool('TupleToolRecoStats')
dttDstK.addTupleTool('TupleToolTrackInfo')
dttDstK.addTupleTool('TupleToolMCBackgroundInfo')
dttDstK.TupleToolMCBackgroundInfo.addTool(BackgroundCategory)
dttDstK.addTupleTool('TupleToolMCTruth')
dttDstK.TupleToolMCTruth.IP2MCPAssociatorTypes = ['DaVinciSmartAssociator']
dttDstK.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolHierarchyExt'
]
dttDstK.k.addTupleTool('TupleToolANNPIDTraining')

dttDstK.k.addTool(TupleToolMCDaughters, name="TupleToolMCDaughtersK")
dttDstK.k.ToolList+=["TupleToolMCDaughters/TupleToolMCDaughtersK"]

# Now define decay tree tuple with uBDT input for pi candidate
dttDstPi = DecayTreeTuple('TupleDstANNPi')
dttDstPi.setDescriptorTemplate(
    '${dst}[(D*(2010)+ -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi+)]CC')
dttDstPi.Inputs = [Dst2D0Pi.outputLocation()]
dttDstPi.pi.addTupleTool('TupleToolPid')
dttDstPi.pi.TupleToolPid.Verbose = True
dttDstPi.addTupleTool('TupleToolTISTOS')
dttDstPi.TupleToolTISTOS.Verbose = True
dttDstPi.TupleToolTISTOS.TriggerList = trig_list
dttDstPi.addTupleTool('TupleToolRecoStats')
dttDstPi.addTupleTool('TupleToolTrackInfo')
dttDstPi.addTupleTool('TupleToolMCBackgroundInfo')
dttDstPi.TupleToolMCBackgroundInfo.addTool(BackgroundCategory)
dttDstPi.addTupleTool('TupleToolMCTruth')
# TupleToolMCTruth default behavior is to try DaVinciSmartAssociator and, if not
# succesfull, try again with MCMatchObjP2MCRelator. Since I still don't understand
# MCMatchObjP2MCRelator very well, let's use only DaVinciSmartAssociator.
dttDstPi.TupleToolMCTruth.IP2MCPAssociatorTypes = ['DaVinciSmartAssociator']
dttDstPi.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolHierarchyExt'
]
dttDstPi.pi.addTupleTool('TupleToolANNPIDTraining')

dttDstPi.pi.addTool(TupleToolMCDaughters, name="TupleToolMCDaughtersPi")
dttDstPi.pi.ToolList+=["TupleToolMCDaughters/TupleToolMCDaughtersPi"]

sequenceDstK = SelectionSequence('SeqDstK',
                                 TopSelection=Dst2D0Pi,
                                 PostSelectionAlgs=[dttDstK])
sequenceDstPi = SelectionSequence('SeqDstPi',
                                  TopSelection=Dst2D0Pi,
                                  PostSelectionAlgs=[dttDstPi])

DaVinci().UserAlgorithms += [sequenceDstK.sequence(), sequenceDstPi.sequence()]

if no_flags:
    #########################################
    # K/pi ntuples for DiF smearing studies #
    #########################################

    # Loosely select true Kaons satisfying ISMUON
    filterKDiF = FilterDesktop(
        'FilterKDiF',
        Code=
        f'ISLONG & ISMUON & (TRGHOSTPROB < 0.5) & in_range(3000, P, 100000) & {isKLoose} & {fromDecay}',
        Preambulo=mc_match_preambulo)

    selectionKDiF = Selection('SelKDiF',
                            Algorithm=filterKDiF,
                            RequiredSelections=[StdAllNoPIDsKaons])

    dttKDiF = DecayTreeTuple('TupleKDiF')
    dttKDiF.setDescriptorTemplate('${k}[K+]CC')
    dttKDiF.Inputs = [selectionKDiF.outputLocation()]
    dttKDiF.k.addTupleTool('TupleToolPid')
    dttKDiF.k.TupleToolPid.Verbose = True
    dttKDiF.addTupleTool('TupleToolTISTOS')
    dttKDiF.TupleToolTISTOS.Verbose = True
    dttKDiF.TupleToolTISTOS.TriggerList = trig_list
    dttKDiF.addTupleTool('TupleToolRecoStats')
    dttKDiF.addTupleTool('TupleToolTrackInfo')
    dttKDiF.addTupleTool('TupleToolMCTruth')
    dttKDiF.TupleToolMCTruth.IP2MCPAssociatorTypes = ['DaVinciSmartAssociator']
    dttKDiF.TupleToolMCTruth.ToolList = [
        'MCTupleToolKinematic',
        'MCTupleToolHierarchyExt'
    ]
    dttKDiF.k.addTupleTool('TupleToolANNPIDTraining')

    dttKDiF.k.addTool(TupleToolMCDaughters, name="TupleToolMCDaughtersKDiF")
    dttKDiF.k.ToolList+=["TupleToolMCDaughters/TupleToolMCDaughtersKDiF"]

    sequenceK_dif = SelectionSequence('SeqKDiF',
                                    TopSelection=selectionKDiF,
                                    PostSelectionAlgs=[dttKDiF])

    # Loosely select true Pions satisfying ISMUON
    filterPiDiF = FilterDesktop(
        'FilterPiDiF',
        Code=
        f'ISLONG & ISMUON & (TRGHOSTPROB < 0.5) & in_range(3000, P, 100000) & {isPiLoose} & {fromDecay}',
        Preambulo=mc_match_preambulo)

    selectionPiDiF = Selection('SelPiDiF',
                            Algorithm=filterPiDiF,
                            RequiredSelections=[StdAllNoPIDsPions])

    dttPiDiF = DecayTreeTuple('TuplePiDiF')
    dttPiDiF.setDescriptorTemplate('${pi}[pi+]CC')
    dttPiDiF.Inputs = [selectionPiDiF.outputLocation()]
    dttPiDiF.pi.addTupleTool('TupleToolPid')
    dttPiDiF.pi.TupleToolPid.Verbose = True
    dttPiDiF.addTupleTool('TupleToolTISTOS')
    dttPiDiF.TupleToolTISTOS.Verbose = True
    dttPiDiF.TupleToolTISTOS.TriggerList = trig_list
    dttPiDiF.addTupleTool('TupleToolRecoStats')
    dttPiDiF.addTupleTool('TupleToolTrackInfo')
    dttPiDiF.addTupleTool('TupleToolMCTruth')
    dttPiDiF.TupleToolMCTruth.IP2MCPAssociatorTypes = ['DaVinciSmartAssociator']
    dttPiDiF.TupleToolMCTruth.ToolList = [
        'MCTupleToolKinematic',
        'MCTupleToolHierarchyExt'
    ]
    dttPiDiF.pi.addTupleTool('TupleToolANNPIDTraining')

    dttPiDiF.pi.addTool(TupleToolMCDaughters, name="TupleToolMCDaughtersPiDif")
    dttPiDiF.pi.ToolList+=["TupleToolMCDaughters/TupleToolMCDaughtersPiDiF"]

    sequencePi_dif = SelectionSequence('SeqPiDiF',
                                    TopSelection=selectionPiDiF,
                                    PostSelectionAlgs=[dttPiDiF])

    DaVinci().UserAlgorithms += [
        sequenceK_dif.sequence(),
        sequencePi_dif.sequence()
    ]


    ######################
    # e and ghost tracks #
    ######################

    # Select true e and ghost tracks
    filterEorGhost = FilterDesktop(
        'FilterEorGhost',
        Code=
        f'ISLONG & {isEorGhost} & (TRGHOSTPROB < 0.5) & in_range(3000, P, 100000)',
        Preambulo=mc_match_preambulo)

    selectionEorGhost = Selection('SelEorGhost',
                                Algorithm=filterEorGhost,
                                RequiredSelections=[StdAllNoPIDsMuons])

    # define D0 -> K pi decay
    D02KPiDauCutsEorGhost = {'K-': 'ALL', 'pi+': 'ALL'}
    D02KPiComCutsEorGhost = 'AALL'
    D02KPiMotCutsEorGhost = 'ALL'
    D02KPiCombinationEorGhost = CombineParticles('CombD02KPiEorGhost',
                                                DecayDescriptor='[D0 -> K- pi+]cc',
                                                MotherCut=D02KPiMotCutsEorGhost,
                                                DaughtersCuts=D02KPiDauCutsEorGhost,
                                                CombinationCut=D02KPiComCutsEorGhost)
    D02KPiEorGhost = Selection('SelD02KPiEorGhost',
                            Algorithm=D02KPiCombinationEorGhost,
                            RequiredSelections=[selectionK, selectionPi])

    # define D* -> D0 pi decay
    Dst2D0PiDauCutsEorGhost = {'D0': 'ALL', 'pi+': 'ALL'}
    Dst2D0PiComCutsEorGhost = 'AALL'
    Dst2D0PiMotCutsEorGhost = 'ALL'
    Dst2D0PiCombinationEorGhost = CombineParticles(
        'CombDst2D0PiEorGhost',
        DecayDescriptor='[D*(2010)+ -> D0 pi+]cc',
        MotherCut=Dst2D0PiMotCutsEorGhost,
        DaughtersCuts=Dst2D0PiDauCutsEorGhost,
        CombinationCut=Dst2D0PiComCutsEorGhost)
    Dst2D0PiEorGhost = Selection('SelDst2D0PiEorGhost',
                                Algorithm=Dst2D0PiCombinationEorGhost,
                                RequiredSelections=[D02KPiEorGhost, selectionPiSoft])

    # define e/ghost B -> D* mu decay (with signal D* + e/ghost track as mu)
    B02DstMuDauCuts = {'D*(2010)+': 'ALL', 'mu-': 'ALL'}
    B02DstMuComCuts = 'AALL'
    B02DstMuMotCuts = 'VFASPF(VCHI2/VDOF) < 6.0'
    B02DstMuCombination = CombineParticles(
        'CombB02DstEorGhost',
        DecayDescriptor='[B~0 -> D*(2010)+ mu-]cc',
        MotherCut=B02DstMuMotCuts,
        DaughtersCuts=B02DstMuDauCuts,
        CombinationCut=B02DstMuComCuts)
    B02DstMu = Selection('SelB02DstEorGhost',
                        Algorithm=B02DstMuCombination,
                        RequiredSelections=[Dst2D0PiEorGhost, selectionEorGhost])

    dttEorGhost = DecayTreeTuple('EorGhost')
    dttEorGhost.setDescriptorTemplate(
        '${b0}[B~0 -> ${dst}(D*(2010)+ -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi+) ${mu}mu-]CC'
    )
    dttEorGhost.Inputs = [B02DstMu.outputLocation()]
    dttEorGhost.mu.addTupleTool('TupleToolPid')
    dttEorGhost.mu.TupleToolPid.Verbose = True
    dttEorGhost.addTupleTool('TupleToolTISTOS')
    dttEorGhost.TupleToolTISTOS.Verbose = True
    dttEorGhost.TupleToolTISTOS.TriggerList = trig_list
    dttEorGhost.addTupleTool('TupleToolRecoStats')
    dttEorGhost.addTupleTool('TupleToolTrackInfo')
    dttEorGhost.addTupleTool('TupleToolMCBackgroundInfo')
    dttEorGhost.TupleToolMCBackgroundInfo.addTool(BackgroundCategory)
    dttEorGhost.addTupleTool('TupleToolMCTruth')
    dttEorGhost.TupleToolMCTruth.IP2MCPAssociatorTypes = ['DaVinciSmartAssociator']
    dttEorGhost.TupleToolMCTruth.ToolList = [] # Produces only TRUEID branch
    dttEorGhost.mu.addTupleTool('TupleToolANNPIDTraining')

    sequence_g = SelectionSequence('SeqEorGhost',
                                TopSelection=B02DstMu,
                                PostSelectionAlgs=[dttEorGhost])

    DaVinci().UserAlgorithms += [sequence_g.sequence()]

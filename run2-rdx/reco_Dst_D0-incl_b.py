from Configurables import (DecayTreeTuple, CombineParticles, FilterDesktop,
                           BackgroundCategory, DaVinci, TrackSmearState)
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
isK        = 'mcMatch("[K+]cc")'
isPi       = 'mcMatch("[pi+]cc")'
isP        = 'mcMatch("[p+]cc")'
isE        = 'mcMatch("[e-]cc")'
isMu       = 'mcMatch("[mu-]cc")'
isGhost    = f'(NINTREE( {isK} | {isPi} | {isP} | {isE} | {isMu} ) < 1)'
isKLoose   = f'( {isK}  | ({isMu} & {fromK} ) )'
isPiLoose  = f'( {isPi} | ({isMu} & {fromPi}) )'


#################################################################
# D* -> D0(-> K pi) pi ntuples for study K/pi misid corrections #
#################################################################

filterK = FilterDesktop(
    'FilterK',
    Code=f'ISLONG & {fromSignal} & {fromDst} & {fromD0} & {isKLoose}',
    Preambulo=mc_match_preambulo)
filterPi = FilterDesktop(
    'FilterPi',
    Code=f'ISLONG & {fromSignal} & {fromDst} & {fromD0} & {isPiLoose}',
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
D02KPiMotCuts = 'ALL'
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
Dst2D0PiMotCuts = 'ALL'
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
dttDstK.addTool(BackgroundCategory)
dttDstK.addTupleTool('TupleToolTISTOS')
dttDstK.addTupleTool('TupleToolRecoStats')
dttDstK.addTupleTool('TupleToolMCBackgroundInfo')
dttDstK.addTupleTool('TupleToolMCTruth')
dttDstK.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolHierarchy'
]
dttDstK.k.addTupleTool('TupleToolANNPIDTraining')

# Now define decay tree tuple with uBDT input for pi candidate
dttDstPi = DecayTreeTuple('TupleDstANNPi')
dttDstPi.setDescriptorTemplate(
    '${dst}[(D*(2010)+ -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi+)]CC')
dttDstPi.Inputs = [Dst2D0Pi.outputLocation()]
dttDstPi.addTool(BackgroundCategory)
dttDstPi.addTupleTool('TupleToolTISTOS')
dttDstPi.addTupleTool('TupleToolRecoStats')
dttDstPi.addTupleTool('TupleToolMCBackgroundInfo')
dttDstPi.addTupleTool('TupleToolMCTruth')
dttDstPi.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolHierarchy'
]
dttDstPi.pi.addTupleTool('TupleToolANNPIDTraining')

sequenceDstK = SelectionSequence('SeqDstK',
                                 TopSelection=Dst2D0Pi,
                                 PostSelectionAlgs=[dttDstK])
sequenceDstPi = SelectionSequence('SeqDstPi',
                                  TopSelection=Dst2D0Pi,
                                  PostSelectionAlgs=[dttDstPi])

DaVinci().UserAlgorithms += [sequenceDstK.sequence(), sequenceDstPi.sequence()]


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
dttKDiF.addTupleTool('TupleToolMCTruth')
dttKDiF.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolHierarchy'
]
dttKDiF.k.addTupleTool('TupleToolANNPIDTraining')

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
dttPiDiF.addTupleTool('TupleToolMCTruth')
dttPiDiF.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolHierarchy'
]
dttPiDiF.pi.addTupleTool('TupleToolANNPIDTraining')

sequencePi_dif = SelectionSequence('SeqPiDiF',
                                   TopSelection=selectionPiDiF,
                                   PostSelectionAlgs=[dttPiDiF])

DaVinci().UserAlgorithms += [
    sequenceK_dif.sequence(),
    sequencePi_dif.sequence()
]


################
# ghost tracks #
################

# Select true ghost tracks
filterGhost = FilterDesktop(
    'FilterGhost',
    Code=
    f'ISLONG & {isGhost} & (TRGHOSTPROB < 0.5) & in_range(3000, P, 100000)',
    Preambulo=mc_match_preambulo)

selectionGhost = Selection('SelGhost',
                           Algorithm=filterGhost,
                           RequiredSelections=[StdAllNoPIDsMuons])

# define D0 -> K pi decay
D02KPiDauCutsGhost = {'K-': 'ALL', 'pi+': 'ALL'}
D02KPiComCutsGhost = 'AALL'
D02KPiMotCutsGhost = 'ALL'
D02KPiCombinationGhost = CombineParticles('CombD02KPiGhost',
                                          DecayDescriptor='[D0 -> K- pi+]cc',
                                          MotherCut=D02KPiMotCutsGhost,
                                          DaughtersCuts=D02KPiDauCutsGhost,
                                          CombinationCut=D02KPiComCutsGhost)
D02KPiGhost = Selection('SelD02KPiGhost',
                        Algorithm=D02KPiCombinationGhost,
                        RequiredSelections=[selectionK, selectionPi])

# define D* -> D0 pi decay
Dst2D0PiDauCutsGhost = {'D0': 'ALL', 'pi+': 'ALL'}
Dst2D0PiComCutsGhost = 'AALL'
Dst2D0PiMotCutsGhost = 'ALL'
Dst2D0PiCombinationGhost = CombineParticles(
    'CombDst2D0PiGhost',
    DecayDescriptor='[D*(2010)+ -> D0 pi+]cc',
    MotherCut=Dst2D0PiMotCutsGhost,
    DaughtersCuts=Dst2D0PiDauCutsGhost,
    CombinationCut=Dst2D0PiComCutsGhost)
Dst2D0PiGhost = Selection('SelDst2D0PiGhost',
                          Algorithm=Dst2D0PiCombinationGhost,
                          RequiredSelections=[D02KPiGhost, selectionPiSoft])

# define ghost B -> D* mu decay (with signal D* + ghost track as mu)
B02DstMuDauCuts = {'D*(2010)+': 'ALL', 'mu-': 'ALL'}
B02DstMuComCuts = 'AALL'
B02DstMuMotCuts = 'VFASPF(VCHI2/VDOF) < 6.0'
B02DstMuCombination = CombineParticles(
    'CombB02DstGhost',
    DecayDescriptor='[B~0 -> D*(2010)+ mu-]cc',
    MotherCut=B02DstMuMotCuts,
    DaughtersCuts=B02DstMuDauCuts,
    CombinationCut=B02DstMuComCuts)
B02DstMu = Selection('SelB02DstGhost',
                     Algorithm=B02DstMuCombination,
                     RequiredSelections=[Dst2D0PiGhost, selectionGhost])

dttGhost = DecayTreeTuple('Ghost')
dttGhost.setDescriptorTemplate(
    '${b0}[B~0 -> ${dst}(D*(2010)+ -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi+) ${mu}mu-]CC'
)
dttGhost.Inputs = [B02DstMu.outputLocation()]
dttGhost.addTool(BackgroundCategory)
dttGhost.addTupleTool('TupleToolMCTruth')
dttGhost.TupleToolMCTruth.ToolList = []  # Produces only TRUEID branch
dttGhost.mu.addTupleTool('TupleToolANNPIDTraining')

sequence_g = SelectionSequence('SeqGhost',
                               TopSelection=B02DstMu,
                               PostSelectionAlgs=[dttGhost])

DaVinci().UserAlgorithms += [sequence_g.sequence()]

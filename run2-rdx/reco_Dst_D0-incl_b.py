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
isEorGhost    = f'(NINTREE( {isK} | {isPi} | {isP} | {isMu} ) < 1)'
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
dttDstK.k.addTupleTool('TupleToolPid')
dttDstK.k.TupleToolPid.Verbose = True
dttDstK.addTupleTool('TupleToolTISTOS')
dttDstK.addTupleTool('TupleToolRecoStats')
dttDstK.addTupleTool('TupleToolMCBackgroundInfo')
dttDstK.TupleToolMCBackgroundInfo.addTool(BackgroundCategory)
dttDstK.addTupleTool('TupleToolMCTruth')
dttDstK.TupleToolMCTruth.IP2MCPAssociatorTypes = ['DaVinciSmartAssociator']
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
dttDstPi.pi.addTupleTool('TupleToolPid')
dttDstPi.pi.TupleToolPid.Verbose = True
dttDstPi.addTupleTool('TupleToolTISTOS')
dttDstPi.addTupleTool('TupleToolRecoStats')
dttDstPi.addTupleTool('TupleToolMCBackgroundInfo')
dttDstPi.TupleToolMCBackgroundInfo.addTool(BackgroundCategory)
dttDstPi.addTupleTool('TupleToolMCTruth')
# TupleToolMCTruth default behavior is to try DaVinciSmartAssociator and, if not
# succesfull, try again with MCMatchObjP2MCRelator. Since I still don't understand
# MCMatchObjP2MCRelator very well, let's use only DaVinciSmartAssociator.
dttDstPi.TupleToolMCTruth.IP2MCPAssociatorTypes = ['DaVinciSmartAssociator']
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
dttKDiF.k.addTupleTool('TupleToolPid')
dttKDiF.k.TupleToolPid.Verbose = True
dttKDiF.addTupleTool('TupleToolMCTruth')
dttKDiF.TupleToolMCTruth.IP2MCPAssociatorTypes = ['DaVinciSmartAssociator']
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
dttPiDiF.pi.addTupleTool('TupleToolPid')
dttPiDiF.pi.TupleToolPid.Verbose = True
dttPiDiF.addTupleTool('TupleToolMCTruth')
dttPiDiF.TupleToolMCTruth.IP2MCPAssociatorTypes = ['DaVinciSmartAssociator']
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

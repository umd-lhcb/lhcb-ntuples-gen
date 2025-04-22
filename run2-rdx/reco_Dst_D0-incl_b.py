from Configurables import DecayTreeTuple, CombineParticles
from DecayTreeTuple.Configuration import *
from PhysSelPython.Wrappers import Selection, SelectionSequence
from StandardParticles import StdAllNoPIDsKaons, StdAllNoPIDsPions

# define D0 -> K pi decay
nameD0 = 'D02KPi'
D02KPiDauCuts = {'K-': 'ISLONG', 'pi+': 'ISLONG'}
D02KPiComCut = '(AM>0)'
D02KPiMotCuts = '(M>0) '
D02KPiCombination = CombineParticles(
    nameD0,
    DecayDescriptor='[D0 -> K- pi+]cc',
    MotherCut=D02KPiMotCuts,
    DaughtersCuts=D02KPiDauCuts,
    CombinationCut=D02KPiComCut)
D02KPi = Selection(
    'Sel' + nameD0,
    Algorithm=D02KPiCombination,
    RequiredSelections=[StdAllNoPIDsKaons, StdAllNoPIDsPions])

# define D* -> D0 pi decay
nameDst = 'Dst2D0Pi'
Dst2D0PiDauCuts = {'D0': '(PT>=0.*MeV)', 'pi+': 'ISLONG'}
Dst2D0PiComCuts = '(AM>0)'
Dst2D0PiMotCuts = '(M>0)'
Dst2D0PiCombination = CombineParticles(
    nameDst,
    DecayDescriptor='[D*(2010)+ -> D0 pi+]cc',
    MotherCut=Dst2D0PiMotCuts,
    DaughtersCuts=Dst2D0PiDauCuts,
    CombinationCut=Dst2D0PiComCuts)
Dst2D0Pi = Selection(
    'Sel' + nameDst,
    Algorithm=Dst2D0PiCombination,
    RequiredSelections=[D02KPi, StdAllNoPIDsPions])

# Define decay tree tuple
dtt = DecayTreeTuple('DecayTree')
dtt.setDescriptorTemplate('${dst}[(D*(2010)+ -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi+)]CC')
# dtt.Decay = 'D*(2010)+ -> ^(D0 -> ^K- ^pi+) ^pi+'
# dtt.addBranches({
#     'Dstar':  'D*(2010)+ -> (D0 -> K- pi+) pi+',
#     'D0':     'D*(2010)+ -> ^(D0 -> K- pi+) pi+',
#     'K':      'D*(2010)+ -> (D0 -> ^K- pi+) pi+',
#     'pi':     'D*(2010)+ -> (D0 -> K- ^pi+) pi+',
#     'pisoft': 'D*(2010)+ -> (D0 -> K- pi+) ^pi+'
# })
dtt.Inputs = [Dst2D0Pi.outputLocation()]

# Add tuple tools
dtt.addTupleTool('TupleToolRecoStats')

dtt.addTupleTool('TupleToolMCTruth')
dtt.TupleToolMCTruth.ToolList = [
    'MCTupleToolKinematic',
    'MCTupleToolPID',
    'MCTupleToolHierarchy'
]

# mubdt_particle = 'k'
# mubdt_particle = 'pi'
# getattr(dtt, mubdt_particle).ToolList += ['TupleToolANNPIDTraining']
dtt.k.addTupleTool('TupleToolANNPIDTraining')
# dtt.pi.addTupleTool('TupleToolANNPIDTraining')

sequenceDstD0Pi = SelectionSequence(
    'Seq' + nameDst, TopSelection=Dst2D0Pi, PostSelectionAlgs=[dtt])


from Configurables import DaVinci
DaVinci().UserAlgorithms += [sequenceDstD0Pi.sequence()]
DaVinci().InputType = 'DST'
DaVinci().PrintFreq = 10000
DaVinci().SkipEvents = 0
DaVinci().Lumi = not DaVinci().Simulation
DaVinci().EvtMax = -1

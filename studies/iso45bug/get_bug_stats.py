import os
import ROOT
from glob import glob
from tabulate import tabulate

class IsoTrack:
    # public:
    #   is_data; // just to be sure that PID stuff is set correctly
    #   id; // true ID for MC
    #   type;
    #   iso_bdt;
    #   TLorentzVector p;
    #   charge;
    #   NNk; // only useful for data
    #   NNghost; // ditto
    #   NNp;
    #   wpid; // prob of passing given PID cut for MC, not useful for data
      def __init__(self, _is_data, _id, _type, _iso_bdt, px, py, pz, e, _charge, _NNk, _NNghost, _NNp, _wpid):
        self.is_data = _is_data
        self.type = _type
        self.iso_bdt = _iso_bdt
        self.charge = _charge
        self.p = ROOT.TLorentzVector(px,py,pz,e)
        if (_is_data):
            self.id = -1
            self.NNk = _NNk
            self.NNghost = _NNghost
            self.NNp = _NNp
            self.wpid = -1.0
        else:
            self.id = _id
            self.wpid = _wpid
            self.NNk = -1.0
            self.NNghost = -1.0
            self.NNp = -1.0;

# user needs to check that if they asked for n that list is actually length n (if that's what they want)!
def GET_N_NONVELO_ISOTRACKS(n, is_data, id1, type1, iso_bdt1, px1, py1, pz1, e1,
                            charge1, NNk1, NNghost1, NNp1, wpid1, id2, type2, iso_bdt2, px2, py2, pz2, e2,
                            charge2, NNk2, NNghost2, NNp2, wpid2, id3, type3, iso_bdt3, px3, py3, pz3, e3,
                            charge3, NNk3, NNghost3, NNp3, wpid3, id4, type4, iso_bdt4, px4, py4, pz4, e4,
                            charge4, NNk4, NNghost4, NNp4, wpid4, id5, type5, iso_bdt5, px5, py5, pz5, e5,
                            charge5, NNk5, NNghost5, NNp5, wpid5):
    result = []
    assert(n>0 and n<=5)
    if (type1 != 1): result.append(IsoTrack(is_data, id1, type1, iso_bdt1, px1, py1, pz1, e1, charge1, NNk1, NNghost1, NNp1, wpid1))
    if (type2 != 1 and len(result)<n): result.append(IsoTrack(is_data, id2, type2, iso_bdt2, px2, py2, pz2, e2, charge2, NNk2, NNghost2, NNp2, wpid2))
    if (type3 != 1 and len(result)<n): result.append(IsoTrack(is_data, id3, type3, iso_bdt3, px3, py3, pz3, e3, charge3, NNk3, NNghost3, NNp3, wpid3))
    if (type4 != 1 and len(result)<n): result.append(IsoTrack(is_data, id4, type4, iso_bdt4, px4, py4, pz4, e4, charge4, NNk4, NNghost4, NNp4, wpid4))
    if (type5 != 1 and len(result)<n): result.append(IsoTrack(is_data, id5, type5, iso_bdt5, px5, py5, pz5, e5, charge5, NNk5, NNghost5, NNp5, wpid5))
    return result

def GET_N_ISOTRACKS(n, is_data, id1, type1, iso_bdt1, px1, py1, pz1, e1,
                    charge1, NNk1, NNghost1, NNp1, wpid1, id2, type2, iso_bdt2, px2, py2, pz2, e2,
                    charge2, NNk2, NNghost2, NNp2, wpid2, id3, type3, iso_bdt3, px3, py3, pz3, e3,
                    charge3, NNk3, NNghost3, NNp3, wpid3, id4, type4, iso_bdt4, px4, py4, pz4, e4,
                    charge4, NNk4, NNghost4, NNp4, wpid4, id5, type5, iso_bdt5, px5, py5, pz5, e5,
                    charge5, NNk5, NNghost5, NNp5, wpid5):
    result = []
    assert(n>0 and n<=5)
    result.append(IsoTrack(is_data, id1, type1, iso_bdt1, px1, py1, pz1, e1, charge1, NNk1, NNghost1, NNp1, wpid1))
    if (len(result)<n): result.append(IsoTrack(is_data, id2, type2, iso_bdt2, px2, py2, pz2, e2, charge2, NNk2, NNghost2, NNp2, wpid2))
    if (len(result)<n): result.append(IsoTrack(is_data, id3, type3, iso_bdt3, px3, py3, pz3, e3, charge3, NNk3, NNghost3, NNp3, wpid3))
    if (len(result)<n): result.append(IsoTrack(is_data, id4, type4, iso_bdt4, px4, py4, pz4, e4, charge4, NNk4, NNghost4, NNp4, wpid4))
    if (len(result)<n): result.append(IsoTrack(is_data, id5, type5, iso_bdt5, px5, py5, pz5, e5, charge5, NNk5, NNghost5, NNp5, wpid5))
    return result

def fISO(tracks):
    if (len(tracks)==0): return False
    return tracks[0].iso_bdt<0.15

def f1OS(tracks, d_id, is_d0):
    if (len(tracks)<2): return False
    return (tracks[0].iso_bdt>0.15) and (tracks[1].iso_bdt<0.15) and (tracks[0].type==3) and \
           (tracks[0].p.P()>5.0) and (tracks[0].p.Pt()>0.15) and tracks[0].charge*d_id*(2*is_d0-1)>0 and \
           (tracks[0].NNk<0.2) and (tracks[0].NNghost<0.2)

def f2OS(tracks):
    if (len(tracks)<3): return False
    return (tracks[0].iso_bdt>0.15) and (tracks[1].iso_bdt>0.0) and (tracks[2].iso_bdt<0.0) and \
           (tracks[0].type==3) and (tracks[1].type==3) and (tracks[0].charge+tracks[1].charge==0) and \
           (tracks[0].NNk<0.2) and (tracks[1].NNk<0.2) and (tracks[0].NNghost<0.2) and (tracks[1].NNghost<0.2)

def fDD(tracks):
    if (len(tracks)<1): return False
    pid_ok = False
    for i in range(min(2,len(tracks))):
        pid_ok = tracks[i].type==3 and tracks[i].NNk>0.2 and tracks[i].NNghost<0.2
        if (pid_ok): break
    return pid_ok and tracks[0].iso_bdt>0.15




print('In data, how often are tracks non-VELO? What about for our (VELO tracks included) 4 skims? (using non-buggy production)\n')
table = [['Decay', '1 Non-VELO', '2 Non-VELO', '3 Non-VELO', '4 Non-VELO', '5 Non-VELO',
                   'Passes ISO, 1 Non-VELO', 'Passes ISO, 2 Non-VELO', 'Passes ISO, 3 Non-VELO', 'Passes ISO, 4 Non-VELO', 'Passes ISO, 5 Non-VELO',
                   'Passes 1OS, 1 Non-VELO', 'Passes 1OS, 2 Non-VELO', 'Passes 1OS, 3 Non-VELO', 'Passes 1OS, 4 Non-VELO', 'Passes 1OS, 5 Non-VELO',
                   'Passes 2OS, 1 Non-VELO', 'Passes 2OS, 2 Non-VELO', 'Passes 2OS, 3 Non-VELO', 'Passes 2OS, 4 Non-VELO', 'Passes 2OS, 5 Non-VELO',
                   'Passes DD, 1 Non-VELO', 'Passes DD, 2 Non-VELO', 'Passes DD, 3 Non-VELO', 'Passes DD, 4 Non-VELO', 'Passes DD, 5 Non-VELO']]
recos = {'DstMu': 'TupleB0', 'D0Mu': 'TupleBminus'}
for job in glob('production/*'):
    if '.py' in job: continue # downloading script
    for reco in recos:
        name = job.split('-')[1] + '-' + reco
        if not ('std' in name.lower() or 'misid' in name.lower()): continue # harder to do this check for MC, need some postprocessing for PID
        rfs = glob(f'{job}/*/output/*.root')
        c = ROOT.TChain(f'{recos[reco]}/DecayTree', 'c')
        for rf in rfs: c.Add(rf)
        # fill histos of booleans for each category
        h1 = ROOT.TH1D('1', '1', 2, 0, 2)
        h2 = ROOT.TH1D('2', '2', 2, 0, 2)
        h3 = ROOT.TH1D('3', '3', 2, 0, 2)
        h4 = ROOT.TH1D('4', '4', 2, 0, 2)
        h5 = ROOT.TH1D('5', '5', 2, 0, 2)
        h1iso = ROOT.TH1D('1iso', '1iso', 2, 0, 2)
        h2iso = ROOT.TH1D('2iso', '2iso', 2, 0, 2)
        h3iso = ROOT.TH1D('3iso', '3iso', 2, 0, 2)
        h4iso = ROOT.TH1D('4iso', '4iso', 2, 0, 2)
        h5iso = ROOT.TH1D('5iso', '5iso', 2, 0, 2)
        h11os = ROOT.TH1D('11os', '11os', 2, 0, 2)
        h21os = ROOT.TH1D('21os', '21os', 2, 0, 2)
        h31os = ROOT.TH1D('31os', '31os', 2, 0, 2)
        h41os = ROOT.TH1D('41os', '41os', 2, 0, 2)
        h51os = ROOT.TH1D('51os', '51os', 2, 0, 2)
        h12os = ROOT.TH1D('12os', '12os', 2, 0, 2)
        h22os = ROOT.TH1D('22os', '22os', 2, 0, 2)
        h32os = ROOT.TH1D('32os', '32os', 2, 0, 2)
        h42os = ROOT.TH1D('42os', '42os', 2, 0, 2)
        h52os = ROOT.TH1D('52os', '52os', 2, 0, 2)
        h1dd = ROOT.TH1D('1dd', '1dd', 2, 0, 2)
        h2dd = ROOT.TH1D('2dd', '2dd', 2, 0, 2)
        h3dd = ROOT.TH1D('3dd', '3dd', 2, 0, 2)
        h4dd = ROOT.TH1D('4dd', '4dd', 2, 0, 2)
        h5dd = ROOT.TH1D('5dd', '5dd', 2, 0, 2)
        for entry in c:
            if reco=='DstMu':
                tracks = GET_N_ISOTRACKS(5, True, -1, c.b0_ISOLATIONNEW_Type, c.b0_ISOLATIONNEW_BDT, c.b0_ISOLATIONNEW_PX, c.b0_ISOLATIONNEW_PY, c.b0_ISOLATIONNEW_PZ,
                                                  c.b0_ISOLATIONNEW_PE, c.b0_ISOLATIONNEW_CHARGE, c.b0_ISOLATIONNEW_NNk, c.b0_ISOLATIONNEW_NNghost, c.b0_ISOLATIONNEW_NNp, -1.0,
                                                  -1, c.b0_ISOLATIONNEW_Type2, c.b0_ISOLATIONNEW_BDT2, c.b0_ISOLATIONNEW_PX2, c.b0_ISOLATIONNEW_PY2, c.b0_ISOLATIONNEW_PZ2,
                                                  c.b0_ISOLATIONNEW_PE2, c.b0_ISOLATIONNEW_CHARGE2, c.b0_ISOLATIONNEW_NNk2, c.b0_ISOLATIONNEW_NNghost2, c.b0_ISOLATIONNEW_NNp2, -1.0,
                                                  -1, c.b0_ISOLATIONNEW_Type3, c.b0_ISOLATIONNEW_BDT3, c.b0_ISOLATIONNEW_PX3, c.b0_ISOLATIONNEW_PY3, c.b0_ISOLATIONNEW_PZ3,
                                                  c.b0_ISOLATIONNEW_PE3, c.b0_ISOLATIONNEW_CHARGE3, c.b0_ISOLATIONNEW_NNk3, c.b0_ISOLATIONNEW_NNghost3, c.b0_ISOLATIONNEW_NNp3, -1.0,
                                                  -1, c.b0_ISOLATIONNEW_Type4, c.b0_ISOLATIONNEW_BDT4, c.b0_ISOLATIONNEW_PX4, c.b0_ISOLATIONNEW_PY4, c.b0_ISOLATIONNEW_PZ4,
                                                  c.b0_ISOLATIONNEW_PE4, c.b0_ISOLATIONNEW_CHARGE4, c.b0_ISOLATIONNEW_NNk4, c.b0_ISOLATIONNEW_NNghost4, c.b0_ISOLATIONNEW_NNp4, -1.0,
                                                  -1, c.b0_ISOLATIONNEW_Type5, c.b0_ISOLATIONNEW_BDT5, c.b0_ISOLATIONNEW_PX5, c.b0_ISOLATIONNEW_PY5, c.b0_ISOLATIONNEW_PZ5,
                                                  c.b0_ISOLATIONNEW_PE5, c.b0_ISOLATIONNEW_CHARGE5, c.b0_ISOLATIONNEW_NNk5, c.b0_ISOLATIONNEW_NNghost5, c.b0_ISOLATIONNEW_NNp5, -1.0)
                h1.Fill(c.b0_ISOLATIONNEW_Type != 1)
                h2.Fill(c.b0_ISOLATIONNEW_Type2 != 1)
                h3.Fill(c.b0_ISOLATIONNEW_Type3 != 1)
                h4.Fill(c.b0_ISOLATIONNEW_Type4 != 1)
                h5.Fill(c.b0_ISOLATIONNEW_Type5 != 1)
                if fISO(tracks):
                    h1iso.Fill(c.b0_ISOLATIONNEW_Type != 1)
                    h2iso.Fill(c.b0_ISOLATIONNEW_Type2 != 1)
                    h3iso.Fill(c.b0_ISOLATIONNEW_Type3 != 1)
                    h4iso.Fill(c.b0_ISOLATIONNEW_Type4 != 1)
                    h5iso.Fill(c.b0_ISOLATIONNEW_Type5 != 1)
                if f1OS(tracks, c.dst_ID, False):
                    h11os.Fill(c.b0_ISOLATIONNEW_Type != 1)
                    h21os.Fill(c.b0_ISOLATIONNEW_Type2 != 1)
                    h31os.Fill(c.b0_ISOLATIONNEW_Type3 != 1)
                    h41os.Fill(c.b0_ISOLATIONNEW_Type4 != 1)
                    h51os.Fill(c.b0_ISOLATIONNEW_Type5 != 1)
                if f2OS(tracks):
                    h12os.Fill(c.b0_ISOLATIONNEW_Type != 1)
                    h22os.Fill(c.b0_ISOLATIONNEW_Type2 != 1)
                    h32os.Fill(c.b0_ISOLATIONNEW_Type3 != 1)
                    h42os.Fill(c.b0_ISOLATIONNEW_Type4 != 1)
                    h52os.Fill(c.b0_ISOLATIONNEW_Type5 != 1)
                if fDD(tracks):
                    h1dd.Fill(c.b0_ISOLATIONNEW_Type != 1)
                    h2dd.Fill(c.b0_ISOLATIONNEW_Type2 != 1)
                    h3dd.Fill(c.b0_ISOLATIONNEW_Type3 != 1)
                    h4dd.Fill(c.b0_ISOLATIONNEW_Type4 != 1)
                    h5dd.Fill(c.b0_ISOLATIONNEW_Type5 != 1)
            else:
                tracks = GET_N_ISOTRACKS(5, True, -1, c.b_ISOLATIONNEW_Type, c.b_ISOLATIONNEW_BDT, c.b_ISOLATIONNEW_PX, c.b_ISOLATIONNEW_PY, c.b_ISOLATIONNEW_PZ,
                                                  c.b_ISOLATIONNEW_PE, c.b_ISOLATIONNEW_CHARGE, c.b_ISOLATIONNEW_NNk, c.b_ISOLATIONNEW_NNghost, c.b_ISOLATIONNEW_NNp, -1.0,
                                                  -1, c.b_ISOLATIONNEW_Type2, c.b_ISOLATIONNEW_BDT2, c.b_ISOLATIONNEW_PX2, c.b_ISOLATIONNEW_PY2, c.b_ISOLATIONNEW_PZ2,
                                                  c.b_ISOLATIONNEW_PE2, c.b_ISOLATIONNEW_CHARGE2, c.b_ISOLATIONNEW_NNk2, c.b_ISOLATIONNEW_NNghost2, c.b_ISOLATIONNEW_NNp2, -1.0,
                                                  -1, c.b_ISOLATIONNEW_Type3, c.b_ISOLATIONNEW_BDT3, c.b_ISOLATIONNEW_PX3, c.b_ISOLATIONNEW_PY3, c.b_ISOLATIONNEW_PZ3,
                                                  c.b_ISOLATIONNEW_PE3, c.b_ISOLATIONNEW_CHARGE3, c.b_ISOLATIONNEW_NNk3, c.b_ISOLATIONNEW_NNghost3, c.b_ISOLATIONNEW_NNp3, -1.0,
                                                  -1, c.b_ISOLATIONNEW_Type4, c.b_ISOLATIONNEW_BDT4, c.b_ISOLATIONNEW_PX4, c.b_ISOLATIONNEW_PY4, c.b_ISOLATIONNEW_PZ4,
                                                  c.b_ISOLATIONNEW_PE4, c.b_ISOLATIONNEW_CHARGE4, c.b_ISOLATIONNEW_NNk4, c.b_ISOLATIONNEW_NNghost4, c.b_ISOLATIONNEW_NNp4, -1.0,
                                                  -1, c.b_ISOLATIONNEW_Type5, c.b_ISOLATIONNEW_BDT5, c.b_ISOLATIONNEW_PX5, c.b_ISOLATIONNEW_PY5, c.b_ISOLATIONNEW_PZ5,
                                                  c.b_ISOLATIONNEW_PE5, c.b_ISOLATIONNEW_CHARGE5, c.b_ISOLATIONNEW_NNk5, c.b_ISOLATIONNEW_NNghost5, c.b_ISOLATIONNEW_NNp5, -1.0)
                h1.Fill(c.b_ISOLATIONNEW_Type != 1)
                h2.Fill(c.b_ISOLATIONNEW_Type2 != 1)
                h3.Fill(c.b_ISOLATIONNEW_Type3 != 1)
                h4.Fill(c.b_ISOLATIONNEW_Type4 != 1)
                h5.Fill(c.b_ISOLATIONNEW_Type5 != 1)
                if fISO(tracks):
                    h1iso.Fill(c.b_ISOLATIONNEW_Type != 1)
                    h2iso.Fill(c.b_ISOLATIONNEW_Type2 != 1)
                    h3iso.Fill(c.b_ISOLATIONNEW_Type3 != 1)
                    h4iso.Fill(c.b_ISOLATIONNEW_Type4 != 1)
                    h5iso.Fill(c.b_ISOLATIONNEW_Type5 != 1)
                if f1OS(tracks, c.d0_ID, True):
                    h11os.Fill(c.b_ISOLATIONNEW_Type != 1)
                    h21os.Fill(c.b_ISOLATIONNEW_Type2 != 1)
                    h31os.Fill(c.b_ISOLATIONNEW_Type3 != 1)
                    h41os.Fill(c.b_ISOLATIONNEW_Type4 != 1)
                    h51os.Fill(c.b_ISOLATIONNEW_Type5 != 1)
                if f2OS(tracks):
                    h12os.Fill(c.b_ISOLATIONNEW_Type != 1)
                    h22os.Fill(c.b_ISOLATIONNEW_Type2 != 1)
                    h32os.Fill(c.b_ISOLATIONNEW_Type3 != 1)
                    h42os.Fill(c.b_ISOLATIONNEW_Type4 != 1)
                    h52os.Fill(c.b_ISOLATIONNEW_Type5 != 1)
                if fDD(tracks):
                    h1dd.Fill(c.b_ISOLATIONNEW_Type != 1)
                    h2dd.Fill(c.b_ISOLATIONNEW_Type2 != 1)
                    h3dd.Fill(c.b_ISOLATIONNEW_Type3 != 1)
                    h4dd.Fill(c.b_ISOLATIONNEW_Type4 != 1)
                    h5dd.Fill(c.b_ISOLATIONNEW_Type5 != 1)
        table.append([name, f'{round(h1.GetMean(),5)} +/- {round(h1.GetMeanError(),5)}',
                            f'{round(h2.GetMean(),5)} +/- {round(h2.GetMeanError(),5)}',
                            f'{round(h3.GetMean(),5)} +/- {round(h3.GetMeanError(),5)}',
                            f'{round(h4.GetMean(),5)} +/- {round(h4.GetMeanError(),5)}',
                            f'{round(h5.GetMean(),5)} +/- {round(h5.GetMeanError(),5)}',
                            f'{round(h1iso.GetMean(),5)} +/- {round(h1iso.GetMeanError(),5)}',
                            f'{round(h2iso.GetMean(),5)} +/- {round(h2iso.GetMeanError(),5)}',
                            f'{round(h3iso.GetMean(),5)} +/- {round(h3iso.GetMeanError(),5)}',
                            f'{round(h4iso.GetMean(),5)} +/- {round(h4iso.GetMeanError(),5)}',
                            f'{round(h5iso.GetMean(),5)} +/- {round(h5iso.GetMeanError(),5)}',
                            f'{round(h11os.GetMean(),5)} +/- {round(h11os.GetMeanError(),5)}',
                            f'{round(h21os.GetMean(),5)} +/- {round(h21os.GetMeanError(),5)}',
                            f'{round(h31os.GetMean(),5)} +/- {round(h31os.GetMeanError(),5)}',
                            f'{round(h41os.GetMean(),5)} +/- {round(h41os.GetMeanError(),5)}',
                            f'{round(h51os.GetMean(),5)} +/- {round(h51os.GetMeanError(),5)}',
                            f'{round(h12os.GetMean(),5)} +/- {round(h12os.GetMeanError(),5)}',
                            f'{round(h22os.GetMean(),5)} +/- {round(h22os.GetMeanError(),5)}',
                            f'{round(h32os.GetMean(),5)} +/- {round(h32os.GetMeanError(),5)}',
                            f'{round(h42os.GetMean(),5)} +/- {round(h42os.GetMeanError(),5)}',
                            f'{round(h52os.GetMean(),5)} +/- {round(h52os.GetMeanError(),5)}',
                            f'{round(h1dd.GetMean(),5)} +/- {round(h1dd.GetMeanError(),5)}',
                            f'{round(h2dd.GetMean(),5)} +/- {round(h2dd.GetMeanError(),5)}',
                            f'{round(h3dd.GetMean(),5)} +/- {round(h3dd.GetMeanError(),5)}',
                            f'{round(h4dd.GetMean(),5)} +/- {round(h4dd.GetMeanError(),5)}',
                            f'{round(h5dd.GetMean(),5)} +/- {round(h5dd.GetMeanError(),5)}'])
print(tabulate(table, tablefmt='github'))




print('In data, how often do we rely on 4th/5th DD tracks if we require tracks satisfying skim requirements to be non-VELO? (using non-buggy production)\n')

table = [['Decay', 'Passes ISO, uses 4', 'Passes ISO, uses 5', 
                   'Passes 1OS, uses 4 not 5', 'Passes 1OS, uses 4 and 5', 'Passes 1OS, uses 5 not 4', 'Passes 1OS, uses 4 or 5', 
                   'Passes 2OS, uses 4 not 5', 'Passes 2OS, uses 4 and 5', 'Passes 2OS, uses 5 not 4', 'Passes 2OS, uses 4 or 5',
                   'Passes DD, uses 4', 'Passes DD, uses 5']]
for job in glob('production/*'):
    if '.py' in job: continue # downloading script
    for reco in recos:
        name = job.split('-')[1] + '-' + reco
        if not ('std' in name.lower() or 'misid' in name.lower()): continue # harder to do this check for MC, need some postprocessing for PID
        rfs = glob(f'{job}/*/output/*.root')
        c = ROOT.TChain(f'{recos[reco]}/DecayTree', 'c')
        for rf in rfs: c.Add(rf)
        # fill histos of booleans for each category
        hiso4 = ROOT.TH1D('iso4', 'iso4', 2, 0, 2)
        hiso5 = ROOT.TH1D('iso5', 'iso5', 2, 0, 2)
        h1os4n5 = ROOT.TH1D('1os4n5', '1os4n5', 2, 0, 2)
        h1os4p5 = ROOT.TH1D('1os4p5', '1os4p5', 2, 0, 2)
        h1os5n4 = ROOT.TH1D('1os5n4', '1os5n4', 2, 0, 2)
        h1os4o5 = ROOT.TH1D('1os4o5', '1os4o5', 2, 0, 2)
        h2os4n5 = ROOT.TH1D('2os4n5', '2os4n5', 2, 0, 2)
        h2os4p5 = ROOT.TH1D('2os4p5', '2os4p5', 2, 0, 2)
        h2os5n4 = ROOT.TH1D('2os5n4', '2os5n4', 2, 0, 2)
        h2os4o5 = ROOT.TH1D('2os4o5', '2os4o5', 2, 0, 2)
        hdd4 = ROOT.TH1D('dd4', 'dd4', 2, 0, 2)
        hdd5 = ROOT.TH1D('dd5', 'dd5', 2, 0, 2)
        for entry in c:
            if reco=='DstMu':
                nonvelo = GET_N_NONVELO_ISOTRACKS(5, True, -1, c.b0_ISOLATIONNEW_Type, c.b0_ISOLATIONNEW_BDT, c.b0_ISOLATIONNEW_PX, c.b0_ISOLATIONNEW_PY, c.b0_ISOLATIONNEW_PZ,
                                                            c.b0_ISOLATIONNEW_PE, c.b0_ISOLATIONNEW_CHARGE, c.b0_ISOLATIONNEW_NNk, c.b0_ISOLATIONNEW_NNghost, c.b0_ISOLATIONNEW_NNp, -1.0,
                                                            -1, c.b0_ISOLATIONNEW_Type2, c.b0_ISOLATIONNEW_BDT2, c.b0_ISOLATIONNEW_PX2, c.b0_ISOLATIONNEW_PY2, c.b0_ISOLATIONNEW_PZ2,
                                                            c.b0_ISOLATIONNEW_PE2, c.b0_ISOLATIONNEW_CHARGE2, c.b0_ISOLATIONNEW_NNk2, c.b0_ISOLATIONNEW_NNghost2, c.b0_ISOLATIONNEW_NNp2, -1.0,
                                                            -1, c.b0_ISOLATIONNEW_Type3, c.b0_ISOLATIONNEW_BDT3, c.b0_ISOLATIONNEW_PX3, c.b0_ISOLATIONNEW_PY3, c.b0_ISOLATIONNEW_PZ3,
                                                            c.b0_ISOLATIONNEW_PE3, c.b0_ISOLATIONNEW_CHARGE3, c.b0_ISOLATIONNEW_NNk3, c.b0_ISOLATIONNEW_NNghost3, c.b0_ISOLATIONNEW_NNp3, -1.0,
                                                            -1, c.b0_ISOLATIONNEW_Type4, c.b0_ISOLATIONNEW_BDT4, c.b0_ISOLATIONNEW_PX4, c.b0_ISOLATIONNEW_PY4, c.b0_ISOLATIONNEW_PZ4,
                                                            c.b0_ISOLATIONNEW_PE4, c.b0_ISOLATIONNEW_CHARGE4, c.b0_ISOLATIONNEW_NNk4, c.b0_ISOLATIONNEW_NNghost4, c.b0_ISOLATIONNEW_NNp4, -1.0,
                                                            -1, c.b0_ISOLATIONNEW_Type5, c.b0_ISOLATIONNEW_BDT5, c.b0_ISOLATIONNEW_PX5, c.b0_ISOLATIONNEW_PY5, c.b0_ISOLATIONNEW_PZ5,
                                                            c.b0_ISOLATIONNEW_PE5, c.b0_ISOLATIONNEW_CHARGE5, c.b0_ISOLATIONNEW_NNk5, c.b0_ISOLATIONNEW_NNghost5, c.b0_ISOLATIONNEW_NNp5, -1.0)
                if fISO(nonvelo):
                    used_bdt = round(nonvelo[0].iso_bdt,5)
                    if used_bdt > -1.5: # don't count the cases with all BDT scores at -2 (not that I think there are any...)
                        hiso4.Fill(used_bdt==round(c.b0_ISOLATIONNEW_BDT4,5))
                        hiso5.Fill(used_bdt==round(c.b0_ISOLATIONNEW_BDT5,5))
                if f1OS(nonvelo, c.dst_ID, False):
                    used_bdts = [round(tr.iso_bdt,5) for tr in nonvelo][:2]
                    if used_bdts[0] > -1.5 and used_bdts[1] > -1.5: # don't count the cases with BDT scores at -2
                        h1os4n5.Fill((round(c.b0_ISOLATIONNEW_BDT4,5) in used_bdts) and not (round(c.b0_ISOLATIONNEW_BDT5,5) in used_bdts))
                        h1os4p5.Fill((round(c.b0_ISOLATIONNEW_BDT4,5) in used_bdts) and (round(c.b0_ISOLATIONNEW_BDT5,5) in used_bdts))
                        h1os5n4.Fill((round(c.b0_ISOLATIONNEW_BDT5,5) in used_bdts) and not (round(c.b0_ISOLATIONNEW_BDT4,5) in used_bdts))
                        h1os4o5.Fill((round(c.b0_ISOLATIONNEW_BDT4,5) in used_bdts) or (round(c.b0_ISOLATIONNEW_BDT5,5) in used_bdts))
                if f2OS(nonvelo):
                    used_bdts = [round(tr.iso_bdt,5) for tr in nonvelo][:3]
                    if used_bdts[0] > -1.5 and used_bdts[1] > -1.5 and used_bdts[2] > -1.5: # don't count the cases with BDT scores at -2
                        h2os4n5.Fill((round(c.b0_ISOLATIONNEW_BDT4,5) in used_bdts) and not (round(c.b0_ISOLATIONNEW_BDT5,5) in used_bdts))
                        h2os4p5.Fill((round(c.b0_ISOLATIONNEW_BDT4,5) in used_bdts) and (round(c.b0_ISOLATIONNEW_BDT5,5) in used_bdts))
                        h2os5n4.Fill((round(c.b0_ISOLATIONNEW_BDT5,5) in used_bdts) and not (round(c.b0_ISOLATIONNEW_BDT4,5) in used_bdts))
                        h2os4o5.Fill((round(c.b0_ISOLATIONNEW_BDT4,5) in used_bdts) or (round(c.b0_ISOLATIONNEW_BDT5,5) in used_bdts))
                if fDD(nonvelo):
                    used_bdt = round(nonvelo[0].iso_bdt,5)
                    if used_bdt > -1.5: # don't count the cases with all BDT scores at -2 (not that I think there are any...)
                        hdd4.Fill(used_bdt==round(c.b0_ISOLATIONNEW_BDT4,5))
                        hdd5.Fill(used_bdt==round(c.b0_ISOLATIONNEW_BDT5,5))
            else:
                nonvelo = GET_N_NONVELO_ISOTRACKS(5, True, -1, c.b_ISOLATIONNEW_Type, c.b_ISOLATIONNEW_BDT, c.b_ISOLATIONNEW_PX, c.b_ISOLATIONNEW_PY, c.b_ISOLATIONNEW_PZ,
                                                            c.b_ISOLATIONNEW_PE, c.b_ISOLATIONNEW_CHARGE, c.b_ISOLATIONNEW_NNk, c.b_ISOLATIONNEW_NNghost, c.b_ISOLATIONNEW_NNp, -1.0,
                                                            -1, c.b_ISOLATIONNEW_Type2, c.b_ISOLATIONNEW_BDT2, c.b_ISOLATIONNEW_PX2, c.b_ISOLATIONNEW_PY2, c.b_ISOLATIONNEW_PZ2,
                                                            c.b_ISOLATIONNEW_PE2, c.b_ISOLATIONNEW_CHARGE2, c.b_ISOLATIONNEW_NNk2, c.b_ISOLATIONNEW_NNghost2, c.b_ISOLATIONNEW_NNp2, -1.0,
                                                            -1, c.b_ISOLATIONNEW_Type3, c.b_ISOLATIONNEW_BDT3, c.b_ISOLATIONNEW_PX3, c.b_ISOLATIONNEW_PY3, c.b_ISOLATIONNEW_PZ3,
                                                            c.b_ISOLATIONNEW_PE3, c.b_ISOLATIONNEW_CHARGE3, c.b_ISOLATIONNEW_NNk3, c.b_ISOLATIONNEW_NNghost3, c.b_ISOLATIONNEW_NNp3, -1.0,
                                                            -1, c.b_ISOLATIONNEW_Type4, c.b_ISOLATIONNEW_BDT4, c.b_ISOLATIONNEW_PX4, c.b_ISOLATIONNEW_PY4, c.b_ISOLATIONNEW_PZ4,
                                                            c.b_ISOLATIONNEW_PE4, c.b_ISOLATIONNEW_CHARGE4, c.b_ISOLATIONNEW_NNk4, c.b_ISOLATIONNEW_NNghost4, c.b_ISOLATIONNEW_NNp4, -1.0,
                                                            -1, c.b_ISOLATIONNEW_Type5, c.b_ISOLATIONNEW_BDT5, c.b_ISOLATIONNEW_PX5, c.b_ISOLATIONNEW_PY5, c.b_ISOLATIONNEW_PZ5,
                                                            c.b_ISOLATIONNEW_PE5, c.b_ISOLATIONNEW_CHARGE5, c.b_ISOLATIONNEW_NNk5, c.b_ISOLATIONNEW_NNghost5, c.b_ISOLATIONNEW_NNp5, -1.0)
                if fISO(nonvelo):
                    used_bdt = round(nonvelo[0].iso_bdt,5)
                    if used_bdt > -1.5: # don't count the cases with all BDT scores at -2 (not that I think there are any...)
                        hiso4.Fill(used_bdt==round(c.b_ISOLATIONNEW_BDT4,5))
                        hiso5.Fill(used_bdt==round(c.b_ISOLATIONNEW_BDT5,5))
                if f1OS(nonvelo, c.d0_ID, True):
                    used_bdts = [round(tr.iso_bdt,5) for tr in nonvelo][:2]
                    if used_bdts[0] > -1.5 and used_bdts[1] > -1.5: # don't count the cases with BDT scores at -2
                        h1os4n5.Fill((round(c.b_ISOLATIONNEW_BDT4,5) in used_bdts) and not (round(c.b_ISOLATIONNEW_BDT5,5) in used_bdts))
                        h1os4p5.Fill((round(c.b_ISOLATIONNEW_BDT4,5) in used_bdts) and (round(c.b_ISOLATIONNEW_BDT5,5) in used_bdts))
                        h1os5n4.Fill((round(c.b_ISOLATIONNEW_BDT5,5) in used_bdts) and not (round(c.b_ISOLATIONNEW_BDT4,5) in used_bdts))
                        h1os4o5.Fill((round(c.b_ISOLATIONNEW_BDT4,5) in used_bdts) or (round(c.b_ISOLATIONNEW_BDT5,5) in used_bdts))
                if f2OS(nonvelo):
                    used_bdts = [round(tr.iso_bdt,5) for tr in nonvelo][:3]
                    if used_bdts[0] > -1.5 and used_bdts[1] > -1.5 and used_bdts[2] > -1.5: # don't count the cases with BDT scores at -2
                        h2os4n5.Fill((round(c.b_ISOLATIONNEW_BDT4,5) in used_bdts) and not (round(c.b_ISOLATIONNEW_BDT5,5) in used_bdts))
                        h2os4p5.Fill((round(c.b_ISOLATIONNEW_BDT4,5) in used_bdts) and (round(c.b_ISOLATIONNEW_BDT5,5) in used_bdts))
                        h2os5n4.Fill((round(c.b_ISOLATIONNEW_BDT5,5) in used_bdts) and not (round(c.b_ISOLATIONNEW_BDT4,5) in used_bdts))
                        h2os4o5.Fill((round(c.b_ISOLATIONNEW_BDT4,5) in used_bdts) or (round(c.b_ISOLATIONNEW_BDT5,5) in used_bdts))
                if fDD(nonvelo):
                    used_bdt = round(nonvelo[0].iso_bdt,5)
                    if used_bdt > -1.5: # don't count the cases with all BDT scores at -2 (not that I think there are any...)
                        hdd4.Fill(used_bdt==round(c.b_ISOLATIONNEW_BDT4,5))
                        hdd5.Fill(used_bdt==round(c.b_ISOLATIONNEW_BDT5,5))
        table.append([name, f'{round(hiso4.GetMean(),5)} +/- {round(hiso4.GetMeanError(),5)}',
                            f'{round(hiso5.GetMean(),5)} +/- {round(hiso5.GetMeanError(),5)}',
                            f'{round(h1os4n5.GetMean(),5)} +/- {round(h1os4n5.GetMeanError(),5)}',
                            f'{round(h1os4p5.GetMean(),5)} +/- {round(h1os4p5.GetMeanError(),5)}',
                            f'{round(h1os5n4.GetMean(),5)} +/- {round(h1os5n4.GetMeanError(),5)}',
                            f'{round(h1os4o5.GetMean(),5)} +/- {round(h1os4o5.GetMeanError(),5)}',
                            f'{round(h2os4n5.GetMean(),5)} +/- {round(h2os4n5.GetMeanError(),5)}',
                            f'{round(h2os4p5.GetMean(),5)} +/- {round(h2os4p5.GetMeanError(),5)}',
                            f'{round(h2os5n4.GetMean(),5)} +/- {round(h2os5n4.GetMeanError(),5)}',
                            f'{round(h2os4o5.GetMean(),5)} +/- {round(h2os4o5.GetMeanError(),5)}',
                            f'{round(hdd4.GetMean(),5)} +/- {round(hdd4.GetMeanError(),5)}',
                            f'{round(hdd5.GetMean(),5)} +/- {round(hdd5.GetMeanError(),5)}'])
print(tabulate(table, tablefmt='github'))





print('\n\nAnd, with the buggy production, how often do we miss what should have been counted as the 4th/5th iso tracks? (track type not considered, and mostly considering cases where 4th/5th iso tracks are allowed to be reordered ad-hoc)\n')

def equal(iso1, iso2):
    return iso1[0]==iso2[0] and iso1[1]==iso2[1] and iso1[2]==iso2[2]

table = [['Decay', 'Correct 4, Correct 5 (given order)', 'Correct 4, Correct 5 (poss. reorder)', 'Correct 4, Wrong 5 (poss. reorder)',
          'Correct 4 (poss. reorder)', 'Correct 4, actual track (poss. reorder)', 'Wrong 4, Correct 5 (poss. reorder)', 'Wrong 4, Wrong 5 (poss. reorder)']]
for job in glob('production/*'):
    if '.py' in job: continue # downloading script
    for reco in recos:
        name = f"{job.split('-')[1]}-{reco}"
        rfs = glob(f'{job}/*/output/*.root')
        c = ROOT.TChain(f'{recos[reco]}/DecayTree', 'c')
        for rf in rfs: c.Add(rf)
        # fill histos of booleans for each category
        c4c5o = ROOT.TH1D('c4c5o', 'c4c5o', 2, 0, 2)
        c4c5 = ROOT.TH1D('c4c5', 'c4c5', 2, 0, 2)
        c4w5 = ROOT.TH1D('c4w5', 'c4w5', 2, 0, 2)
        c4 = ROOT.TH1D('c4', 'c4', 2, 0, 2)
        c4real = ROOT.TH1D('c4real', 'c4real', 2, 0, 2)
        w4c5 = ROOT.TH1D('w4c5', 'w4c5', 2, 0, 2)
        w4w5 = ROOT.TH1D('w4w5', 'w4w5', 2, 0, 2)
        for entry in c:
            if reco=='DstMu':
                iso4right = (round(c.b0_ISOLATIONNEW_BDT4,5), c.b0_ISOLATIONNEW_Type4, round(c.b0_ISOLATIONNEW_PX4,5))
                iso5right = (round(c.b0_ISOLATIONNEW_BDT5,5), c.b0_ISOLATIONNEW_Type5, round(c.b0_ISOLATIONNEW_PX5,5))
                iso4bug = (round(c.b0_ISOLATION_BDT4,5), c.b0_ISOLATION_Type4, round(c.b0_ISOLATION_PX4,5))
                iso5bug = (round(c.b0_ISOLATION_BDT5,5), c.b0_ISOLATION_Type5, round(c.b0_ISOLATION_PX5,5))
                iso4bugah, iso5bugah = iso4bug, iso5bug
                if iso5bug[0] > iso4bug[0]: iso4bugah, iso5bugah = iso5bug, iso4bug # this is easy to do ad-hoc, so check if this is enough to fix
                c4c5o.Fill(equal(iso4right, iso4bug) and equal(iso5right, iso5bug))
                c4c5.Fill(equal(iso4right, iso4bugah) and equal(iso5right, iso5bugah))
                c4w5.Fill(equal(iso4right, iso4bugah) and not equal(iso5right, iso5bugah))
                c4.Fill(equal(iso4right, iso4bugah))
                if iso4right[0] >= -1.5: c4real.Fill(equal(iso4right, iso4bugah)) # -2 if no 4th iso track
                w4c5.Fill(not equal(iso4right, iso4bugah) and equal(iso5right, iso5bugah))
                w4w5.Fill(not equal(iso4right, iso4bugah) and not equal(iso5right, iso5bugah))
            else:
                iso4right = (round(c.b_ISOLATIONNEW_BDT4,5), c.b_ISOLATIONNEW_Type4, round(c.b_ISOLATIONNEW_PX4,5))
                iso5right = (round(c.b_ISOLATIONNEW_BDT5,5), c.b_ISOLATIONNEW_Type5, round(c.b_ISOLATIONNEW_PX5,5))
                iso4bug = (round(c.b_ISOLATION_BDT4,5), c.b_ISOLATION_Type4, round(c.b_ISOLATION_PX4,5))
                iso5bug = (round(c.b_ISOLATION_BDT5,5), c.b_ISOLATION_Type5, round(c.b_ISOLATION_PX5,5))
                iso4bugah, iso5bugah = iso4bug, iso5bug
                if iso5bug[0] > iso4bug[0]: iso4bugah, iso5bugah = iso5bug, iso4bug # this is easy to do ad-hoc, so check if this is enough to fix
                c4c5o.Fill(equal(iso4right, iso4bug) and equal(iso5right, iso5bug))
                c4c5.Fill(equal(iso4right, iso4bugah) and equal(iso5right, iso5bugah))
                c4w5.Fill(equal(iso4right, iso4bugah) and not equal(iso5right, iso5bugah))
                c4.Fill(equal(iso4right, iso4bugah))
                if iso4right[0] >= -1.5: c4real.Fill(equal(iso4right, iso4bugah)) # -2 if no 4th iso track
                w4c5.Fill(not equal(iso4right, iso4bugah) and equal(iso5right, iso5bugah))
                w4w5.Fill(not equal(iso4right, iso4bugah) and not equal(iso5right, iso5bugah))
        table.append([name, f'{round(c4c5o.GetMean(),5)} +/- {round(c4c5o.GetMeanError(),5)}',
                            f'{round(c4c5.GetMean(),5)} +/- {round(c4c5.GetMeanError(),5)}',
                            f'{round(c4w5.GetMean(),5)} +/- {round(c4w5.GetMeanError(),5)}',
                            f'{round(c4.GetMean(),5)} +/- {round(c4.GetMeanError(),5)}',
                            f'{round(c4real.GetMean(),5)} +/- {round(c4real.GetMeanError(),5)}',
                            f'{round(w4c5.GetMean(),5)} +/- {round(w4c5.GetMeanError(),5)}',
                            f'{round(w4w5.GetMean(),5)} +/- {round(w4w5.GetMeanError(),5)}'])

print(tabulate(table, tablefmt='github'))
// Author: Alex Fernez

#pragma once

#include <assert.h>
#include <TLorentzVector.h>

using namespace std;

class IsoTrack {
    public:
      bool is_data; // just to be sure that PID stuff is set correctly
      int id; // true ID for MC
      int type;
      double iso_bdt;
      TLorentzVector p;
      int charge;
      double NNk; // only useful for data
      double NNghost; // ditto
      double NNp;
      double wpid; // prob of passing given PID cut for MC, not useful for data

      IsoTrack(bool _is_data, int _id, int _type, double _iso_bdt, double px, double py, double pz, double e, 
               int _charge, double _NNk, double _NNghost, double _NNp, double _wpid) {
        is_data=_is_data; type=_type; iso_bdt=_iso_bdt; charge=_charge;
        p = TLorentzVector(px,py,pz,e);
        if (_is_data) {
            id=-1;
            NNk=_NNk; NNghost=_NNghost; NNp=_NNp;
            wpid=-1.0;
        } else {
            id=_id;
            wpid=_wpid;
            NNk=-1.0; NNghost=-1.0; NNp=-1.0;
        }
      }
};

vector<IsoTrack> GET_N_ISOTRACKS(int n, bool is_data, 
        int id1, int type1, double iso_bdt1, double px1, double py1, double pz1, double e1,
        int charge1, double NNk1, double NNghost1, double NNp1, double wpid1,
        int id2, int type2, double iso_bdt2, double px2, double py2, double pz2, double e2,
        int charge2, double NNk2, double NNghost2, double NNp2, double wpid2,
        int id3, int type3, double iso_bdt3, double px3, double py3, double pz3, double e3,
        int charge3, double NNk3, double NNghost3, double NNp3, double wpid3,
        int id4, int type4, double iso_bdt4, double px4, double py4, double pz4, double e4,
        int charge4, double NNk4, double NNghost4, double NNp4, double wpid4,
        int id5, int type5, double iso_bdt5, double px5, double py5, double pz5, double e5,
        int charge5, double NNk5, double NNghost5, double NNp5, double wpid5) {
    vector<IsoTrack> result;
    assert(n>0 && n<=5);
    result.push_back(IsoTrack(is_data, id1, type1, iso_bdt1, px1, py1, pz1, e1, charge1, NNk1, NNghost1, NNp1, wpid1));
    if (result.size()<n) result.push_back(IsoTrack(is_data, id2, type2, iso_bdt2, px2, py2, pz2, e2, charge2, NNk2, NNghost2, NNp2, wpid2));
    if (result.size()<n) result.push_back(IsoTrack(is_data, id3, type3, iso_bdt3, px3, py3, pz3, e3, charge3, NNk3, NNghost3, NNp3, wpid3));
    if (result.size()<n) result.push_back(IsoTrack(is_data, id4, type4, iso_bdt4, px4, py4, pz4, e4, charge4, NNk4, NNghost4, NNp4, wpid4));
    if (result.size()<n) result.push_back(IsoTrack(is_data, id5, type5, iso_bdt5, px5, py5, pz5, e5, charge5, NNk5, NNghost5, NNp5, wpid5));
    return result;
}

// user needs to check that if they asked for n that list is actually length n (if that's what they want)!
vector<IsoTrack> GET_N_NONVELO_ISOTRACKS(int n, bool is_data, 
        int id1, int type1, double iso_bdt1, double px1, double py1, double pz1, double e1,
        int charge1, double NNk1, double NNghost1, double NNp1, double wpid1,
        int id2, int type2, double iso_bdt2, double px2, double py2, double pz2, double e2,
        int charge2, double NNk2, double NNghost2, double NNp2, double wpid2,
        int id3, int type3, double iso_bdt3, double px3, double py3, double pz3, double e3,
        int charge3, double NNk3, double NNghost3, double NNp3, double wpid3,
        int id4, int type4, double iso_bdt4, double px4, double py4, double pz4, double e4,
        int charge4, double NNk4, double NNghost4, double NNp4, double wpid4,
        int id5, int type5, double iso_bdt5, double px5, double py5, double pz5, double e5,
        int charge5, double NNk5, double NNghost5, double NNp5, double wpid5) {
    vector<IsoTrack> result;
    assert(n>0 && n<=5);
    if (type1 != 1) result.push_back(IsoTrack(is_data, id1, type1, iso_bdt1, px1, py1, pz1, e1, charge1, NNk1, NNghost1, NNp1, wpid1));
    if (type2 != 1 && result.size()<n) result.push_back(IsoTrack(is_data, id2, type2, iso_bdt2, px2, py2, pz2, e2, charge2, NNk2, NNghost2, NNp2, wpid2));
    if (type3 != 1 && result.size()<n) result.push_back(IsoTrack(is_data, id3, type3, iso_bdt3, px3, py3, pz3, e3, charge3, NNk3, NNghost3, NNp3, wpid3));
    if (type4 != 1 && result.size()<n) result.push_back(IsoTrack(is_data, id4, type4, iso_bdt4, px4, py4, pz4, e4, charge4, NNk4, NNghost4, NNp4, wpid4));
    if (type5 != 1 && result.size()<n) result.push_back(IsoTrack(is_data, id5, type5, iso_bdt5, px5, py5, pz5, e5, charge5, NNk5, NNghost5, NNp5, wpid5));
    // if (result.size()<n) { // if went through all 5 stored iso tracks and couldn't find n non-VELO, return an empty list so user doesn't abuse function
    //     vector<IsoTrack> zero;
    //     return zero;
    // }
    return result;
}
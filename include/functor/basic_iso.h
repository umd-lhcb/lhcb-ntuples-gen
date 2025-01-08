// Author: Alex Fernez

#pragma once

using namespace std;

class IsoTrack {
    public:
      Int_t type;
      Double_t iso_bdt;
      Int_t charge;
      Double_t NNk; // either the value of NNk for data or -1 for MC
      Double_t NNghost; // ditto
      Double_t w_pid; // prob of passing given PID cut for MC or -1 for data

      IsoTrack(Int_t _type, Double_t _iso_bdt, Int_t _charge, Double_t _NNk, Double_t _NNghost) {
        type=_type; iso_bdt=_iso_bdt; charge=_charge; NNk=_NNk; NNghost=_NNghost; w_pid=-1.0;
      }
      IsoTrack(Int_t _type, Double_t _iso_bdt, Int_t _charge, Double_t _w_pid) {
        type=_type; iso_bdt=_iso_bdt; charge=_charge; NNk=-1.0; NNghost=-1.0; w_pid=_w_pid;
      }
};

vector<IsoTrack> GET_FIRST_N_NONVELO_ISOTRACKS(vector<IsoTrack>& tracks, int n) {
    vector<IsoTrack> result;
    int start=0;
    while (result.size()<n && start<n) {
        for (int i=start; i<tracks.size(); i++) {
            if (tracks[i].type != 1) {
                result.push_back(tracks[i]);
                start = i;
                break;
            }
        }
        start++;
    }
    if (result.size()<n) { // don't trust user to do this check themselves
        vector<IsoTrack> nullresult;
        return nullresult;
    }
    return result;
}
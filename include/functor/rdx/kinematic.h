// Author: Yipeng Sun, Svende Braun
// License: BSD 2-clause
// Last Change: Tue Mar 07, 2023 at 04:39 PM -0500

#pragma once

#include <vector>

#include <Math/Vector3D.h>
#include <Math/Vector4D.h>
#include <Math/VectorUtil.h>
#include <TFile.h>
#include <TH1D.h>
#include <TMath.h>
#include <TROOT.h>
#include <TLorentzVector.h>
#include <TRandom.h>

#include "functor/basic.h"
#include "functor/basic_iso.h"
#include "functor/basic_kinematic.h"

using std::vector;

using ROOT::Math::LorentzVector;
using ROOT::Math::PtEtaPhiMVector;
using ROOT::Math::PxPyPzEVector;

using ROOT::Math::DisplacementVector3D;
using ROOT::Math::XYZVector;

// Helpers /////////////////////////////////////////////////////////////////////

Double_t MINV(Double_t pi_px, Double_t pi_py, Double_t pi_pz, Double_t pi_pe,
              Double_t dst_px, Double_t dst_py, Double_t dst_pz,
              Double_t dst_pe) {
  auto v4_pi     = ROOT::Math::PxPyPzEVector(pi_px, pi_py, pi_pz, pi_pe);
  auto v4_dst    = ROOT::Math::PxPyPzEVector(dst_px, dst_py, dst_pz, dst_pe);
  auto v4_dst_pi = v4_pi + v4_dst;
  auto dst_iso_m = v4_dst_pi.M();
  return dst_iso_m;
}

Double_t MINV2(Double_t pi_px, Double_t pi_py, Double_t pi_pz, Double_t pi_pe,
               Double_t dst_px, Double_t dst_py, Double_t dst_pz,
               Double_t dst_pe) {
  auto dst_iso_m =
      MINV(pi_px, pi_py, pi_pz, pi_pe, dst_px, dst_py, dst_pz, dst_pe);
  return dst_iso_m * dst_iso_m;
}

Double_t ISO_DELTAM(Double_t pi_px, Double_t pi_py, Double_t pi_pz,
                    Double_t pi_pe, Double_t dst_px, Double_t dst_py,
                    Double_t dst_pz, Double_t dst_pe, Double_t dst_m) {
  auto v4_pi     = ROOT::Math::PxPyPzEVector(pi_px, pi_py, pi_pz, pi_pe);
  auto v4_dst    = ROOT::Math::PxPyPzEVector(dst_px, dst_py, dst_pz, dst_pe);
  auto v4_dst_pi = v4_pi + v4_dst;
  auto dst_iso_m = v4_dst_pi.M();
  return dst_iso_m - dst_m;
}

// Kinematics //////////////////////////////////////////////////////////////////

Double_t FD_TRANS(Double_t endvtx_x, Double_t ownpv_x, Double_t endvtx_y,
                  Double_t ownpv_y) {
  auto x = endvtx_x - ownpv_x;
  auto y = endvtx_y - ownpv_y;
  return TMath::Sqrt(x * x + y * y);
}

// For differentiating K*/K
Double_t MX_MASS(Double_t b_px, Double_t b_py, Double_t b_pz, Double_t b_pe,
                 Double_t d0_px, Double_t d0_py, Double_t d0_pz, Double_t d0_pe,
                 Double_t d1_px, Double_t d1_py, Double_t d1_pz,
                 Double_t d1_pe) {
  auto TBp  = PxPyPzEVector(b_px, b_py, b_pz, b_pe);
  auto TD0p = PxPyPzEVector(d0_px, d0_py, d0_pz, d0_pe);
  auto TD1p = PxPyPzEVector(d1_px, d1_py, d1_pz, d1_pe);
  return (TBp - TD0p - TD1p).M();
}

// Rest frame approximation ////////////////////////////////////////////////////

template <typename T>
PxPyPzEVector B_P_EST(Double_t b_pz, Double_t b_m,
                      DisplacementVector3D<T>& v3_b_flight) {
  const Double_t b_m_ref = 5279.61;

  auto cos_x = v3_b_flight.Unit().X();
  auto cos_y = v3_b_flight.Unit().Y();
  auto cos_z = v3_b_flight.Unit().Z();

  Double_t b_p_mag = (b_m_ref / b_m) * b_pz / cos_z;
  return PxPyPzEVector(b_p_mag * cos_x, b_p_mag * cos_y, b_p_mag * cos_z,
                       TMath::Sqrt(b_p_mag * b_p_mag + b_m_ref * b_m_ref));
}

template <typename T>
Double_t MMISS(LorentzVector<T> v4_b, LorentzVector<T> v4_dmu) {
  auto v4_diff = v4_b - v4_dmu;
  return M2(v4_diff);
}

template <typename T>
Double_t EL(LorentzVector<T> v4_mu, LorentzVector<T> v4_b) {
  auto v3_boost     = v4_b.BoostToCM();
  auto v4_mu_b_rest = ROOT::Math::VectorUtil::boost(v4_mu, v3_boost);
  return v4_mu_b_rest.E();
}

template <typename T>
Double_t Q2(LorentzVector<T> v4_b, LorentzVector<T> v4_d) {
  auto v4_diff = v4_b - v4_d;
  return M2(v4_diff);
}

// Vertexing ///////////////////////////////////////////////////////////////////

template <typename T>
Double_t VTX_THETA(T b_vtx_x, T pv_x, T b_vtx_y, T pv_y, T b_vtx_z, T pv_z) {
  auto flight = XYZVector(b_vtx_x - pv_x, b_vtx_y - pv_y, b_vtx_z - pv_z);
  return flight.Theta();
}


// Reconstruct mass of phi candidate with the least isolated opposite-sign long tracks assumming
// they are kaons. To be used with is_iso or wdd to ensure there is at least a kaon
// among the 3 tracks
Float_t MASS_PHI(Int_t type1, Int_t chrg1, Float_t px1, Float_t py1, Float_t pz1,
                Int_t type2, Int_t chrg2, Float_t px2, Float_t py2, Float_t pz2,
                Int_t type3, Int_t chrg3, Float_t px3, Float_t py3, Float_t pz3){

  TLorentzVector phiKaon1, phiKaon2;
  if (type1 == 3 && type2 == 3 && chrg1*chrg2 < 0) {
    phiKaon1 = TLorentzVector(px1, py1, pz1, sqrt(pow(494, 2) + pow(px1, 2) + pow(py1, 2) + pow(pz1, 2)));
    phiKaon2 = TLorentzVector(px2, py2, pz2, sqrt(pow(494, 2) + pow(px2, 2) + pow(py2, 2) + pow(pz2, 2)));
  } else if (type1 == 3 && type3 == 3 && chrg1*chrg3 < 0) {
    phiKaon1 = TLorentzVector(px1, py1, pz1, sqrt(pow(494, 2) + pow(px1, 2) + pow(py1, 2) + pow(pz1, 2)));
    phiKaon2 = TLorentzVector(px3, py3, pz3, sqrt(pow(494, 2) + pow(px3, 2) + pow(py3, 2) + pow(pz3, 2)));
  } else if (type2 == 3 && type3 == 3 && chrg2*chrg3 < 0) {
    phiKaon1 = TLorentzVector(px2, py2, pz2, sqrt(pow(494, 2) + pow(px2, 2) + pow(py2, 2) + pow(pz2, 2)));
    phiKaon2 = TLorentzVector(px3, py3, pz3, sqrt(pow(494, 2) + pow(px3, 2) + pow(py3, 2) + pow(pz3, 2)));
  } else {
    return -99.;
  }

  return (phiKaon1 + phiKaon2).M();
}

// Reconstruct mass of the D0/D* and the least isolated track under the pion mass assumption
Float_t MASS_DX_ISO1(Float_t dx_e, Float_t dx_px, Float_t dx_py, Float_t dx_pz,
                     Float_t px1, Float_t py1, Float_t pz1){

  TLorentzVector pDx(dx_px, dx_py, dx_pz, dx_e);
  Float_t mpi = 139.57;
  Float_t p3Iso1 = sqrt(pow(px1,2) + pow(py1,2) + pow(pz1,2));
  TLorentzVector pIso1(px1, py1, pz1, sqrt(pow(mpi,2) + pow(p3Iso1,2)));

  return (pDx + pIso1).M();
}

// Reconstruct mass of the D0/D* and the least isolated track under the proton mass assumption
Float_t MASS_DX_ISO1_PROT(Float_t dx_e, Float_t dx_px, Float_t dx_py, Float_t dx_pz,
                          Float_t px1, Float_t py1, Float_t pz1){

  TLorentzVector pDx(dx_px, dx_py, dx_pz, dx_e);
  Float_t mpr = 938.27;
  Float_t p3Iso1 = sqrt(pow(px1,2) + pow(py1,2) + pow(pz1,2));
  TLorentzVector pIso1(px1, py1, pz1, sqrt(pow(mpr,2) + pow(p3Iso1,2)));

  return (pDx + pIso1).M();
}

// Reconstruct mass of the D0/D* and the least isolated track under the kaon mass assumption
Float_t MASS_DX_ISO1_K(Float_t dx_e, Float_t dx_px, Float_t dx_py, Float_t dx_pz,
                       Float_t px1, Float_t py1, Float_t pz1){

  TLorentzVector pDx(dx_px, dx_py, dx_pz, dx_e);
  Float_t m_k = 493.68;
  Float_t p3Iso1 = sqrt(pow(px1,2) + pow(py1,2) + pow(pz1,2));
  TLorentzVector pIso1(px1, py1, pz1, sqrt(pow(m_k,2) + pow(p3Iso1,2)));

  return (pDx + pIso1).M();
}

// Reconstruct mass of the D0/D* and the two least isolated tracks under the pion mass assumption
Float_t MASS_DX_ISO1_ISO2(Float_t dx_e, Float_t dx_px, Float_t dx_py, Float_t dx_pz,
                          Float_t px1, Float_t py1, Float_t pz1, Float_t px2, Float_t py2, Float_t pz2){

  TLorentzVector pDx(dx_px, dx_py, dx_pz, dx_e);
  Float_t mpi = 139.57;
  Float_t p3Iso1 = sqrt(pow(px1,2) + pow(py1,2) + pow(pz1,2));
  TLorentzVector pIso1(px1, py1, pz1, sqrt(pow(mpi,2) + pow(p3Iso1,2)));
  Float_t p3Iso2 = sqrt(pow(px2,2) + pow(py2,2) + pow(pz2,2));
  TLorentzVector pIso2(px2, py2, pz2, sqrt(pow(mpi,2) + pow(p3Iso2,2)));

  return (pDx + pIso1 + pIso2).M();
}

// proxy for D** mass: if only one non-iso track, assume it's a pion, else search for track that has correct charge to
// pair with the D(*) to have come from D**->D(*)pi
// iso tracks reconstructed with pion mass hypothesis, but use it again explicitly here
// note: momenta in GeV here, 'tracks' has 2 iso tracks ordered least->most iso
double MASS_DX_PI(double d_px, double d_py, double d_pz, double d_e, int d_id, bool is_d0, vector<IsoTrack> tracks) {
  TLorentzVector p_d(d_px, d_py, d_pz, d_e);
  bool found_pi = false;
  TLorentzVector p_pi; // apply pion mass hypothesis on this
  TLorentzVector p_track;
  double m_pi = 0.13957;
  double no_cand = -0.099;
  int num_noniso = 0;
  for (auto i=0; i<tracks.size(); i++) {
    if (tracks[i].iso_bdt>0.15) num_noniso++;
  }
  if (num_noniso==1) {
    found_pi = true;
    p_track = tracks[0].p;
  }
  if (num_noniso>1) {
    // take the least iso track that has correct charge
    for (int i=0; i<num_noniso; i++) {
      if (tracks[i].charge*d_id*(2*is_d0-1)>0) {
        found_pi = true;
        p_track = tracks[i].p;
        break;
      }
    }
  }
  if (!found_pi) return no_cand;
  double pmag2 = pow(p_track.Px(),2)+pow(p_track.Py(),2)+pow(p_track.Pz(),2);
  p_pi.SetPxPyPzE(p_track.Px(), p_track.Py(), p_track.Pz(), sqrt(pow(m_pi,2)+pmag2));
  return (p_d + p_pi).M();
}

// proxy for D**s mass: consider track with highest NNk score (for MC, highest prob to pass NNk>0.2) to be kaon track
// iso tracks reconstructed with pion mass hypothesis, use kaon mass hypothesis here instead
// note: momenta in GeV here, 'tracks' has 3 iso tracks ordered least->most iso
double MASS_DX_K(double d_px, double d_py, double d_pz, double d_e, int d_id, vector<IsoTrack> tracks) {
  TLorentzVector p_d(d_px, d_py, d_pz, d_e);
  TLorentzVector p_k; // apply kaon mass hypothesis on this
  bool found_k = false;
  TLorentzVector p_track;
  double max_nnk = -1.0;
  double m_k = 0.49368;
  double no_cand = -0.099;
  for (auto i=0; i<tracks.size(); i++) {
    if (tracks[i].is_data) {
      assert(tracks[i].wpid==-1.0); // just checking that isotracks created correctly...
      if (tracks[i].NNk>max_nnk) {
        found_k = true;
        p_track = tracks[i].p;
        max_nnk = tracks[i].NNk;
      }
    } else { // looking at MC tracks
      assert(tracks[i].wpid>=0.0 && tracks[i].wpid<=1.0); // should be shifted already, just a check before referencing the value
      if (tracks[i].wpid>max_nnk) {
        found_k = true;
        p_track = tracks[i].p;
        max_nnk = tracks[i].wpid; // wpid should be prob that track satifies NNk>0.2
      }
    }
  }
  if (!found_k) return no_cand;
  double pmag2 = pow(p_track.Px(),2)+pow(p_track.Py(),2)+pow(p_track.Pz(),2);
  p_k.SetPxPyPzE(p_track.Px(), p_track.Py(), p_track.Pz(), sqrt(pow(m_k,2)+pmag2));
  return (p_d + p_k).M();
}

double DSTST_TRUE_MASS(double b_dau1_true_e, double b_dau1_true_px,
                       double b_dau1_true_py, double b_dau1_true_pz) {
  const TLorentzVector d(b_dau1_true_px, b_dau1_true_py, b_dau1_true_pz,
                         b_dau1_true_e);
  return d.M();
}

double W_EVTGEN_FIX(int mc_id, int truthmatch, double m) {
  if ((mc_id == 11874430) || (mc_id == 11874440) || (mc_id == 12873450) ||
      (mc_id == 12873460)) {
    // D**
    TString histo_name = "";
    if (truthmatch % 10 == 0) {
      if (truthmatch == 210) {
        // D_0*
        histo_name = "w_evtgen_fix_D0st_mu";
      } else if (truthmatch == 110) {
        // D_0*0
        histo_name = "w_evtgen_fix_D0st0_mu";
      } else if (truthmatch == 240 || truthmatch == 250) {
        // D'_1
        histo_name = "w_evtgen_fix_D1p_mu";
      } else if (truthmatch == 140 || truthmatch == 150) {
        // D'_10
        histo_name = "w_evtgen_fix_D1p0_mu";
      } else if (truthmatch == 220 || truthmatch == 230
                 || truthmatch == 500220 || truthmatch == 500230) {
        // D_1
        histo_name = "w_evtgen_fix_D1_mu";
      } else if (truthmatch == 120 || truthmatch == 130
                 || truthmatch == 500120 || truthmatch == 500130) {
        // D_10
        histo_name = "w_evtgen_fix_D10_mu";
      } else if (truthmatch == 260 || truthmatch == 270 || truthmatch == 280
                 || truthmatch == 500260 || truthmatch == 500270) {
        // D_2*
        histo_name = "w_evtgen_fix_D2st_mu";
      } else if (truthmatch == 160 || truthmatch == 170 || truthmatch == 180
                 || truthmatch == 500160 || truthmatch == 500170) {
        // D_2*0
        histo_name = "w_evtgen_fix_D2st0_mu";
      }
    } else {
      if (truthmatch == 211) {
        // D_0*
        histo_name = "w_evtgen_fix_D0st_tau";
      } else if (truthmatch == 111) {
        // D_0*0
        histo_name = "w_evtgen_fix_D0st0_tau";
      } else if (truthmatch == 241 || truthmatch == 251) {
        // D'_1
        histo_name = "w_evtgen_fix_D1p_tau";
      } else if (truthmatch == 141 || truthmatch == 151) {
        // D'_10
        histo_name = "w_evtgen_fix_D1p0_tau";
      } else if (truthmatch == 221 || truthmatch == 231
                 || truthmatch == 500221 || truthmatch == 500231) {
        // D_1
        histo_name = "w_evtgen_fix_D1_tau";
      } else if (truthmatch == 121 || truthmatch == 131
                 || truthmatch == 500121 || truthmatch == 500131) {
        // D_10
        histo_name = "w_evtgen_fix_D10_tau";
      } else if (truthmatch == 261 || truthmatch == 271 || truthmatch == 281
                 || truthmatch == 500261 || truthmatch == 500271) {
        // D_2*
        histo_name = "w_evtgen_fix_D2st_tau";
      } else if (truthmatch == 161 || truthmatch == 171 || truthmatch == 181
                 || truthmatch == 500161 || truthmatch == 500171) {
        // D_2*0
        histo_name = "w_evtgen_fix_D2st0_tau";
      }
    }

    if (histo_name == "") {
      // cout << "ERROR Could not find histogram for tm code " << truthmatch << endl;
      return 1.;
    }

    TFile f_weights("../../../run2-rdx/reweight/evtgen/evtgen_fix.root", "read");
    TH1D* histo;
    f_weights.GetObject(histo_name, histo);
    if (histo == nullptr) {
      cout << "ERROR Could not find histogram " << histo_name << " for tm code " << truthmatch << endl;
      return 1.;
    }
    return histo->Interpolate(m);
  } else {
    // Not D**
    return 1.;
  }
}

// double MASS_DX_K_RS(double d_px, double d_py, double d_pz, double d_e, int d_id, vector<IsoTrack> tracks) {
//   TLorentzVector p_d(d_px, d_py, d_pz, d_e);
//   TLorentzVector p_k; // apply kaon mass hypothesis on this
//   bool found_k = false;
//   TLorentzVector p_track;
//   double max_nnk = -1.0;
//   double m_k = 0.49368;
//   double no_cand = -0.099;
//   bool ws = false;
//   for (auto i=0; i<tracks.size(); i++) {
//     if (tracks[i].is_data) {
//       assert(tracks[i].wpid==-1.0); // just checking that isotracks created correctly...
//       if (tracks[i].NNk>max_nnk) {
//         found_k = true;
//         if (!(d_id*tracks[i].charge>0)) ws=true;
//         else ws=false;
//         p_track = tracks[i].p;
//         max_nnk = tracks[i].NNk;
//       }
//     } else { // looking at MC tracks
//       assert(tracks[i].wpid>=0.0 && tracks[i].wpid<=1.0); // should be shifted already, just a check before referencing the value
//       if (tracks[i].wpid>max_nnk) {
//         found_k = true;
//         if (!(d_id*tracks[i].charge>0)) ws=true;
//         else ws=false;
//         p_track = tracks[i].p;
//         max_nnk = tracks[i].wpid; // wpid should be prob that track satifies NNk>0.2
//       }
//     }
//   }
//   if (!found_k || ws) return no_cand;
//   double pmag2 = pow(p_track.Px(),2)+pow(p_track.Py(),2)+pow(p_track.Pz(),2);
//   p_k.SetPxPyPzE(p_track.Px(), p_track.Py(), p_track.Pz(), sqrt(pow(m_k,2)+pmag2));
//   return (p_d + p_k).M();
// }

// double MASS_DX_K_WS(double d_px, double d_py, double d_pz, double d_e, int d_id, vector<IsoTrack> tracks) {
//   TLorentzVector p_d(d_px, d_py, d_pz, d_e);
//   TLorentzVector p_k; // apply kaon mass hypothesis on this
//   bool found_k = false;
//   TLorentzVector p_track;
//   double max_nnk = -1.0;
//   double m_k = 0.49368;
//   double no_cand = -0.099;
//   bool rs = false;
//   for (auto i=0; i<tracks.size(); i++) {
//     if (tracks[i].is_data) {
//       assert(tracks[i].wpid==-1.0); // just checking that isotracks created correctly...
//       if (tracks[i].NNk>max_nnk) {
//         found_k = true;
//         if (d_id*tracks[i].charge>0) rs=true;
//         else rs=false;
//         p_track = tracks[i].p;
//         max_nnk = tracks[i].NNk;
//       }
//     } else { // looking at MC tracks
//       assert(tracks[i].wpid>=0.0 && tracks[i].wpid<=1.0); // should be shifted already, just a check before referencing the value
//       if (tracks[i].wpid>max_nnk) {
//         found_k = true;
//         if (d_id*tracks[i].charge>0) rs=true;
//         else rs=false;
//         p_track = tracks[i].p;
//         max_nnk = tracks[i].wpid; // wpid should be prob that track satifies NNk>0.2
//       }
//     }
//   }
//   if (!found_k || rs) return no_cand;
//   double pmag2 = pow(p_track.Px(),2)+pow(p_track.Py(),2)+pow(p_track.Pz(),2);
//   p_k.SetPxPyPzE(p_track.Px(), p_track.Py(), p_track.Pz(), sqrt(pow(m_k,2)+pmag2));
//   return (p_d + p_k).M();
// }

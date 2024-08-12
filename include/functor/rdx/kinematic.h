// Author: Yipeng Sun, Svende Braun
// License: BSD 2-clause
// Last Change: Tue Mar 07, 2023 at 04:39 PM -0500

#pragma once

#include <vector>

#include <Math/Vector3D.h>
#include <Math/Vector4D.h>
#include <Math/VectorUtil.h>
#include <TMath.h>
#include <TROOT.h>
#include <TLorentzVector.h>

#include "functor/basic.h"
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

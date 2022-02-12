// Author: Yipeng Sun, Svede Braun
// License: BSD 2-clause
// Last Change: Sat Feb 12, 2022 at 04:32 PM -0500

#pragma once

#include <Math/Vector3D.h>
#include <Math/Vector4D.h>
#include <Math/VectorUtil.h>
#include <TMath.h>
#include <TROOT.h>

#include "functor/basic_kinematic.h"

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

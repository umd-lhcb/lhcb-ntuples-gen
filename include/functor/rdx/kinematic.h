// Author: Yipeng Sun, Svende Braun
// License: BSD 2-clause
// Last Change: Tue Jun 14, 2022 at 01:32 AM -0400

#pragma once

#include <vector>

#include <Math/Vector3D.h>
#include <Math/Vector4D.h>
#include <Math/VectorUtil.h>
#include <TMath.h>
#include <TROOT.h>

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

// Computing mDD and mDX (mDX for K/K* differentiation), D*
vector<Double_t> DD_MX_MASS_DST(Double_t mu_mom_px, Double_t mu_mom_py,
                                Double_t mu_mom_pz, Double_t mu_mom_pe,
                                Double_t dst_px, Double_t dst_py,
                                Double_t dst_pz, Double_t dst_pe,
                                int mu_gdmom_id, Double_t mu_gdmom_px,
                                Double_t mu_gdmom_py, Double_t mu_gdmom_pz,
                                Double_t mu_gdmom_pe, Double_t b_px,
                                Double_t b_py, Double_t b_pz, Double_t b_pe) {
  auto Tmumomp =
      ROOT::Math::PxPyPzEVector(mu_mom_px, mu_mom_py, mu_mom_pz, mu_mom_pe);
  auto     TDstp = ROOT::Math::PxPyPzEVector(dst_px, dst_py, dst_pz, dst_pe);
  auto     Tmugdmomp = ROOT::Math::PxPyPzEVector(mu_gdmom_px, mu_gdmom_py,
                                             mu_gdmom_pz, mu_gdmom_pe);
  auto     TBp       = ROOT::Math::PxPyPzEVector(b_px, b_py, b_pz, b_pe);
  Double_t mDD       = (Tmumomp + TDstp).M2();
  Double_t mX_DD     = (TBp - TDstp - Tmumomp).M();

  if (ABS(mu_gdmom_id) == 413 || ABS(mu_gdmom_id) == 423 ||
      ABS(mu_gdmom_id) == 433) {
    mDD   = (Tmugdmomp + TDstp).M2();
    mX_DD = (TBp - TDstp - Tmugdmomp).M();
  }

  return {mDD, mX_DD};
}

// Computing mDD and mDX (mDX for K/K* differentiation), D0
vector<Double_t> DD_MX_MASS_D0(
    Double_t mu_mom_px, Double_t mu_mom_py, Double_t mu_mom_pz,
    Double_t mu_mom_pe, Double_t d_mom_px, Double_t d_mom_py, Double_t d_mom_pz,
    Double_t d_mom_pe, int mu_gdmom_id, Double_t mu_gdmom_px,
    Double_t mu_gdmom_py, Double_t mu_gdmom_pz, Double_t mu_gdmom_pe,
    Double_t d_px, Double_t d_py, Double_t d_pz, Double_t d_pe, int d_mom_id,
    Double_t b_px, Double_t b_py, Double_t b_pz, Double_t b_pe) {
  auto Tmumomp =
      ROOT::Math::PxPyPzEVector(mu_mom_px, mu_mom_py, mu_mom_pz, mu_mom_pe);
  auto TDmomp =
      ROOT::Math::PxPyPzEVector(d_mom_px, d_mom_py, d_mom_pz, d_mom_pe);
  auto Tmugdmomp = ROOT::Math::PxPyPzEVector(mu_gdmom_px, mu_gdmom_py,
                                             mu_gdmom_pz, mu_gdmom_pe);
  auto TDp       = ROOT::Math::PxPyPzEVector(d_px, d_py, d_pz, d_pe);
  auto TBp       = ROOT::Math::PxPyPzEVector(b_px, b_py, b_pz, b_pe);

  Double_t mDD = 0.0, mX_DD = 0.0;
  if (ABS(d_mom_id) == 413 || ABS(d_mom_id) == 423) {
    mDD   = (Tmumomp + TDmomp).M2();
    mX_DD = (TBp - TDmomp - Tmumomp).M();

    if (ABS(mu_gdmom_id) == 413 || ABS(mu_gdmom_id) == 423 ||
        ABS(mu_gdmom_id) == 433) {
      mDD   = (Tmugdmomp + TDmomp).M2();
      mX_DD = (TBp - TDmomp - Tmugdmomp).M();
    }
  } else {
    mDD   = (Tmumomp + TDp).M2();
    mX_DD = (TBp - TDp - Tmumomp).M();
    if (ABS(mu_gdmom_id) == 413 || ABS(mu_gdmom_id) == 423 ||
        ABS(mu_gdmom_id) == 433) {
      mDD   = (Tmugdmomp + TDp).M2();
      mX_DD = (TBp - TDp - Tmugdmomp).M();
    }
  }
  return {mDD, mX_DD};
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

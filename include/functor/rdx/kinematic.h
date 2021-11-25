// Author: Yipeng Sun, Svede Braun
// License: BSD 2-clause
// Last Change: Thu Nov 25, 2021 at 11:59 PM +0100

#ifndef _LNG_FUNCTOR_RDX_KINEMATIC_H_
#define _LNG_FUNCTOR_RDX_KINEMATIC_H_

#include <Math/Vector4D.h>
#include <TLorentzVector.h>
#include <TMath.h>
#include <TROOT.h>
#include <TVector3.h>

// Helpers /////////////////////////////////////////////////////////////////////

TVector3 VEC_DELTA(Double_t Xf, Double_t Yf, Double_t Zf, Double_t Xi,
                   Double_t Yi, Double_t Zi) {
  TVector3 v;
  v.SetXYZ(Xf - Xi, Yf - Yi, Zf - Zi);
  return v;
}

TLorentzVector FOUR_VEC(Double_t X, Double_t Y, Double_t Z, Double_t T) {
  TLorentzVector v;
  v.SetXYZT(X, Y, Z, T);
  return v;
}

Double_t M2(TLorentzVector v) { return v.M2(); }

Double_t M2(Double_t PX, Double_t PY, Double_t PZ, Double_t PE) {
  auto v = ROOT::Math::PxPyPzEVector(PX, PY, PZ, PE);
  return v.M2();
}

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

// Original name: mm_mom
// Current name: mm_dst_mom
// Meaning: Missing mass between D* and its mother.
// Defined in: AddB.C, L3138, L3085-3095
Double_t MM_DST_MOM(TLorentzVector& v_dst_mom_p, TLorentzVector& v_dst_p) {
  Double_t mm_dst_mom = M2(v_dst_mom_p - v_dst_p);
  if (mm_dst_mom > 0)
    return sqrt(mm_dst_mom);
  else
    return 0.0;
}

Double_t ETA(Double_t p, Double_t pz) {
  return 0.5 * TMath::Log((p + pz) / (p - pz));
}

Double_t FD_TRANS(Double_t endvtx_x, Double_t ownpv_x, Double_t endvtx_y,
                  Double_t ownpv_y) {
  auto x = endvtx_x - ownpv_x;
  auto y = endvtx_y - ownpv_y;
  return TMath::Sqrt(x * x + y * y);
}

// Rest frame approximation ////////////////////////////////////////////////////

TLorentzVector B_P_EST(Double_t b_pz, Double_t b_m, TVector3 v3_b_flight) {
  const Double_t b_m_ref = 5279.61;

  Double_t tan_theta = v3_b_flight.Unit().Perp() / v3_b_flight.Unit().Z();
  Double_t b_pt      = (b_m_ref / b_m) * tan_theta * b_pz;

  TLorentzVector v4_b_p_est;
  v4_b_p_est.SetPtEtaPhiM(b_pt, v3_b_flight.Unit().Eta(),
                          v3_b_flight.Unit().Phi(), b_m_ref);

  return v4_b_p_est;
}

TLorentzVector BOOST(TLorentzVector v, TVector3 v_b) {
  v.Boost(v_b);
  return v;
}

#endif

// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Sat Mar 13, 2021 at 09:37 PM +0100

#ifndef _LNG_FUNCTOR_RDX_KINEMATIC_H_
#define _LNG_FUNCTOR_RDX_KINEMATIC_H_

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

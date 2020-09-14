// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Mon Sep 14, 2020 at 06:02 PM +0800

#ifndef _LNG_FUNCTOR_KINEMATIC_H_
#define _LNG_FUNCTOR_KINEMATIC_H_

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

// Rest frame approximation ////////////////////////////////////////////////////

TLorentzVector P_EST(Double_t PZ, Double_t m, TVector3 flight) {
  const Double_t B_M = 5279.61;

  Double_t Tan_theta = flight.Unit().Perp() / flight.Unit().Z();
  Double_t PT        = TMath::Power((B_M / m), 1) * Tan_theta * PZ;

  TLorentzVector P;
  P.SetPtEtaPhiM(PT, flight.Unit().Eta(), flight.Unit().Phi(), B_M);

  return P;
}

#endif

// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Tue Oct 15, 2019 at 01:50 AM -0400

#ifndef _LNG_FUNCTOR_PARTICLE_H_
#define _LNG_FUNCTOR_PARTICLE_H_

#include <TLorentzVector.h>
#include <TMath.h>
#include <TROOT.h>
#include <TVector3.h>

// General /////////////////////////////////////////////////////////////////////

Bool_t ISDATA(ULong64_t time) { return (time > 0); }

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

// Muon-related ////////////////////////////////////////////////////////////////

Bool_t MU_PID(Bool_t id_correctness, Double_t PID) {
  return id_correctness && (PID > 2.0);
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

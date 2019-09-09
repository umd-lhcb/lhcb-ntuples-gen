// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Mon Sep 09, 2019 at 12:49 PM -0400

#ifndef _LNG_FUNCTOR_PARTICLE_H_
#define _LNG_FUNCTOR_PARTICLE_H_

#include <TLorentzVector.h>
#include <TMath.h>
#include <TROOT.h>
#include <TVector3.h>

// General /////////////////////////////////////////////////////////////////////

Bool_t ISDATA(ULong64_t time) {
  if (time > 0)
    return true;
  else
    return false;
}

// Muon-related ////////////////////////////////////////////////////////////////

Bool_t MU_PID(Bool_t id_correctness, Double_t PID) {
  return id_correctness && (PID > 2.0);
}

// Rest frame approximation ////////////////////////////////////////////////////

TVector3 B0_FLIGHT_VECTOR(Double_t Xf, Double_t Yf, Double_t Zf, Double_t Xi,
                          Double_t Yi, Double_t Zi) {
  TVector3 v;
  v.SetXYZ(Xf - Xi, Yf - Yi, Zf - Zi);
  return v;
}

Double_t M2_MISS(Double_t E, Double_t PX, Double_t PY, Double_t PZ, Double_t m,
                 TVector3 flight) {
  const Double_t B_M = 5279.61;

  TLorentzVector P_reco;
  P_reco.SetXYZT(PX, PY, PZ, E);

  Double_t Tan_theta = flight.Unit().Perp() / flight.Unit().Z();
  Double_t PT        = TMath::Power((B_M / m), 1) * Tan_theta * PZ;

  TLorentzVector P;
  P.SetPtEtaPhiM(PT, flight.Unit().Eta(), flight.Unit().Phi(), B_M);

  TLorentzVector P_miss = P - P_reco;
  return P_miss.M2();
}

#endif

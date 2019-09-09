// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Mon Sep 09, 2019 at 02:45 AM -0400

#ifndef _LNG_FUNCTOR_PARTICLE_H_
#define _LNG_FUNCTOR_PARTICLE_H_

#include <TLorentzVector.h>
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

TVector3 B0_FLIGHT_VECTOR(Double_t X_f, Double_t Y_f, Double_t Z_f,
                          Double_t X_i, Double_t Y_i, Double_t Z_i) {
  TVector3 v;
  v.SetXYZ(X_f - X_i, Y_f - Y_i, Z_f - Z_i);
  return v;
}

Double_t M2_MISS(Double_t E, Double_t PX, Double_t PY, Double_t PZ,
                 TVector3 flight) {
  const Double_t B_M = 5279.61;
  const Double_t PT  = 5800;

  TLorentzVector P;
  P.SetPtEtaPhiM(PT, flight.Unit().Eta(), flight.Unit().Phi(), B_M);

  TLorentzVector P_reco;
  P_reco.SetXYZT(PX, PY, PZ, E);

  TLorentzVector P_miss = P - P_reco;
  return P_miss.M2();
}

#endif

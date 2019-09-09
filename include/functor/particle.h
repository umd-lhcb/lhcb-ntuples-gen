// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Mon Sep 09, 2019 at 02:03 AM -0400

#ifndef _LNG_FUNCTOR_PARTICLE_H_
#define _LNG_FUNCTOR_PARTICLE_H_

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

Double_t M2_MISS(Double_t m, Double_t PX, Double_t PY, Double_t PZ,
                 TVector3 flight) {
  TVector3 P_vec;
  P_vec.SetXYZ(PX, PY, PZ);
  P_vec           = P_vec - flight.Unit() * (P_vec.Dot(flight.Unit()));
  Double_t P      = P_vec.Mag();
  Double_t m_miss = sqrt(m * m + P * P) + P;
  return m_miss * m_miss;
}

#endif

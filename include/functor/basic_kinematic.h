// Author: Yipeng Sun, Svede Braun
// License: BSD 2-clause
// Last Change: Sat Feb 12, 2022 at 04:32 PM -0500

#pragma once

#include <Math/Vector4D.h>
#include <Math/VectorUtil.h>
#include <TMath.h>
#include <TROOT.h>

using ROOT::Math::LorentzVector;
using ROOT::Math::PxPyPzEVector;

template <typename T>
Double_t M2(LorentzVector<T>& v4) {
  return v4.M2();
}

Double_t M2(Double_t PX, Double_t PY, Double_t PZ, Double_t PE) {
  return PxPyPzEVector(PX, PY, PZ, PE).M2();
}

Double_t ETA(Double_t p, Double_t pz) {
  return 0.5 * TMath::Log((p + pz) / (p - pz));
}

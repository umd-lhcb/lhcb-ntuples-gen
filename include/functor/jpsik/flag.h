// Author: Manuel Franco Sevilla
// License: BSD 2-clause
// Last Change: Fri May 20, 2022 at 01:58 AM -0400

#pragma once

#include <TMath.h>

#include <vector>

#include "functor/basic.h"

// Flags ///////////////////////////////////////////////////////////////////////

// Original name: l0mupt
// Meaning: Either of the muons in the J/Psi -> mumu triggered L0muon and has pT > 2 GeV
// Needed due to mismodeling at low pT
Bool_t L0MUPT(double mu_pt, bool mu_l0, double amu_pt, bool amu_l0) {
  bool flag = false;
  if(mu_l0 && mu_pt > 2000) flag = true;
  if(amu_l0 && amu_pt > 2000) flag = true;

  return flag;
}

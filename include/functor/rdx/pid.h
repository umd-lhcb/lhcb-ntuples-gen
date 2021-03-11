// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Fri Sep 18, 2020 at 08:48 PM +0800

#ifndef _LNG_FUNCTOR_PID_H_
#define _LNG_FUNCTOR_PID_H_

#include <TMath.h>
#include <TROOT.h>

// Original name: muPID
// Current name: mu_pid
// Meaning: Real muon or not
// Defined in: AddB.C, LN2500, LN2540
Bool_t MU_PID(Int_t mu_true_id) {
  if (TMath::Abs(mu_true_id) == 13) return true;
  return false;
}

Bool_t MU_PID(Bool_t mu_is_mu, Double_t mu_pid_mu) {
  if (mu_is_mu && mu_pid_mu > 2.0) return true;
  return false;
}

Bool_t MU_VETO(Bool_t pi_is_mu, Bool_t k_is_mu) {
  if (pi_is_mu || k_is_mu) return true;
  return false;
}

#endif

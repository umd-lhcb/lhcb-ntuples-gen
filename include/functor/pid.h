// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Tue Sep 15, 2020 at 02:04 AM +0800

#ifndef _LNG_FUNCTOR_PID_H_
#define _LNG_FUNCTOR_PID_H_

#include <TMath.h>
#include <TROOT.h>

// Muon PID ////////////////////////////////////////////////////////////////////

// Original name: muPID
// Current name: mu_pid
// Meaning: Real muon or not
// Defined in: AddB.C, LN2500, LN2540
Bool_t MU_PID(Bool_t is_data, Int_t mu_true_id, Bool_t mu_is_mu,
              Double_t mu_pid_mu) {
  if ((!is_data && TMath::Abs(mu_true_id) == 13) ||
      (mu_is_mu && mu_pid_mu > 2.0))
    return true;
  return false;
}

#endif

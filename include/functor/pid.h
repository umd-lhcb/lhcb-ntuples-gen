// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Fri Sep 11, 2020 at 06:35 PM +0800

#ifndef _LNG_FUNCTOR_PID_H_
#define _LNG_FUNCTOR_PID_H_

#include <TROOT.h>

// Muon PID ////////////////////////////////////////////////////////////////////

Bool_t MU_PID(Bool_t id_correctness, Double_t PID) {
  return id_correctness && (PID > 2.0);
}

#endif

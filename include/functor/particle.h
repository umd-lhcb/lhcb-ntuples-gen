// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Sun Sep 08, 2019 at 12:12 AM -0400

#ifndef _LNG_FUNCTOR_PARTICLE_H_
#define _LNG_FUNCTOR_PARTICLE_H_

#include <TROOT.h>

// General /////////////////////////////////////////////////////////////////////

Bool_t ISDATA(ULong64_t time) {
  if (time > 0) return true;
  else return false;
}

// Muon- related ///////////////////////////////////////////////////////////////

Bool_t MU_PID(Bool_t id_correctness, Double_t PID) {
  return id_correctness && (PID > 2.0);
}

#endif

// Author: Yipeng Sun, Alex Fernez
// License: BSD 2-clause
// Last Change: Jul 16, 2021

#ifndef _LNG_FUNCTOR_RDX_TRUTH_MATCH_H_
#define _LNG_FUNCTOR_RDX_TRUTH_MATCH_H_

#include <TMath.h>

#include "functor/rdx/flag.h"

////////// D* Truth-Matching Selections based on
////////// https://github.com/umd-lhcb/RDRDstRun1AnalysisPreservation/blob/f78365bfc3000ef70ced2ed271ec42aa866c44af/proc/redoHistos.C

// Bool_t MC_TRUTH_MATCH_BD2DSTMUNU(...) {
//   return ...;
// }
//
// ...
//

// ** need to include all possible parameters used in flag functions **
Bool_t MC_TRUTH_MATCH_DST(int decay_id/*, mu_mom_key, ...*/) {
  // switch (decay_id) {
  //   case 11574021: return MC_TRUTH_MATCH_BD2DSTMUNU(...);
  //   ...
  // }
  return false;
}


////////// D0 Truth-Matching Selections based on
////////// https://github.com/umd-lhcb/RDRDstRun1AnalysisPreservation/blob/f78365bfc3000ef70ced2ed271ec42aa866c44af/proc/redoHistos_D0.C

// Bool_t MC_TRUTH_MATCH_BU2D0MUNU(...) {
//   return ...;
// }
//
// ...
//

// ** need to include all possible parameters used in flag functions **
Bool_t MC_TRUTH_MATCH_D0(int decay_id/*, mu_mom_key, ...*/) {
  // switch (decay_id) {
  //   case 12573012: return MC_TRUTH_MATCH_BU2D0MUNU(...);
  //   ...
  // }
  return false;
}


#endif

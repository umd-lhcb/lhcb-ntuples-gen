// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Sat Oct 09, 2021 at 12:13 AM +0200
// NOTE: All kinematic variables are in MeV

#ifndef _LNG_FUNCTOR_RDX_SKIMS_H_
#define _LNG_FUNCTOR_RDX_SKIMS_H_

#include <TDataType.h>

#include "functor/basic.h"

// Skims ///////////////////////////////////////////////////////////////////////
// NOTE: Units are in GeV!

Bool_t FLAG_ISO(Bool_t add_flags, Double_t iso_bdt1) {
  return add_flags && iso_bdt1 < 0.15;
}

// clang-format off
Bool_t FLAG_DD(Bool_t add_flags,
               Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
               Int_t iso_type1, Int_t iso_type2, Int_t iso_type3,
               Float_t iso_p1, Float_t iso_p2, Float_t iso_p3,
               Float_t iso_pt1, Float_t iso_pt2, Float_t iso_pt3,
               Float_t iso_nnk1, Float_t iso_nnk2, Float_t iso_nnk3) {
  // clang-format on
  auto pid_ok =
      MAX(IF(iso_bdt1 <= -1.1, 0.0f, iso_nnk1) * (iso_type1 == 3),
          IF(iso_bdt2 <= -1.1, 0.0f, iso_nnk2) * (iso_type2 == 3),
          IF(iso_bdt3 <= -1.1, 0.0f, iso_nnk3) * (iso_type3 == 3)) > 0.2;

  auto kinematic_ok = MAX(iso_p1 * (iso_pt1 > 0.15),
                          iso_p2 * (iso_pt2 > 0.15) * (iso_bdt2 > -1.1),
                          iso_p3 * (iso_pt3 > 0.15) * (iso_bdt3 > -1.1)) > 5.0;

  return add_flags && (iso_bdt1 > 0.15) && pid_ok && kinematic_ok;
}

// clang-format off
Bool_t FLAG_2OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
                Int_t iso_type1, Int_t iso_type2,
                Float_t iso_p1, Float_t iso_p2,
                Float_t iso_pt1, Float_t iso_pt2,
                Int_t iso_chrg1, Int_t iso_chrg2,
                Float_t iso_nnk1, Float_t iso_nnk2) {
  // clang-format on
  return add_flags && (iso_bdt1 > 0.15) && (iso_bdt2 > 0.15) &&
         (iso_bdt3 < 0.15) && (iso_type1 == 3) && (iso_type2 == 3) &&
         (MAX(iso_p1 * (iso_pt1 > 0.15), iso_p2 * (iso_pt2 > 0.15)) > 5.0) &&
         (iso_chrg1 != 0) && (iso_chrg1 + iso_chrg2 == 0) &&
         (iso_chrg1 < 100) && (iso_nnk1 < 0.2) && (iso_nnk2 < 0.2);
}

// clang-format off
Bool_t FLAG_1OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2,
                Int_t iso_type1,
                Float_t iso_p1,
                Float_t iso_pt1,
                Int_t iso_chrg1,
                Float_t iso_nnk1,
                Int_t d0_id) {
  // clang-format on
  return add_flags && (iso_bdt1 > 0.15) && (iso_bdt2 < 0.15) &&
         (iso_type1 == 3) && (iso_p1 > 5.0) && (iso_pt1 > 0.15) &&
         (iso_chrg1 * d0_id) > 0 && (iso_nnk1 < 0.2);
}

// clang-format off
// For D**
Bool_t FLAG_1OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2,
                Int_t iso_type1,
                Float_t iso_p1, Float_t iso_pt1,
                Int_t iso_chrg1,
                Float_t iso_nnk1,
                Int_t dst_id, Double_t dst_iso_deltam) {
  // clang-format on
  return add_flags && (iso_bdt1 > 0.15) && (iso_bdt2 < 0.15) &&
         (iso_type1 == 3) && (iso_p1 > 5.0) && (iso_pt1 > 0.15) &&
         (iso_chrg1 * dst_id < 0) && (iso_nnk1 < 0.2) &&
         (0.36 < dst_iso_deltam) && (dst_iso_deltam < 0.6);  // Phoebe's cut
  // (2.4 < dst_iso_invm && dst_iso_invm < 2.52)  // Greg's cut
}

#endif

// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Thu Jun 23, 2022 at 02:28 PM -0400
// NOTE: All kinematic variables are in MeV

#pragma once

#include <TDataType.h>

#include "functor/basic.h"

// Skims ///////////////////////////////////////////////////////////////////////
// NOTE: Units are in GeV!

Bool_t FLAG_ISO(Bool_t add_flags, Double_t iso_bdt1) {
  return add_flags && iso_bdt1 < 0.15;
}

Double_t WT_ISO(Bool_t add_flags, Double_t iso_bdt1) {
  return static_cast<Double_t>(FLAG_ISO(add_flags, iso_bdt1));
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
      MAX(IF(iso_bdt1 > -1.1, iso_nnk1, 0.0f) * (iso_type1 == 3),
          IF(iso_bdt2 > -1.1, iso_nnk2, 0.0f) * (iso_type2 == 3),
          IF(iso_bdt3 > -1.1, iso_nnk3, 0.0f) * (iso_type3 == 3)) > 0.2;

  auto kinematic_ok = MAX(iso_p1 * (iso_pt1 > 0.15),
                          iso_p2 * (iso_pt2 > 0.15) * (iso_bdt2 > -1.1),
                          iso_p3 * (iso_pt3 > 0.15) * (iso_bdt3 > -1.1)) > 5.0;

  return add_flags && (iso_bdt1 > 0.15) && pid_ok && kinematic_ok;
}

// clang-format off
Double_t WT_DD(Bool_t add_flags,
               Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
               Int_t iso_type1, Int_t iso_type2, Int_t iso_type3,
               Float_t iso_p1, Float_t iso_p2, Float_t iso_p3,
               Float_t iso_pt1, Float_t iso_pt2, Float_t iso_pt3,
               Double_t iso_nnk1_wt, Double_t iso_nnk2_wt,
               Double_t iso_nnk3_wt) {
  // clang-format on
  auto kinematic_ok = MAX(iso_p1 * (iso_pt1 > 0.15),
                          iso_p2 * (iso_pt2 > 0.15) * (iso_bdt2 > -1.1),
                          iso_p3 * (iso_pt3 > 0.15) * (iso_bdt3 > -1.1)) > 5.0;
  auto prefac =
      static_cast<Double_t>(kinematic_ok && add_flags && iso_bdt1 > 0.15);

  // This is to translate the 'MAX' PID lines.
  // Think in terms of Venn diagram!
  // Don't know why Phoebe chose '-2' instead of '-1.1' in her code:
  //   https://gitlab.cern.ch/bhamilto/rdvsrdst-histfactory/-/blob/master/proc/redoHistos_Dst.C#L1603
  iso_nnk1_wt = IF(iso_bdt1 > -1.1, iso_nnk1_wt, 0.0) * (iso_type1 == 3);
  iso_nnk2_wt = IF(iso_bdt2 > -1.1, iso_nnk2_wt, 0.0) * (iso_type2 == 3);
  iso_nnk3_wt = IF(iso_bdt3 > -1.1, iso_nnk3_wt, 0.0) * (iso_type3 == 3);

  Double_t wt_pid = iso_nnk1_wt + iso_nnk2_wt + iso_nnk3_wt -
                    iso_nnk1_wt * iso_nnk2_wt - iso_nnk1_wt * iso_nnk3_wt -
                    iso_nnk2_wt * iso_nnk3_wt +
                    iso_nnk1_wt * iso_nnk2_wt * iso_nnk3_wt;

  return prefac * wt_pid;
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
         (iso_chrg1 != iso_chrg2) && (iso_chrg1 * iso_chrg2 != 0) &&
         (iso_chrg1 < 100) && (iso_nnk1 < 0.2) && (iso_nnk2 < 0.2);
}

// clang-format off
Double_t WT_2OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
                Int_t iso_type1, Int_t iso_type2,
                Float_t iso_p1, Float_t iso_p2,
                Float_t iso_pt1, Float_t iso_pt2,
                Int_t iso_chrg1, Int_t iso_chrg2,
                Double_t iso_nnk1_wt, Double_t iso_nnk2_wt) {
  auto prefac = static_cast<Double_t>(
      FLAG_2OS(add_flags,
               iso_bdt1, iso_bdt2, iso_bdt3,
               iso_type1, iso_type2,
               iso_p1, iso_p2,
               iso_pt1, iso_pt2,
               iso_chrg1, iso_chrg2,
               0.0f, 0.0f));
  // clang-format on

  return prefac * iso_nnk1_wt * iso_nnk2_wt;
}

// clang-format off
Bool_t FLAG_1OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2,
                Int_t iso_type1,
                Float_t iso_p1, Float_t iso_pt1,
                Int_t iso_chrg1,
                Float_t iso_nnk1,
                Int_t d0_id) {
  // clang-format on
  return add_flags && (iso_bdt1 > 0.15) && (iso_bdt2 < 0.15) &&
         (iso_type1 == 3) && (iso_p1 > 5.0) && (iso_pt1 > 0.15) &&
         (iso_chrg1 * d0_id) > 0 && (iso_nnk1 < 0.2);
}

// clang-format off
Double_t WT_1OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2,
                Int_t iso_type1,
                Float_t iso_p1, Float_t iso_pt1,
                Int_t iso_chrg1,
                Double_t iso_nnk1_wt,
                Int_t d0_id) {
  auto prefac = static_cast<Double_t>(
      FLAG_1OS(add_flags,
               iso_bdt1, iso_bdt2,
               iso_type1,
               iso_p1, iso_pt1,
               iso_chrg1,
               0.0f,
               d0_id));
  // clang-format on

  return prefac * iso_nnk1_wt;
}

// clang-format off
Bool_t FLAG_PROT(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2,
                Int_t iso_type1,
                Float_t iso_p1, Float_t iso_pt1,
                Int_t iso_chrg1,
                Float_t iso_nnp1,
                Int_t d0_id) {
  // clang-format on
  return add_flags && (iso_bdt1 > 0.15) && (iso_bdt2 < 0.15) &&
         (iso_type1 == 3) && (iso_p1 > 5.0) && (iso_pt1 > 0.15) &&
         (iso_chrg1 * d0_id) > 0 && (iso_nnp1 > 0.4);
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
         IN_RANGE(dst_iso_deltam, 0.36, 0.6);  // Phoebe's cut
  // IN_RANGE(dst_iso_invm, 2.4, 2.52)  // Greg's cut
}

// clang-format off
// For D**
Double_t WT_1OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2,
                Int_t iso_type1,
                Float_t iso_p1, Float_t iso_pt1,
                Int_t iso_chrg1,
                Double_t iso_nnk1_wt,
                Int_t dst_id, Double_t dst_iso_deltam) {
  auto prefac = static_cast<Double_t>(
      FLAG_1OS(add_flags,
               iso_bdt1, iso_bdt2,
               iso_type1,
               iso_p1, iso_pt1,
               iso_chrg1,
               0.0f,
               dst_id, dst_iso_deltam)
      );
  // clang-format on

  return prefac * iso_nnk1_wt;
}

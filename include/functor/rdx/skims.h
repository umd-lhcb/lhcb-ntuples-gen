// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Thu Sep 29, 2022 at 01:06 AM -0400
// NOTE: All kinematic variables are in MeV

#pragma once

#include <TDataType.h>

#include "functor/basic.h"

// Skims ///////////////////////////////////////////////////////////////////////
// NOTE: Units are in GeV!

Bool_t FLAG_ISO(Bool_t add_flags, Double_t iso_bdt1) {
  return add_flags && iso_bdt1 < 0.15;
}

Bool_t FLAG_ISO_ANG(Bool_t add_flags, Int_t iso_type1, Double_t iso_bdt1, Int_t iso_type2, Double_t iso_bdt2,
                    Int_t iso_type3, Double_t iso_bdt3) {
  // note: if all iso tracks are VELO, returns true!
  // recall iso tracks ordered largest (least isolated) to smallest bdt score
  return add_flags && MAX((iso_type1 != 1) * iso_bdt1, (iso_type2 != 1) * iso_bdt2,
                          (iso_type3 != 1) * iso_bdt3) < 0.15;
}

Double_t WT_ISO(Bool_t add_flags, Double_t iso_bdt1) {
  return static_cast<Double_t>(FLAG_ISO(add_flags, iso_bdt1));
}

Double_t WT_ISO_ANG(Bool_t add_flags, Int_t iso_type1, Double_t iso_bdt1, Int_t iso_type2, Double_t iso_bdt2,
                    Int_t iso_type3, Double_t iso_bdt3) {
  return static_cast<Double_t>(FLAG_ISO_ANG(add_flags, iso_type1, iso_bdt1, iso_type2, iso_bdt2, iso_type3, iso_bdt3));
}

// clang-format off
Bool_t FLAG_DD(Bool_t add_flags,
               Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
               Int_t iso_type1, Int_t iso_type2, Int_t iso_type3,
               Float_t iso_p1, Float_t iso_p2, Float_t iso_p3,
               Float_t iso_pt1, Float_t iso_pt2, Float_t iso_pt3,
               Float_t iso_nnk1, Float_t iso_nnk2, Float_t iso_nnk3, Float_t k_cut,
               Float_t iso_nnghost1, Float_t iso_nnghost2, Float_t iso_nnghost3,
               Float_t ghost_cut) {
  // clang-format on
  auto pid_ok =
      MAX(IF(iso_bdt1 > -1.1, iso_nnk1, 0.0f) * (iso_type1 == 3) * (iso_nnghost1 < ghost_cut),
          IF(iso_bdt2 > -1.1, iso_nnk2, 0.0f) * (iso_type2 == 3) * (iso_nnghost2 < ghost_cut),
          IF(iso_bdt3 > -1.1, iso_nnk3, 0.0f) * (iso_type3 == 3) * (iso_nnghost3 < ghost_cut)) > k_cut;

  auto kinematic_ok = MAX(iso_p1 * (iso_pt1 > 0.15),
                          iso_p2 * (iso_pt2 > 0.15) * (iso_bdt2 > -1.1),
                          iso_p3 * (iso_pt3 > 0.15) * (iso_bdt3 > -1.1)) > 5.0;

  return add_flags && (iso_bdt1 > 0.15) && pid_ok && kinematic_ok;
}

Bool_t FLAG_DD_ANG(Bool_t add_flags, Double_t iso_bdt1, Double_t iso_bdt2,
                   Int_t iso_type1, Int_t iso_type2, Float_t iso_nnk1, Float_t iso_nnk2,
                   Float_t iso_nnghost1, Float_t iso_nnghost2) {
  // note: I'm getting rid of the iso_bdt > -1.1 check! Phoebe only does this for the DD it seems,
  // and the angular analysis doesn't check it anywhere (TODO consider if this is what you really
  // want... iso_bdt=-2 means no track was found...)
  auto pid_ok = MAX(iso_nnk1 * (iso_type1 == 3) * (iso_nnghost1 < 0.2),
                    iso_nnk2 * (iso_type2 == 3) * (iso_nnghost2 < 0.2)) > 0.2;

  auto iso_bdt_ok = MAX(iso_bdt1 * (iso_type1 != 1), iso_bdt2 * (iso_type2 != 1)) > 0.15;

  // note: angular analysis doesn't have the kinematic cleaning cuts for DD
  return add_flags && iso_bdt_ok && pid_ok;
}

// clang-format off
Double_t WT_DD(Bool_t add_flags,
               Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
               Int_t iso_type1, Int_t iso_type2, Int_t iso_type3,
               Float_t iso_p1, Float_t iso_p2, Float_t iso_p3,
               Float_t iso_pt1, Float_t iso_pt2, Float_t iso_pt3,
               Double_t iso_wt1, Double_t iso_wt2,
               Double_t iso_wt3) {
  // clang-format on
  auto kinematic_ok = MAX(iso_p1 * (iso_pt1 > 0.15),
                          iso_p2 * (iso_pt2 > 0.15) * (iso_bdt2 > -1.1),
                          iso_p3 * (iso_pt3 > 0.15) * (iso_bdt3 > -1.1)) > 5.0;
  auto prefac =
      static_cast<Double_t>(kinematic_ok && add_flags && iso_bdt1 > 0.15);

  // This is to translate the 'MAX' PID lines.
  // Think in terms of Venn diagram!
  // No track found: -2. Valid values: [-1, some positive number]
  // So '> -2' and '> -1.1' is the same thing
  //   https://gitlab.cern.ch/bhamilto/rdvsrdst-histfactory/-/blob/master/proc/redoHistos_Dst.C#L1603
  iso_wt1 = IF(iso_bdt1 > -1.1, iso_wt1, 0.0) * (iso_type1 == 3);
  iso_wt2 = IF(iso_bdt2 > -1.1, iso_wt2, 0.0) * (iso_type2 == 3);
  iso_wt3 = IF(iso_bdt3 > -1.1, iso_wt3, 0.0) * (iso_type3 == 3);

  Double_t wt_pid = iso_wt1 + iso_wt2 + iso_wt3 -
                    iso_wt1 * iso_wt2 - iso_wt1 * iso_wt3 -
                    iso_wt2 * iso_wt3 +
                    iso_wt1 * iso_wt2 * iso_wt3;

  return prefac * wt_pid;
}

Double_t WT_DD_ANG(Bool_t add_flags, Double_t iso_bdt1, Double_t iso_bdt2,
                   Int_t iso_type1, Int_t iso_type2,
                   Double_t iso_wt1, Double_t iso_wt2) {
  auto iso_bdt_ok = MAX(iso_bdt1 * (iso_type1 != 1), iso_bdt2 * (iso_type2 != 1)) > 0.15;
  auto prefac = static_cast<Double_t>(add_flags && iso_bdt_ok);

  // This is to translate the 'MAX' PID lines.
  // Think in terms of Venn diagram!
  iso_wt1 = iso_wt1 * (iso_type1 == 3);
  iso_wt2 = iso_wt2 * (iso_type2 == 3);

  Double_t wt_pid = iso_wt1 + iso_wt2 - iso_wt1 * iso_wt2;

  return prefac * wt_pid;
}

// clang-format off
Bool_t FLAG_2OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
                Int_t iso_type1, Int_t iso_type2,
                Float_t iso_p1, Float_t iso_p2,
                Float_t iso_pt1, Float_t iso_pt2,
                Int_t iso_chrg1, Int_t iso_chrg2,
                Float_t iso_nnk1, Float_t iso_nnk2, Float_t k_cut,
                Float_t iso_nnghost1, Float_t iso_nnghost2, Float_t ghost_cut) {
  // clang-format on
  return add_flags && (iso_bdt1 > 0.15) && (iso_bdt2 > 0.15) &&
         (iso_bdt3 < 0.15) && (iso_type1 == 3) && (iso_type2 == 3) &&
         (MAX(iso_p1 * (iso_pt1 > 0.15), iso_p2 * (iso_pt2 > 0.15)) > 5.0) &&
         (iso_chrg1 != iso_chrg2) && (iso_chrg1 * iso_chrg2 != 0) &&
         (iso_chrg1 < 100) && (iso_nnk1 < k_cut) && (iso_nnk2 < k_cut) &&
         (iso_nnghost1 < ghost_cut) && (iso_nnghost2 < ghost_cut);
}

Bool_t FLAG_2OS_ANG(Bool_t add_flags, Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
                    Int_t iso_type1, Int_t iso_type2,
                    Int_t iso_chrg1, Int_t iso_chrg2,
                    Float_t iso_nnk1, Float_t iso_nnk2,
                    Float_t iso_nnghost1, Float_t iso_nnghost2) {
  // note: we don't keep a fourth iso track, so cut won't be exactly the same as angular analysis
  // also, angular analysis uses normal 0.15 cutoff for first iso track bdt, but then uses 0.0 for
  // second and third tracks--probably because of a transcription error (run1 RD(*) has 0.0 in the
  // ANA note table), but I'll follow along with it
  // also, again angular analysis removes kinematic cleaning cuts
  // Double_t bdt1 = -2.0; Double_t bdt2 = -2.0; Double_t bdt3 = -2.0;
  // Bool_t pid_ok = false;
  // Bool_t chrg_ok = false;
  // if (iso_type1==3 && iso_type2==3) {
  //   bdt1 = iso_bdt1; bdt2 = iso_bdt2;
  //   if (iso_type3!=1 && iso_nnghost3 < 0.2) bdt3 = iso_bdt3; ...
  //   pid_ok = iso_nnk1 < 0.2 && iso_nnghost1 < 0.2 && iso_nnk2 < 0.2 && iso_nnghost2 < 0.2;
  //   chrg_ok = (iso_chrg1 + iso_chrg2 == 0);
  // } else if (iso_type1==3 && iso_type3==3) {
  //   bdt1 = iso_bdt1; bdt2 = iso_bdt3;
  //   pid_ok = iso_nnk1 < 0.2 && iso_nnghost1 < 0.2 && iso_nnk3 < 0.2 && iso_nnghost3 < 0.2;
  //   chrg_ok = (iso_chrg1 + iso_chrg3 == 0);
  // } else if (iso_type2==3 && iso_type3==3) {
  //   bdt1 = iso_bdt2; bdt2 = iso_bdt3;
  //   pid_ok = iso_nnk2 < 0.2 && iso_nnghost2 < 0.2 && iso_nnk3 < 0.2 && iso_nnghost3 < 0.2;
  //   chrg_ok = (iso_chrg2 + iso_chrg3 == 0);
  // }
  // return add_flags && bdt1 > 0.15 && bdt2 > 0.0 && bdt3 < 0.0 && chrg_ok && pid_ok;
  return add_flags && (iso_bdt1 > 0.15) && (iso_bdt2 > 0.0) &&
         (iso_bdt3 < 0.0) && (iso_type1 == 3) && (iso_type2 == 3) &&
         (iso_chrg1 + iso_chrg2 == 0) && (iso_nnk1 < 0.2) && (iso_nnk2 < 0.2) &&
         (iso_nnghost1 < 0.2) && (iso_nnghost2 < 0.2);
}

// clang-format off
Double_t WT_2OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
                Int_t iso_type1, Int_t iso_type2,
                Float_t iso_p1, Float_t iso_p2,
                Float_t iso_pt1, Float_t iso_pt2,
                Int_t iso_chrg1, Int_t iso_chrg2,
                Double_t iso_wt1, Double_t iso_wt2) {
  auto prefac = static_cast<Double_t>(
      FLAG_2OS(add_flags,
               iso_bdt1, iso_bdt2, iso_bdt3,
               iso_type1, iso_type2,
               iso_p1, iso_p2,
               iso_pt1, iso_pt2,
               iso_chrg1, iso_chrg2,
               0.0f, 0.0f, 1.0f,
               0.0f, 0.0f, 1.0f));
  // clang-format on
  // need track 1 and 2 to both pass PID cuts here, so take the intersection weight (if no ghost cuts,
  // iso_wti is prob that track i isn't K; if ghost cuts, iso_wti is prob that track i isn't K and
  // isn't ghost)
  return prefac * iso_wt1 * iso_wt2;
}

Double_t WT_2OS_ANG(Bool_t add_flags, Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
                    Int_t iso_type1, Int_t iso_type2,
                    Int_t iso_chrg1, Int_t iso_chrg2,
                    Double_t iso_wt1, Double_t iso_wt2) {
  auto prefac = static_cast<Double_t>(
      FLAG_2OS_ANG(add_flags, iso_bdt1, iso_bdt2, iso_bdt3, iso_type1, iso_type2,
                   iso_chrg1, iso_chrg2, 0.0f, 0.0f, 0.0f, 0.0f));
  return prefac * iso_wt1 * iso_wt2;
}

// clang-format off
// For D** in D0mu sample
Bool_t FLAG_1OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2,
                Int_t iso_type1,
                Float_t iso_p1, Float_t iso_pt1,
                Int_t iso_chrg1,
                Float_t iso_nnk1, Float_t k_cut,
                Float_t iso_nnghost1, Float_t ghost_cut,
                Int_t d0_id) {
  // clang-format on
  return add_flags && (iso_bdt1 > 0.15) && (iso_bdt2 < 0.15) &&
         (iso_type1 == 3) && (iso_p1 > 5.0) && (iso_pt1 > 0.15) &&
         (iso_chrg1 * d0_id) > 0 && (iso_nnk1 < k_cut) && (iso_nnghost1 < ghost_cut);
}

// clang-format off
// For D** in D*mu sample
Bool_t FLAG_1OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2,
                Int_t iso_type1,
                Float_t iso_p1, Float_t iso_pt1,
                Int_t iso_chrg1,
                Float_t iso_nnk1, Float_t k_cut,
                Float_t iso_nnghost1, Float_t ghost_cut,
                Int_t dst_id, Double_t dst_iso_deltam) {
  // clang-format on
  return add_flags && (iso_bdt1 > 0.15) && (iso_bdt2 < 0.15) &&
         (iso_type1 == 3) && (iso_p1 > 5.0) && (iso_pt1 > 0.15) &&
         (iso_chrg1 * dst_id < 0) && (iso_nnk1 < k_cut) && (iso_nnghost1 < ghost_cut) &&
         IN_RANGE(dst_iso_deltam, 0.36, 0.6);  // Phoebe's cut
         // IN_RANGE(dst_iso_invm, 2.4, 2.52)  // Greg's cut
}

Bool_t FLAG_1OS_ANG(Bool_t add_flags, Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
                    Int_t iso_type1, Int_t iso_type2, Float_t iso_p1, Float_t iso_pt1, 
                    Float_t iso_p2, Float_t iso_pt2, Int_t iso_chrg1, Int_t iso_chrg2,
                    Float_t iso_nnk1, Float_t iso_nnk2, Float_t iso_nnghost1, Float_t iso_nnghost2,
                    Int_t d_id, Bool_t d_is_dst) {
  // note: we don't keep a fourth iso track, so cut won't be exactly the same as angular analysis
  // also, angular analysis removes D* mass window cut (so now selection is identical for D0 and
  // D* samples, except for D* you want the extra pi and the D*+ to have opposite charge)
  Double_t bdt1 = -2.0; Double_t bdt2 = 1.0;
  Int_t type1 = 0;
  Double_t p1 = 0.0; Double_t pt1 = 0.0;
  Int_t chrg1 = 0;
  Float_t nnk1 = 1.0; Float_t nnghost1 = 1.0;
  if (iso_type1 != 1) {
    bdt1 = iso_bdt1; type1 = iso_type1; p1 = iso_p1; pt1 = iso_pt1; chrg1 = iso_chrg1;
    nnk1 = iso_nnk1; nnghost1 = iso_nnghost1;
    if (iso_type2 != 1) bdt2 = iso_bdt2;
    else bdt2 = iso_bdt3;
  } else if (iso_type2 != 1) {
    bdt1 = iso_bdt2; type1 = iso_type2; p1 = iso_p2; pt1 = iso_pt2; chrg1 = iso_chrg2;
    nnk1 = iso_nnk2; nnghost1 = iso_nnghost2;
    bdt2 = iso_bdt3;
  }
  if (d_is_dst) chrg1 *= -1;
  return add_flags && (bdt1 > 0.15) && (bdt2 < 0.15) && (type1 == 3) && 
         (p1 > 5.0) && (pt1 > 0.15) && (chrg1 * d_id) > 0 && (nnk1 < 0.2) && (nnghost1 < 0.2);
}

// clang-format off
Double_t WT_1OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2,
                Int_t iso_type1,
                Float_t iso_p1, Float_t iso_pt1,
                Int_t iso_chrg1,
                Double_t iso_wt1,
                Int_t d0_id) {
  auto prefac = static_cast<Double_t>(
      FLAG_1OS(add_flags,
               iso_bdt1, iso_bdt2,
               iso_type1,
               iso_p1, iso_pt1,
               iso_chrg1,
               0.0f, 1.0f,
               0.0f, 1.0f,
               d0_id));
  // clang-format on
  return prefac * iso_wt1;
}

Double_t WT_1OS_ANG(Bool_t add_flags, Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
                    Int_t iso_type1, Int_t iso_type2, Float_t iso_p1, Float_t iso_pt1, 
                    Float_t iso_p2, Float_t iso_pt2, Int_t iso_chrg1, Int_t iso_chrg2,
                    Double_t iso_wt1, Double_t iso_wt2, Int_t d_id, Bool_t d_is_dst) {
  auto prefac = static_cast<Double_t>(
      FLAG_1OS_ANG(add_flags, iso_bdt1, iso_bdt2, iso_bdt3, iso_type1, iso_type2,
                   iso_p1, iso_pt1, iso_p2, iso_pt2, iso_chrg1, iso_chrg2,
                    0.0f, 0.0f, 0.0f, 0.0f, d_id, d_is_dst));
  // clang-format on
  if (iso_type1 != 1) { // first iso track is considered to be pi in FLAG_1OS_ANG
    return prefac * iso_wt1;
  } else if (iso_type2 != 1) { // second iso track is considered to be pi in FLAG_1OS_ANG
    return prefac * iso_wt2;
  } // else reject event for 1OS (prefac should also be 0)
  return 0.0;
}

// clang-format off
// For D** in D*mu sample
Double_t WT_1OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2,
                Int_t iso_type1,
                Float_t iso_p1, Float_t iso_pt1,
                Int_t iso_chrg1,
                Double_t iso_wt1,
                Int_t dst_id, Double_t dst_iso_deltam) {
  auto prefac = static_cast<Double_t>(
      FLAG_1OS(add_flags,
               iso_bdt1, iso_bdt2,
               iso_type1,
               iso_p1, iso_pt1,
               iso_chrg1,
               0.0f, 1.0f,
               0.0f, 1.0f,
               dst_id, dst_iso_deltam)
      );
  // clang-format on
  return prefac * iso_wt1;
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
         (iso_type1 == 3) && (iso_p1 > 15.6) && (iso_pt1 > 0.15) &&
         (iso_chrg1 * d0_id) > 0 && (iso_nnp1 > 0.4);
}

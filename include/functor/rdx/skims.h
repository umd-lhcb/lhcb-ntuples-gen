// Author: Yipeng Sun, Alex Fernez
// NOTE: All kinematic variables are in MeV

#pragma once

#include <TDataType.h>

#include "functor/basic.h"
#include "functor/basic_iso.h"

// Skims ///////////////////////////////////////////////////////////////////////
// NOTE: Units are in GeV!

Bool_t FLAG_ISO(Bool_t add_flags, Double_t iso_bdt1) {
  return add_flags && iso_bdt1 < 0.15;
}

Bool_t FLAG_ISO_ANG(Bool_t add_flags, vector<IsoTrack> nvtracks) {
  // note: nvtracks are all nonvelo tracks, by construction
  // recall iso tracks ordered largest (least isolated) to smallest bdt score
  // this is slightly different than angular analysis; look at all 5 iso tracks, and if all are VELO, return False
  if (nvtracks.size()==0) return false;
  return add_flags && nvtracks[0].iso_bdt<0.15;
}

Double_t WT_ISO(Bool_t add_flags, Double_t iso_bdt1) {
  return static_cast<Double_t>(FLAG_ISO(add_flags, iso_bdt1));
}

Double_t WT_ISO_ANG(Bool_t add_flags, vector<IsoTrack> nvtracks) {
  return static_cast<Double_t>(FLAG_ISO_ANG(add_flags, nvtracks));
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

Bool_t FLAG_DD_ANG(Bool_t add_flags, vector<IsoTrack> nvtracks) {
  // note: no kinematic cleaning cuts as were done for run1 DD
  // only considering two least isolated nonvelo tracks to be kaon, vs 3 least iso for run1 DD
  if (nvtracks.size()<1) return false;
  auto pid_ok = false;
  for (size_t i=0; i<min(size_t(2),nvtracks.size()); i++) {
    pid_ok = nvtracks[i].type==3 && nvtracks[i].NNk>0.2 && nvtracks[i].NNghost<0.2;
    if (pid_ok) break;
  }
  return add_flags && pid_ok && nvtracks[0].iso_bdt>0.15;
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

Double_t WT_DD_ANG(Bool_t add_flags, vector<IsoTrack> nvtracks) {
  // note: no kinematic cleaning cuts as were done for run1 DD
  // only considering two least isolated nonvelo tracks to be kaon, vs 3 least iso for run1 DD
  if (nvtracks.size()<1) return 0.0;
  double wpid;
  if (nvtracks.size()==1) wpid = nvtracks[0].wpid * nvtracks[0].type==3;
  else {wpid = (nvtracks[0].wpid * nvtracks[0].type==3) + (nvtracks[1].wpid * nvtracks[1].type==3) -
               (nvtracks[0].wpid * nvtracks[0].type==3)*(nvtracks[1].wpid * nvtracks[1].type==3);}
  return wpid * add_flags * nvtracks[0].iso_bdt>0.15;
}

// clang-format off
Bool_t FLAG_2OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
                Int_t iso_type1, Int_t iso_type2,
                Float_t iso_p1, Float_t iso_p2,
                Float_t iso_pt1, Float_t iso_pt2,
                Int_t iso_chrg1, Int_t iso_chrg2,
                Float_t iso_nnk1, Float_t iso_nnk2, Float_t iso_nnk3, Float_t k_cut,
                Float_t iso_nnghost1, Float_t iso_nnghost2, Float_t ghost_cut) {
  // clang-format on
  return add_flags && (iso_bdt1 > 0.15) && (iso_bdt2 > 0.15) &&
         (iso_bdt3 < 0.15) && (iso_type1 == 3) && (iso_type2 == 3) &&
         (MAX(iso_p1 * (iso_pt1 > 0.15), iso_p2 * (iso_pt2 > 0.15)) > 5.0) &&
         (iso_chrg1 != iso_chrg2) && (iso_chrg1 * iso_chrg2 != 0) &&
         (iso_chrg1 < 100) && (iso_nnk1 < k_cut) && (iso_nnk2 < k_cut) &&
         (iso_bdt3<-1.1 || iso_nnk3<k_cut) &&
         (iso_nnghost1 < ghost_cut) && (iso_nnghost2 < ghost_cut);
}

Bool_t FLAG_2OS_ANG(Bool_t add_flags, vector<IsoTrack> nvtracks) {
  // note: angular analysis uses normal 0.15 cutoff for first iso track bdt, but then uses 0.0 for
  // second and third tracks--assumedly because run1 RD(*) ANA note not updated (0.0 used to try for higher
  // stats); I'm going to use 0.0 in the hopes of comparing to them
  // also, again angular analysis removes kinematic cleaning cuts
  // charge requirement is also different vs run1 2OS- allows both pions to be neutral, but this should never happen, so irrelevant
  if (nvtracks.size()<3) return false;
  return add_flags && (nvtracks[0].iso_bdt>0.15) && (nvtracks[1].iso_bdt>0.0) && (nvtracks[2].iso_bdt<0.0) && 
         (nvtracks[0].type==3) && (nvtracks[1].type==3) && (nvtracks[0].charge+nvtracks[1].charge==0) && 
         (nvtracks[0].NNk<0.2) && (nvtracks[1].NNk<0.2) && (nvtracks[0].NNghost<0.2) && (nvtracks[1].NNghost<0.2);
}

// clang-format off
Double_t WT_2OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
                Int_t iso_type1, Int_t iso_type2,
                Float_t iso_p1, Float_t iso_p2,
                Float_t iso_pt1, Float_t iso_pt2,
                Int_t iso_chrg1, Int_t iso_chrg2,
                Double_t iso_wt1, Double_t iso_wt2, Double_t iso_wt3) {
  auto prefac = static_cast<Double_t>(
      FLAG_2OS(add_flags,
               iso_bdt1, iso_bdt2, iso_bdt3,
               iso_type1, iso_type2,
               iso_p1, iso_p2,
               iso_pt1, iso_pt2,
               iso_chrg1, iso_chrg2,
               0.0f, 0.0f, 0.0f, 1.0f,
               0.0f, 0.0f, 1.0f));
  // clang-format on
  // need track 1 and 2 to both pass PID cuts here, so take the intersection weight (if no ghost cuts,
  // iso_wti is prob that track i isn't K; if ghost cuts, iso_wti is prob that track i isn't K and
  // isn't ghost)
  Double_t iso_wt3_or = (iso_bdt3<-1.1 ? 1. : iso_wt3);
  return prefac * iso_wt1 * iso_wt2 * iso_wt3_or;
}

Double_t WT_2OS_ANG(Bool_t add_flags, vector<IsoTrack> nvtracks) {
  if (nvtracks.size()<3) return 0.0;
  return nvtracks[0].wpid * nvtracks[1].wpid * 
         (add_flags && (nvtracks[0].iso_bdt>0.15) && (nvtracks[1].iso_bdt>0.0) && (nvtracks[2].iso_bdt<0.0) && 
          (nvtracks[0].type==3) && (nvtracks[1].type==3) && (nvtracks[0].charge+nvtracks[1].charge==0));
}

// clang-format off
// For D** in D0mu sample
Bool_t FLAG_1OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
                Int_t iso_type1,
                Float_t iso_p1, Float_t iso_pt1,
                Int_t iso_chrg1,
                Float_t iso_nnk1, Float_t iso_nnk2, Float_t iso_nnk3, Float_t k_cut,
                Float_t iso_nnghost1, Float_t ghost_cut,
                Int_t d0_id) {
  // clang-format on
  return add_flags && (iso_bdt1 > 0.15) && (iso_bdt2 < 0.15) &&
    (iso_type1 == 3) && (iso_p1 > 5.0) && (iso_pt1 > 0.15) &&
    (iso_bdt2<-1.1 || iso_nnk2<k_cut) && (iso_bdt3<-1.1 || iso_nnk3<k_cut) &&
    (iso_chrg1 * d0_id) > 0 && (iso_nnk1 < k_cut) && (iso_nnghost1 < ghost_cut);
}

// clang-format off
// For D** in D*mu sample
Bool_t FLAG_1OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
                Int_t iso_type1,
                Float_t iso_p1, Float_t iso_pt1,
                Int_t iso_chrg1,
                Float_t iso_nnk1, Float_t iso_nnk2, Float_t iso_nnk3, Float_t k_cut,
                Float_t iso_nnghost1, Float_t ghost_cut,
                Int_t dst_id, Double_t dst_iso_deltam) {
  // clang-format on
  return add_flags && (iso_bdt1 > 0.15) && (iso_bdt2 < 0.15) &&
    (iso_type1 == 3) && (iso_p1 > 5.0) && (iso_pt1 > 0.15) &&
    (iso_chrg1 * dst_id < 0) && (iso_nnk1 < k_cut) && (iso_nnghost1 < ghost_cut) &&
    (iso_bdt2<-1.1 || iso_nnk2<k_cut) && (iso_bdt3<-1.1 || iso_nnk3<k_cut) &&
    IN_RANGE(dst_iso_deltam, 0.36, 0.6);  // Phoebe's cut
         // IN_RANGE(dst_iso_invm, 2.4, 2.52)  // Greg's cut
}

Bool_t FLAG_1OS_ANG(Bool_t add_flags, vector<IsoTrack> nvtracks, Int_t d_id, Bool_t is_d0) {
  // angular analysis removes D* mass window cut (so now selection is identical for D0 and
  // D* samples, except for D* you want the extra pi and the D*+ to have opposite charge)
  if (nvtracks.size()<2) return false;
  return add_flags && (nvtracks[0].iso_bdt>0.15) && (nvtracks[1].iso_bdt<0.15) && (nvtracks[0].type==3) && 
         (nvtracks[0].p.P()>5.0) && (nvtracks[0].p.Pt()>0.15) && nvtracks[0].charge*d_id*(2*is_d0-1)>0 &&
         (nvtracks[0].NNk<0.2) && (nvtracks[0].NNghost<0.2);
}

// clang-format off
Double_t WT_1OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
                Int_t iso_type1,
                Float_t iso_p1, Float_t iso_pt1,
                Int_t iso_chrg1,
                Double_t iso_wt1, Double_t iso_wt2, Double_t iso_wt3, 
                Int_t d0_id) {
  auto prefac = static_cast<Double_t>(
      FLAG_1OS(add_flags,
               iso_bdt1, iso_bdt2, iso_bdt3,
               iso_type1,
               iso_p1, iso_pt1,
               iso_chrg1,
               0.0f, 0.0f, 0.0f, 1.0f,
               0.0f, 1.0f,
               d0_id));
  // clang-format on
  Double_t iso_wt2_or = (iso_bdt2<-1.1 ? 1. : iso_wt2);
  Double_t iso_wt3_or = (iso_bdt3<-1.1 ? 1. : iso_wt3);
  return prefac * iso_wt1 * iso_wt2_or * iso_wt3_or;
}

Double_t WT_1OS_ANG(Bool_t add_flags, vector<IsoTrack> nvtracks, Int_t d_id, Bool_t is_d0) {
  if (nvtracks.size()<2) return false;
  return nvtracks[0].wpid * (add_flags && (nvtracks[0].iso_bdt>0.15) && (nvtracks[1].iso_bdt<0.15) && (nvtracks[0].type==3) && 
                             (nvtracks[0].p.P()>5.0) && (nvtracks[0].p.Pt()>0.15) && nvtracks[0].charge*d_id*(2*is_d0-1)>0);
}

// clang-format off
// For D** in D*mu sample
Double_t WT_1OS(Bool_t add_flags,
                Double_t iso_bdt1, Double_t iso_bdt2, Double_t iso_bdt3,
                Int_t iso_type1,
                Float_t iso_p1, Float_t iso_pt1,
                Int_t iso_chrg1,
                Double_t iso_wt1, Double_t iso_wt2, Double_t iso_wt3, 
                Int_t dst_id, Double_t dst_iso_deltam) {
  auto prefac = static_cast<Double_t>(
      FLAG_1OS(add_flags,
               iso_bdt1, iso_bdt2, iso_bdt3,
               iso_type1,
               iso_p1, iso_pt1,
               iso_chrg1,
               0.0f, 0.0f, 0.0f, 1.0f,
               0.0f, 1.0f,
               dst_id, dst_iso_deltam)
      );
  // clang-format on
  Double_t iso_wt2_or = (iso_bdt2<-1.1 ? 1. : iso_wt2);
  Double_t iso_wt3_or = (iso_bdt3<-1.1 ? 1. : iso_wt3);
  return prefac * iso_wt1 * iso_wt2_or * iso_wt3_or;
}
// clang-format off
// Only define proton-enriched skim for D0 sample
Bool_t FLAG_PROT(Bool_t add_flags,
                 Double_t iso_bdt1, Double_t iso_bdt2,
                 Int_t iso_type1,
                 Float_t iso_p1, Float_t iso_pt1,
                 Int_t iso_chrg1,
                 Float_t iso_nnp1,
                 Float_t iso_nnghost1, Float_t ghost_cut,
                 Int_t d0_id) {
  // clang-format on
  return add_flags && (iso_bdt1 > 0.15) && (iso_bdt2 < 0.15) &&
         (iso_type1 == 3) && (iso_p1 > 15.6) && (iso_pt1 > 0.15) &&
         (iso_chrg1 * d0_id) > 0 && (iso_nnp1 > 0.4) && (iso_nnghost1 < ghost_cut);
}

// Efficiency for proton PID cut, mocking up D** as Lambdas
Double_t WT_ISO_PROT(Int_t true_id, Double_t w_pi, Double_t w_k, Double_t w_p,
                    Double_t w_e, Double_t w_mu, Double_t w_ghost, int mc_id) {
  true_id = ABS(true_id);
  //if(mc_id==11874430 || mc_id==11874440 || mc_id==12873450 || mc_id==12873460) return w_p;
  if (true_id == 2212) return w_p;
  if (true_id == 211) return w_pi;
  if (true_id == 321) return w_k;
  if (true_id == 11) return w_e;
  if (true_id == 13) return w_mu;
  return w_ghost;
}

Double_t WT_PROT(Bool_t add_flags,
                 Double_t iso_bdt1, Double_t iso_bdt2,
                 Int_t iso_type1, Float_t iso_p1, Float_t iso_pt1,
                 Int_t iso_chrg1, Int_t d0_id,
                 Int_t true_id, Double_t w_pi, Double_t w_k, Double_t w_p,
                 Double_t w_e, Double_t w_mu, Double_t w_ghost, int mc_id) {
  // clang-format on
  auto prefac = static_cast<Double_t>(
               add_flags && (iso_bdt1 > 0.15) && (iso_bdt2 < 0.15) &&
               (iso_type1 == 3) && (iso_p1 > 15.6) && (iso_pt1 > 0.15) &&
               (iso_chrg1 * d0_id) > 0);
  
  return prefac * WT_ISO_PROT(true_id, w_pi, w_k, w_p, w_e, w_mu, w_ghost, mc_id);
}

// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Fri Sep 11, 2020 at 09:03 PM +0800
//
//  _______  _______  _______  _______           _______
//  ___________________________ (  ____ \(  ____ )(  ___  )(  ____ \|\     /|(
//  ____ \\__   __/\__   __/\__   __/ | (    \/| (    )|| (   ) || (    \/| ) (
//  || (    \/   ) (      ) (      ) ( | (_____ | (____)|| (___) || |      |
//  (___) || (__       | |      | |      | |
//  (_____  )|  _____)|  ___  || | ____ |  ___  ||  __)      | |      | |      |
//  |
//        ) || (      | (   ) || | \_  )| (   ) || (         | |      | |      |
//        |
//  /\____) || )      | )   ( || (___) || )   ( || (____/\   | |      | |   ___)
//  (___
//  \_______)|/       |/     \|(_______)|/     \|(_______/   )_(      )_(
//  \_______/

#ifndef _LNG_FUNCTOR_FLAG_H_
#define _LNG_FUNCTOR_FLAG_H_

#include <TMath.h>
#include <TROOT.h>

#include <vector>

#include "functor/basic.h"

// Flags ///////////////////////////////////////////////////////////////////////

std::vector<std::vector<Bool_t> > MC_FLAGS(
    Int_t mu_mom_key, Int_t d0_mom_key, Int_t dst_mom_key, Int_t mu_gd_mom_key,
    Int_t dst_gd_mom_key, Int_t mu_gd_gd_mom_key, Int_t dst_gd_gd_mom_key) {
  // Initialize flags
  std::vector<std::vector<Bool_t> > flags;
  for (auto i = 0; i < 4; i++) {
    flags.push_back(std::vector<Bool_t>({false, false, false}));
  }
  // Conversion table
  // Phoebe        this
  // ----------    --------
  // onezero       [0][0]
  // twozero       [0][1]
  // ...
  // oneone        [1][0]
  // ...
  // threetwo      [3][1]
  // threethree    [3][2]

  if (mu_mom_key == d0_mom_key && mu_mom_key > 0) flags[0][0] = true;
  if (mu_gd_mom_key == d0_mom_key && d0_mom_key > 0) flags[0][1] = true;
  if (mu_gd_gd_mom_key == d0_mom_key && mu_gd_gd_mom_key > 0)
    flags[0][2] = true;

  if (mu_mom_key == dst_mom_key && mu_mom_key > 0) flags[1][0] = true;
  if (mu_mom_key == dst_gd_mom_key && mu_mom_key > 0) flags[1][1] = true;
  if (mu_mom_key == dst_gd_gd_mom_key && mu_mom_key > 0) flags[1][2] = true;

  if (mu_gd_mom_key == dst_mom_key && mu_gd_mom_key > 0) flags[2][0] = true;
  if (mu_gd_mom_key == dst_gd_mom_key && mu_gd_mom_key > 0) flags[2][1] = true;
  if (mu_gd_mom_key == dst_gd_gd_mom_key && mu_gd_mom_key > 0)
    flags[2][2] = true;

  if (mu_gd_gd_mom_key == dst_mom_key && mu_gd_gd_mom_key > 0)
    flags[3][0] = true;
  if (mu_gd_gd_mom_key == dst_gd_mom_key && mu_gd_gd_mom_key > 0)
    flags[3][1] = true;
  if (mu_gd_gd_mom_key == dst_gd_gd_mom_key && mu_gd_gd_mom_key > 0)
    flags[3][2] = true;

  return flags;
}

Bool_t FLAG_DST_SB() {
  Bool_t flag_dst_sb = false;

  return flag_dst_sb;
}

Bool_t FLAG_TAU(std::vector<std::vector<Bool_t> > mc_flags, Int_t mu_true_id,
                Int_t mu_mom_id, Int_t mu_gd_mom_id) {
  auto abs_mu_true_id   = TMath::Abs(mu_true_id);
  auto abs_mu_mom_id    = TMath::Abs(mu_mom_id);
  auto abs_mu_gd_mom_id = TMath::Abs(mu_gd_mom_id);

  auto mu_gd_mom_possible_ids = std::vector<Int_t>({511, 521, 531});
  if (VEC_OR(mc_flags[2]) && abs_mu_true_id == 13 && abs_mu_mom_id == 15 &&
      VEC_OR_EQ(mu_gd_mom_possible_ids, abs_mu_gd_mom_id))
    return true;

  return false;
}

// Other flags /////////////////////////////////////////////////////////////////

Bool_t IS_DATA(ULong64_t time) {
  // Special treatment for some run 1 data: We remove some real data if they
  // fall within a specific time window
  // FIXME: Ask Phoebe why
  if (time > 0 && (time <= 1345.7332e12 || time >= 1345.7335e12))
    return true;
  else
    return false;
}

Bool_t JUST_DST(std::vector<std::vector<Bool_t> >& mc_flags, Int_t mu_mom_id,
                Int_t dst_mom_id) {
  Bool_t just_dst = false;

  auto abs_mu_mom_id  = TMath::Abs(mu_mom_id);
  auto abs_dst_mom_id = TMath::Abs(dst_mom_id);

  auto mu_mom_possible_ids  = std::vector<Int_t>({411, 421, 431});
  auto dst_mom_possible_ids = std::vector<Int_t>({511, 521, 531});
  if ((VEC_OR(mc_flags[2]) || VEC_OR(mc_flags[3])) &&  /* LN2779 */
      VEC_OR_EQ(mu_mom_possible_ids, abs_mu_mom_id) && /* LN2779 */
      VEC_OR_EQ(dst_mom_possible_ids, abs_dst_mom_id) /* LN2836 */)
    just_dst = true;

  return just_dst;
}

Bool_t DST_OK(Int_t d0_bkg_cat, Int_t dst_bkg_cat) {
  // NOTE: Weird background classifier bug (for run 1, at least).
  //       If D0 has survived cuts then it can't possibly be CAT 50 (low mass
  //       background - missed fine state particle).
  if (dst_bkg_cat == 0 || (dst_bkg_cat == 50 && d0_bkg_cat == 50)) return true;
  return false;
}

// Types ///////////////////////////////////////////////////////////////////////

Int_t B_TYPE(std::vector<std::vector<Bool_t> >& mc_flags, Int_t mu_true_id,
             Int_t mu_mom_id, Int_t mu_gd_mom_id, Int_t dst_mom_id,
             Int_t dst_gd_mom_id, Int_t dst_gd_gd_mom_id) {
  Int_t b_type = 0;

  auto abs_mu_true_id       = TMath::Abs(mu_true_id);
  auto abs_mu_mom_id        = TMath::Abs(mu_mom_id);
  auto abs_mu_gd_mom_id     = TMath::Abs(mu_gd_mom_id);
  auto abs_dst_mom_id       = TMath::Abs(dst_mom_id);
  auto abs_dst_gd_mom_id    = TMath::Abs(dst_gd_mom_id);
  auto abs_dst_gd_gd_mom_id = TMath::Abs(dst_gd_gd_mom_id);

  if ((mc_flags[0][0] || mc_flags[0][1]) && abs_mu_true_id == 13)
    b_type = TMath::Abs(mu_mom_id);

  auto mu_ancestor_possible_ids = std::vector<Int_t>({511, 521, 531});
  if ((VEC_OR(mc_flags[1]) || mc_flags[0][0]) && abs_mu_true_id == 13 &&
      VEC_OR_EQ(mu_ancestor_possible_ids, abs_mu_mom_id))
    b_type = abs_mu_mom_id;

  if ((VEC_OR(mc_flags[2]) || mc_flags[0][1]) && abs_mu_true_id == 13 &&
      abs_mu_mom_id == 15 &&
      VEC_OR_EQ(mu_ancestor_possible_ids, abs_mu_gd_mom_id))
    b_type = abs_mu_gd_mom_id;

  // LN2779
  // NOTE: We don't need the is_data flag. Because all these branches are
  //       MC-only, and these flags will be automatically skipped for data.
  auto mu_mom_possible_ids = std::vector<Int_t>({411, 421, 431});
  if ((VEC_OR(mc_flags[2]) || VEC_OR(mc_flags[3])) &&
      VEC_OR_EQ(mu_mom_possible_ids, abs_mu_mom_id)) {
    // LN2836
    auto dst_possible_ids = std::vector<Int_t>({511, 521, 531});
    if (VEC_OR_EQ(dst_possible_ids, abs_dst_mom_id))
      b_type = abs_dst_mom_id;
    else if (VEC_OR_EQ(dst_possible_ids, abs_dst_gd_mom_id))
      b_type = abs_dst_gd_mom_id;
    else if (VEC_OR_EQ(dst_possible_ids, abs_dst_gd_gd_mom_id))
      b_type = abs_dst_gd_gd_mom_id;
    // FIXME: There's a else clause in Phoebe's spaghetti which set b_type to
    // -1,
    //        but that one is never executed.
    // FIXME: Also don't understand the utility of `flagD0mu`
  }

  return b_type;
}

Int_t DSS_TYPE(std::vector<std::vector<Bool_t> >& mc_flags, Int_t mu_mom_id,
               Int_t dst_mom_id, Int_t dst_gd_mom_id, Int_t dst_gd_gd_mom_id) {
  Int_t dss_type = 0;

  auto abs_mu_mom_id        = TMath::Abs(mu_mom_id);
  auto abs_dst_mom_id       = TMath::Abs(dst_mom_id);
  auto abs_dst_gd_mom_id    = TMath::Abs(dst_gd_mom_id);
  auto abs_dst_gd_gd_mom_id = TMath::Abs(dst_gd_gd_mom_id);

  // LN2779
  // NOTE: We don't need the is_data flag. Because all these branches are
  //       MC-only, and these flags will be automatically skipped for data.
  auto mu_mom_possible_ids = std::vector<Int_t>({411, 421, 431});
  if ((VEC_OR(mc_flags[2]) || VEC_OR(mc_flags[3])) &&
      VEC_OR_EQ(mu_mom_possible_ids, abs_mu_mom_id)) {
    // FIXME: In LN2836, dss_type can never be set because we have conflicting
    // if
    //        conditions, here I deviate from Phoebe's.
    auto dst_possible_ids = std::vector<Int_t>({511, 521, 531});
    if (VEC_OR_EQ(dst_possible_ids, abs_dst_gd_mom_id))
      dss_type = abs_dst_mom_id;
    else if (VEC_OR_EQ(dst_possible_ids, abs_dst_gd_gd_mom_id))
      dss_type = -1;
  }

  return dss_type;
}

#endif

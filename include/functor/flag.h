// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Tue Sep 15, 2020 at 12:20 AM +0800

#ifndef _LNG_FUNCTOR_FLAG_H_
#define _LNG_FUNCTOR_FLAG_H_

#include <TMath.h>
#include <TROOT.h>

#include <vector>

#include "functor/basic.h"

// Flags ///////////////////////////////////////////////////////////////////////

// Original name: oneone, onetwo, ... (See LN2711-2712)
// Current name: mc_flags or v_mc_flags (all flags put in a vector)
// Meaning: Flags for decay modes.
// Defined in: AddB.C, LN2724-2754
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

// Original name: flagtaumu
// Current name: flag_tau
// Meaning: MC semi-tauonic B decay
// Defined in: AddB.C, LN2481, LN2743-2746
Bool_t FLAG_TAU(std::vector<std::vector<Bool_t> >& mc_flags, Int_t mu_true_id,
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

// Original name: flagBmu
// Current name: flag_mu
// Meaning: MC semi-muonic B decay
// Defined in: AddB.C, LN2479, LN2742-2747
Bool_t FLAG_MU(std::vector<std::vector<Bool_t> >& mc_flags, Int_t mu_true_id,
               Int_t mu_mom_id) {
  auto abs_mu_true_id = TMath::Abs(mu_true_id);
  auto abs_mu_mom_id  = TMath::Abs(mu_mom_id);

  auto mu_mom_possible_ids = std::vector<Int_t>({511, 521, 531});
  if (VEC_OR(mc_flags[1]) && abs_mu_true_id == 13 &&
      VEC_OR_EQ(mu_mom_possible_ids, abs_mu_mom_id))
    return true;

  return false;
}

// Original name: flagTauonicD
// Current name: flag_two_d_tau
// Meaning: MC semitauonic with tau from 431 (D+_s) and with two D mesons
// Defined in: AddB.C, LN2497, LN2791-2792
Bool_t FLAG_TWO_D_TAU(Int_t mu_mom_id, Int_t mu_gd_mom_id) {
  auto abs_mu_mom_id    = TMath::Abs(mu_mom_id);
  auto abs_mu_gd_mom_id = TMath::Abs(mu_gd_mom_id);

  if (abs_mu_mom_id == 15 && abs_mu_gd_mom_id == 431) return true;

  return false;
}

// Original name: flagDoubleD
// Current name: flag_two_d_mu
// Meaning: MC semimuonic with mu from (411, 421, or 431) and two D mesons
// Defined in: AddB.C, LN2496, LN2754, LN2759, LN4362
Bool_t FLAG_TWO_D_MU(std::vector<std::vector<Bool_t> >& mc_flags,
                     Int_t mu_mom_id, Int_t mu_gd_gd_mom_id, Int_t dst_mom_id) {
  auto abs_mu_mom_id       = TMath::Abs(mu_mom_id);
  auto abs_mu_gd_gd_mom_id = TMath::Abs(mu_gd_gd_mom_id);
  auto abs_dst_mom_id      = TMath::Abs(dst_mom_id);

  auto mu_gd_gd_mom_possible_ids = std::vector<Int_t>({10433, 20433});
  auto dst_mom_possible_ids      = std::vector<Int_t>({511, 521, 531});
  // LN2754
  if (VEC_OR_EQ(mu_gd_gd_mom_possible_ids, abs_mu_gd_gd_mom_id) &&
      VEC_OR_EQ(dst_mom_possible_ids, abs_dst_mom_id))
    return true;

  // LN2759
  auto mu_mom_possible_ids = std::vector<Int_t>({411, 421, 431});
  if ((VEC_OR(mc_flags[2]) || VEC_OR(mc_flags[3])) &&
      VEC_OR_EQ(mu_mom_possible_ids, abs_mu_mom_id))
    return true;

  return false;
}

// Other flags /////////////////////////////////////////////////////////////////

// Original name: isData
// Current name: is_data
// Meaning: True if event is real data, and not in a time window where real data
//          was bad
// Defined in: AddB.C, LN2435, LN2439
Bool_t IS_DATA(ULong64_t time) {
  // Special treatment for some run 1 data: We remove some real data if they
  // fall within a specific time window.
  // This narrow time window has some of the physical variables (B mass maybe?)
  // wrong, so we discard them
  if (time > 0 && (time <= 1345.7332e12 || time >= 1345.7335e12)) return true;
  return false;
}

// Original name: justDst
// Current name: just_dst
// Meaning: D* from B, not D**
// Defined in: AddB.C, LN2478, LN2816
Bool_t JUST_DST(std::vector<std::vector<Bool_t> >& mc_flags, Int_t mu_mom_id,
                Int_t dst_mom_id) {
  auto abs_mu_mom_id  = TMath::Abs(mu_mom_id);
  auto abs_dst_mom_id = TMath::Abs(dst_mom_id);

  auto mu_mom_possible_ids  = std::vector<Int_t>({411, 421, 431});
  auto dst_mom_possible_ids = std::vector<Int_t>({511, 521, 531});
  if ((VEC_OR(mc_flags[2]) || VEC_OR(mc_flags[3])) &&  /* LN2779 */
      VEC_OR_EQ(mu_mom_possible_ids, abs_mu_mom_id) && /* LN2779 */
      VEC_OR_EQ(dst_mom_possible_ids, abs_dst_mom_id) /* LN2836 */)
    return true;

  return false;
}

// Original name: justDst
// Current name: just_dst
// Meaning: D* from B, not D**
// Defined in: AddB.C, LN2478, LN2816
Bool_t DST_OK(Int_t d0_bkg_cat, Int_t dst_bkg_cat) {
  // NOTE: Weird background classifier bug (for run 1, at least).
  //       If D0 has survived cuts then it can't possibly be CAT 50 (low mass
  //       background - missed fine state particle).
  if (dst_bkg_cat == 0 || (dst_bkg_cat == 50 && d0_bkg_cat == 50)) return true;
  return false;
}

// Types ///////////////////////////////////////////////////////////////////////

// Original name: Btype: b_type
// Current name: b_type
// Meaning: type of B meson (B0==511, B-==521, B0_s==531)
// Defined in: AddB.C, LN2485, LN2740-2753, LN2814-2837 (obsolete, according to
//             Phoebe), LN2841-2862
Int_t B_TYPE(std::vector<std::vector<Bool_t> >& mc_flags, Bool_t flag_d0_mu,
             Int_t mu_true_id, Int_t mu_mom_id, Int_t mu_gd_mom_id,
             Int_t dst_mom_id, Int_t dst_gd_mom_id, Int_t dst_gd_gd_mom_id) {
  Int_t b_type = 0;

  auto abs_mu_true_id       = TMath::Abs(mu_true_id);
  auto abs_mu_mom_id        = TMath::Abs(mu_mom_id);
  auto abs_mu_gd_mom_id     = TMath::Abs(mu_gd_mom_id);
  auto abs_dst_mom_id       = TMath::Abs(dst_mom_id);
  auto abs_dst_gd_mom_id    = TMath::Abs(dst_gd_mom_id);
  auto abs_dst_gd_gd_mom_id = TMath::Abs(dst_gd_gd_mom_id);

  // LN2740
  if ((mc_flags[0][0] || mc_flags[0][1]) && abs_mu_true_id == 13)
    b_type = abs_mu_mom_id;

  auto mu_ancestor_possible_ids = std::vector<Int_t>({511, 521, 531});
  // LN2742, LN2744, LN2747, LN2748-2750
  if ((VEC_OR(mc_flags[1]) || mc_flags[0][0]) && abs_mu_true_id == 13 &&
      VEC_OR_EQ(mu_ancestor_possible_ids, abs_mu_mom_id))
    b_type = abs_mu_mom_id;

  // LN2743, LN2745-2746, LN2751-2753
  if ((VEC_OR(mc_flags[2]) || mc_flags[0][1]) && abs_mu_true_id == 13 &&
      abs_mu_mom_id == 15 &&
      VEC_OR_EQ(mu_ancestor_possible_ids, abs_mu_gd_mom_id))
    b_type = abs_mu_gd_mom_id;

  auto dst_ancester_possible_ids = mu_ancestor_possible_ids;
  if (!flag_d0_mu) {                                          /* LN2841 */
    if (VEC_OR_EQ(dst_ancester_possible_ids, abs_dst_mom_id)) /* LN2843 */
      b_type = abs_dst_mom_id;
    else if (VEC_OR_EQ(dst_ancester_possible_ids, abs_dst_gd_mom_id))
      // LN2848
      b_type = abs_dst_gd_mom_id;
    else if (VEC_OR_EQ(dst_ancester_possible_ids, abs_dst_gd_gd_mom_id))
      // LN2853
      b_type = abs_dst_gd_gd_mom_id;
  } else
    b_type = -1;  // LN2860

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

// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Fri Apr 30, 2021 at 03:07 PM +0200

#ifndef _LNG_FUNCTOR_RDX_FLAG_H_
#define _LNG_FUNCTOR_RDX_FLAG_H_

#include <Math/Vector4D.h>
#include <Math/Vector4Dfwd.h>
#include <TMath.h>
#include <TROOT.h>
#include <TVector3.h>

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

  // 10433: D+_s1(2536)
  // 20433: D+_s1(2460)
  // 511: B0
  // 521: B+
  // 531: B0_s
  auto mu_gd_gd_mom_possible_ids = std::vector<Int_t>({10433, 20433});
  auto dst_mom_possible_ids      = std::vector<Int_t>({511, 521, 531});
  // LN2754
  if (VEC_OR_EQ(mu_gd_gd_mom_possible_ids, abs_mu_gd_gd_mom_id) &&
      VEC_OR_EQ(dst_mom_possible_ids, abs_dst_mom_id))
    return true;

  // 411: D+
  // 421: D-
  // 431: D+_s
  // LN2759
  auto mu_mom_possible_ids = std::vector<Int_t>({411, 421, 431});
  if ((VEC_OR(mc_flags[2]) || VEC_OR(mc_flags[3])) &&
      VEC_OR_EQ(mu_mom_possible_ids, abs_mu_mom_id))
    return true;

  return false;
}

// Original name: flagD0mu
// Current name: flag_d0_mu
// Meaning: MC B -> D0 mu decay
// Defined in: AddB.C, LN2495, LN2740
Bool_t FLAG_D0_MU(std::vector<std::vector<Bool_t> >& mc_flags,
                  Int_t                              mu_true_id) {
  if ((mc_flags[0][0] || mc_flags[0][1]) && TMath::Abs(mu_true_id) == 13)
    return true;
  return false;
}

// Global selection flags for run 1 ////////////////////////////////////////////

// NOTE: These P and PT variables are in GeV, NOT the default MeV!!
//       Selections are based on Run 1 R(D(*)) ANA, v2020.07.31, p.11, Table 6.
// clang-format off
Bool_t FLAG_SEL_D0_RUN1(Double_t k_pt, Double_t pi_pt,
                        Double_t k_p, Double_t pi_p,
                        Bool_t k_hlt1_tos, Bool_t pi_hlt1_tos,
                        Double_t k_ip_chi2, Double_t pi_ip_chi2,
                        Double_t k_pid_k, Double_t pi_pid_k,
                        Double_t k_gh_prob, Double_t pi_gh_prob,
                        Bool_t mu_veto,
                        Double_t d0_pt,
                        Bool_t d0_hlt2,
                        Double_t d0_endvtx_chi2, Double_t d0_endvtx_ndof,
                        Double_t d0_ip, Double_t d0_ip_chi2,
                        Double_t d0_dira,
                        Double_t d0_fd_chi2,
                        Double_t d0_m) {
  // clang-format on
  auto d0_m_ref = 1865.49;

  // clang-format off
  if (/* K, pi */
      ((k_hlt1_tos && k_pt > 1.7) || (pi_hlt1_tos && pi_pt > 1.7)) &&
      k_pt > 0.8 && pi_pt > 0.8 && k_pt+pi_pt > 1.4 &&  /* AddB.C, LN2554 */
      (k_hlt1_tos || pi_hlt1_tos) &&  /* AddB.C, LN2572 */
      ////
      k_p > 2 && pi_p > 2 &&
      k_ip_chi2 > 45 && pi_ip_chi2 > 45 &&
      /* The sum of 2 PT are trivially true */
      k_pid_k > 4 && pi_pid_k < 2 &&
      !mu_veto &&  /* Equivalent to: neither K nor Pi is Mu */
      k_gh_prob < 0.5 && pi_gh_prob < 0.5 &&
      /* D0 */
      d0_pt > 2 &&
      d0_hlt2 &&
      d0_endvtx_chi2/d0_endvtx_ndof < 4 &&
      TMath::Log(d0_ip) > -3.5 &&
      d0_ip_chi2 > 9 &&
      d0_dira > 0.9998 &&
      d0_fd_chi2 > 250 &&
      TMath::Abs(d0_m - d0_m_ref) < 23.4  /* This is in MeV!!! */
      )
    // clang-format on
    return true;
  return false;
}

Bool_t FLAG_SEL_GOOD_TRACKS(TVector3              ref_trk,
                            std::vector<TVector3> other_trks) {
  for (auto v3_other : other_trks) {
    auto inner_prod = ref_trk.Dot(v3_other);
    auto magnitude  = ref_trk.Mag() * v3_other.Mag();

    if (TMath::Log10(1 - inner_prod / magnitude) <= -6.5) return false;
  }
  return true;
}

// clang-format off
Bool_t FLAG_SEL_MU_RUN1(Double_t mu_p,
                        Double_t mu_eta,
                        Bool_t mu_is_mu,
                        Double_t mu_pid_mu, Double_t mu_pid_e,
                        Double_t mu_bdt_mu,
                        Bool_t good_trks) {
  if (/* PID related */
      mu_is_mu && mu_pid_mu > 2 && mu_pid_e < 1 && mu_bdt_mu > 0.25 &&
      /* Momentum */
      mu_p > 3 && mu_p < 100 &&
      /* Acceptance */
      mu_eta > 1.7 && mu_eta < 5. &&
      /* If tracks are well-separated angularly */
      good_trks
      )
    // clang-format on
    return true;
  return false;
}

// clang-format off
Bool_t FLAG_SEL_BMINUSD0_RUN1(Bool_t flag_sel_d0, Bool_t flag_sel_mu,
                              Double_t b_endvtx_chi2, Double_t b_endvtx_ndof,
                              Double_t b_fd_trans,
                              Double_t b_dira,
                              Double_t b_m,
                              Double_t mu_px, Double_t mu_py, Double_t mu_pz,
                              Double_t d0_px, Double_t d0_py, Double_t d0_pz,
                              Double_t d0_m) {
  const Double_t pi_m = 139.57;
  const Double_t d0_m_diff = 165.;

  auto v4_mu_pi_m = ROOT::Math::PxPyPzMVector(mu_px, mu_py, mu_pz, pi_m);
  auto v4_d0 = ROOT::Math::PxPyPzMVector(d0_px, d0_py, d0_pz, d0_m);
  auto v4_d0_pi_m = v4_mu_pi_m + v4_d0;
  auto d0_m_pi_m = v4_d0_pi_m.M();

  if (/* Daughter particles */
      flag_sel_d0 && flag_sel_mu &&
      /* FD */
      b_fd_trans < 7. &&
      /* Vertex quality */
      b_endvtx_chi2/b_endvtx_ndof < 6 && b_dira > 0.9995 &&
      /* Mass */
      b_m < 5200 &&
      /* Replace Muon mass hypothesis */
      TMath::Abs(d0_m_pi_m - d0_m) > d0_m_diff
      )
    // clang-format on
    return true;
  return false;
}

// NOTE: These P and PT variables are in GeV, NOT the default MeV!!
//       Selections are based on Run 1 R(D(*)) ANA, v2020.07.31, p.11, Table 8.
// NOTE: The following cuts are missing from Table 6, and are recovered in
// AddB.C:
//       mu_ip_chi2 > 45
//       mu_gh_prob < 0.5
Bool_t FLAG_SEL_B0DST_RUN1(Bool_t flag_sel_d0, Double_t spi_gh_prob,
                           Double_t dst_endvtx_chi2, Double_t dst_endvtx_ndof,
                           Double_t dst_m, Double_t d0_m, Bool_t mu_is_mu,
                           Double_t mu_p, Double_t mu_eta, Double_t mu_pid_mu,
                           Double_t mu_pid_e, Double_t mu_ip_chi2,
                           Double_t mu_gh_prob, TVector3 v3_mu_p,
                           TVector3 v3_k_p, TVector3 v3_pi_p, TVector3 v3_spi_p,
                           Double_t b0_discard_mu_chi2, Double_t b0_endvtx_chi2,
                           Double_t b0_endvtx_ndof, Double_t b0_fd_trans,
                           Double_t b0_dira, Double_t b0_m, Double_t iso_bdt) {
  auto dst_d0_delta_m_ref = 145.454;

  auto track_well_separated = true;
  for (auto v3_p : std::vector<TVector3>{v3_k_p, v3_pi_p, v3_spi_p}) {
    auto inner_prod = v3_mu_p.Dot(v3_p);
    auto magnitude  = v3_mu_p.Mag() * v3_p.Mag();

    if (TMath::Log10(1 - inner_prod / magnitude) <= -6.5) {
      track_well_separated = false;
      break;
    }
  }

  // clang-format off
  if (flag_sel_d0 && /* For D*, we require it to pass all D0 selections */
      /* slow Pi */
      spi_gh_prob < 0.25 &&
      /* D* */
      dst_endvtx_chi2/dst_endvtx_ndof < 10 &&
      TMath::Abs(dst_m - d0_m - dst_d0_delta_m_ref) < 2 &&
      /* Mu */
      mu_is_mu &&
      (mu_p > 3 && mu_p < 100) &&
      (mu_eta > 1.7 && mu_eta < 5) &&
      mu_pid_mu > 2 &&
      mu_pid_e < 1 &&
      mu_ip_chi2 > 45 &&   /* AddB.C, LN2562 */
      mu_gh_prob < 0.5 &&  /* AddB.C, LN2563 */
      track_well_separated &&
      /* D0 Mu combo, already applied in DaVinci */
      /* D* Mu combo */
      b0_discard_mu_chi2 <= 6 &&  /* AddB.C, LN2567 */
      b0_endvtx_chi2 < 24 &&  /* FIXME: AddB.C, LN2569, different from ANA! */
      b0_endvtx_chi2/b0_endvtx_ndof < 6 &&
      b0_fd_trans < 7 &&
      b0_dira > 0.9995 &&
      b0_m < 5280 /* MeV! */ &&
      iso_bdt < 0.15
      )
    // clang-format on
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

// Original name: ishigher
// Current name: is_2pi
// Meaning: 2S D** instead of 1P D**? Phoebe says check if 2pi cocktail member
// Defined in: AddB.C, LN3255-3269
Bool_t IS_2PI(Bool_t flag_mu, Bool_t just_dst, Bool_t dst_ok, Bool_t mu_pid,
              Int_t dst_mom_id, Int_t dst_gd_mom_id) {
  auto abs_dst_mom_id    = TMath::Abs(dst_mom_id);
  auto abs_dst_gd_mom_id = TMath::Abs(dst_gd_mom_id);

  auto dst_mom_possible_ids =
      std::vector<Int_t>({100411, 100421, 100413, 100423});
  auto dst_gd_mom_possible_ids = std::vector<Int_t>({511, 521});
  // LN3258-3267
  // FIXME: `CocktailHigher` is not defined anywhere!
  if (flag_mu && !just_dst && dst_ok && mu_pid &&
      VEC_OR_EQ(dst_mom_possible_ids, abs_dst_mom_id) &&
      VEC_OR_EQ(dst_gd_mom_possible_ids, abs_dst_gd_mom_id))
    return true;
  return false;
}

// Original name: justDst
// Current name: just_dst
// Meaning: D* from B, not D**
// Defined in: AddB.C, LN2478, LN2816
Bool_t JUST_DST(Int_t dst_mom_id) {
  auto abs_dst_mom_id = TMath::Abs(dst_mom_id);

  auto dst_mom_possible_ids = std::vector<Int_t>({511, 521, 531});
  if (VEC_OR_EQ(dst_mom_possible_ids, abs_dst_mom_id) /* LN2814 */) return true;

  return false;
}

// Original name: DstOk
// Current name: dst_ok
// Meaning: Workaround weird background classifier bug.
//          If D0 has survived cuts then it can't possibly be CAT 50 (low mass
//          background - missed fine state particle).
// Defined in: AddB.C, LN2476, LN2547
Bool_t DST_OK(Int_t d0_bkg_cat, Int_t dst_bkg_cat) {
  if (dst_bkg_cat == 0 || (dst_bkg_cat == 50 && d0_bkg_cat == 50)) return true;
  return false;
}

// Types ///////////////////////////////////////////////////////////////////////

// Original name: Btype
// Current name: b_type
// Meaning: Type of B meson (B0==511, B-==521, B0_s==531)
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
    else
      b_type = -1;  // LN2862
  }

  return b_type;
}

// Original name: Dststtype
// Current name: dss_type
// Meaning: Type of D** (D1+==10413, D10==10423, D2*+==415, D2*0==425,
//          Ds2*==435, D1'+==20413, D1'0==20423, Ds1'==10433?)
// Defined in: AddB.C, LN2498, LN2814-2837 (obsolete, according to Phoebe),
//             LN2841-2862
Int_t DSS_TYPE(Bool_t flag_d0_mu, Int_t dst_mom_id, Int_t dst_gd_mom_id,
               Int_t dst_gd_gd_mom_id) {
  Int_t dss_type = 0;

  auto abs_dst_mom_id       = TMath::Abs(dst_mom_id);
  auto abs_dst_gd_mom_id    = TMath::Abs(dst_gd_mom_id);
  auto abs_dst_gd_gd_mom_id = TMath::Abs(dst_gd_gd_mom_id);

  auto dst_ancester_possible_ids = std::vector<Int_t>({511, 521, 531});
  if (!flag_d0_mu) { /* LN2841 */
    if (VEC_OR_EQ(dst_ancester_possible_ids, abs_dst_gd_mom_id))
      // LN2848
      dss_type = abs_dst_mom_id;
    else if (VEC_OR_EQ(dst_ancester_possible_ids, abs_dst_gd_gd_mom_id))
      // LN2853
      dss_type = -1;
  }

  return dss_type;
}

#endif

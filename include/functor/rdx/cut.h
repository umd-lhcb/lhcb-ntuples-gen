// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Thu Jun 24, 2021 at 05:48 AM +0200

#ifndef _LNG_FUNCTOR_RDX_CUT_H_
#define _LNG_FUNCTOR_RDX_CUT_H_

#include <Math/Vector3D.h>
#include <Math/Vector4D.h>
#include <TMath.h>
#include <TVector3.h>

#include <vector>

#include "functor/basic.h"
#include "pdg.h"

// Run 1 DaVinci cuts //////////////////////////////////////////////////////////
// Here we should assume all variables are in their original DaVinci units.
// WARN: Here all kinematic variables are in MeV

// NOTE: We can't have too many inputs variables (up to 32 for input+output) as
//       numpy doesn't support that
// clang-format off
Bool_t FLAG_SEL_RUN1_STRIP(Double_t mu_ip_chi2, Double_t mu_gh_prob,
                           Double_t mu_pid_mu, Double_t mu_p,
                           Double_t mu_tr_chi2ndof,
                           Double_t k_pid_k, Double_t k_ip_chi2,
                           Double_t k_p, Double_t k_pt, Double_t k_gh_prob,
                           Double_t pi_pid_k, Double_t pi_ip_chi2,
                           Double_t pi_p, Double_t pi_pt, Double_t pi_gh_prob,
                           Double_t d0_mm,
                           Double_t d0_endvtx_chi2, Double_t d0_endvtx_ndof,
                           Double_t d0_fd_chi2, Double_t d0_dira) {
  // clang-format on
  auto mu_cuts = (mu_ip_chi2 > 45.0) && (mu_gh_prob < 0.5) && (mu_pid_mu > 2) &&
                 (mu_p > 3000.0) && (mu_tr_chi2ndof < 3.0);
  auto k_cuts = (k_pid_k > 4.0) && (k_ip_chi2 > 45.0) && (k_p > 2000.0) &&
                (k_pt > 300.0) && (k_gh_prob < 0.5);
  auto pi_cuts = (pi_pid_k < 2.0) && (pi_ip_chi2 > 45.0) && (pi_p > 2000.0) &&
                 (pi_pt > 300.0) && (pi_gh_prob < 0.5);
  auto k_pi_cuts = (k_pt + pi_pt > 1400.0);
  auto d0_cuts   = (TMath::Abs(d0_mm - PDG_M_D0) < 80.0) &&
                 (d0_endvtx_chi2 / d0_endvtx_ndof < 4.0) &&
                 (d0_fd_chi2 > 250.0) && (d0_dira > 0.9998);

  return mu_cuts && k_cuts && pi_cuts && k_pi_cuts && d0_cuts;
}

// clang-format off
Bool_t FLAG_SEL_RUN1_DV(Double_t spi_ip_chi2, Double_t spi_gh_prob,
                        Double_t spi_tr_chi2ndof,
                        Double_t d0_m,
                        Double_t dst_mm, Double_t dst_m,
                        Double_t dst_endvtx_chi2, Double_t dst_endvtx_ndof,
                        Double_t b0_mm,
                        Double_t b0_endvtx_chi2, Double_t b0_endvtx_ndof,
                        Double_t b0_dira) {
  // clang-format on
  auto spi_cuts =
      (spi_ip_chi2 > 0.0) && (spi_gh_prob < 0.25) && (spi_tr_chi2ndof < 3.0);
  auto dst_cuts = (TMath::Abs(dst_mm - PDG_M_Dst) < 125.0) &&
                  (dst_endvtx_chi2 / dst_endvtx_ndof < 100.0);
  auto d0_dst_cuts = (dst_m - d0_m < 160.0);
  auto b0_cuts     = (0.0 < b0_mm && b0_mm < 10000.0) &&
                 (b0_endvtx_chi2 / b0_endvtx_ndof < 6.0) && (b0_dira > 0.9995);

  return spi_cuts && dst_cuts && d0_dst_cuts && b0_cuts;
}

// Run 2 DaVinci cuts //////////////////////////////////////////////////////////
// WARN: Here all kinematic variables are in MeV

// clang-format off
Bool_t FLAG_SEL_RUN2_STRIP(Double_t mu_ip_chi2, Double_t mu_gh_prob,
                           Double_t mu_pid_mu, Double_t mu_p,
                           Double_t mu_tr_chi2ndof,
                           Double_t k_pid_k, Double_t k_ip_chi2,
                           Double_t k_p, Double_t k_pt, Double_t k_gh_prob,
                           Double_t pi_pid_k, Double_t pi_ip_chi2,
                           Double_t pi_p, Double_t pi_pt, Double_t pi_gh_prob,
                           Double_t d0_mm,
                           Double_t d0_endvtx_chi2, Double_t d0_endvtx_ndof,
                           Double_t d0_fd_chi2, Double_t d0_dira) {
  // clang-format on
  auto mu_cuts = (mu_ip_chi2 > 16.0) && (mu_gh_prob < 0.5) &&
                 (mu_pid_mu > -200) && (mu_p > 3000.0) &&
                 (mu_tr_chi2ndof < 3.0);
  auto k_cuts = (k_pid_k > 4.0) && (k_ip_chi2 > 9.0) && (k_p > 2000.0) &&
                (k_pt > 300.0) && (k_gh_prob < 0.5);
  auto pi_cuts = (pi_pid_k < 2.0) && (pi_ip_chi2 > 9.0) && (pi_p > 2000.0) &&
                 (pi_pt > 300.0) && (pi_gh_prob < 0.5);
  auto k_pi_cuts = (k_pt + pi_pt > 2500.0);
  auto d0_cuts   = (TMath::Abs(d0_mm - PDG_M_D0) < 80.0) &&
                 (d0_endvtx_chi2 / d0_endvtx_ndof < 4.0) &&
                 (d0_fd_chi2 > 25.0) && (d0_dira > 0.999);

  return mu_cuts && k_cuts && pi_cuts && k_pi_cuts && d0_cuts;
}

Bool_t FLAG_SEL_RUN2_DV(Double_t spi_ip_chi2, Double_t spi_gh_prob,
                        Double_t spi_tr_chi2ndof, Double_t d0_m,
                        Double_t dst_mm, Double_t dst_m,
                        Double_t dst_endvtx_chi2, Double_t dst_endvtx_ndof,
                        Double_t b0_mm, Double_t b0_endvtx_chi2,
                        Double_t b0_endvtx_ndof, Double_t b0_dira) {
  // clang-format on
  auto spi_cuts =
      (spi_ip_chi2 > 0.0) && (spi_gh_prob < 0.25) && (spi_tr_chi2ndof < 3.0);
  auto dst_cuts = (TMath::Abs(dst_mm - PDG_M_Dst) < 125.0) &&
                  (dst_endvtx_chi2 / dst_endvtx_ndof < 100.0);
  auto d0_dst_cuts = (dst_m - d0_m < 160.0);
  auto b0_cuts     = (0.0 < b0_mm && b0_mm < 10000.0) &&
                 (b0_endvtx_chi2 / b0_endvtx_ndof < 6.0) && (b0_dira > 0.999);

  return spi_cuts && dst_cuts && d0_dst_cuts && b0_cuts;
}

// Global selection flags for run 1 ////////////////////////////////////////////
// WARN: Here all kinematic variables are in GeV, except for mass (still in MeV)
// Selections are based on Run 1 R(D(*)) ANA, v2020.07.31, p.11, Table 6.

Bool_t FLAG_SEL_D0_PID_OK_RUN1(Double_t k_pid_k, Double_t pi_pid_k,
                               Bool_t k_is_mu, Bool_t pi_is_mu) {
  return k_pid_k > 4 && pi_pid_k < 2 && !k_is_mu && !pi_is_mu;
}

// NOTE: These P and PT variables are in GeV, NOT the default MeV!!
// clang-format off
Bool_t FLAG_SEL_D0_RUN1(Bool_t flag_d0_pid_ok,
                        Double_t k_pt, Double_t pi_pt,
                        Double_t k_p, Double_t pi_p,
                        Bool_t k_hlt1_tos, Bool_t pi_hlt1_tos,
                        Double_t k_ip_chi2, Double_t pi_ip_chi2,
                        Double_t k_gh_prob, Double_t pi_gh_prob,
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
  if (flag_d0_pid_ok &&
      /* K, pi */
      ((k_hlt1_tos && k_pt > 1.7) || (pi_hlt1_tos && pi_pt > 1.7)) &&
      k_pt > 0.8 && pi_pt > 0.8 && k_pt+pi_pt > 1.4 &&  /* AddB.C, LN2554 */
      //(k_hlt1_tos || pi_hlt1_tos) &&  /* AddB.C, LN2572, this is redundant */
      ////
      k_p > 2 && pi_p > 2 &&
      k_ip_chi2 > 45 && pi_ip_chi2 > 45 &&
      k_gh_prob < 0.5 && pi_gh_prob < 0.5 &&
      /* D0 */
      d0_pt > 2 &&
      d0_hlt2 &&
      d0_endvtx_chi2/d0_endvtx_ndof < 4 &&
      TMath::Log(d0_ip) > -3.5 &&
      d0_ip_chi2 > 9 &&
      d0_dira > 0.9998 &&  /* should be loosed for run 2 */
      d0_fd_chi2 > 250 &&
      TMath::Abs(d0_m - d0_m_ref) < 23.4  /* This is in MeV!!! */
      )
    // clang-format on
    return true;
  return false;
}

Bool_t FLAG_SEL_GOOD_TRACKS(ROOT::Math::XYZVector              ref_trk,
                            std::vector<ROOT::Math::XYZVector> other_trks) {
  for (auto v3_other : other_trks) {
    auto inner_prod = ref_trk.Dot(v3_other);
    auto magnitude  = TMath::Sqrt(ref_trk.Mag2() * v3_other.Mag2());

    if (TMath::Log10(1 - inner_prod / magnitude) <= -6.5) return false;
  }
  return true;
}

Bool_t FLAG_SEL_MU_PID_OK_RUN1(Bool_t mu_is_mu, Double_t mu_pid_mu,
                               Double_t mu_pid_e, Double_t mu_bdt_mu) {
  return mu_is_mu && mu_pid_mu > 2 && mu_pid_e < 1 && mu_bdt_mu > 0.25;
}

// clang-format off
Bool_t FLAG_SEL_MU_RUN1(Bool_t flag_good_trks, Bool_t flag_mu_pid_ok,
                        Double_t mu_p,
                        Double_t mu_eta,
                        Double_t mu_ip_chi2, Double_t mu_gh_prob
                        ) {
  if (/* If tracks are well-separated angularly */
      flag_good_trks &&
      /* Mu PID related */
      flag_mu_pid_ok &&
      /* Momentum */
      mu_p > 3 && mu_p < 100 &&
      /* Acceptance */
      mu_eta > 1.7 && mu_eta < 5. &&
      /* Track quality */
      mu_ip_chi2 > 45 && mu_gh_prob < 0.5
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
  // clang-format on
  const Double_t pi_m      = 139.57;
  const Double_t d0_m_diff = 165.;

  // Alternative mass hypothesis, where we now assume Muon is a Pion
  auto v4_mu_pi_m = ROOT::Math::PxPyPzMVector(mu_px, mu_py, mu_pz, pi_m);
  auto v4_d0      = ROOT::Math::PxPyPzMVector(d0_px, d0_py, d0_pz, d0_m);
  auto v4_d0_pi_m = v4_mu_pi_m + v4_d0;
  auto d0_m_pi_m  = v4_d0_pi_m.M();

  // clang-format off
  if (/* Daughter particles */
      flag_sel_d0 && flag_sel_mu &&
      /* FD */
      b_fd_trans < 7 &&
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
//       Selections are based on Run 1 R(D(*)) ANA, v2020.07.31, p.11,
//       Table 8.
// NOTE: The following cuts are missing from Table 6, and are recovered in
// AddB.C:
//       mu_ip_chi2 > 45
//       mu_gh_prob < 0.5
// clang-format off
Bool_t FLAG_SEL_B0DST_RUN1(Bool_t flag_sel_d0, Bool_t flag_sel_mu,
                           Double_t spi_gh_prob,
                           Double_t dst_endvtx_chi2, Double_t dst_endvtx_ndof,
                           Double_t dst_m, Double_t d0_m,
                           // Double_t b0_discard_mu_chi2,
                           Double_t b0_endvtx_chi2, Double_t b0_endvtx_ndof,
                           Double_t b0_fd_trans,
                           Double_t b0_dira,
                           Double_t b0_m) {
  // clang-format on
  auto dst_d0_delta_m_ref = 145.454;

  // clang-format off
  if (flag_sel_d0 && flag_sel_mu &&
      /* slow Pi */
      spi_gh_prob < 0.25 &&
      /* D* */
      dst_endvtx_chi2/dst_endvtx_ndof < 10 &&
      TMath::Abs(dst_m - d0_m - dst_d0_delta_m_ref) < 2 &&
      /* D0 Mu combo, already applied in DaVinci */
      /* D* Mu combo */
      // b0_discard_mu_chi2 <= 6 &&  // AddB.C, LN2567, but not in ANA!
      b0_endvtx_chi2 < 24 &&  /* FIXME: AddB.C, LN2569, different from ANA! */
      b0_endvtx_chi2/b0_endvtx_ndof < 6 &&
      b0_fd_trans < 7 &&
      b0_dira > 0.9995 &&
      b0_m < 5280 /* MeV! */
      )
    // clang-format on
    return true;
  return false;
}

#endif

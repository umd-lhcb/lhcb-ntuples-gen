// Author: Yipeng Sun, Svende Braun
// License: BSD 2-clause
// Last Change: Thu Mar 23, 2023 at 10:15 PM -0400
// NOTE: All kinematic variables are in MeV

#pragma once

#include <Math/Vector3D.h>
#include <Math/Vector4D.h>
#include <TMath.h>
#include <TRandom.h>
#include <assert.h>
#include <vector>

#include "functor/basic.h"
#include "pdg.h"

using std::vector;

// Run 1 DaVinci cuts //////////////////////////////////////////////////////////
// Here we should assume all variables are in their original DaVinci units.

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
// Selections are based on Run 1 R(D(*)) ANA, v2020.07.31, p.11, Table 6.

Bool_t FLAG_SEL_D0_PID_OK_RUN1(Double_t k_pid_k, Double_t pi_pid_k,
                               Bool_t k_is_mu, Bool_t pi_is_mu) {
  return k_pid_k > 4.0 && pi_pid_k < 2.0 && !k_is_mu && !pi_is_mu;
}

// clang-format off
Bool_t FLAG_SEL_D0_RUN1(Bool_t flag_d0_pid_ok,
                        Double_t k_pt, Double_t pi_pt,
                        Bool_t k_hlt1_tos, Bool_t pi_hlt1_tos,
                        Double_t k_ip_chi2, Double_t pi_ip_chi2,
                        Double_t k_gh_prob, Double_t pi_gh_prob,
                        Double_t d0_pt,
                        Bool_t d0_hlt2,
                        Double_t d0_endvtx_chi2, Double_t d0_endvtx_ndof,
                        Double_t d0_ip, Double_t d0_ip_chi2,
                        Double_t d0_dira,
                        Double_t d0_fd_chi2) {
  if (flag_d0_pid_ok &&
      /* K, pi */
      ((k_hlt1_tos && k_pt > 1700.0) || (pi_hlt1_tos && pi_pt > 1700.0)) &&
      k_pt > 500.0 && pi_pt > 500.0 && k_pt+pi_pt > 1400.0 &&
      k_ip_chi2 > 45.0 && pi_ip_chi2 > 45.0 &&
      k_gh_prob < 0.5 && pi_gh_prob < 0.5 &&
      /* D0 */
      d0_pt > 2000.0 &&
      d0_hlt2 && // TODO: Alex--why is this here? I assume relic debugging thing? It's manually set to true
      d0_endvtx_chi2/d0_endvtx_ndof < 4.0 &&
      TMath::Log(d0_ip) > -3.5 &&
      d0_ip_chi2 > 9.0 &&
      d0_dira > 0.9998 &&  /* should be loosed for run 2 */
      d0_fd_chi2 > 250.0
      )
    // clang-format on
    return true;
  return false;
}

Bool_t FLAG_SEL_D0_RUN2ANG(Bool_t flag_d0_pid_ok,
                         //  Double_t k_pt, Double_t pi_pt,
                         //  Bool_t k_hlt1_tos, Bool_t pi_hlt1_tos,
                         //  Double_t k_ip_chi2, Double_t pi_ip_chi2,
                         //  Double_t k_gh_prob, Double_t pi_gh_prob,
                         //  Double_t d0_pt,
                         //  Double_t d0_endvtx_chi2, Double_t d0_endvtx_ndof,
                           Double_t d0_ip, Double_t d0_ip_chi2) {
                         //  Double_t d0_dira,
                         //  Double_t d0_fd_chi2) {
  if (flag_d0_pid_ok &&
      /* K, pi */
      // ((k_hlt1_tos && k_pt > 1700.0) || (pi_hlt1_tos && pi_pt > 1700.0)) &&
      // k_pt > 500.0 && pi_pt > 500.0 && k_pt+pi_pt > 1400.0 &&
      // k_ip_chi2 > 45.0 && pi_ip_chi2 > 45.0 &&
      // k_gh_prob < 0.5 && pi_gh_prob < 0.5 &&
      /* D0 */
      // d0_pt > 2000.0 &&
      // d0_endvtx_chi2/d0_endvtx_ndof < 4.0 &&
      TMath::Log(d0_ip) > -3.5 &&
      d0_ip_chi2 > 9.0 //&&
      // d0_dira > 0.999 &&
      // d0_fd_chi2 > 250.0
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

    if (TMath::Log10(1.0 - inner_prod / magnitude) <= -6.5) return false;
  }
  return true;
}

Bool_t FLAG_SEL_MU_PID_OK_RUN1(Bool_t mu_is_mu, Double_t mu_pid_mu,
                               Double_t mu_pid_e) {
  return mu_is_mu && mu_pid_mu > 2.0 && mu_pid_e < 1.0;
}

Bool_t FLAG_SEL_MU_PID_OK_RUN2ANG(Bool_t mu_is_mu, Double_t mu_pid_mu,
                                  Double_t mu_pid_e) {
  return mu_is_mu && mu_pid_mu > 2.0 && mu_pid_e < 1.0;
}

// clang-format off
Bool_t FLAG_SEL_MU_RUN1(Bool_t flag_mu_pid_ok, Bool_t flag_good_trks,
                        Double_t mu_p,
                        Double_t mu_eta, Bool_t mu_hasMuon,
                        Double_t mu_ip_chi2, Double_t mu_gh_prob) {
  if (/* If tracks are well-separated angularly */
      flag_good_trks &&
      /* Mu PID related */
      flag_mu_pid_ok &&
      /* Momentum */
      IN_RANGE(mu_p, 3.0e3, 100.0e3) &&
      /* Acceptance */
      IN_RANGE(mu_eta, 1.7, 5.0) && mu_hasMuon &&
      /* Track quality */
      mu_ip_chi2 > 45.0 && mu_gh_prob < 0.5
      )
    // clang-format on
    return true;
  return false;
}

Bool_t FLAG_SEL_MU_RUN2ANG(Bool_t flag_mu_pid_ok_loose, Bool_t flag_good_trks,
                           Double_t mu_p,
                           Double_t mu_eta) {
                        //   Double_t mu_ip_chi2,
                        //   Double_t mu_gh_prob) {
  if (/* If tracks are well-separated angularly */
      flag_good_trks &&
      /* Mu PID related */
      flag_mu_pid_ok_loose &&
      /* Momentum */
      IN_RANGE(mu_p, 3.0e3, 100.0e3) &&
      /* Acceptance */
      IN_RANGE(mu_eta, 1.7, 5.0) //&&
      /* Track quality */
      // mu_ip_chi2 > 45.0 && 
      // mu_gh_prob < 0.5
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
                              Double_t d0_dst_veto_deltam) {
  // clang-format off
  if (/* Daughter particles */
      flag_sel_d0 && flag_sel_mu &&
      /* FD */
      b_fd_trans < 7.0 &&
      /* Vertex quality */
      b_endvtx_chi2 / b_endvtx_ndof < 6.0 && b_dira > 0.9995 &&
      /* Veto D* in D0 sample */
      d0_dst_veto_deltam > 4.0  // MeV!
      )
    // clang-format on
    return true;
  return false;
}

Bool_t FLAG_SEL_BMINUSD0_RUN2ANG(Bool_t flag_sel_d0_loose, Bool_t flag_sel_mu_loose,
                                 Double_t b_endvtx_chi2, Double_t b_endvtx_ndof,
                                 Double_t b_fd_trans,
                                 Double_t b_dira,
                                 Double_t d0_dst_veto_deltam) {
  // clang-format off
  if (/* Daughter particles */
      flag_sel_d0_loose && flag_sel_mu_loose &&
      /* FD */
      b_fd_trans < 7.0 &&
      /* Vertex quality */
      b_endvtx_chi2 / b_endvtx_ndof < 6.0 && b_dira > 0.999 &&
      /* Veto D* in D0 sample */
      d0_dst_veto_deltam > 4.0  // MeV!
      )
    // clang-format on
    return true;
  return false;
}

// Selections are based on Run 1 R(D(*)) ANA, v2020.07.31, p.11, Table 8.
// NOTE: The following cuts are missing from Table 6, and are recovered in
// AddB.C:
//       mu_ip_chi2 > 45
//       mu_gh_prob < 0.5
// clang-format off
Bool_t FLAG_SEL_B0DST_RUN1(Bool_t flag_sel_d0, Bool_t flag_sel_mu,
                           Double_t spi_gh_prob,
                           Double_t dst_endvtx_chi2, Double_t dst_endvtx_ndof,
                           Double_t b0_discard_mu_chi2,
                           Double_t b0_endvtx_chi2, Double_t b0_endvtx_ndof,
                           Double_t b0_fd_trans,
                           Double_t b0_dira) {
  // clang-format off
  if (flag_sel_d0 && flag_sel_mu &&
      /* slow Pi */
      spi_gh_prob < 0.25 &&
      /* D* */
      dst_endvtx_chi2 / dst_endvtx_ndof < 10.0 &&
      /* D* Mu combo */
      b0_discard_mu_chi2 < 6.0 &&  // this is actually the D0Mu chi2
      // Alex: note to self--what about D0mu DIRA > 0.9995? TODO
      b0_endvtx_chi2 < 24.0 &&
      b0_endvtx_chi2 / b0_endvtx_ndof < 6.0 &&
      b0_fd_trans < 7.0 &&
      b0_dira > 0.9995
      )
    // clang-format on
    return true;
  return false;
}

// RUN2ANG cuts are the cuts that the run2 angular analysis uses (which, in turn, were
// the loosest cuts we found could be applied [TODO document presentations])
Bool_t FLAG_SEL_B0DST_RUN2ANG(Bool_t flag_sel_d0_loose, Bool_t flag_sel_mu_loose,
                              // Double_t spi_gh_prob,
                              Double_t dst_endvtx_chi2, Double_t dst_endvtx_ndof,
                              // Double_t b0_discard_mu_chi2,
                              Double_t b0_endvtx_chi2, Double_t b0_endvtx_ndof,
                              Double_t b0_fd_trans,
                              Double_t b0_dira) {

  if (flag_sel_d0_loose && flag_sel_mu_loose &&
      /* slow Pi */
      // spi_gh_prob < 0.25 &&
      /* D* */
      dst_endvtx_chi2 / dst_endvtx_ndof < 10.0 &&
      /* D* Mu combo */
      // b0_discard_mu_chi2 < 6.0 &&  // this is actually the D0Mu chi2 // TODO not sure if this should be applied?
      // b0_endvtx_chi2 < 24.0 &&
      b0_endvtx_chi2 / b0_endvtx_ndof < 6.0 &&
      b0_fd_trans < 7.0 &&
      b0_dira > 0.999
      )
    // clang-format on
    return true;
  return false;
}

// D mass-window cuts //////////////////////////////////////////////////////////

Bool_t FLAG_SEL_D0_MASS(Double_t d0_m, Double_t d0_m_ref = 1864.83) {
  return ABS(d0_m - d0_m_ref) < 23.4;
}

Bool_t FLAG_SEL_D0_MASS_HYPO(Double_t d0_m, Double_t d0_m_pi_m) {
  /* Replace Muon mass hypothesis */
  if (d0_m_pi_m - d0_m > 165.0) return true;
  return false;
}

Bool_t FLAG_SEL_D0_MASS_HYPO(Double_t mu_px, Double_t mu_py, Double_t mu_pz,
                             Double_t d0_px, Double_t d0_py, Double_t d0_pz,
                             Double_t d0_m) {
  const Double_t pi_m = 139.57;

  // Alternative mass hypothesis, where we now assume Muon is a Pion
  auto v4_mu_pi_m = ROOT::Math::PxPyPzMVector(mu_px, mu_py, mu_pz, pi_m);
  auto v4_d0      = ROOT::Math::PxPyPzMVector(d0_px, d0_py, d0_pz, d0_m);
  auto v4_d0_pi_m = v4_mu_pi_m + v4_d0;
  auto d0_m_pi_m  = v4_d0_pi_m.M();

  return FLAG_SEL_D0_MASS_HYPO(d0_m, d0_m_pi_m);
}

Bool_t FLAG_SEL_DST_MASS(Double_t dst_m, Double_t d0_m) {
  auto dst_ref_deltam = ABS(dst_m - d0_m - 145.454);
  return dst_ref_deltam < 2.0;
}

// B mass cuts /////////////////////////////////////////////////////////////////

Bool_t FLAG_SEL_BMINUS_MASS(Double_t b_m) { return b_m < 5200.0; }

Bool_t FLAG_SEL_BMINUS_MASS_SB(Double_t b_m) { return b_m > 5400.0; }

Bool_t FLAG_SEL_B0_MASS(Double_t b0_m) { return b0_m < 5280.0; }

Bool_t FLAG_SEL_B0_MASS_SB(Double_t b0_m) { return b0_m > 5400.0; }

// DD branching fraction weights ////////////////////////////////////////////////

Double_t WT_DD_BF(int mu_mom_id) {
  Double_t wt = 0.0;
  if (ABS(mu_mom_id) == 411) wt = 0.1607;
  if (ABS(mu_mom_id) == 421) wt = 0.0649;
  if (ABS(mu_mom_id) == 431) wt = 0.0709;
  return wt;
}

Double_t WT_MISS_DstDK(int year) {
  // Missing DstDK needs to be reweighted to reflect rel BFs of related modes in already produced DDX
  // [what was requested is in square brackets]
  // Previously simulated 11894600- 2015: 37.68 [26.82], 2016: 208.89 [154.36], 2017: 214.13 [160.93], 2018: 282.22 [205.26] (million)
  // Simulated 11895400 (missing DstDK) [expect 1.5*0.066 x above]- 2015: 0?, 2016: 25.03 [15.26], 2017: 25.32 [15.91], 2018: 25.52 [20.29]
  double rel_bf_sum = (0.0020+0.0018+0.0033) / 
                        (0.0118+0.0053+0.0020+0.0079+0.0118+0.0018+0.0018+0.0033+0.0017+0.0033+0.000203+0.000406+0.000547+
                         0.0006+0.0012+0.0012+0.0024+0.0042+0.0040+0.00107+0.0003+0.0005+0.0011+0.0024+0.0025+0.0025+0.0005+
                         0.0005+0.0005+0.0010+0.0022+0.0022+0.0037+0.0037+0.0010+0.0062+0.00033+0.0004+0.0043+0.0054);
  double isospin_fac = 1.5;
  double n_2015_prev = 18643389 + 19035403;
  double n_2016_prev = 108049987 + 100838019;
  double n_2017_prev = 109024813 + 105104194;
  double n_2018_prev = 140117141 + 142106832;
  double n_2016 = 12314931 + 12717396;
  double n_2017 = 12518386 + 12797493;
  double n_2018 = 12787255 + 12731332;
  if (year==2016) return (isospin_fac * rel_bf_sum * n_2016_prev)/n_2016;
  if (year==2017) return (isospin_fac * rel_bf_sum * n_2017_prev)/n_2017;
  if (year==2018) return (isospin_fac * rel_bf_sum * n_2018_prev)/n_2018;
  assert(false); // shouldn't be looking at any other year than these
}

Double_t WT_MISS_DstDspi(int year, int mc_id) {
  // Missing DstDspi needs to be reweighted relative to already produced DDX
  // Missing DstDspi is used for both D* and D0 sample (D0 sample already contained DDspi, which doesn't
  // need to be reweighted); naively, choose to reweight missing DstDspi to be 10% of D* DDX BF
  // (so x/(1+x)=0.1 => x=0.111, ie. 11.1% of current total D* DDX MC))
  // [what was requested is in square brackets]
  // Previously simulated 11894610- 2015: 13.98 [9.51], 2016: 94.37 [54.70], 2017: 78.58 [57.03], 2018: 98.34 [72.74] (million)
  // Previously simulated 12895400- 2015: 6.04 [3.84], 2016: 39.35 [22.11], 2017: 41.90 [23.05], 2018: 38.25 [29.40] (million)
  // Simulated 11894400 (missing D*Dspi)- 2015: 0?, 2016: 12.34 [xx], 2017: 18.00 [xx], 2018: 14.17 [xx]
  // Simulated 12895410 (missing D*Dspi)- 2015: 0?, 2016: 12.57 [xx], 2017: 16.53 [xx], 2018: 12.94 [xx]
  double frac = 0.111;
  if (year==2016) {
    if (mc_id==11894400) return frac * 94.37 / 12.34;
    if (mc_id==12895410) return frac * 39.35 / 12.57;
    assert(false); // shouldn't be looking at any other mc IDs than these
  }
  if (year==2017) {
    if (mc_id==11894400) return frac * 78.58 / 18.00;
    if (mc_id==12895410) return frac * 41.90 / 16.53;
    assert(false); // shouldn't be looking at any other mc IDs than these
  }
  if (year==2018) {
    if (mc_id==11894400) return frac * 98.34 / 14.17;
    if (mc_id==12895410) return frac * 38.25 / 12.94;
    assert(false); // shouldn't be looking at any other mc IDs than these
  }
  assert(false); // shouldn't be looking at any other year than these
}

// DD Dalitz-inspired weights //////////////////////////////////////////////////

vector<Double_t> WT_DALITZ(Double_t dd_msq, Double_t dd_m_min,
                           Double_t dd_m_max) {
  Double_t Daltweightp  = 1;
  Double_t Daltweightm  = 1;
  Double_t Daltweightqp = 1;
  Double_t Daltweightqm = 1;

  Double_t min2 = dd_m_min * dd_m_min;
  Double_t max2 = dd_m_max * dd_m_max;

  Daltweightp  = (1 + 2 * (sqrt((dd_msq - min2) / (max2 - min2)) - 0.5));
  Daltweightm  = (1 - 2 * (sqrt((dd_msq - min2) / (max2 - min2)) - 0.5));
  Daltweightqp = (8 * (sqrt((dd_msq - min2) / (max2 - min2)) - 0.5) *
                  (sqrt((dd_msq - min2) / (max2 - min2)) - 0.5));
  Daltweightqm = (2 - 8 * (sqrt((dd_msq - min2) / (max2 - min2)) - 0.5) *
                          (sqrt((dd_msq - min2) / (max2 - min2)) - 0.5));

  return {Daltweightp, Daltweightm, Daltweightqp, Daltweightqm};
}

Double_t WT_ISO_NNK(Int_t true_id, Double_t w_pi, Double_t w_k, Double_t w_p,
                    Double_t w_e, Double_t w_mu, Double_t w_ghost) {
  true_id = ABS(true_id);
  if (true_id == 211) return w_pi;
  if (true_id == 321) return w_k;
  if (true_id == 2212) return w_p;
  if (true_id == 11) return w_e;
  if (true_id == 13) return w_mu;
  return w_ghost;
}

// Fake D** heavy Pi0Pi0 component /////////////////////////////////////////////

Double_t FAKE_ISO_BDT(Int_t truthmatch, Double_t raw_bdt, Int_t true_id1,
                      Int_t true_id2, Int_t true_id3) {
  int ratio = truthmatch / 100000;
  if (!(ratio == 4 || ratio == 3)) return raw_bdt;

  // Make sure it's not a Pi+Pi0 event
  true_id1 = TMath::Abs(true_id1);
  true_id2 = TMath::Abs(true_id2);
  true_id3 = TMath::Abs(true_id3);
  if (true_id1 == 111 || true_id2 == 111 || true_id3 == 111) return raw_bdt;

  Double_t rand = gRandom->Uniform(0, 100);
  if (rand <= 33) return -2;
  return raw_bdt;
}

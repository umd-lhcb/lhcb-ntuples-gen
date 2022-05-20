// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Fri May 20, 2022 at 02:14 AM -0400
// NOTE: All kinematic variables are in MeV

#pragma once

#include <Math/Vector3D.h>
#include <Math/Vector4D.h>
#include <TMath.h>

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
      d0_hlt2 &&
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
      IN_RANGE(mu_p, 3.0e3, 100.0e3) &&
      /* Acceptance */
      IN_RANGE(mu_eta, 1.7, 5.0) &&
      /* Track quality */
      mu_ip_chi2 > 45.0 && mu_gh_prob < 0.5
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
      dst_endvtx_chi2/dst_endvtx_ndof < 10.0 &&
      /* D* Mu combo */
      b0_discard_mu_chi2 < 6.0 &&  // Not in ANA!
      b0_endvtx_chi2 < 24.0 &&
      b0_endvtx_chi2/b0_endvtx_ndof < 6.0 &&
      b0_fd_trans < 7.0 &&
      b0_dira > 0.9995
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
  if (d0_m_pi_m - d0_m > 165.0 && d0_m_pi_m - d0_m - 145.454 > 4.0) return true;
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

// m(DD) selection /////////////////////////////////////////////////////////////

// D* reconstruction
vector<Double_t> FLAG_SEL_DD_MASS_DST(
    Double_t mu_mom_px, Double_t mu_mom_py, Double_t mu_mom_pz,
    Double_t mu_mom_pe, Double_t dst_px, Double_t dst_py, Double_t dst_pz,
    Double_t dst_pe, int mu_gdmom_id, Double_t mu_gdmom_px,
    Double_t mu_gdmom_py, Double_t mu_gdmom_pz, Double_t mu_gdmom_pe,
    Double_t b_px, Double_t b_py, Double_t b_pz, Double_t b_pe) {
  auto Tmumomp =
      ROOT::Math::PxPyPzEVector(mu_mom_px, mu_mom_py, mu_mom_pz, mu_mom_pe);
  auto     TDstp = ROOT::Math::PxPyPzEVector(dst_px, dst_py, dst_pz, dst_pe);
  auto     Tmugdmomp = ROOT::Math::PxPyPzEVector(mu_gdmom_px, mu_gdmom_py,
                                             mu_gdmom_pz, mu_gdmom_pe);
  auto     TBp       = ROOT::Math::PxPyPzEVector(b_px, b_py, b_pz, b_pe);
  Double_t mDD       = (Tmumomp + TDstp).M2();
  Double_t mX_DD     = (TBp - TDstp - Tmumomp).M();

  if (ABS(mu_gdmom_id) == 413 || ABS(mu_gdmom_id) == 423 ||
      ABS(mu_gdmom_id) == 433) {
    mDD   = (Tmugdmomp + TDstp).M2();
    mX_DD = (TBp - TDstp - Tmugdmomp).M();
  }

  return {mDD, mX_DD};
}

// D0 reconstruction
vector<Double_t> FLAG_SEL_DD_MASS_D0(
    Double_t mu_mom_px, Double_t mu_mom_py, Double_t mu_mom_pz,
    Double_t mu_mom_pe, Double_t d_mom_px, Double_t d_mom_py, Double_t d_mom_pz,
    Double_t d_mom_pe, int mu_gdmom_id, Double_t mu_gdmom_px,
    Double_t mu_gdmom_py, Double_t mu_gdmom_pz, Double_t mu_gdmom_pe,
    Double_t d_px, Double_t d_py, Double_t d_pz, Double_t d_pe, int d_mom_id,
    Double_t b_px, Double_t b_py, Double_t b_pz, Double_t b_pe) {
  auto Tmumomp =
      ROOT::Math::PxPyPzEVector(mu_mom_px, mu_mom_py, mu_mom_pz, mu_mom_pe);
  auto TDmomp =
      ROOT::Math::PxPyPzEVector(d_mom_px, d_mom_py, d_mom_pz, d_mom_pe);
  auto     Tmugdmomp = ROOT::Math::PxPyPzEVector(mu_gdmom_px, mu_gdmom_py,
                                             mu_gdmom_pz, mu_gdmom_pe);
  auto     TDp       = ROOT::Math::PxPyPzEVector(d_px, d_py, d_pz, d_pe);
  auto     TBp       = ROOT::Math::PxPyPzEVector(b_px, b_py, b_pz, b_pe);
  Double_t mDD, mX_DD;

  if (ABS(d_mom_id) == 413 || ABS(d_mom_id) == 423) {
    mDD   = (Tmumomp + TDmomp).M2();
    mX_DD = (TBp - TDmomp - Tmumomp).M();

    if (ABS(mu_gdmom_id) == 413 || ABS(mu_gdmom_id) == 423 ||
        ABS(mu_gdmom_id) == 433) {
      mDD   = (Tmugdmomp + TDmomp).M2();
      mX_DD = (TBp - TDmomp - Tmugdmomp).M();
    }
  } else {
    mDD   = (Tmumomp + TDp).M2();
    mX_DD = (TBp - TDp - Tmumomp).M();
    if (ABS(mu_gdmom_id) == 413 || ABS(mu_gdmom_id) == 423 ||
        ABS(mu_gdmom_id) == 433) {
      mDD   = (Tmugdmomp + TDp).M2();
      mX_DD = (TBp - TDp - Tmugdmomp).M();
    }
  }
  return {mDD, mX_DD};
}

Double_t FLAG_SEL_MX_WEIGHT(Double_t b_px, Double_t b_py, Double_t b_pz,
                            Double_t b_pe, Double_t d0_px, Double_t d0_py,
                            Double_t d0_pz, Double_t d0_pe, Double_t d1_px,
                            Double_t d1_py, Double_t d1_pz, Double_t d1_pe) {
  auto     TBp  = ROOT::Math::PxPyPzEVector(b_px, b_py, b_pz, b_pe);
  auto     TD0p = ROOT::Math::PxPyPzEVector(d0_px, d0_py, d0_pz, d0_pe);
  auto     TD1p = ROOT::Math::PxPyPzEVector(d1_px, d1_py, d1_pz, d1_pe);
  Double_t mX   = (TBp - TD0p - TD1p).M();
  return mX;
  // if(mX>620) return true;
  // return false;
}

Double_t FLAG_SEL_DWEIGHT(int mu_mom_id) {
  Double_t weightD;
  if (ABS(mu_mom_id) == 411) weightD = 0.1607;
  if (ABS(mu_mom_id) == 421) weightD = 0.0649;
  if (ABS(mu_mom_id) == 431) weightD = 0.0709;
  return weightD;
}

vector<Double_t> FLAG_SEL_DALWEIGHT(Double_t mDD, int b_ID) {
  Double_t Daltweightp  = 1;
  Double_t Daltweightm  = 1;
  Double_t Daltweightqp = 1;
  Double_t Daltweightqm = 1;
  if (SQRT(mDD) < 4990) {
    Double_t min;
    if (ABS(b_ID) == 511) {
      min = 2010 + 1864.8;
    }  // if B0 use Dst mass
    if (ABS(b_ID) == 512) {
      min = 1864.8 + 1864.8;
    }  // if Bu use D0 mass
    Double_t max  = 5280 - 489.;
    Double_t min2 = min * min;
    Double_t max2 = max * max;
    Daltweightp   = (1 + 2 * (sqrt((mDD - min2) / (max2 - min2)) - 0.5));
    Daltweightm   = (1 - 2 * (sqrt((mDD - min2) / (max2 - min2)) - 0.5));
    Daltweightqp  = (8 * (sqrt((mDD - min2) / (max2 - min2)) - 0.5) *
                    (sqrt((mDD - min2) / (max2 - min2)) - 0.5));
    Daltweightqm  = (2 - 8 * (sqrt((mDD - min2) / (max2 - min2)) - 0.5) *
                            (sqrt((mDD - min2) / (max2 - min2)) - 0.5));
  }

  return {Daltweightp, Daltweightm, Daltweightqp, Daltweightqm};
}

// B mass cuts /////////////////////////////////////////////////////////////////

Bool_t FLAG_SEL_BMINUS_MASS(Double_t b_m) { return b_m < 5200.0; }

Bool_t FLAG_SEL_BMINUS_MASS_SB(Double_t b_m) { return b_m > 5400.0; }

Bool_t FLAG_SEL_B0_MASS(Double_t b0_m) { return b0_m < 5280.0; }

Bool_t FLAG_SEL_B0_MASS_SB(Double_t b0_m) { return b0_m > 5400.0; }

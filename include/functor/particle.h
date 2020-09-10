// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Fri Sep 11, 2020 at 01:04 AM +0800

#ifndef _LNG_FUNCTOR_PARTICLE_H_
#define _LNG_FUNCTOR_PARTICLE_H_

#include <TLorentzVector.h>
#include <TMath.h>
#include <TROOT.h>
#include <TVector3.h>
#include <TMath.h>

#include <vector>

// Boolean /////////////////////////////////////////////////////////////////////

Bool_t ALL_TRUE(std::vector<Bool_t>& vec) {
  return std::all_of(vec.begin(), vec.end(), [](Bool_t v) { return v; });
}

Bool_t ALL_FALSE(std::vector<Bool_t>& vec) {
  return std::all_of(vec.begin(), vec.end(), [](Bool_t v) { return !v; });
}

Bool_t VEC_AND(std::vector<Bool_t>& vec) {
  return std::find(vec.begin(), vec.end(), false) == vec.end();
}

Bool_t VEC_OR(std::vector<Bool_t>& vec) {
  return std::find(vec.begin(), vec.end(), true) != vec.end();
}

template<class T>
Bool_t VEC_OR_EQ(std::vector<T>& vec, T expr) {
  for (auto v : vec) {
    if (expr == v) return true;
  }
  return false;
}

// General /////////////////////////////////////////////////////////////////////

TVector3 VEC_DELTA(Double_t Xf, Double_t Yf, Double_t Zf, Double_t Xi,
                   Double_t Yi, Double_t Zi) {
  TVector3 v;
  v.SetXYZ(Xf - Xi, Yf - Yi, Zf - Zi);
  return v;
}

TLorentzVector FOUR_VEC(Double_t X, Double_t Y, Double_t Z, Double_t T) {
  TLorentzVector v;
  v.SetXYZT(X, Y, Z, T);
  return v;
}

Double_t M2(TLorentzVector v) { return v.M2(); }

// Flags ///////////////////////////////////////////////////////////////////////

Bool_t IS_DATA(ULong64_t time) {
  // Special treatment for some run 1 data: We remove some real data if they
  // fall within a specific time window
  // FIXME: Ask Phoebe why
  if (time > 0 && (time <= 1345.7332e12 || time >= 1345.7335e12)) return true;
  else return false;
}

std::vector<std::vector<Bool_t> > MC_FLAGS(
    Int_t mu_mom_key, Int_t d0_mom_key, Int_t dst_mom_key,
    Int_t mu_gd_mom_key, Int_t dst_gd_mom_key,
    Int_t mu_gd_gd_mom_key, Int_t dst_gd_gd_mom_key
    ) {
  // Initialize flags
  std::vector<std::vector<Bool_t> > flags;
  for (auto i=0; i<4; i++) {
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

Int_t B_TYPE(std::vector<std::vector<Bool_t> >& mc_flags,
    Int_t mu_true_id, Int_t mu_mom_id, Int_t mu_gd_mom_id,
    Int_t dst_mom_id, Int_t dst_gd_mom_id, Int_t dst_gd_gd_mom_id
    ) {
  Int_t b_type = 0;

  auto abs_mu_true_id = TMath::Abs(mu_true_id);
  auto abs_mu_mom_id = TMath::Abs(mu_mom_id);
  auto abs_mu_gd_mom_id = TMath::Abs(mu_gd_mom_id);
  auto abs_dst_mom_id = TMath::Abs(dst_mom_id);
  auto abs_dst_gd_mom_id = TMath::Abs(dst_gd_mom_id);
  auto abs_dst_gd_gd_mom_id = TMath::Abs(dst_gd_gd_mom_id);

  if ((mc_flags[0][0] || mc_flags[0][1]) && abs_mu_true_id == 13)
    b_type = TMath::Abs(mu_mom_id);

  if (VEC_OR(mc_flags[1]) && abs_mu_true_id == 13 && abs_mu_mom_id == 511)
    b_type = 511;
  if (VEC_OR(mc_flags[2]) && abs_mu_true_id == 13 && abs_mu_mom_id == 15 &&
      abs_mu_gd_mom_id == 511)
    b_type = 511;
  if (mc_flags[0][0] && abs_mu_true_id == 13 && abs_mu_mom_id == 511)
    b_type = 511;
  if (mc_flags[0][1] && abs_mu_true_id == 13 && abs_mu_mom_id == 15 &&
      abs_mu_gd_mom_id == 511)
    b_type = 511;

  if (VEC_OR(mc_flags[1]) && abs_mu_true_id == 13 && abs_mu_mom_id == 521)
    b_type = 521;
  if (VEC_OR(mc_flags[2]) && abs_mu_true_id == 13 && abs_mu_mom_id == 15 &&
      abs_mu_gd_mom_id == 521)
    b_type = 521;
  if (mc_flags[0][0] && abs_mu_true_id == 13 && abs_mu_mom_id == 521)
    b_type = 521;
  if (mc_flags[0][1] && abs_mu_true_id == 13 && abs_mu_mom_id == 15 &&
      abs_mu_gd_mom_id == 521)
    b_type = 521;

  if (VEC_OR(mc_flags[1]) && abs_mu_true_id == 13 && abs_mu_mom_id == 531)
    b_type = 531;
  if (VEC_OR(mc_flags[2]) && abs_mu_true_id == 13 && abs_mu_mom_id == 15 &&
      abs_mu_gd_mom_id == 531)
    b_type = 531;
  if (mc_flags[0][0] && abs_mu_true_id == 13 && abs_mu_mom_id == 531)
    b_type = 531;
  if (mc_flags[0][1] && abs_mu_true_id == 13 && abs_mu_mom_id == 15 &&
      abs_mu_gd_mom_id == 531)
    b_type = 531;

  auto dst_possible_ids = std::vector<Int_t>({511, 521, 531});
  if (VEC_OR_EQ(dst_possible_ids, abs_dst_mom_id))
    b_type = abs_dst_mom_id;
  else if (VEC_OR_EQ(dst_possible_ids, abs_dst_gd_mom_id))
    b_type = abs_dst_gd_mom_id;
  else if (VEC_OR_EQ(dst_possible_ids, abs_dst_gd_gd_mom_id))
    b_type = abs_dst_gd_gd_mom_id;
  // FIXME: There's a else clause in Phoebe's spaghetti which set b_type to -1,
  //        but that one is never executed.
  // FIXME: Also don't understand the utility of `flagD0mu`

  return b_type;
}

Int_t DSS_TYPE(Int_t dst_mom_id, Int_t dst_gd_mom_id) {
  Int_t dss_type = 0;

  auto abs_dst_mom_id = TMath::Abs(dst_mom_id);
  auto abs_dst_gd_mom_id = TMath::Abs(dst_gd_mom_id);

  if (abs_dst_mom_id == 511 || abs_dst_gd_mom_id == 521 ||
      abs_dst_gd_mom_id == 531)
    dss_type = abs_dst_mom_id;

  return dss_type;
}

// Kinematics //////////////////////////////////////////////////////////////////

Double_t MM_DST_MOM(TLorentzVector& v_dst_mom_p, TLorentzVector& v_dst_p) {
  Double_t mm_dst_mom = M2(v_dst_mom_p - v_dst_p);
  if (mm_dst_mom > 0) return sqrt(mm_dst_mom);
  else return 0.0;
}

// Muon-related ////////////////////////////////////////////////////////////////

Bool_t MU_PID(Bool_t id_correctness, Double_t PID) {
  return id_correctness && (PID > 2.0);
}

// Rest frame approximation ////////////////////////////////////////////////////

TLorentzVector P_EST(Double_t PZ, Double_t m, TVector3 flight) {
  const Double_t B_M = 5279.61;

  Double_t Tan_theta = flight.Unit().Perp() / flight.Unit().Z();
  Double_t PT        = TMath::Power((B_M / m), 1) * Tan_theta * PZ;

  TLorentzVector P;
  P.SetPtEtaPhiM(PT, flight.Unit().Eta(), flight.Unit().Phi(), B_M);

  return P;
}

#endif

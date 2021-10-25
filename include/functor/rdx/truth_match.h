// Author: Alex Fernez, Yipeng Sun
// License: BSD 2-clause

#ifndef _LNG_FUNCTOR_RDX_TRUTH_MATCH_H_
#define _LNG_FUNCTOR_RDX_TRUTH_MATCH_H_

#include <TLorentzVector.h>
#include <TMath.h>
#include <assert.h>
#include <map>

#include "functor/basic.h"
#include "pdg.h"

using namespace std;

// TODO check things against code in gitlab (again) instead of preservation
// repo; also change the links

//////////////////////////////
// General Helper Functions //
//////////////////////////////

int HUNDREDS_DIGIT(int a) { return floor((a % 1000) / 100); }

bool IS_DDX(int decay_id) {
  auto ddx_ids = vector<int>{11894600, 12893600, 11894200, 12893610,
                             11894610, 12895400, 11894210, 12895000};

  if (find(ddx_ids.begin(), ddx_ids.end(), decay_id) == ddx_ids.end())
    return false;
  return true;
}

//////////////////////////////////
// General Truth-Matching Class //
//////////////////////////////////

// There are a lot of variables being used in the truth-matching functions. In
// order to guard against typos, do the truth-matching via OOP, so that you only
// have to pass the variables once. This template class should never be used for
// truth-matching, but it's useful to organize the structure and for common
// variables/functions
class TruthMatch {
 protected:
  // List codes used for truthmatching (some subset to be added together based
  // on matched decay)
  int mu      = 0;
  int tau     = 1;
  int d0      = 10;
  int dp      = 20;
  int dst0    = 30;
  int dstp    = 40;
  int dstst0  = 100;
  int dststp  = 200;
  int dHstst0 = 300;
  int dHststp = 400;
  int dsstst  = 500;
  int d0st    = 10;
  int d1      = 20;
  int d1p     = 30;
  int d2st    = 40;
  int dst2S   = 10;
  int d2S     = 20;
  int d2750   = 30;
  int d3000   = 40;
  // TODO DD cocktail codes
  int dd_bd               = 100000;
  int dd_bu               = 200000;
  int dstst_higher_to_dst = 300000;
  int dstst_higher_to_d   = 400000;
  int dstst_twopi         = 500000;

  // useful to have a map as a reference for D** cocktails (PDG MC ID -> our
  // code)
  map<int, int> pdg_to_code{
      {PDG_ID_D0st_0, d0st},
      {PDG_ID_D1_0, d1},
      {PDG_ID_D1p_0, d1p},
      {PDG_ID_D2st_0, d2st},
      {PDG_ID_D0st, d0st},
      {PDG_ID_D1, d1},
      {PDG_ID_D1p, d1p},
      {PDG_ID_D2st, d2st},
      {PDG_ID_Dst2S_0, dst2S},
      {PDG_ID_D2S_0, d2S},
      {FAKE_ID_D2750_0, d2750},
      {FAKE_ID_D3000_0, d3000},
      {PDG_ID_Dst2S, dst2S},
      {PDG_ID_D2S, d2S},
      {FAKE_ID_D2750, d2750},
      {FAKE_ID_D3000, d3000},
      {PDG_ID_D1p_s, d1p},
      {PDG_ID_D2st_s, d2st}};  // Ds0*,Ds2* do not exist for us

  // Sets of particles used for some truth-matching
  vector<int> b_mesons{PDG_ID_B0, PDG_ID_Bu, PDG_ID_Bs};
  vector<int> dst_dst0{PDG_ID_Dst, PDG_ID_Dst0};
  vector<int> b0_bu{PDG_ID_B0, PDG_ID_Bu};
  vector<int> charged_dstst{PDG_ID_D0st, PDG_ID_D1, PDG_ID_D1p, PDG_ID_D2st};
  vector<int> neutral_dstst{PDG_ID_D0st_0, PDG_ID_D1_0, PDG_ID_D1p_0,
                            PDG_ID_D2st_0};
  vector<int> strange_dstst{PDG_ID_D1p_s, PDG_ID_D2st_s};
  vector<int> charged_dstst_higher{PDG_ID_Dst2S, PDG_ID_D2S, FAKE_ID_D2750,
                                   FAKE_ID_D3000};
  vector<int> neutral_dstst_higher{PDG_ID_Dst2S_0, PDG_ID_D2S_0,
                                   FAKE_ID_D2750_0, FAKE_ID_D3000_0};
  vector<int> d0st_d0st0{PDG_ID_D0st, PDG_ID_D0st_0};
  vector<int> d1_d10{PDG_ID_D1, PDG_ID_D1_0};
  vector<int> d_mesons{PDG_ID_D, PDG_ID_D0, PDG_ID_Ds};
  vector<int> dstst_s_1_mesons{PDG_ID_D1_s, PDG_ID_D1p_s};

 public:
  int truthmatch = 0;
  int added = 0;  // variable sums up cocktail/special info while truthmatching
                  // is occuring, then gets added to truthmatch

  // Derived from (and used in place of) decay mode # considered (set on
  // construction)
  int  b_expect_id;
  bool tau_expect;
  bool dstst_higher;
  int  dst_expect_id;
  // some debugging flags
  bool debug_dstst_all_cocktail;
  bool debug_dstst_higher_separate_cocktail;
  bool debug_dstst_s_all_cocktail;
  bool debug_dd_all_cocktail;

  virtual bool COMMON_SELEC() = 0;         // differs between D0/D* samples
  bool         DSTST_OKAY(int dstst_id) {  // same between D0/D* samples
    return ((b_expect_id == PDG_ID_B0 && VEC_OR_EQ(charged_dstst, dstst_id) &&
             !dstst_higher) ||
            (b_expect_id == PDG_ID_Bu && VEC_OR_EQ(neutral_dstst, dstst_id) &&
             !dstst_higher) ||
            (b_expect_id == PDG_ID_Bs && VEC_OR_EQ(strange_dstst, dstst_id) &&
             !dstst_higher) ||
            (b_expect_id == PDG_ID_B0 &&
             VEC_OR_EQ(charged_dstst_higher, dstst_id) && dstst_higher) ||
            (b_expect_id == PDG_ID_Bu &&
             VEC_OR_EQ(neutral_dstst_higher, dstst_id) && dstst_higher));
  }
  virtual bool TWO_PI() = 0;  // different between D0/D* samples
  virtual bool B_BKGCAT_OKAY() {
    return false;
  }  // different between D0/D* samples; TODO should implement this func for D*
     // sample too
  void DSTST_COCKTAIL_ADDED(int dstst_id) {  // same between D0/D* samples
    // nominally add cockatil info for D**, Ds**, not done for D**H unless
    // specified otherwise
    if ((!dstst_higher && b_expect_id != PDG_ID_Bs &&
         !debug_dstst_all_cocktail) ||
        (dstst_higher && debug_dstst_higher_separate_cocktail) ||
        (b_expect_id == PDG_ID_Bs && !debug_dstst_s_all_cocktail)) {
      added += pdg_to_code[dstst_id];
    }
  }
  void DSTST_TWOPI_ADDED() {  // same between D0/D* samples
    // If (light) D** decay, specify if D**->D(*)pipi
    if (b_expect_id != PDG_ID_Bs && !dstst_higher && TWO_PI())
      added += dstst_twopi;
  }

  virtual bool TRUTH_MATCH_NORMSIG() = 0;
  virtual bool TRUTH_MATCH_DSTST()   = 0;
  virtual bool TRUTH_MATCH_DD()      = 0;
};

//////////////////////////////////
// D* Truth-Matching Selections //
//////////////////////////////////
// Based on Phoebe's:
//   https://github.com/umd-lhcb/RDRDstRun1AnalysisPreservation/blob/de225b567e7004a45f6003ef117428f421e7fa13/proc/redoHistos_Dst.C
//   https://github.com/umd-lhcb/RDRDstRun1AnalysisPreservation/blob/ca8f0df0e1206f9bd3f3c64d12958ffb1025574a/proc/AddB.C

class DstTruthMatch : public TruthMatch {
 private:
  int            decay_id;
  int            mu_id;
  int            mu_mom_id;
  int            mu_gdmom_id;
  int            mu_gdgdmom_id;
  int            mu_mom_key;
  int            mu_gdmom_key;
  int            mu_gdgdmom_key;
  int            dst_mom_id;
  int            dst_gdmom_id;
  int            dst_gdgdmom_id;
  int            dst_mom_key;
  int            dst_gdmom_key;
  int            dst_gdgdmom_key;
  TLorentzVector dst_mom_truep4;
  TLorentzVector dst_truep4;
  int            dst_bkgcat;
  int            d0_bkgcat;
  int            b_bkgcat;

 public:
  ///////// Helpers

  bool COMMON_SELEC() {
    return (dst_bkgcat == 0 || (dst_bkgcat == 50 && d0_bkgcat == 50)) &&
           mu_id == PDG_ID_mu;
  }

  bool TWO_PI() {
    double mm2_mom = (dst_mom_truep4 - dst_truep4).M2();  // MeV
    return mm2_mom > 0 && sqrt(mm2_mom) > 250;
  }

  //////// Specific Decay Truth-Matching

  // Normalization and Signal
  // Phoebe redoHistos_Dst.C: flagBmu/flagtaumu>0. && JustDst>0. && DstOk>0. &&
  // muPID==1. && Btype==511 && [for norm only] Y_BKGCAT==0
  // TODO: Phoebe does some redefining of her Y_BKGCAT in her AddB.C, but I've
  // just used the b_bkgcat from the ntuple as-is
  bool TRUTH_MATCH_NORMSIG() {
    // Make sure ancestry of mu is correct, including making sure B in mu
    // ancestry and B in D* ancestry are the same
    bool mu_ancestry_ok = false;
    if (!tau_expect) {
      mu_ancestry_ok =
          mu_mom_id == PDG_ID_B0 && mu_mom_key > 0 && mu_mom_key == dst_mom_key;
    } else {  // else looking at a signal decay
      mu_ancestry_ok = mu_mom_id == PDG_ID_tau && mu_gdmom_id == PDG_ID_B0 &&
                       mu_gdmom_key > 0 && mu_gdmom_key == dst_mom_key;
    }

    // Implement the b_bkgcat selection for normalization, and ensure (really, a
    // second check) that D* mom is B0
    return ((b_bkgcat == 0) || tau_expect) && dst_mom_id == PDG_ID_B0 &&
           mu_ancestry_ok;
  }

  // D**, D_H**, D_s**
  // Phoebe redoHistos_Dst.C: flagBmu/flagtaumu>0 && JustDst<1  && DstOk>0. &&
  // Btype==[b_expect_id] && Dststtype==[D** cocktail] && muPID == 1 Note: I
  // don't implement Phoebe's ishigher, instead just using the variable
  // dstst_higher to keep track of the considered decay ID Note: compared to the
  // D0 sample, this selection is simpler because here the decay is required to
  // go B->D**->D*
  bool TRUTH_MATCH_DSTST() {
    // Check if D** (just D* mom here) is okay
    bool dst_mom_id_ok = false;
    if (DSTST_OKAY(dst_mom_id)) {
      dst_mom_id_ok = true;
      DSTST_COCKTAIL_ADDED(dst_mom_id);
      if (!TWO_PI())
        assert(!VEC_OR_EQ(
            d0st_d0st0,
            dst_mom_id));  // just make sure that there are no D0*->D*pi decays
    }

    // Make sure ancestry of mu is correct, including making sure B in mu
    // ancestry and B in D* ancestry are the same
    bool mu_ancestry_ok = false;
    if (!tau_expect) {
      mu_ancestry_ok = mu_mom_id == b_expect_id && mu_mom_key > 0 &&
                       mu_mom_key == dst_gdmom_key;
    } else {  // else looking at a signal-like decay
      mu_ancestry_ok = mu_mom_id == PDG_ID_tau && mu_gdmom_id == b_expect_id &&
                       mu_mom_key > 0 && mu_gdmom_key == dst_gdmom_key;
    }

    DSTST_TWOPI_ADDED();  // specify if D**->D*pipi decay

    // If D**H, will always go as D**H->D* for D* sample reconstruction (TODO
    // maybe worth adding an assert statement to be sure of this)
    if (dstst_higher) added += dstst_higher_to_dst;

    // Finally, ensure the D** mom (and thus D* gdmom) is in fact the correct B
    return dst_mom_id_ok && mu_ancestry_ok && dst_gdmom_id == b_expect_id;
  }

  // DD
  // Phoebe's redoHistos_Dst.C: DstOk>0. && muPID==1 && Btype==[b_expect_id] &&
  // ((flagDoubleD>0 && flagTauonicD<1) OR flagTauonicD>0) Truthfully, though
  // confusing, her truth-matching seems somewhat minimalistic/loose to me;
  // perhaps for the best? Note: the use of the mu and D* ancestry keys is quite
  // different here wrt other truth-matching; I think the general idea is that
  // D* and mu should
  //   have SOME common ancestor, whereas for the other truth-matching we were
  //   always explicitly ensuring that that common ancestor was the B. In fact,
  //   for the tauonic DD decays, no key matching is done at all.
  // I won't implement a cocktail selection here for now: it isn't possible
  // without more information about daughters (which will come for us via
  // TupleToolSLTruth)
  bool TRUTH_MATCH_DD() {
    // For a DD decay with no tau, ensure at least that the mu came from a (spin
    // 0) charm meson and that mu and D* have some ancesteor in common, OR, as
    // a special case, just check its gdgdmom is Ds1(') and D* mom is in fact B;
    // also explicitly reject the conditions that are used to qualify a DD decay
    // with a tau. For the DD decay with a tau, require that mu's mother is a
    // tau and gdmom is Ds (don't bother with key-checking).
    bool mu_ancestry_ok_or_special = false;
    bool dd_tau_ok = mu_mom_id == PDG_ID_tau && mu_gdmom_id == PDG_ID_Ds;
    if (!tau_expect) {
      vector<int> dst_lineage_keys{dst_mom_key, dst_gdmom_key, dst_gdgdmom_key};
      bool        mu_dst_common_ancestor =
          (mu_gdmom_key > 0 && VEC_OR_EQ(dst_lineage_keys, mu_gdmom_key)) ||
          (mu_gdgdmom_key > 0 && VEC_OR_EQ(dst_lineage_keys, mu_gdgdmom_key));
      mu_ancestry_ok_or_special =
          !dd_tau_ok &&
          ((VEC_OR_EQ(d_mesons, mu_mom_id) && mu_dst_common_ancestor) ||
           (VEC_OR_EQ(dstst_s_1_mesons, mu_gdgdmom_id) &&
            dst_mom_id == b_expect_id));
    } else {  // else looking at a signal-like decay
      mu_ancestry_ok_or_special = dd_tau_ok;
    }

    // TODO separate cocktails
    if (!debug_dd_all_cocktail) added += 0;

    // Also, just ensure that there is a B somewhere within three generations of
    // the D*
    vector<int> dst_lineage_ids{dst_mom_id, dst_gdmom_id, dst_gdgdmom_id};
    return mu_ancestry_ok_or_special && VEC_OR_EQ(dst_lineage_ids, b_expect_id);
  }

  ////////// Constructor

  DstTruthMatch(int decay_id_, int mu_id_, int mu_mom_id_, int mu_gdmom_id_,
                int mu_gdgdmom_id_, int mu_mom_key_, int mu_gdmom_key_,
                int mu_gdgdmom_key_, int dst_mom_id_, int dst_gdmom_id_,
                int dst_gdgdmom_id_, int dst_mom_key_, int dst_gdmom_key_,
                int dst_gdgdmom_key_, double dst_mom_trueE_,
                double dst_mom_truePx_, double dst_mom_truePy_,
                double dst_mom_truePz_, double dst_trueE_, double dst_truePx_,
                double dst_truePy_, double dst_truePz_, int dst_bkgcat_,
                int d0_bkgcat_, int b_bkgcat_, bool debug_dstst_all_cocktail_,
                bool debug_dstst_higher_separate_cocktail_,
                bool debug_dstst_s_all_cocktail_, bool debug_dd_all_cocktail_) {
    // set simple fields; ensure all IDs are positive- not looking for wrong
    // signs when truth-matching
    decay_id        = decay_id_;
    mu_id           = abs(mu_id_);
    mu_mom_id       = abs(mu_mom_id_);
    mu_gdmom_id     = abs(mu_gdmom_id_);
    mu_gdgdmom_id   = abs(mu_gdgdmom_id_);
    mu_mom_key      = mu_mom_key_;
    mu_gdmom_key    = mu_gdmom_key_;
    mu_gdgdmom_key  = mu_gdgdmom_key_;
    dst_mom_id      = abs(dst_mom_id_);
    dst_gdmom_id    = abs(dst_gdmom_id_);
    dst_gdgdmom_id  = abs(dst_gdgdmom_id_);
    dst_mom_key     = dst_mom_key_;
    dst_gdmom_key   = dst_gdmom_key_;
    dst_gdgdmom_key = dst_gdgdmom_key_;
    dst_mom_truep4.SetPxPyPzE(dst_mom_truePx_, dst_mom_truePy_, dst_mom_truePz_,
                              dst_mom_trueE_);
    dst_truep4.SetPxPyPzE(dst_truePx_, dst_truePy_, dst_truePz_, dst_trueE_);
    dst_bkgcat               = dst_bkgcat_;
    d0_bkgcat                = d0_bkgcat_;
    b_bkgcat                 = b_bkgcat_;
    debug_dstst_all_cocktail = debug_dstst_all_cocktail_;
    debug_dstst_higher_separate_cocktail =
        debug_dstst_higher_separate_cocktail_;
    debug_dstst_s_all_cocktail = debug_dstst_s_all_cocktail_;
    debug_dd_all_cocktail      = debug_dd_all_cocktail_;

    // set decay descriptors and call truth-matching
    if (COMMON_SELEC()) {  // make sure some common selections are fulfilled
                           // first
      switch (decay_id) {
        case 11574021:
          tau_expect = false;
          if (TRUTH_MATCH_NORMSIG()) truthmatch = dstp + mu;
          break;
        case 11574011:
          tau_expect = true;
          if (TRUTH_MATCH_NORMSIG()) truthmatch = dstp + tau;
          break;
        case 11874430:
          b_expect_id  = PDG_ID_B0;
          tau_expect   = false;
          dstst_higher = false;
          if (TRUTH_MATCH_DSTST()) truthmatch = dststp + mu + added;
          break;
        case 11874440:
          b_expect_id  = PDG_ID_B0;
          tau_expect   = true;
          dstst_higher = false;
          if (TRUTH_MATCH_DSTST()) truthmatch = dststp + tau + added;
          break;
        case 12873450:
          b_expect_id  = PDG_ID_Bu;
          tau_expect   = false;
          dstst_higher = false;
          if (TRUTH_MATCH_DSTST()) truthmatch = dstst0 + mu + added;
          break;
        case 12873460:
          b_expect_id  = PDG_ID_Bu;
          tau_expect   = true;
          dstst_higher = false;
          if (TRUTH_MATCH_DSTST()) truthmatch = dstst0 + tau + added;
          break;
        case 11676012:
          b_expect_id  = PDG_ID_B0;
          tau_expect   = false;
          dstst_higher = true;
          if (TRUTH_MATCH_DSTST()) truthmatch = dHststp + mu + added;
          break;
        case 12675402:
          b_expect_id  = PDG_ID_Bu;
          tau_expect   = false;
          dstst_higher = true;
          if (TRUTH_MATCH_DSTST()) truthmatch = dHstst0 + mu + added;
          break;
        case 13674000:
          b_expect_id  = PDG_ID_Bs;
          tau_expect   = false;
          dstst_higher = false;
          if (TRUTH_MATCH_DSTST()) truthmatch = dsstst + mu + added;
          break;
        case 11894610:
          b_expect_id = PDG_ID_B0;
          tau_expect  = false;
          if (TRUTH_MATCH_DD()) truthmatch = dd_bd + mu + added;
          break;
        case 12895400:
          b_expect_id = PDG_ID_Bu;
          tau_expect  = false;
          if (TRUTH_MATCH_DD()) truthmatch = dd_bu + mu + added;
          break;
        case 11894210:
          b_expect_id = PDG_ID_B0;
          tau_expect  = true;
          if (TRUTH_MATCH_DD()) truthmatch = dd_bd + tau + added;
          break;
        case 12895000:
          b_expect_id = PDG_ID_Bu;
          tau_expect  = true;
          if (TRUTH_MATCH_DD()) truthmatch = dd_bu + tau + added;
          break;
      }
    }
  }
};

//////////////////////////////////
// D0 Truth-Matching Selections //
//////////////////////////////////
// Based on Phoebe's:
//   https://github.com/umd-lhcb/RDRDstRun1AnalysisPreservation/blob/ca8f0df0e1206f9bd3f3c64d12958ffb1025574a/proc/redoHistos_D0.C
//   https://github.com/umd-lhcb/RDRDstRun1AnalysisPreservation/blob/ca8f0df0e1206f9bd3f3c64d12958ffb1025574a/proc/AddD0B_temp.C

class D0TruthMatch : public TruthMatch {
 private:
  int            decay_id;
  int            b_id;
  int            mu_id;
  int            mu_mom_id;
  int            mu_gdmom_id;
  int            mu_gdgdmom_id;
  int            mu_gdgdgdmom_id;
  int            mu_mom_key;
  int            mu_gdmom_key;
  int            mu_gdgdmom_key;
  int            mu_gdgdgdmom_key;
  int            d_mom_id;
  int            d_gdmom_id;
  int            d_gdgdmom_id;
  int            d_gdgdgdmom_id;
  int            d_mom_key;
  int            d_gdmom_key;
  int            d_gdgdmom_key;
  int            d_gdgdgdmom_key;
  TLorentzVector d_truep4;
  TLorentzVector d_mom_truep4;
  TLorentzVector d_gdmom_truep4;
  int            b_bkgcat;
  double         d_m;
  // special variables used for D** truth-matching: copied from Phoebe's code
  int Btype     = 0;
  int Dststtype = 0;

 public:
  ///////// Helpers

  bool COMMON_SELEC() { return mu_id == PDG_ID_mu; }

  // TODO Phoebe redefines Y_BKGCAT in her AddD0B_temp.C too much; for now, I'm
  // just implementing something similar Need nu_mu momentum info in order to
  // exactly copy Phoebe's implementation!
  bool B_BKGCAT_OKAY() {
    return (!tau_expect && dst_expect_id == -1 && b_bkgcat == 0) ||
           (tau_expect && dst_expect_id == -1 && b_bkgcat == 10) ||
           (!tau_expect && dst_expect_id != -1 /* && b_bkgcat==5*/) ||
           (tau_expect && dst_expect_id != -1 /* && b_bkgcat==15*/);
  }

  // Requires D0 has B either as gdmom or gdgdmom (TODO think about this to
  // ensure it's right...)
  bool SIMPLEDSTST_KEYMATCH() {
    bool b_is_gdmom   = VEC_OR_EQ(b_mesons, d_gdmom_id);
    bool b_is_gdgdmom = VEC_OR_EQ(b_mesons, d_gdgdmom_id);
    if (b_is_gdmom)
      return (mu_mom_key == d_gdmom_key || mu_gdmom_key == d_gdmom_key);
    else if (b_is_gdgdmom)
      return (mu_mom_key == d_gdgdmom_key || mu_gdmom_key == d_gdgdmom_key);
    else
      return false;
  }

  // Note that there is SOME key matching done here (via Phoebe's simpleDstst);
  // if the key-matching fails, just return without setting Btype and Dststtype
  // (they are defaulted to 0). Also if B->D0, return without setting the
  // variables (this function is assumedly only used for D** truth-matching)
  void SET_BTYPE_DSTSTTYPE() {
    if (VEC_OR_EQ(b_mesons, d_mom_id))
      return;
    else if (VEC_OR_EQ(b_mesons, d_gdmom_id)) {
      if (!(SIMPLEDSTST_KEYMATCH())) return;
      Btype     = d_gdmom_id;
      Dststtype = d_mom_id;
    } else if (VEC_OR_EQ(b_mesons, d_gdgdmom_id) &&
               VEC_OR_EQ(dst_dst0, d_mom_id)) {
      if (!(SIMPLEDSTST_KEYMATCH())) return;
      Btype     = d_gdgdmom_id;
      Dststtype = d_gdmom_id;
    } else if (VEC_OR_EQ(b_mesons, d_gdgdmom_id) && b_id == d_gdgdmom_id)
      Btype = d_gdgdmom_id;
    else if (VEC_OR_EQ(b_mesons, d_gdgdgdmom_id) && b_id == d_gdgdgdmom_id)
      Btype = d_gdgdgdmom_id;
    else if (VEC_OR_EQ(b_mesons, mu_gdmom_id) && b_id == mu_gdmom_id)
      Btype = mu_gdmom_id;
    else if (VEC_OR_EQ(b_mesons, mu_gdgdmom_id) && b_id == mu_gdgdmom_id)
      Btype = mu_gdgdmom_id;
    else if (VEC_OR_EQ(b_mesons, mu_gdgdgdmom_id) && b_id == mu_gdgdgdmom_id)
      Btype = mu_gdgdgdmom_id;
    else
      Dststtype = -2;  // done to copy Phoebe's code more precisely, but also to
                       // ensure works correctly with my code

    // note that b_bkgcat here is used in Phoebe's code before she redefines it
    if (Dststtype == 0 && b_bkgcat == 50 &&
        (VEC_OR_EQ(b0_bu, mu_mom_id) ||
         (mu_mom_id == 15 &&
          VEC_OR_EQ(b0_bu, mu_gdmom_id)))) {  // Phoebe has a typo in this line
                                              // (2907) I think
      Btype = b_id;
      if (HUNDREDS_DIGIT(d_gdgdmom_id) == 4)
        Dststtype = d_gdgdmom_id;
      else if (HUNDREDS_DIGIT(d_gdgdmom_id) == 5 &&
               HUNDREDS_DIGIT(d_gdmom_id) == 4)
        Dststtype = d_gdmom_id;
      else if (HUNDREDS_DIGIT(d_gdmom_id) == 5 && HUNDREDS_DIGIT(d_mom_id) == 4)
        Dststtype = d_mom_id;
    }

    // in redoHistos_D0.C, Phoebe does one last thing to fix a truth-matching
    // bug
    if (mu_mom_id == PDG_ID_tau && Dststtype == 0 && !SIMPLEDSTST_KEYMATCH() &&
        VEC_OR_EQ(d1_d10, d_gdmom_id))
      Dststtype = d_gdmom_id;
  }

  bool TWO_PI() {
    // A bit confusing, but for now, just copy Phoebe's implementation (TODO
    // think about this...)
    double mm2_mom;
    if (!(VEC_OR_EQ(dst_dst0, d_mom_id) && VEC_OR_EQ(b_mesons, d_gdgdmom_id)))
      mm2_mom = (d_mom_truep4 - d_truep4).M2();  // Mev
    else
      mm2_mom = (d_gdmom_truep4 - d_mom_truep4).M2();  // MeV
    return mm2_mom > 0 && sqrt(mm2_mom) > 220;
  }

  //////// Specific Decay Truth-Matching

  // Normalization and Signal
  // Phoebe redoHistos_D0.C: flagBmu/flagtaumu>0 && muPID==1 &&
  // Y_BKGCAT==0/10/5/15 (Dmu, Dtau, D*mu, D*tau) && Btype==b_expect_id &&
  // JustDst>0 [for Dmu, Dtau] Note: JustDst is a misnomer- it should really be
  // "JustD0"
  bool TRUTH_MATCH_NORMSIG() {
    // Make sure ancestry of mu is correct, including making sure B in mu
    // ancestry and B in D0 ancestry are the same Note that a check that
    // B(->D*)->D0 proceeds as expected for the decay (should) occur later when
    // selecting on b_bkgcat, so it's fine here to just look at all of the keys
    // of the D0 ancestors to check against the B from the mu ancestry
    bool        mu_ancestry_ok = false;
    vector<int> d_lineage_keys{d_mom_key, d_gdmom_key, d_gdgdmom_key};
    if (!tau_expect) {
      mu_ancestry_ok = mu_mom_id == b_expect_id && mu_mom_key > 0 &&
                       VEC_OR_EQ(d_lineage_keys, mu_mom_key);
    } else {  // else looking at a signal decay
      mu_ancestry_ok = mu_mom_id == PDG_ID_tau && mu_gdmom_id == b_expect_id &&
                       mu_mom_key > 0 &&
                       VEC_OR_EQ(d_lineage_keys, mu_gdmom_key);
    }

    // Implement the b_bkgcat selection (note that this is used for all decay
    // modes here, whereas for the D* sample it was only used for normalization)
    // Also, if decay goes like B->D0, then require that the correct B is indeed
    // the mother of the D0
    return B_BKGCAT_OKAY() &&
           (dst_expect_id != -1 || d_mom_id == b_expect_id) && mu_ancestry_ok;
  }

  // D**, D_H**, D_s**
  // Phoebe redoHistos_D0.C: flagBmu/flagtaumu>0 && JustDst<1 &&
  // Btype==[b_expect_id] && Dststtype==[D** cocktail] (not for D**H) &&
  // muPID==1 && simpleDstst (not for D**H,s) Note: I don't implement Phoebe's
  // ishigher, instead just using the variable dstst_higher to keep track of the
  // considered decay ID Note: Phoebe combines D**H decays into a
  // B(+,0)->D**H->D*(+,0), a B(+,0)->D**H->D*+, and a B(+,0)->D**H->D0
  // template; this is implemented (at least partially) in 'added' Note: I think
  // Phoebe makes a (small) logical mistake in her AddD0B_temp.C and, by not
  // checking for "onefour/twofour" when setting flagBmu, she cuts out decays
  // that go like B->D1,D2*->X->X->D0. For now, though, I will just copy her
  // code. TODO: rethink if this is correct or not Note: simpleDstst seems like
  // a misnomer to me: it just checks that (if decay goes B->D**->D0 or
  // B->D**->X->D0) then B key matches between mu/D0
  bool TRUTH_MATCH_DSTST() {
    // Once the B and D** are found, make sure the D** is one of the possible
    // cocktails for the decay mode, and check that Btype is as expected
    SET_BTYPE_DSTSTTYPE();
    bool b_and_dstst_id_ok = false;
    if (DSTST_OKAY(Dststtype) && Btype == b_expect_id) {
      b_and_dstst_id_ok = true;
      DSTST_COCKTAIL_ADDED(Dststtype);
      // TODO as done for D* truthmatching above, should check there are no
      // unallowed D** decays with an assert statement
    }

    // Make sure ancestry of mu is correct, including trying to make sure B in
    // mu ancestry and B in D0 ancestry are the same Note that
    // SET_BTYPE_DSTSTTYPE() does some key-matching, though I'm not convinced it
    // always exactly checks that, wherever the B is in the D0 ancestry, its the
    // same as the B from the mu ancestry (this is only explicitly done for the
    // cases B->D**->D0 and B->D**->D*->D0). But, for now, copy Phoebe's code
    // and (though repetitive), just check here that there is indeed some key
    // from D0 ancestry that will match B key from mu ancestry. Note: you can
    // see that decays like B->D**->X->X->D0 are cut out here explicitly; only
    // up to d_gdgdmom_key is checked. TODO think about this...
    bool        mu_ancestry_ok = false;
    vector<int> d_lineage_keys{d_mom_key, d_gdmom_key, d_gdgdmom_key};
    if (!tau_expect) {
      mu_ancestry_ok = mu_mom_id == b_expect_id && mu_mom_key > 0 &&
                       VEC_OR_EQ(d_lineage_keys, mu_mom_key);
    } else {  // else looking at a signal decay
      mu_ancestry_ok = mu_mom_id == PDG_ID_tau && mu_gdmom_id == b_expect_id &&
                       mu_mom_key > 0 &&
                       VEC_OR_EQ(d_lineage_keys, mu_gdmom_key);
    }

    DSTST_TWOPI_ADDED();  // specify if D**->D(*)pipi decay

    // If D**H, separate D**H->D* from D**H->D
    if (dstst_higher) {
      if (VEC_OR_EQ(dst_dst0, d_mom_id))
        added += dstst_higher_to_dst;  // copied from how Phoebe does it
      else
        added += dstst_higher_to_d;  // else D**H->D
    }

    return b_and_dstst_id_ok && mu_ancestry_ok;
  }

  // DD
  // Phoebe's redoHistos_D0.C: muPID==1 && Btype==b_expect_id && ((flagDoubleD>0
  // && flagTauonicD<1) OR flagTauonicD>0) Truthfully, though confusing, her
  // truth-matching seems somewhat minimalistic/loose to me; perhaps for the
  // best? Note the use of the mu and D0 ancestry keys is quite different here
  // wrt other truth-matching; I think the general idea is that D0 and mu should
  //   have SOME common ancestor, whereas for the other truth-matching we were
  //   always explicitly ensuring that that common ancestor was the B. In fact,
  //   for the tauonic DD decays, no key matching is done at all.
  // I won't implement a cocktail selection here for now: it isn't possible
  // without more information about daughters (which will come for us via
  // TupleToolSLTruth)
  bool TRUTH_MATCH_DD() {
    // For a DD decay with no tau, ensure at least that the mu came from a (spin
    // 0) charm meson and that mu and D0 have some ancesteor in common; also
    // explicitly reject the conditions that are used to qualify a DD decay with
    // a tau. For the DD decay with a tau, require that mu's mother is a tau and
    // gdmom is Ds (don't bother with key-checking).
    bool mu_ancestry_ok = false;
    bool dd_tau_ok      = mu_mom_id == PDG_ID_tau && mu_gdmom_id == PDG_ID_Ds;
    if (!tau_expect) {
      vector<int> d_lineage_keys(
          {d_mom_key, d_gdmom_key, d_gdgdmom_key, d_gdgdgdmom_key});
      bool mu_d_common_ancestor =
          (mu_gdmom_key > 0 && VEC_OR_EQ(d_lineage_keys, mu_gdmom_key)) ||
          (mu_gdgdmom_key > 0 && VEC_OR_EQ(d_lineage_keys, mu_gdgdmom_key)) ||
          (mu_gdgdgdmom_key > 0 && VEC_OR_EQ(d_lineage_keys, mu_gdgdgdmom_key));
      mu_ancestry_ok = !dd_tau_ok && VEC_OR_EQ(d_mesons, mu_mom_id) &&
                       (mu_d_common_ancestor || b_bkgcat == 50);
    } else {  // else looking at a signal-like decay
      mu_ancestry_ok = dd_tau_ok;
    }

    // TODO separate cocktails
    if (!debug_dd_all_cocktail) added += 0;

    // Also, just check that the B ID is as expected for the decay
    return mu_ancestry_ok && b_id == b_expect_id;
  }

  ////////// Constructor (no default)

  D0TruthMatch(int decay_id_, int b_id_, int mu_id_, int mu_mom_id_,
               int mu_gdmom_id_, int mu_gdgdmom_id_, int mu_gdgdgdmom_id_,
               int mu_mom_key_, int mu_gdmom_key_, int mu_gdgdmom_key_,
               int mu_gdgdgdmom_key_, int d_mom_id_, int d_gdmom_id_,
               int d_gdgdmom_id_, int d_gdgdgdmom_id_, int d_mom_key_,
               int d_gdmom_key_, int d_gdgdmom_key_, int d_gdgdgdmom_key_,
               double d_trueE_, double d_truePx_, double d_truePy_,
               double d_truePz_, double d_mom_trueE_, double d_mom_truePx_,
               double d_mom_truePy_, double d_mom_truePz_,
               double d_gdmom_trueE_, double d_gdmom_truePx_,
               double d_gdmom_truePy_, double d_gdmom_truePz_, int b_bkgcat_,
               bool debug_dstst_all_cocktail_,
               bool debug_dstst_higher_separate_cocktail_,
               bool debug_dstst_s_all_cocktail_, bool debug_dd_all_cocktail_) {
    // set simple fields; ensure all IDs (except maybe cocktail_id) are
    // positive- not looking for wrong signs when truth-matching
    decay_id         = decay_id_;
    b_id             = abs(b_id_);
    mu_id            = abs(mu_id_);
    mu_mom_id        = abs(mu_mom_id_);
    mu_gdmom_id      = abs(mu_gdmom_id_);
    mu_gdgdmom_id    = abs(mu_gdgdmom_id_);
    mu_gdgdgdmom_id  = abs(mu_gdgdgdmom_id_);
    mu_mom_key       = mu_mom_key_;
    mu_gdmom_key     = mu_gdmom_key_;
    mu_gdgdmom_key   = mu_gdgdmom_key_;
    mu_gdgdgdmom_key = mu_gdgdgdmom_key_;
    d_mom_id         = abs(d_mom_id_);
    d_gdmom_id       = abs(d_gdmom_id_);
    d_gdgdmom_id     = abs(d_gdgdmom_id_);
    d_gdgdgdmom_id   = abs(d_gdgdmom_id_);
    d_mom_key        = d_mom_key_;
    d_gdmom_key      = d_gdmom_key_;
    d_gdgdmom_key    = d_gdgdmom_key_;
    d_gdgdgdmom_key  = d_gdgdgdmom_key_;
    d_truep4.SetPxPyPzE(d_truePx_, d_truePy_, d_truePz_, d_trueE_);
    d_mom_truep4.SetPxPyPzE(d_mom_truePx_, d_mom_truePy_, d_mom_truePz_,
                            d_mom_trueE_);
    d_gdmom_truep4.SetPxPyPzE(d_gdmom_truePx_, d_gdmom_truePy_, d_gdmom_truePz_,
                              d_gdmom_trueE_);
    b_bkgcat                 = b_bkgcat_;
    debug_dstst_all_cocktail = debug_dstst_all_cocktail_;
    debug_dstst_higher_separate_cocktail =
        debug_dstst_higher_separate_cocktail_;
    debug_dstst_s_all_cocktail = debug_dstst_s_all_cocktail_;
    debug_dd_all_cocktail      = debug_dd_all_cocktail_;

    // set decay descriptors and call truth-matching
    if (COMMON_SELEC()) {  // make sure some common selections are fulfilled
                           // first
      switch (decay_id) {
        case 12573012:
          b_expect_id   = PDG_ID_Bu;
          dst_expect_id = -1;
          tau_expect    = false;
          if (TRUTH_MATCH_NORMSIG()) truthmatch = d0 + mu;
          break;
        case 11574021:
          b_expect_id   = PDG_ID_B0;
          dst_expect_id = PDG_ID_Dst;
          tau_expect    = false;
          if (TRUTH_MATCH_NORMSIG()) truthmatch = dstp + mu;
          break;
        case 12773410:
          b_expect_id   = PDG_ID_Bu;
          dst_expect_id = PDG_ID_Dst0;
          tau_expect    = false;
          if (TRUTH_MATCH_NORMSIG()) truthmatch = dst0 + mu;
          break;
        case 12573001:
          b_expect_id   = PDG_ID_Bu;
          dst_expect_id = -1;
          tau_expect    = true;
          if (TRUTH_MATCH_NORMSIG()) truthmatch = d0 + tau;
          break;
        case 11574011:
          b_expect_id   = PDG_ID_B0;
          dst_expect_id = PDG_ID_Dst;
          tau_expect    = true;
          if (TRUTH_MATCH_NORMSIG()) truthmatch = dstp + tau;
          break;
        case 12773400:
          b_expect_id   = PDG_ID_Bu;
          dst_expect_id = PDG_ID_Dst0;
          tau_expect    = true;
          if (TRUTH_MATCH_NORMSIG()) truthmatch = dst0 + tau;
          break;
        case 11874430:
          b_expect_id  = PDG_ID_B0;
          tau_expect   = false;
          dstst_higher = false;
          if (TRUTH_MATCH_DSTST()) truthmatch = dststp + mu + added;
          break;
        case 11874440:
          b_expect_id  = PDG_ID_B0;
          tau_expect   = true;
          dstst_higher = false;
          if (TRUTH_MATCH_DSTST()) truthmatch = dststp + tau + added;
          break;
        case 12873450:
          b_expect_id  = PDG_ID_Bu;
          tau_expect   = false;
          dstst_higher = false;
          if (TRUTH_MATCH_DSTST()) truthmatch = dstst0 + mu + added;
          break;
        case 12873460:
          b_expect_id  = PDG_ID_Bu;
          tau_expect   = true;
          dstst_higher = false;
          if (TRUTH_MATCH_DSTST()) truthmatch = dstst0 + tau + added;
          break;
        case 12675011:
          b_expect_id  = PDG_ID_Bu;
          tau_expect   = false;
          dstst_higher = true;
          if (TRUTH_MATCH_DSTST()) truthmatch = dHstst0 + mu + added;
          break;
        case 11674401:
          b_expect_id  = PDG_ID_B0;
          tau_expect   = false;
          dstst_higher = true;
          if (TRUTH_MATCH_DSTST()) truthmatch = dHststp + mu + added;
          break;
        case 12675402:
          b_expect_id  = PDG_ID_Bu;
          tau_expect   = false;
          dstst_higher = true;
          if (TRUTH_MATCH_DSTST()) truthmatch = dHstst0 + mu + added;
          break;
        case 11676012:
          b_expect_id  = PDG_ID_B0;
          tau_expect   = false;
          dstst_higher = true;
          if (TRUTH_MATCH_DSTST()) truthmatch = dHststp + mu + added;
          break;
        case 12875440:
          b_expect_id  = PDG_ID_Bu;
          tau_expect   = false;
          dstst_higher = true;
          if (TRUTH_MATCH_DSTST()) truthmatch = dHstst0 + mu + added;
          break;
        case 13874020:
          b_expect_id  = PDG_ID_Bs;
          tau_expect   = false;
          dstst_higher = false;
          if (TRUTH_MATCH_DSTST()) truthmatch = dsstst + mu + added;
          break;
        case 13674000:
          b_expect_id  = PDG_ID_Bs;
          tau_expect   = false;
          dstst_higher = false;
          if (TRUTH_MATCH_DSTST()) truthmatch = dsstst + mu + added;
          break;
        case 11894600:
          b_expect_id = PDG_ID_B0;
          tau_expect  = false;
          if (TRUTH_MATCH_DD()) truthmatch = dd_bd + mu + added;
          break;
        case 12893600:
          b_expect_id = PDG_ID_Bu;
          tau_expect  = false;
          if (TRUTH_MATCH_DD()) truthmatch = dd_bu + mu + added;
          break;
        case 11894200:
          b_expect_id = PDG_ID_B0;
          tau_expect  = true;
          if (TRUTH_MATCH_DD()) truthmatch = dd_bd + tau + added;
          break;
        case 12893610:
          b_expect_id = PDG_ID_Bu;
          tau_expect  = true;
          if (TRUTH_MATCH_DD()) truthmatch = dd_bu + tau + added;
          break;
      }
    }
  }
};

////////////////////
// User Functions //
////////////////////
// Notes for user:
// It is the user's responsibility to set decay_id correctly; there is no way
// for me to check this internally (unless we add a decay_id branch to ntuples
// elsewhere)

// TODO: since this is for user, maybe change input paramater names to match
// what is usually found in ntuples?
//////// Truth-Matching Selection Function (for users) for Decays Reconstructed
/// as B0 -> D*+ [-> D0 [-> K- pi+] spi+] mu- (nu)
int MC_TRUTH_MATCH_DST(int decay_id, int mu_id, int mu_mom_id, int mu_gdmom_id,
                       int mu_gdgdmom_id, int mu_mom_key, int mu_gdmom_key,
                       int mu_gdgdmom_key, int dst_mom_id, int dst_gdmom_id,
                       int dst_gdgdmom_id, int dst_mom_key, int dst_gdmom_key,
                       int dst_gdgdmom_key, double dst_mom_trueE,
                       double dst_mom_truePx, double dst_mom_truePy,
                       double dst_mom_truePz, double dst_trueE,
                       double dst_truePx, double dst_truePy, double dst_truePz,
                       int dst_bkgcat, int d0_bkgcat, int b_bkgcat,
                       bool debug_dstst_all_cocktail             = false,
                       bool debug_dstst_higher_separate_cocktail = false,
                       bool debug_dstst_s_all_cocktail           = false,
                       bool debug_dd_all_cocktail                = true) {
  // create object for event truth-matching; truth-matching will be done
  // internally when object created
  DstTruthMatch event(
      decay_id, mu_id, mu_mom_id, mu_gdmom_id, mu_gdgdmom_id, mu_mom_key,
      mu_gdmom_key, mu_gdgdmom_key, dst_mom_id, dst_gdmom_id, dst_gdgdmom_id,
      dst_mom_key, dst_gdmom_key, dst_gdgdmom_key, dst_mom_trueE,
      dst_mom_truePx, dst_mom_truePy, dst_mom_truePz, dst_trueE, dst_truePx,
      dst_truePy, dst_truePz, dst_bkgcat, d0_bkgcat, b_bkgcat,
      debug_dstst_all_cocktail, debug_dstst_higher_separate_cocktail,
      debug_dstst_s_all_cocktail, debug_dd_all_cocktail);
  return event.truthmatch;
}

//////// Truth-Matching Selection Function (for users) for Decays Reconstructed
/// as B- -> D0 [-> K- pi+] mu- (nu)
int MC_TRUTH_MATCH_D0(int decay_id, int b_id, int mu_id, int mu_mom_id,
                      int mu_gdmom_id, int mu_gdgdmom_id, int mu_gdgdgdmom_id,
                      int mu_mom_key, int mu_gdmom_key, int mu_gdgdmom_key,
                      int mu_gdgdgdmom_key, int d_mom_id, int d_gdmom_id,
                      int d_gdgdmom_id, int d_gdgdgdmom_id, int d_mom_key,
                      int d_gdmom_key, int d_gdgdmom_key, int d_gdgdgdmom_key,
                      double d_trueE, double d_truePx, double d_truePy,
                      double d_truePz, double d_mom_trueE, double d_mom_truePx,
                      double d_mom_truePy, double d_mom_truePz,
                      double d_gdmom_trueE, double d_gdmom_truePx,
                      double d_gdmom_truePy, double d_gdmom_truePz,
                      int b_bkgcat, bool debug_dstst_all_cocktail = false,
                      bool debug_dstst_higher_separate_cocktail = false,
                      bool debug_dstst_s_all_cocktail           = false,
                      bool debug_dd_all_cocktail                = true) {
  D0TruthMatch event(
      decay_id, b_id, mu_id, mu_mom_id, mu_gdmom_id, mu_gdgdmom_id,
      mu_gdgdgdmom_id, mu_mom_key, mu_gdmom_key, mu_gdgdmom_key,
      mu_gdgdgdmom_key, d_mom_id, d_gdmom_id, d_gdgdmom_id, d_gdgdgdmom_id,
      d_mom_key, d_gdmom_key, d_gdgdmom_key, d_gdgdgdmom_key, d_trueE, d_truePx,
      d_truePy, d_truePz, d_mom_trueE, d_mom_truePx, d_mom_truePy, d_mom_truePz,
      d_gdmom_trueE, d_gdmom_truePx, d_gdmom_truePy, d_gdmom_truePz, b_bkgcat,
      debug_dstst_all_cocktail, debug_dstst_higher_separate_cocktail,
      debug_dstst_s_all_cocktail, debug_dd_all_cocktail);
  return event.truthmatch;
}

#endif

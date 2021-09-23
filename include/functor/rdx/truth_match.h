// Author: Yipeng Sun, Alex Fernez
// License: BSD 2-clause
// Last Change: Sep 23, 2021

#ifndef _LNG_FUNCTOR_RDX_TRUTH_MATCH_H_
#define _LNG_FUNCTOR_RDX_TRUTH_MATCH_H_

#include <TMath.h>
#include <assert.h>

#include "pdg.h"
#include "functor/basic.h"
#include "TLorentzVector.h"

using namespace std;

// TODO take advantage of similarity of truth-matching classes and make a TruthMatch class that both inherit from
// TODO check things against code in gitlab instead of preservation repo; also change the links

/////////// General Helper Functions

int HUNDREDS_DIGIT(int a) {
  return floor((a%1000)/100);
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

///////////////////////////////// D* Truth-Matching Selections based on Phoebe's
////////// https://github.com/umd-lhcb/RDRDstRun1AnalysisPreservation/blob/de225b567e7004a45f6003ef117428f421e7fa13/proc/redoHistos_Dst.C
////// and https://github.com/umd-lhcb/RDRDstRun1AnalysisPreservation/blob/ca8f0df0e1206f9bd3f3c64d12958ffb1025574a/proc/AddB.C

// There are a lot of variables being used in the truth-matching functions. In order to guard against typos, do the
// truth-matching via OOP, so that you only have to enter pass the variables once.
class DstTruthMatch {

  private:

    int decay_id; int mu_id; int mu_mom_id; int mu_gdmom_id; int mu_gdgdmom_id; int mu_mom_key; int mu_gdmom_key; int mu_gdgdmom_key;
    int dst_mom_id; int dst_gdmom_id; int dst_gdgdmom_id; int dst_mom_key; int dst_gdmom_key; int dst_gdgdmom_key;
    TLorentzVector dst_mom_truep4; TLorentzVector dst_truep4; int dst_bkgcat; int d0_bkgcat; int b_bkgcat; int cocktail_id; bool twopi;
    // Lists of particles
    vector<int> charged_dstst{PDG_ID_D1,PDG_ID_D1p,PDG_ID_D2st};
    vector<int> neutral_dstst{PDG_ID_D1_0,PDG_ID_D1p_0,PDG_ID_D2st_0};
    vector<int> strange_dstst{PDG_ID_D1p_s, PDG_ID_D2st_s};
    vector<int> charged_dstst_higher{PDG_ID_Dst2S, PDG_ID_D2S, FAKE_ID_D2750, FAKE_ID_D3000};
    vector<int> neutral_dstst_higher{PDG_ID_Dst2S_0, PDG_ID_D2S_0, FAKE_ID_D2750_0, FAKE_ID_D3000_0};
    vector<int> d_mesons{PDG_ID_D, PDG_ID_D0, PDG_ID_Ds};
    vector<int> dstst_s_1_mesons{PDG_ID_D1_s, PDG_ID_D1p_s};
    // Derived from (and used in place of) decay mode # considered (set on construction)
    int b_expect_id; bool tau_expect; bool dstst_higher;
    // variable for successful truth-matching (set on construction)
    bool truth_matched=false;


  public:

    ///////// Helpers

    bool DST_COMMON_SELEC() {
      return (dst_bkgcat==0 || (dst_bkgcat==50 && d0_bkgcat==50)) && mu_id==PDG_ID_mu;
    }

    bool DSTST_OKAY(int dstst_id) {
      return (  (b_expect_id==PDG_ID_B0 && VEC_OR_EQ(charged_dstst, dstst_id) && !dstst_higher)
             || (b_expect_id==PDG_ID_Bu && VEC_OR_EQ(neutral_dstst, dstst_id) && !dstst_higher)
             || (b_expect_id==PDG_ID_Bs && VEC_OR_EQ(strange_dstst, dstst_id) && !dstst_higher)
             || (b_expect_id==PDG_ID_B0 && VEC_OR_EQ(charged_dstst_higher, dstst_id) && dstst_higher)
             || (b_expect_id==PDG_ID_B0 && VEC_OR_EQ(neutral_dstst_higher, dstst_id) && dstst_higher) );
    }

    bool TWO_PI() {
      double mm2_mom = (dst_mom_truep4-dst_truep4).M2(); // MeV
      return mm2_mom>0 && sqrt(mm2_mom)>250;
    }

    //////// Specific Decay Truth-Matching

    // Normalization and Signal
    // Phoebe redoHistos_Dst.C: flagBmu/flagtaumu > 0. && JustDst > 0. && DstOk > 0. && muPID == 1. && Btype == 511 && [for norm only] Y_BKGCAT==0
    // TODO Note: Phoebe does some redefining of her Y_BKGCAT in her AddB.C, but I've just used the b_bkgcat from the ntuple as-is
    bool MC_TRUTH_MATCH_BD2DST() {
      // Make sure ancestry of mu is correct, including making sure B in mu ancestry and B in D* ancestry are the same
      bool mu_ancestry_ok = false;
      if (!tau_expect) {
        mu_ancestry_ok = mu_mom_id==PDG_ID_B0 && mu_mom_key>0 && mu_mom_key==dst_mom_key;
      } else { // else looking at a signal decay
        mu_ancestry_ok = mu_mom_id==PDG_ID_tau && mu_gdmom_id==PDG_ID_B0 && mu_gdmom_key>0 && mu_gdmom_key==dst_mom_key;
      }

      // Implement the b_bkgcat selection for normalization, and ensure (really, a second check) that D* mom is B0
      return ((b_bkgcat==0) || tau_expect) && dst_mom_id==PDG_ID_B0 && mu_ancestry_ok;
    }

    // D**, D_H**, D_s**
    // Phoebe redoHistos_Dst.C: flagBmu/flagtaumu > 0 && JustDst < 1  && DstOk > 0. && Btype==511/521/531 && Dststtype == [D** cocktail] && muPID == 1 && mm_mom<250 (not for D**H,s)
    // Note: I don't implement Phoebe's ishigher, instead just using the variable dstst_higher to keep track of the considered decay ID
    // Note: compared to the D0 sample, this selection is simpler because here the decay is required to go B->D**->D*
    // TODO: check this function against Phoebe again...
    bool MC_TRUTH_MATCH_B2DSTST() {
      // Make sure requested cocktail is acceptable, then check if D* mom is right. It is worth noting here which cocktails are acceptable (look at defined
      // lists of particles [private fields])
      assert(DSTST_OKAY(cocktail_id) || cocktail_id==-1);
      bool dst_mom_id_ok = false;
      if (dst_mom_id==cocktail_id) dst_mom_id_ok=true;
      else if (cocktail_id==-1 && DSTST_OKAY(dst_mom_id)) dst_mom_id_ok=true;

      // Make sure ancestry of mu is correct, including making sure B in mu ancestry and B in D* ancestry are the same
      bool mu_ancestry_ok = false;
      if (!tau_expect) {
        mu_ancestry_ok = mu_mom_id==b_expect_id && mu_mom_key>0 && mu_mom_key==dst_gdmom_key;
      } else { // else looking at a signal-like decay
        mu_ancestry_ok = mu_mom_id==PDG_ID_tau && mu_gdmom_id==b_expect_id && mu_mom_key>0 && mu_gdmom_key==dst_gdmom_key;
      }

      // Finally, ensure the D** mom (and thus D* gdmom) is in fact the correct B, and cut out D** events where the D** goes to two pions (like Phoebe),
      // as requested by the user--don't do for strange/higher D**
      return dst_mom_id_ok && mu_ancestry_ok && dst_gdmom_id==b_expect_id && ((b_expect_id==PDG_ID_Bs || dstst_higher) || ((!twopi && !TWO_PI()) || (twopi && TWO_PI())));
    }

    // DD
    // Phoebe's redoHistos_Dst.C: DstOk > 0. && muPID == 1 && Btype==511/521 && ((flagDoubleD > 0 && flagTauonicD < 1) OR flagTauonicD > 0)
    // Truthfully, though confusing, her truth-matching seems somewhat minimalistic/loose to me, which may be the best way to go...
    // Note: the use of the mu and D* ancestry keys is quite different here wrt other truth-matching; I think the general idea is that D* and mu should
    //   have SOME common ancestor, whereas for the other truth-matching we were always explicitly ensuring that that common ancestor was the B. In fact,
    //   for the tauonic DD decays, no key matching is done at all.
    // I won't implement a cocktail selection here for now: it isn't possible without more information about daughters (which will come for us via TupleToolSLTruth)
    // TODO: check this function against Phoebe again...
    bool MC_TRUTH_MATCH_B2DSTDX() {
      // For a DD decay with no tau, ensure at least that the mu came from a (spin 0) charm meson and that mu and D* have some ancesteor in common, OR, as
      // a special case, just check its gdgdmom is Ds1(') and D* mom is in fact B; also explicitly reject the conditions that are used to qualify a DD decay
      // with a tau. For the DD decay with a tau, require that mu's mother is a tau and gdmom is Ds (don't bother with key-checking).
      bool mu_ancestry_ok_or_special=false;
      bool dd_tau_ok = mu_mom_id==PDG_ID_tau && mu_gdmom_id==PDG_ID_Ds;
      if (!tau_expect) {
        vector<int> dst_lineage_keys{dst_mom_key, dst_gdmom_key, dst_gdgdmom_key};
        bool mu_dst_common_ancestor = (mu_gdmom_key>0 && VEC_OR_EQ(dst_lineage_keys, mu_gdmom_key)) || (mu_gdgdmom_key>0 && VEC_OR_EQ(dst_lineage_keys, mu_gdgdmom_key));
        mu_ancestry_ok_or_special = !dd_tau_ok && ((VEC_OR_EQ(d_mesons, mu_mom_id) && mu_dst_common_ancestor) || (VEC_OR_EQ(dstst_s_1_mesons, mu_gdgdmom_id) && dst_mom_id==b_expect_id));
      } else { // else looking at a signal-like decay
        mu_ancestry_ok_or_special=dd_tau_ok;
      }

      // Also, just ensure that there is a B somewhere within three generations of the D*
      vector<int> dst_lineage_ids{dst_mom_id, dst_gdmom_id, dst_gdgdmom_id};
      return mu_ancestry_ok_or_special && VEC_OR_EQ(dst_lineage_ids, b_expect_id);
    }

    ////////// Constructor (no default)

    DstTruthMatch(int decay_id_, int mu_id_, int mu_mom_id_, int mu_gdmom_id_, int mu_gdgdmom_id_, int mu_mom_key_, int mu_gdmom_key_, int mu_gdgdmom_key_,
                  int dst_mom_id_, int dst_gdmom_id_, int dst_gdgdmom_id_, int dst_mom_key_, int dst_gdmom_key_, int dst_gdgdmom_key_,
                  double dst_mom_trueE_, double dst_mom_truePx_, double dst_mom_truePy_, double dst_mom_truePz_, double dst_trueE_, double dst_truePx_,
                  double dst_truePy_, double dst_truePz_, int dst_bkgcat_, int d0_bkgcat_, int b_bkgcat_, int cocktail_id_, bool twopi_) {
      // set simple fields; ensure all IDs (except maybe cocktail_id) are positive- not looking for wrong signs when truth-matching
      decay_id=decay_id_; mu_id=abs(mu_id_); mu_mom_id=abs(mu_mom_id_); mu_gdmom_id=abs(mu_gdmom_id_); mu_gdgdmom_id=abs(mu_gdgdmom_id_); mu_mom_key=mu_mom_key_;
      mu_gdmom_key=mu_gdmom_key_; mu_gdgdmom_key=mu_gdgdmom_key_; dst_mom_id=abs(dst_mom_id_); dst_gdmom_id=abs(dst_gdmom_id_); dst_gdgdmom_id=abs(dst_gdgdmom_id_);
      dst_mom_key=dst_mom_key_; dst_gdmom_key=dst_gdmom_key_; dst_gdgdmom_key=dst_gdgdmom_key_;
      dst_mom_truep4.SetPxPyPzE(dst_mom_truePx_, dst_mom_truePy_, dst_mom_truePz_, dst_mom_trueE_); dst_truep4.SetPxPyPzE(dst_truePx_, dst_truePy_, dst_truePz_, dst_trueE_);
      dst_bkgcat=dst_bkgcat_; d0_bkgcat=d0_bkgcat_; b_bkgcat=b_bkgcat_; cocktail_id=cocktail_id_; twopi=twopi_;

      // set decay descriptors and call truth-matching
      if (DST_COMMON_SELEC()) { // make sure some common selections are fulfilled first
        switch (decay_id) {
          case 11574021: tau_expect=false; truth_matched=MC_TRUTH_MATCH_BD2DST(); break;
          case 11574011: tau_expect=true; truth_matched=MC_TRUTH_MATCH_BD2DST(); break;
          case 11874430: b_expect_id=PDG_ID_B0; tau_expect=false; dstst_higher=false; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 11874440: b_expect_id=PDG_ID_B0; tau_expect=true; dstst_higher=false; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 12873450: b_expect_id=PDG_ID_Bu; tau_expect=false; dstst_higher=false; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 12873460: b_expect_id=PDG_ID_Bu; tau_expect=true; dstst_higher=false; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 11676012: b_expect_id=PDG_ID_B0; tau_expect=false; dstst_higher=true; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 12675402: b_expect_id=PDG_ID_Bu; tau_expect=false; dstst_higher=true; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 13674000: b_expect_id=PDG_ID_Bs; tau_expect=false; dstst_higher=false; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 11894610: b_expect_id=PDG_ID_B0; tau_expect=false; truth_matched=MC_TRUTH_MATCH_B2DSTDX(); break;
          case 12895400: b_expect_id=PDG_ID_Bu; tau_expect=false; truth_matched=MC_TRUTH_MATCH_B2DSTDX(); break;
          case 11894210: b_expect_id=PDG_ID_B0; tau_expect=true; truth_matched=MC_TRUTH_MATCH_B2DSTDX(); break;
          case 12895000: b_expect_id=PDG_ID_Bu; tau_expect=true; truth_matched=MC_TRUTH_MATCH_B2DSTDX(); break;
        }
      }
    }

    // Allows access to calculated truth-matching
    bool TRUTH_MATCHED() {return truth_matched;}
};


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

///////////////////////////////// D0 Truth-Matching Selections based on Phoebe's
////////// https://github.com/umd-lhcb/RDRDstRun1AnalysisPreservation/blob/ca8f0df0e1206f9bd3f3c64d12958ffb1025574a/proc/redoHistos_D0.C
////// and https://github.com/umd-lhcb/RDRDstRun1AnalysisPreservation/blob/ca8f0df0e1206f9bd3f3c64d12958ffb1025574a/proc/AddD0B_temp.C

// There are a lot of variables being used in the truth-matching functions. In order to guard against typos, do the
// truth-matching via OOP, so that you only have to enter pass the variables once.
class D0TruthMatch {

  private:

    int decay_id; int b_id; int mu_id; int mu_mom_id; int mu_gdmom_id; int mu_gdgdmom_id; int mu_gdgdgdmom_id; int mu_mom_key; int mu_gdmom_key; int mu_gdgdmom_key; int mu_gdgdgdmom_key;
    int d_mom_id; int d_gdmom_id; int d_gdgdmom_id; int d_gdgdgdmom_id; int d_mom_key; int d_gdmom_key; int d_gdgdmom_key; int d_gdgdgdmom_key;
    TLorentzVector d_truep4; TLorentzVector d_mom_truep4; TLorentzVector d_gdmom_truep4;
    int b_bkgcat; double d_m; int cocktail_id; bool twopi;
    // special variables used for D** truth-matching: copied from Phoebe's code
    int Btype=0; int Dststtype=0;
    // Lists of particles
    vector<int> b_mesons{PDG_ID_B0, PDG_ID_Bu, PDG_ID_Bs};
    vector<int> dst_dst0{PDG_ID_Dst, PDG_ID_Dst0};
    vector<int> b0_bu{PDG_ID_B0, PDG_ID_Bu};
    vector<int> charged_dstst{PDG_ID_D0st, PDG_ID_D1, PDG_ID_D1p, PDG_ID_D2st};
    vector<int> neutral_dstst{PDG_ID_D0st_0, PDG_ID_D1_0, PDG_ID_D1p_0, PDG_ID_D2st_0};
    vector<int> strange_dstst{PDG_ID_D1p_s, PDG_ID_D2st_s};
    vector<int> charged_dstst_higher{PDG_ID_Dst2S, PDG_ID_D2S, FAKE_ID_D2750, FAKE_ID_D3000};
    vector<int> neutral_dstst_higher{PDG_ID_Dst2S_0, PDG_ID_D2S_0, FAKE_ID_D2750_0, FAKE_ID_D3000_0};
    vector<int> d1_d10{PDG_ID_D1, PDG_ID_D1_0};
    vector<int> d_mesons{PDG_ID_D, PDG_ID_D0, PDG_ID_Ds};
    // Derived from (and used in place of) decay mode # considered (set on construction)
    int b_expect_id; bool tau_expect; bool dstst_higher; int dst_expect_id;
    // variable for successful truth-matching (set on construction)
    bool truth_matched=false;


  public:

    ///////// Helpers

    bool D0_COMMON_SELEC() {
      return (abs(d_m-PDG_M_D0)<23.4 && mu_id==PDG_ID_mu);
    }

    bool DSTST_OKAY(int dstst_id) {
      return (  (b_expect_id==PDG_ID_B0 && VEC_OR_EQ(charged_dstst, dstst_id) && !dstst_higher)
             || (b_expect_id==PDG_ID_Bu && VEC_OR_EQ(neutral_dstst, dstst_id) && !dstst_higher)
             || (b_expect_id==PDG_ID_Bs && VEC_OR_EQ(strange_dstst, dstst_id) && !dstst_higher)
             || (b_expect_id==PDG_ID_B0 && VEC_OR_EQ(charged_dstst_higher, dstst_id) && dstst_higher)
             || (b_expect_id==PDG_ID_B0 && VEC_OR_EQ(neutral_dstst_higher, dstst_id) && dstst_higher) );
    }

    // TODO Phoebe redefines Y_BKGCAT in her AddD0B_temp.C too much; for now, I'm just implementing something similar
    // Need nu_mu momentum info in order to exactly copy Phoebe's implementation!
    bool B_BKGCAT_OKAY() {
      return (!tau_expect && dst_expect_id==-1 && b_bkgcat==0) || (tau_expect && dst_expect_id==-1 && b_bkgcat==10)
             || (!tau_expect && dst_expect_id!=-1/* && b_bkgcat==5*/) || (tau_expect && dst_expect_id!=-1/* && b_bkgcat==15*/);
    }

    // Requires D0 has B either as gdmom or gdgdmom
    bool SIMPLEDSTST_KEYMATCH() {
      bool b_is_gdmom=VEC_OR_EQ(b_mesons, d_gdmom_id);
      bool b_is_gdgdmom=VEC_OR_EQ(b_mesons, d_gdgdmom_id);
      if (b_is_gdmom) return (mu_mom_key==d_gdmom_key || mu_gdmom_key==d_gdmom_key);
      else if (b_is_gdgdmom) return (mu_mom_key==d_gdgdmom_key || mu_gdmom_key==d_gdgdmom_key);
      else return false;
    }

    // Note that there is SOME key matching done here (via Phoebe's simpleDstst); if the key-matching fails, just return without
    // setting Btype and Dststtype (they are defaulted to 0). Also if B->D0, return without setting the variables (this function
    // is assumedly only used for D** truth-matching)
    void SET_BTYPE_DSTSTTYPE() {
      if (VEC_OR_EQ(b_mesons, d_mom_id)) return;
      else if (VEC_OR_EQ(b_mesons, d_gdmom_id)) {
        if (!(SIMPLEDSTST_KEYMATCH())) return;
        Btype=d_gdmom_id;
        Dststtype=d_mom_id;
      }
      else if (VEC_OR_EQ(b_mesons, d_gdgdmom_id) && VEC_OR_EQ(dst_dst0, d_mom_id)) {
        if (!(SIMPLEDSTST_KEYMATCH())) return;
        Btype=d_gdgdmom_id;
        Dststtype=d_gdmom_id;
      }
      else if (VEC_OR_EQ(b_mesons, d_gdgdmom_id) && b_id==d_gdgdmom_id) Btype=d_gdgdmom_id;
      else if (VEC_OR_EQ(b_mesons, d_gdgdgdmom_id) && b_id==d_gdgdgdmom_id) Btype=d_gdgdgdmom_id;
      else if (VEC_OR_EQ(b_mesons, mu_gdmom_id) && b_id==mu_gdmom_id) Btype=mu_gdmom_id;
      else if (VEC_OR_EQ(b_mesons, mu_gdgdmom_id) && b_id==mu_gdgdmom_id) Btype=mu_gdgdmom_id;
      else if (VEC_OR_EQ(b_mesons, mu_gdgdgdmom_id) && b_id==mu_gdgdgdmom_id) Btype=mu_gdgdgdmom_id;
      else Dststtype=-2; // done to copy Phoebe's code more precisely, but also to ensure works correctly with my code

      // note that b_bkgcat here is used in Phoebe's code before she redefines it
      if (Dststtype==0 && b_bkgcat==50 && (VEC_OR_EQ(b0_bu, mu_mom_id) || (mu_mom_id==15 && VEC_OR_EQ(b0_bu, mu_gdmom_id)))) { // Phoebe has a typo in this line (2907)
        Btype=b_id;
        if (HUNDREDS_DIGIT(d_gdgdmom_id)==4) Dststtype=d_gdgdmom_id;
        else if (HUNDREDS_DIGIT(d_gdgdmom_id)==5 && HUNDREDS_DIGIT(d_gdmom_id)==4) Dststtype=d_gdmom_id;
        else if (HUNDREDS_DIGIT(d_gdmom_id)==5 && HUNDREDS_DIGIT(d_mom_id)==4) Dststtype=d_mom_id;
      }

      // in redoHistos_D0.C, Phoebe does one last thing to fix a truth-matching bug
      if (mu_mom_id==PDG_ID_tau && Dststtype==0 && !SIMPLEDSTST_KEYMATCH() && VEC_OR_EQ(d1_d10, d_gdmom_id)) Dststtype=d_gdmom_id;
    }

    bool TWO_PI() {
      // A bit confusing, but for now, just copy Phoebe's implementation (TODO think about this...)
      double mm2_mom;
      if (!(VEC_OR_EQ(dst_dst0, d_mom_id) && VEC_OR_EQ(b_mesons, d_gdgdmom_id))) mm2_mom=(d_mom_truep4-d_truep4).M2(); // Mev
      else mm2_mom=(d_gdmom_truep4-d_mom_truep4).M2(); // MeV
      return mm2_mom>0 && sqrt(mm2_mom)>220;
    }

    //////// Specific Decay Truth-Matching

    // Normalization and Signal
    // Phoebe redoHistos_D0.C: flagBmu/flagtaumu > 0 && muPID==1 && Y_BKGCAT==0/10/5/15 (Dmu, Dtau, D*mu, D*tau) && Btype==b_expect_id && JustDst > 0 (for Dmu, Dtau)
    // Note: JustDst is a misnomer- it should really be "JustD0"
    bool MC_TRUTH_MATCH_B2D() {
      // Make sure ancestry of mu is correct, including making sure B in mu ancestry and B in D0 ancestry are the same
      // Note that a check that B(->D*)->D0 proceeds as expected for the decay (should) occur later when selecting on b_bkgcat, so it's fine here to just look at all
      // of the keys of the D0 ancestors to check against the B from the mu ancestry
      bool mu_ancestry_ok = false;
      vector<int> d_lineage_keys{d_mom_key, d_gdmom_key, d_gdgdmom_key};
      if (!tau_expect) {
        mu_ancestry_ok = mu_mom_id==b_expect_id && mu_mom_key>0 && VEC_OR_EQ(d_lineage_keys, mu_mom_key);
      } else { // else looking at a signal decay
        mu_ancestry_ok = mu_mom_id==PDG_ID_tau && mu_gdmom_id==b_expect_id && mu_mom_key>0 && VEC_OR_EQ(d_lineage_keys, mu_gdmom_key);
      }

      // Implement the b_bkgcat selection (note that this is used for all decay modes here, whereas for the D* sample it was only used for normalization)
      // Also, if decay goes like B->D0, then require that the correct B is indeed the mother of the D0
      return B_BKGCAT_OKAY() && (dst_expect_id!=-1 || d_mom_id==b_expect_id) && mu_ancestry_ok;
    }

    // D**, D_H**, D_s**
    // Phoebe redoHistos_D0.C: flagBmu/flagtaumu > 0 && JustDst < 1 && Btype == [b_expect_id] && Dststtype == [cocktail_id] && muPID == 1 && mm_mom<220 (not for D**H,s) && simpleDstst (not for D**H,s)
    // Note: I don't implement Phoebe's ishigher, instead just using the variable dstst_higher to keep track of the considered decay ID
    // Note: Phoebe combines D**H decays into a B(+,0)->D**H->D*(+,0), a B(+,0)->D**H->D*+, and a B(+,0)->D**H->D0 template. I will separate into the explicit
    // 5 decay modes for this function instead (separating B0/B+ and D*+/D*0).
    // Note: I think Phoebe makes a (small) logical mistake in her AddD0B_temp.C and, by not checking for "onefour/twofour" when setting flagBmu, she cuts out
    // decays that go like B->D1,D2*->X->X->D0. For now, though, I will just copy her code. TODO: rethink if this is correct or not
    // Note: simpleDstst seems like a misnomer to me: it just checks that (if decay goes B->D**->D0 or B->D**->X->D0) then B key matches between mu/D0
    bool MC_TRUTH_MATCH_B2DSTST() {
      // Once the B and D** are found, make sure the requested cocktail is acceptable and the D** matches the cocktail or, if no cocktail selected,
      // is one of the possible cocktails for the decay mode. Also, do a quick check that Btype is as expected for the decay mode
      SET_BTYPE_DSTSTTYPE();
      assert(DSTST_OKAY(cocktail_id) || cocktail_id==-1);
      bool b_and_dstst_id_ok=false;
      if (Dststtype==cocktail_id && Btype==b_expect_id) b_and_dstst_id_ok=true;
      else if (cocktail_id==-1 && DSTST_OKAY(Dststtype) && Btype==b_expect_id) b_and_dstst_id_ok=true;

      // Make sure ancestry of mu is correct, including trying to make sure B in mu ancestry and B in D0 ancestry are the same
      // Note that SET_BTYPE_DSTSTTYPE() does some key-matching, though I'm not convinced it always exactly checks that, wherever the B is in the D0 ancestry,
      // its the same as the B from the mu ancestry (this is only explicitly done for the cases B->D**->D0 and B->D**->D*->D0). But, for now, copy Phoebe's code
      // and (though repetitive), just check here that there is indeed some key from D0 ancestry that will match B key from mu ancestry.
      // Note: you can see that decays like B->D**->X->X->D0 are cut out here explicitly; only up to d_gdgdmom_key is checked. TODO think about this...
      bool mu_ancestry_ok = false;
      vector<int> d_lineage_keys{d_mom_key, d_gdmom_key, d_gdgdmom_key};
      if (!tau_expect) {
        mu_ancestry_ok = mu_mom_id==b_expect_id && mu_mom_key>0 && VEC_OR_EQ(d_lineage_keys, mu_mom_key);
      } else { // else looking at a signal decay
        mu_ancestry_ok = mu_mom_id==PDG_ID_tau && mu_gdmom_id==b_expect_id && mu_mom_key>0 && VEC_OR_EQ(d_lineage_keys, mu_gdmom_key);
      }

      // Lastly, cut out D** events where the D** goes to two pions (like Phoebe), as requested by user--don't do for strange/higher D**
      return b_and_dstst_id_ok && mu_ancestry_ok && ((b_expect_id==PDG_ID_Bs || dstst_higher) || ((!twopi && !TWO_PI()) || (twopi && TWO_PI())));
    }

    // DD
    // Phoebe's redoHistos_D0.C: muPID == 1 && Btype==b_expect_id && ((flagDoubleD > 0 && flagTauonicD < 1) OR flagTauonicD > 0)
    // Truthfully, though confusing, her truth-matching seems somewhat minimalistic/loose to me, which may be the best way to go...
    // Note the use of the mu and D0 ancestry keys is quite different here wrt other truth-matching; I think the general idea is that D0 and mu should
    // have SOME common ancestor, whereas for the other truth-matching we were always explicitly ensuring that that common ancestor was the B. In fact,
    // for the tauonic DD decays, no key matching is done at all.
    // I won't implement a cocktail selection here for now: it isn't possible without more information about daughters (which will come for us via TupleToolSLTruth)
    // TODO: check over this function
    bool MC_TRUTH_MATCH_B2DDX() {
      // For a DD decay with no tau, ensure at least that the mu came from a (spin 0) charm meson and that mu and D0 have some ancesteor in common; also explicitly
      // reject the conditions that are used to qualify a DD decay with a tau. For the DD decay with a tau, require that mu's mother is a tau and gdmom is Ds (don't
      // bother with key-checking).
      bool mu_ancestry_ok=false;
      bool dd_tau_ok = mu_mom_id==PDG_ID_tau && mu_gdmom_id==PDG_ID_Ds;
      if (!tau_expect) {
        vector<int> d_lineage_keys({d_mom_key, d_gdmom_key, d_gdgdmom_key, d_gdgdgdmom_key});
        bool mu_d_common_ancestor = (mu_gdmom_key>0 && VEC_OR_EQ(d_lineage_keys, mu_gdmom_key)) || (mu_gdgdmom_key>0 && VEC_OR_EQ(d_lineage_keys, mu_gdgdmom_key)) || (mu_gdgdgdmom_key>0 && VEC_OR_EQ(d_lineage_keys, mu_gdgdgdmom_key));
        mu_ancestry_ok = !dd_tau_ok && VEC_OR_EQ(d_mesons, mu_mom_id) && (mu_d_common_ancestor || b_bkgcat==50);
      } else { // else looking at a signal-like decay
        mu_ancestry_ok=dd_tau_ok;
      }

      // Also, just check that the B ID is as expected for the decay
      return mu_ancestry_ok && b_id==b_expect_id;
    }

    ////////// Constructor (no default)

    D0TruthMatch(int decay_id_, int b_id_, int mu_id_, int mu_mom_id_, int mu_gdmom_id_, int mu_gdgdmom_id_, int mu_gdgdgdmom_id_, int mu_mom_key_, int mu_gdmom_key_, int mu_gdgdmom_key_, int mu_gdgdgdmom_key_,
                  int d_mom_id_, int d_gdmom_id_, int d_gdgdmom_id_, int d_gdgdgdmom_id_, int d_mom_key_, int d_gdmom_key_, int d_gdgdmom_key_, int d_gdgdgdmom_key_,
                  double d_trueE_, double d_truePx_, double d_truePy_, double d_truePz_, double d_mom_trueE_, double d_mom_truePx_, double d_mom_truePy_, double d_mom_truePz_,
                  double d_gdmom_trueE_, double d_gdmom_truePx_, double d_gdmom_truePy_, double d_gdmom_truePz_, int b_bkgcat_, double d_m_, int cocktail_id_, bool twopi_) {
      // set simple fields; ensure all IDs (except maybe cocktail_id) are positive- not looking for wrong signs when truth-matching
      decay_id=decay_id_; b_id=abs(b_id_); mu_id=abs(mu_id_); mu_mom_id=abs(mu_mom_id_); mu_gdmom_id=abs(mu_gdmom_id_); mu_gdgdmom_id=abs(mu_gdgdmom_id_); mu_gdgdgdmom_id=abs(mu_gdgdgdmom_id_); mu_mom_key=mu_mom_key_;
      mu_gdmom_key=mu_gdmom_key_; mu_gdgdmom_key=mu_gdgdmom_key_; mu_gdgdgdmom_key=mu_gdgdgdmom_key_; d_mom_id=abs(d_mom_id_); d_gdmom_id=abs(d_gdmom_id_); d_gdgdmom_id=abs(d_gdgdmom_id_); d_gdgdgdmom_id=abs(d_gdgdmom_id_);
      d_mom_key=d_mom_key_; d_gdmom_key=d_gdmom_key_; d_gdgdmom_key=d_gdgdmom_key_; d_gdgdgdmom_key=d_gdgdgdmom_key_;
      d_truep4.SetPxPyPzE(d_truePx_, d_truePy_, d_truePz_, d_trueE_); d_mom_truep4.SetPxPyPzE(d_mom_truePx_, d_mom_truePy_, d_mom_truePz_, d_mom_trueE_);
      d_gdmom_truep4.SetPxPyPzE(d_gdmom_truePx_, d_gdmom_truePy_, d_gdmom_truePz_, d_gdmom_trueE_);
      b_bkgcat=b_bkgcat_; d_m=d_m_; cocktail_id=cocktail_id_; twopi=twopi_;

      // set decay descriptors and call truth-matching
      if (D0_COMMON_SELEC()) { // make sure some common selections are fulfilled first
        switch (decay_id) {
          case 12573012: b_expect_id=PDG_ID_Bu; dst_expect_id=-1; tau_expect=false; truth_matched=MC_TRUTH_MATCH_B2D(); break;
          case 11574021: b_expect_id=PDG_ID_B0; dst_expect_id=PDG_ID_Dst; tau_expect=false; truth_matched=MC_TRUTH_MATCH_B2D(); break;
          case 12773410: b_expect_id=PDG_ID_Bu; dst_expect_id=PDG_ID_Dst0; tau_expect=false; truth_matched=MC_TRUTH_MATCH_B2D(); break;
          case 12573001: b_expect_id=PDG_ID_Bu; dst_expect_id=-1; tau_expect=true; truth_matched=MC_TRUTH_MATCH_B2D(); break;
          case 11574011: b_expect_id=PDG_ID_B0; dst_expect_id=PDG_ID_Dst; tau_expect=true; truth_matched=MC_TRUTH_MATCH_B2D(); break;
          case 12773400: b_expect_id=PDG_ID_Bu; dst_expect_id=PDG_ID_Dst0; tau_expect=true; truth_matched=MC_TRUTH_MATCH_B2D(); break;
          case 11874430: b_expect_id=PDG_ID_B0; tau_expect=false; dstst_higher=false; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 11874440: b_expect_id=PDG_ID_B0; tau_expect=true; dstst_higher=false; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 12873450: b_expect_id=PDG_ID_Bu; tau_expect=false; dstst_higher=false; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 12873460: b_expect_id=PDG_ID_Bu; tau_expect=true; dstst_higher=false; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 12675011: b_expect_id=PDG_ID_Bu; tau_expect=false; dstst_higher=true; dst_expect_id=-1; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 11674401: b_expect_id=PDG_ID_B0; tau_expect=false; dstst_higher=true; dst_expect_id=-1; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 12675402: b_expect_id=PDG_ID_Bu; tau_expect=false; dstst_higher=true; dst_expect_id=PDG_ID_Dst; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 11676012: b_expect_id=PDG_ID_B0; tau_expect=false; dstst_higher=true; dst_expect_id=PDG_ID_Dst; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 12875440: b_expect_id=PDG_ID_Bu; tau_expect=false; dstst_higher=true; dst_expect_id=PDG_ID_Dst0; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          // note: everywhere else, dst_expect_id=-1 signifies that you explicitly don't expect a D* in the decay chain, but here for the D**s decay mode
          // 13874020, I use it to signify that there may be a D* (0 or +) or there may not be; this decay mode is a mix of possibilities (note: I don't use this feature...)
          case 13874020: b_expect_id=PDG_ID_Bs; tau_expect=false; dstst_higher=false; dst_expect_id=-1; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 13674000: b_expect_id=PDG_ID_Bs; tau_expect=false; dstst_higher=false; dst_expect_id=PDG_ID_Dst; truth_matched=MC_TRUTH_MATCH_B2DSTST(); break;
          case 11894600: b_expect_id=PDG_ID_B0; tau_expect=false; truth_matched=MC_TRUTH_MATCH_B2DDX(); break;
          case 12893600: b_expect_id=PDG_ID_Bu; tau_expect=false; truth_matched=MC_TRUTH_MATCH_B2DDX(); break;
          case 11894200: b_expect_id=PDG_ID_B0; tau_expect=true; truth_matched=MC_TRUTH_MATCH_B2DDX(); break;
          case 12893610: b_expect_id=PDG_ID_Bu; tau_expect=true; truth_matched=MC_TRUTH_MATCH_B2DDX(); break;
        }
      }
    }

    // Allows access to calculated truth-matching
    bool TRUTH_MATCHED() {return truth_matched;}
};





//////////// User Functions

// Notes for user:
// Setting cocktail ID allows you to select out certain D** (and D_H**, D_s**) cocktails. If set to -1, all cocktails are accepted.
// Setting twopi allows you to select whether D**->D(*) pi pi decays are allowed (as implemented by Phoebe).
// It is the user's responsibility to set decay_id correctly; there is no way (I think) for me to check this internally

// TODO: since this is for user, maybe change input paramater names to match what is usually found in ntuples?
//////// Truth-Matching Selection Function (for users) for Decays Reconstructed as B0 -> D*+ [-> D0 [-> K- pi+] spi+] mu-
bool MC_TRUTH_MATCH_DST(int decay_id, int mu_id, int mu_mom_id, int mu_gdmom_id, int mu_gdgdmom_id, int mu_mom_key, int mu_gdmom_key, int mu_gdgdmom_key,
                        int dst_mom_id, int dst_gdmom_id, int dst_gdgdmom_id, int dst_mom_key, int dst_gdmom_key, int dst_gdgdmom_key,
                        double dst_mom_trueE, double dst_mom_truePx, double dst_mom_truePy, double dst_mom_truePz, double dst_trueE, double dst_truePx,
                        double dst_truePy, double dst_truePz, int dst_bkgcat, int d0_bkgcat, int b_bkgcat, int cocktail_id=-1, bool twopi=false) {
  // create object for event truth-matching; truth-matching will be done internally when object created
  DstTruthMatch event(decay_id, mu_id, mu_mom_id, mu_gdmom_id, mu_gdgdmom_id, mu_mom_key, mu_gdmom_key, mu_gdgdmom_key, dst_mom_id, dst_gdmom_id,
                      dst_gdgdmom_id, dst_mom_key, dst_gdmom_key, dst_gdgdmom_key, dst_mom_trueE, dst_mom_truePx, dst_mom_truePy, dst_mom_truePz,
                      dst_trueE, dst_truePx, dst_truePy, dst_truePz, dst_bkgcat, d0_bkgcat, b_bkgcat, cocktail_id, twopi);
  return event.TRUTH_MATCHED();
}

//////// Truth-Matching Selection Function (for users) for Decays Reconstructed as B0 -> D*+ [-> D0 [-> K- pi+] spi+] mu-
bool MC_TRUTH_MATCH_D0(int decay_id, int b_id, int mu_id, int mu_mom_id, int mu_gdmom_id, int mu_gdgdmom_id, int mu_gdgdgdmom_id, int mu_mom_key, int mu_gdmom_key, int mu_gdgdmom_key, int mu_gdgdgdmom_key,
                       int d_mom_id, int d_gdmom_id, int d_gdgdmom_id, int d_gdgdgdmom_id, int d_mom_key, int d_gdmom_key, int d_gdgdmom_key, int d_gdgdgdmom_key,
                       double d_trueE, double d_truePx, double d_truePy, double d_truePz, double d_mom_trueE, double d_mom_truePx, double d_mom_truePy, double d_mom_truePz,
                       double d_gdmom_trueE, double d_gdmom_truePx, double d_gdmom_truePy, double d_gdmom_truePz,
                       int b_bkgcat, double d_m, int cocktail_id=-1, bool twopi=false) {
  D0TruthMatch event(decay_id, b_id, mu_id, mu_mom_id, mu_gdmom_id, mu_gdgdmom_id, mu_gdgdgdmom_id, mu_mom_key, mu_gdmom_key, mu_gdgdmom_key, mu_gdgdgdmom_key,
                     d_mom_id, d_gdmom_id, d_gdgdmom_id, d_gdgdgdmom_id, d_mom_key, d_gdmom_key, d_gdgdmom_key, d_gdgdgdmom_key, d_trueE, d_truePx, d_truePy,
                     d_truePz, d_mom_trueE, d_mom_truePx, d_mom_truePy, d_mom_truePz, d_gdmom_trueE, d_gdmom_truePx, d_gdmom_truePy, d_gdmom_truePz,
                     b_bkgcat, d_m, cocktail_id, twopi);
  return event.TRUTH_MATCHED();
}


#endif

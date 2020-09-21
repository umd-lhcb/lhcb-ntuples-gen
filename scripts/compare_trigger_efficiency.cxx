#include <fstream>
#include <iomanip>
#include <iostream>
#include <vector>
#include "TChain.h"
#include "TString.h"

using namespace std;
using std::cout;
using std::endl;

void compare_trigger_efficiency() {
  TString treename("TupleB0/DecayTree");
  TChain  run1(treename);
  run1.Add(
      "../ntuples/pre-0.9.0/Dst-cutflow_mc/"
      "Dst--20_03_18--cutflow_mc--cocktail--2011--md.root");
  TChain run2(treename);
  run2.Add(
      "../ntuples/pre-0.9.0/Dst-cutflow_mc/"
      "Dst--20_03_18--cutflow_mc--cocktail--2016--md.root");

  double n1 = run1.GetEntries(), n2 = run2.GetEntries();
  cout << endl
       << "Loaded Run 1 with " << n1 << " entries, and Run 2 with " << n2
       << endl
       << endl;

  cout << "COMPARING L0 EFFICIENCIES" << endl;
  TString fullL0(
      "(muplus_L0Global_TIS && (Y_L0Global_TIS || "
      "Dst_2010_minus_L0HadronDecision_TOS))");
  cout << fixed << setprecision(3);
  vector<TString> vcuts = {
      "Y_L0Global_TIS", "Dst_2010_minus_L0HadronDecision_TOS",
      "(Y_L0Global_TIS || Dst_2010_minus_L0HadronDecision_TOS)", fullL0};
  for (unsigned icut = 0; icut < vcuts.size(); icut++) {
    double ncut1 = run1.GetEntries(vcuts[icut]),
           ncut2 = run2.GetEntries(vcuts[icut]);
    cout << "Double ratio of " << ncut2 / ncut1 / n2 * n1 << " for cut \""
         << vcuts[icut] << "\"" << endl;
  }
  cout << endl;

  cout << "COMPARING HLT1 EFFICIENCIES" << endl;
  double n1L0 = run1.GetEntries(fullL0), n2L0 = run2.GetEntries(fullL0);
  vector<TString> vcutsHLT = {fullL0 + "&&(Y_Hlt1Phys_Dec)"};
  TString         run1HLT1(fullL0 +
                   "&& (Kplus_Hlt1TrackAllL0Decision_TOS || "
                   "piminus0_Hlt1TrackAllL0Decision_TOS)");

  for (unsigned icut = 0; icut < vcutsHLT.size(); icut++) {
    double ncut1 = run1.GetEntries(run1HLT1),
           ncut2 = run2.GetEntries(vcutsHLT[icut]);
    cout << "Double ratio of " << ncut2 / ncut1 / n2L0 * n1L0 << " for cut \""
         << vcutsHLT[icut] << "\"" << endl;
  }
  cout << endl;
}

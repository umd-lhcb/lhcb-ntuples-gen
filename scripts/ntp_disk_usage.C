#include <algorithm>  // std::sort
#include <iomanip>
#include <iostream>
#include <locale>
#include <set>
#include <string>

#include "TBranch.h"
#include "TChain.h"
#include "TLeaf.h"
#include "TString.h"

using namespace std;

TString addCommas(double num) {
  TString result(Form("%f", num));
  int     posdot(result.First('.'));
  if (posdot == -1) posdot = result.Length();
  for (int ind(posdot - 3); ind > 0; ind -= 3) result.Insert(ind, ",");
  return result;
}

TString roundNumber(double num, int decimals, double denom = 1.) {
  if (denom == 0) return " - ";
  double neg = 1;
  if (num * denom < 0) neg = -1;
  num /= neg * denom;
  num += 0.5 * pow(10., -decimals);
  long    num_int = static_cast<long>(num);
  long    num_dec = static_cast<long>((num - num_int) * pow(10., decimals));
  TString s_dec(Form("%ld", num_dec));  // s_dec.Remove(0,1);
  TString result = "";
  if (neg < 0) result += "-";
  result += Form("%ld", num_int);
  if (decimals > 0) {
    result += ".";
    result += s_dec;
  }

  TString afterdot = result;
  afterdot.Remove(0, afterdot.First(".") + 1);
  for (int i = 0; i < decimals - afterdot.Length(); i++) result += "0";
  return result;
}

struct Variable {
  TString name;
  long    zip_size, tot_size;

  bool operator<(const Variable &var) const {
    // return (zip_size<var.zip_size)
    //   || (zip_size==var.zip_size && tot_size<var.tot_size)
    //   || (zip_size==var.zip_size && tot_size==var.tot_size && name<var.name);
    return (name > var.name);
  }
};

class comma_numpunct : public numpunct<char> {
 protected:
  virtual char do_thousands_sep() const { return ','; }

  virtual string do_grouping() const { return "\03"; }
};

int findVar(const Variable &var, vector<Variable> &vars) {
  int index = -1;
  for (size_t ivar = 0; ivar < vars.size(); ivar++) {
    if (var.name == vars[ivar].name) {
      index = ivar;
      break;
    }
  }

  return index;
}

bool varCompare(const Variable &var1, const Variable &var2) {
  return var1.zip_size > var2.zip_size;
}

int ntp_disk_usage(TString filename, TString nametree = "tree") {
  cout.imbue(locale(locale(), new comma_numpunct));

  TChain chain(nametree);
  if (!chain.Add(filename) || !chain.GetListOfLeaves()) {
    cout << endl << "No tree found in " << filename << endl << endl;
    return 1;
  }

  long   zip_sum(0), tot_sum(0);
  Ssiz_t max_length(0);
  double nentries = chain.GetEntries();

  vector<Variable>        vars, allvars;
  set<Variable>::iterator it;

  for (int i = 0; i < chain.GetListOfLeaves()->GetSize(); ++i) {
    TBranch *b =
        static_cast<TLeaf *>(chain.GetListOfLeaves()->At(i))->GetBranch();
    if (!b) continue;
    Variable v;
    v.name     = b->GetName();
    v.zip_size = b->GetZipBytes();
    v.tot_size = b->GetTotBytes();

    allvars.push_back(v);
    zip_sum += v.zip_size;
    tot_sum += v.tot_size;
    if (v.name.Length() > max_length) max_length = v.name.Length();

    if (v.name.First('_') >= 0)
      v.name.Remove(v.name.First('_'), v.name.Length() - v.name.First('_'));
    int index = findVar(v, vars);
    if (index == -1)
      vars.push_back(v);
    else {
      vars[index].zip_size += v.zip_size;
      vars[index].tot_size += v.tot_size;
    }
  }  // Loop over branches

  int     wbytes = 10, wother = 11;
  int     digitsBytes = 1;
  TString sep         = "      ";
  sort(vars.begin(), vars.end(), varCompare);
  sort(allvars.begin(), allvars.end(), varCompare);
  cout << endl
       << filename << endl
       << endl
       << "Tree \"" << nametree << "\" occupies " << zip_sum
       << " bytes and has " << addCommas(nentries) << " entries ("
       << roundNumber(zip_sum, 2, nentries * 1024) << " kB/event):" << endl;
  cout << endl
       << setw(max_length) << "Branch name" << ' ' << setw(wbytes) << "Byte/ev"
       << ' ' << setw(wother) << "Frac. [%]" << ' ' << setw(wother)
       << "Cumulative" << sep << setw(max_length) << "Branch group name" << ' '
       << setw(wbytes) << "Byte/ev" << ' ' << setw(wother) << "Frac. [%]" << ' '
       << setw(wother) << "Cumulative" << endl;
  for (int ind = 0; ind < (max_length + wbytes + 2 * wother + 3); ind++)
    cout << "=";
  cout << sep;
  for (int ind = 0; ind < (max_length + wbytes + 2 * wother + 3); ind++)
    cout << "=";
  cout << endl
       << setw(max_length) << "Total" << ' ' << setw(wbytes)
       << roundNumber(zip_sum, digitsBytes, nentries) << ' ' << setw(wother)
       << "100.00" << ' ' << setw(wother) << "-" << sep << setw(max_length)
       << "Total" << ' ' << setw(wbytes)
       << roundNumber(zip_sum, digitsBytes, nentries) << ' ' << setw(wother)
       << "100.00" << ' ' << setw(wother) << "-" << endl;
  long running_total(0), tot2 = 0;
  for (size_t ivar = 0; ivar < allvars.size(); ivar++) {
    running_total += allvars[ivar].zip_size;
    double this_frac = (100.0 * allvars[ivar].zip_size) / zip_sum;
    double tot_frac  = (100.0 * running_total) / zip_sum;
    cout << setw(max_length) << allvars[ivar].name << " " << setw(wbytes)
         << roundNumber(allvars[ivar].zip_size, digitsBytes, nentries) << " "
         << setw(wother) << roundNumber(this_frac, 2) << " " << setw(wother)
         << roundNumber(tot_frac, 2) << sep;
    if (ivar < vars.size()) {
      tot2 += vars[ivar].zip_size;
      this_frac = (100.0 * vars[ivar].zip_size) / zip_sum;
      tot_frac  = (100.0 * tot2) / zip_sum;
      cout << setw(max_length) << vars[ivar].name << " " << setw(wbytes)
           << roundNumber(vars[ivar].zip_size, digitsBytes, nentries) << " "
           << setw(wother) << roundNumber(this_frac, 2) << " " << setw(wother)
           << roundNumber(tot_frac, 2);
    }
    cout << endl;
  }  // Loop over all branches
  cout << endl;

  return 0;
}

// {% gendate: %}

#include <TFile.h>
#include <TString.h>
#include <TTree.h>
#include <TTreeReader.h>

#include <Math/Vector3D.h>
#include <Math/Vector4D.h>
#include <TMath.h>

#include <istream>
#include <vector>

#include "ui.h"  // Progress bar

// System headers
// {% join: (format_list: "#include <{}>", directive.system_headers), "\n" %}

// User headers
// {% join: (format_list: "#include \"{}\"", directive.user_headers), "\n" %}

using namespace std;
using namespace ROOT::Math;

//////////////////////
// Helper functions //
//////////////////////

Double_t calc_pseudo_rand_num(Double_t value, int magic = 9) {
  Double_t denom_ref = TMath::Power(10, TMath::Floor(log10(value)) - magic);
  Double_t denom_com = TMath::Power(10, static_cast<int>(log10(value)) - magic);

  return value / denom_ref - TMath::Floor(value / denom_com);
}

template <class T>
Int_t max_elem_idx(vector<T>& vec) {
  return distance(vec.begin(), max_element(vec.begin(), vec.end()));
}

/////////////////////////
// Generated functions //
/////////////////////////

// Generator for each output tree
// {% for tree_out, config in directive.trees->items: %}
void generator_/* {% guard: tree_out %} */ (TTree*  input_tree,
                                            TString output_suffix) {
  auto output_file = new TFile(
      /* {% quote: tree_out %} */ + output_suffix +".root", "recreate");
  TTreeReader reader(input_tree);
  TTree       output("tree", "tree");

  // Load needed branches from ntuple
  // {% for var in config.input %}
  //   {% format: "TTreeReaderValue<{}> {}(reader, \"{}\");", var.type, var.fname, var.name %}
  // {% endfor %}

  // Define output branches and store output variables in vectors
  // {% for var in config.output %}
  //   {% declare: var.type, var.fname %}
  //   {% format: "output.Branch(\"{}\", &{});", var.name, var.fname %}
  //   {% if config.one_cand_only.enable then %}
  //     {% format: "vector<{}> {}_stash;", var.type, var.fname %}
  //   {% endif %}
  // {% endfor %}

  // Define temporary variables
  // {% for var in config.tmp %}
  //   {% declare: var.type, var.fname %}
  // {% endfor %}

  ULong64_t        prevEventNumber = 0;
  Long64_t         num_of_cand = input_tree->GetEntries();
  Long64_t         cand_idx = 0;
  Long64_t         step_size = TMath::Max(1ll, num_of_cand / 100);
  string           progress_msg = "Generating ";
  auto progress = new progress_bar(std::clog, 79u, progress_msg + /* {% quote: tree_out %} */);
  vector<Double_t> pseudo_rand_seq;

  while (reader.Next()) {
    cand_idx += 1;
    if (!(cand_idx % step_size) || cand_idx == num_of_cand)
      progress->write(
        static_cast<float>(cand_idx) / static_cast<float>(num_of_cand));

    // Define variables required by selection
    // {% for var in config.pre_sel_vars %}
    //   {% assign: var.fname, (deref_var: var.rval, config.input_br) %}
    // {% endfor %}

    // Now only keep candidates that pass selections
    if (/* {% join: (deref_var_list: config.sel, config.input_br), " && " %} */) {
      // {% if config.one_cand_only.enable then %}
      // Keep only 1 B candidate for multi-B events
      if (prevEventNumber != *raw_eventNumber && !pseudo_rand_seq.empty()) {
        // Select which B to keep for previous event
        //   We do this by finding the index of the largest element in PRS.
        auto idx = max_elem_idx(pseudo_rand_seq);

        // Assign values for each output branch in this loop
        // {% for var in config.output %}
        //   {% format: "{} = {}_stash[idx];", var.fname, var.fname %}
        // {% endfor %}

        // Clear values of vectors storing output branches
        // {% for var in config.output %}
        //   {% format: "{}_stash.clear();", var.fname %}
        // {% endfor %}
        pseudo_rand_seq.clear();

        output.Fill();  // Fill the output tree

        prevEventNumber = *raw_eventNumber;
      }
      // {% else %}
      // Keep all B candidates for multi-B events
      //
      // Compute post-selection variables (i.e. temp and output variables)
      // {% for var in config.post_sel_vars %}
      //   {% assign: var.fname, (deref_var: var.rval, config.input_br) %}
      // {% endfor %}

      output.Fill();
      // {% endif %}

      // {% if config.one_cand_only.enable then %}
      // Always compute the pseudo random number for current candidate
      pseudo_rand_seq.push_back(
          calc_pseudo_rand_num(/* {% config.one_cand_only.branch %} */));

      // Compute post-selection variables (i.e. temp and output variables)
      // {% for var in config.post_sel_vars %}
      //   {% assign: var.fname, (deref_var: var.rval, config.input_br) %}
      // {% endfor %}

      // Store output variables in vectors
      // {% for var in config.output %}
      //   {% format: "{}_stash.push_back({});", var.fname, (deref_var: var.fname, config.input_br) %}
      // {% endfor %}
      // {% endif %}
    }
  }

  // {% if config.one_cand_only.enable then %}
  // Special treatment for the last event
  if (!pseudo_rand_seq.empty()) {
    auto idx = max_elem_idx(pseudo_rand_seq);

    // {% for var in config.output %}
    //   {% format: "{} = {}_stash[idx];", var.fname, var.fname %}
    // {% endfor %}

    output.Fill();  // Fill the output tree
  }
  // {% endif %}

  output_file->Write("", TObject::kOverwrite);  // Keep the latest cycle only
  delete progress;
  delete output_file;
}

// {% endfor %}

//////////
// Main //
//////////

int main(int, char** argv) {
  TString out_suffix = TString(argv[1]);

  TFile* ntuple = new TFile(/* {% quote: directive.ntuple %} */);
  cout << "The ntuple being worked on is: " << /* {% quote: directive.ntuple %} */ << endl;

  vector<TFile*> friend_ntuples;
  // {% for friend in directive.friends %}
  friend_ntuples.push_back(new TFile(/* {% quote: friend %} */));
  cout << "Additional friend ntuple: " << /* {% quote: friend %} */ << endl;
  // {% endfor %}

  // Define input trees and container to store associated friend trees
  // {% for tree in directive.input_trees %}
  //   {% format: "auto tree_{} = static_cast<TTree*>(ntuple->Get(\"{}\"));", (guard: tree), tree %}
  //   {% format: "vector<TTree*> friends_{};", (guard: tree) %}
  // {% endfor %}

  // Handle friend trees
  TTree* tmp_tree;
  // {% for tree in directive.input_trees %}
  //   {% for idx, state in enum: directive.tree_relations[tree] %}
  //     {% if state then %}
  //       {% format: "tmp_tree = static_cast<TTree*>(friend_ntuples[{}]->Get(\"{}\"));", idx, tree %}
  //       tmp_tree->BuildIndex("runNumber", "eventNumber");
  //       {% format: "tree_{}->AddFriend(tmp_tree, \"{}\", true);", (guard: tree), idx %}
           friends_/* {% guard: tree %} */.push_back(tmp_tree);
           cout << "Handling input tree: " << /* {% quote: tree %} */ << endl;
  //     {% endif %}
  //   {% endfor %}
  // {% endfor %}

  // {% for tree_out, prop in directive.trees->items: %}
  //   {% format: "generator_{}(tree_{}, out_suffix);", (guard: tree_out), (guard: prop.input_tree) %}
  // {% endfor %}

  // Cleanups
  cout << "Cleanups" << endl;
  delete ntuple;
  // {% for tree in directive.input_trees %}
    for (auto tree : friends_/* {% guard: tree %} */) delete tree;
  // {% endfor %}
  for (auto ntp : friend_ntuples) delete ntp;

  return 0;
}

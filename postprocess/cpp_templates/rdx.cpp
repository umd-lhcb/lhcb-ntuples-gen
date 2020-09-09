// {% gendate: %}
#include <TFile.h>
#include <TTree.h>
#include <TTreeReader.h>
#include <TBranch.h>

#include <vector>
#include <TH1D.h>
#include <TMath.h>

// System headers
// {% join: (format_list: "#include <{}>", directive.system_headers), "\n" %}

// User headers
// {% join: (format_list: "#include \"{}\"", directive.user_headers), "\n" %}

using namespace std;

//////////////////////
// Helper functions //
//////////////////////

Double_t calc_pseudo_rand_num(Double_t value, int magic=9) {
  Double_t denom_ref = TMath::Power(10, TMath::Floor(log10(value))     - magic);
  Double_t denom_com = TMath::Power(10, static_cast<int>(log10(value)) - magic);

  return value/denom_ref - TMath::Floor(value/denom_com);
}

template <class T>
Int_t max_elem_idx(vector<T>& vec) {
  return distance(vec.begin(), max_element(vec.begin(), vec.end()));
}


/////////////////////////
// Generated functions //
/////////////////////////

// Generator for each output tree
// {% for output_tree, config in directive.trees->items: %}
void generator_/* {% output_tree %} */(TFile *input_file, TFile *output_file) {
  TTreeReader reader("/* {% config.input_tree %} */", input_file);
  TTree output(/* {% format: "\"{}\", \"{}\"", output_tree, output_tree %} */);

  // Load needed branches from ntuple
  // {% for var in config.input_branches %}
  //   {% format: "TTreeReaderValue<{}> {}(reader, \"{}\");", var.type, var.name, var.name %}
  // {% endfor %}

  // Define output branches and store output variables in vectors
  // {% for var in config.output_branches %}
  //   {% format: "{} {}_out;", var.type, var.name %}
  //   {% format: "output.Branch(\"{}\", &{}_out);", var.name, var.name %}
  //   {% format: "vector<{}> {}_out_stash;", var.type, var.name %}
  // {% endfor %}

  ULong_t prevEventNumber = 0;
  vector<Double_t> pseudo_rand_seq;  // "PRS"

  while (reader.Next()) {
    // Define all variables in case required by selection
    //
    // Input branches
    //   All input branches are already available via TTreeReaderValue<>
    //   variables.
    //
    // Transient variables (renamed output branches and temp variables)
    // {% for var in config.transient_vars %}
    //   {% format: "{} {} = {};", var.type, var.name, (deref_var: var.rvalue, config.input_branch_names) %}
    // {% endfor %}

    // Now only keep candidates that pass selections
    if (/* {% join: (deref_var_list: config.selection, config.input_branch_names), " && " %} */) {

      // Keep only 1 B cand for multi-B events
      if (prevEventNumber != *eventNumber && !pseudo_rand_seq.empty()) {
        // Select which B to keep for previous event
        //   We do this by finding the index of the largest element in PRS.
        auto idx = max_elem_idx(pseudo_rand_seq);

        // Assign values for each output branch in this loop
        // {% for var in config.output_branches %}
        //   {% format: "{}_out = {}_out_stash[idx];", var.name, var.name %}
        // {% endfor %}

        // Clear values of vectors storing output branches
        // {% for var in config.output_branches %}
        //   {% format: "{}_out_stash.clear();", var.name %}
        // {% endfor %}
        pseudo_rand_seq.clear();

        output.Fill();  // Fill the output tree

        prevEventNumber = *eventNumber;
      }

      // Always compute the pseudo random number for current candidate
      pseudo_rand_seq.push_back(calc_pseudo_rand_num(b0_pt));

      // Store variables in vectors
      // {% for var in config.output_branches %}
      //   {% format: "{}_out_stash.push_back({});", var.name, (deref_var: var.name, config.input_branch_names) %}
      // {% endfor %}
    }
  }

  // Special treatment for the last event
  auto idx = max_elem_idx(pseudo_rand_seq);

  // {% for var in config.output_branches %}
  //   {% format: "{}_out = {}_out_stash[idx];", var.name, var.name %}
  // {% endfor %}

  output.Fill();  // Fill the output tree

  output_file->Write();
}

// {% endfor %}


//////////
// Main //
//////////

int main(int, char** argv) {
  TFile* input_file = new TFile(argv[1], "read");
  TFile* output_file = new TFile(argv[2], "recreate");

  // {% for output_tree in directive.trees->keys: %}
  generator_/* {% output_tree %} */(input_file, output_file);
  // {% endfor %}

  output_file->Close();

  delete input_file;
  delete output_file;

  return 0;
}

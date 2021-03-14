// {% gendate: %}
#include <TFile.h>
#include <TTree.h>
#include <TTreeReader.h>
#include <TBranch.h>
#include <TObject.h>

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
  // {% for var in config.input %}
  //   {% format: "TTreeReaderValue<{}> {}(reader, \"{}\");", var.type, var.fname, var.name %}
  // {% endfor %}

  // Define output branches and store output variables in vectors
  // {% for var in config.output %}
  //   {% format: "{} {};", var.type, var.fname %}
  //   {% format: "output.Branch(\"{}\", &{});", var.name, var.fname %}
  //   {% format: "vector<{}> {}_stash;", var.type, var.fname %}
  // {% endfor %}

  // Define temporary variables
  // {% for var in config.tmp %}
  //   {% format: "{} {};", var.type, var.fname %}
  // {% endfor %}

  ULong64_t prevEventNumber = 0;
  vector<Double_t> pseudo_rand_seq;

  while (reader.Next()) {
    // Define variables required by selection
    // {% for var in config.pre_sel_vars %}
    //   {% format: "{} = {};", var.fname, (deref_var: var.rval, config.input_br) %}
    // {% endfor %}

    // Now only keep candidates that pass selections
    if (/* {% join: (deref_var_list: config.sel, config.input_br), " && " %} */) {

      // Keep only 1 B cand for multi-B events
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

      // Always compute the pseudo random number for current candidate
      pseudo_rand_seq.push_back(calc_pseudo_rand_num(/* {% config.one_cand_only.branch %} */));

      // Compute post-selection variables (i.e. temp and output variables)
      // {% for var in config.post_sel_vars %}
      //   {% format: "{} = {};", var.fname, (deref_var: var.rval, config.input_br) %}
      // {% endfor %}

      // Store output variables in vectors
      // {% for var in config.output %}
      //   {% format: "{}_stash.push_back({});", var.fname, (deref_var: var.fname, config.input_br) %}
      // {% endfor %}
    }
  }

  // Special treatment for the last event
  auto idx = max_elem_idx(pseudo_rand_seq);

  // {% for var in config.output %}
  //   {% format: "{} = {}_stash[idx];", var.fname, var.fname %}
  // {% endfor %}

  output.Fill();  // Fill the output tree

  output_file->Write("", TObject::kOverwrite);
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

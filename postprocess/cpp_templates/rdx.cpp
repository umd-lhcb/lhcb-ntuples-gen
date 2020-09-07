// {% gendate: %}
#include <TFile.h>
#include <TTree.h>
#include <TTreeReader.h>
#include <TBranch.h>

#include <vector>

// System headers
// {% join: (format_list: "#include <{}>", directive.system_headers), "\n" %}

// User headers
// {% join: (format_list: "#include \"{}\"", directive.user_headers), "\n" %}

using namespace std;

// Generator for each output tree
// {% for output_tree, config in directive.trees->items: %}
void generator_/* {% output_tree %} */(TFile *input_file, TFile *output_file) {
  TTreeReader reader("/* {% config.input_tree %} */", input_file);
  TTree output(/* {% format: "\"{}\", \"{}\"", output_tree, output_tree %} */);

  // Load branches for keeping only 1 candidate for multi-candidate events
  TTreeReaderValue<UInt_t> runNumber(reader, "runNumber");
  TTreeReaderValue<ULong64_t> eventNumber(reader, "eventNumber");

  // Store variables of B candidates reconstructed from the same event
  // temporarily in vectors
  // {% for var in config.input_branches %}
  //   {% format: "vector<{}> {}_stash;", var.type, var.name %}
  // {% endfor %}
  // {% for var in config.temp_variables %}
  //   {% format: "vector<{}> {}_stash;", var.type, var.name %}
  // {% endfor %}

  // Load needed branches from ntuple
  // {% for var in config.input_branches %}
  //   {% format: "TTreeReaderValue<{}> {}(reader, \"{}\");", var.type, var.name, var.name %}
  // {% endfor %}

  // Define output branches
  // {% for var in config.output_branches %}
  //   {% format: "{} {}_out;", var.type, var.name %}
  //   {% format: "output.Branch(\"{}\", &{}_out);", var.name, var.name %}
  // {% endfor %}

  while (reader.Next()) {
    // Define temp variables (in case required by selection)
    // {% for var in config.temp_variables %}
    //   {% format: "{} {} = {};", var.type, var.name, (deref_var: var.rvalue, config.input_branch_names) %}
    // {% endfor %}

    // Now only keep candidates that pass selections
    if (/* {% join: (deref_var_list: config.selection, config.input_branch_names), " && " %} */) {

      // Assign values for each output branch in this loop
      // {% for var in config.output_branches %}
      //   {% format: "{}_out = {};", var.name, (deref_var: var.rvalue, config.input_branch_names) %}
      // {% endfor %}

      output.Fill();
    }
  }

  output_file->Write();
}

// {% endfor %}

int main(int, char** argv) {
  TFile *input_file = new TFile(argv[1], "read");
  TFile *output_file = new TFile(argv[2], "recreate");

  // {% for output_tree in directive.trees->keys: %}
  generator_/* {% output_tree %} */(input_file, output_file);
  // {% endfor %}

  output_file->Close();

  delete input_file;
  delete output_file;

  return 0;
}

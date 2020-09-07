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

  UInt_t prevRunNumber = 0;
  ULong_t prevEventNumber = 0;

  while (reader.Next()) {
    // Define all variables in case required by selection
    //
    // Input branches
    //   All input branches are already available via TTreeReaderValue<>
    //   variables.
    //
    // Temporary variables
    // {% for var in config.temp_variables %}
    //   {% format: "{} {} = {};", var.type, var.name, (deref_var: var.rvalue, config.input_branch_names) %}
    // {% endfor %}
    //
    // Output branches
    //   We define them if they don't have a naming clash with the existing
    //   input branches.
    // {% for var in config.output_branches_uniq %}
    //   {% format: "{} {} = {};", var.type, var.name, (deref_var: var.rvalue, config.input_branch_names) %}
    // {% endfor %}

    // Now only keep candidates that pass selections
    if (/* {% join: (deref_var_list: config.selection, config.input_branch_names), " && " %} */) {
      // {% for var in config.output_branches %}
      //   {% format: "{}_out_stash.push_back({});", var.name, (deref_var: var.name, config.input_branch_names) %}
      // {% endfor %}

      // Assign values for each output branch in this loop
      // {% for var in config.output_branches %}
      //   {% format: "{}_out = {}_out_stash[0];", var.name, var.name %}
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

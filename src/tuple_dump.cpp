// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Tue Jul 02, 2019 at 12:50 AM -0400

#include <TDirectoryFile.h>
#include <TFile.h>
#include <TKey.h>
#include <TLeaf.h>
#include <TList.h>
#include <TObjArray.h>
#include <TTree.h>
#include <fstream>
#include <iostream>
#include <string>

std::string INDENT = "    ";

////////////////////////////////////////////////////////////////////////////////
// Declarations
////////////////////////////////////////////////////////////////////////////////

TList *get_keys(TFile *);
TObjArray *get_branches(TTree *);
std::string get_branch_datatype(TBranch *);
std::vector<std::string> traverse_ntuples(TList *);

////////////////////////////////////////////////////////////////////////////////
// Main
////////////////////////////////////////////////////////////////////////////////

int main(int argc, char **argv) {
  char *input_filename = argv[1];
  std::string output_filename = argv[2];

  TFile *ntuple = new TFile(input_filename, "read");
  std::ofstream output_file;
  output_file.open(output_filename);

  // Traverse through the whole TFile and find all tree names inside.
  auto tree_names = traverse_ntuples(get_keys(ntuple));

  for (auto &&tree_name : tree_names) {
    output_file << tree_name << ":" << std::endl;
    auto tree = dynamic_cast<TTree *>(ntuple->Get(tree_name.c_str()));
    for (const auto &&branch : *get_branches(tree)) {
      const std::string branch_name = branch->GetName();
      const std::string datatype = get_branch_datatype((TBranch *)branch);

      output_file << INDENT << branch_name << ": " << datatype << std::endl;
    }
    output_file << std::endl;
  }

  delete ntuple;
  return 0;
}

////////////////////////////////////////////////////////////////////////////////
// ROOT objects handlers
////////////////////////////////////////////////////////////////////////////////

TList *get_keys(TFile *ntuple) { return ntuple->GetListOfKeys(); }
TObjArray *get_branches(TTree *tree) { return tree->GetListOfBranches(); }

std::string get_branch_datatype(TBranch *branch) {
  TObjArray *leaves = branch->GetListOfLeaves();
  std::string datatype;

  for (const auto &&leaf : *leaves) {
    datatype =
        ((TLeaf *)leaf)->GetTypeName();  // We assume the branch is
                                         // filled with homogeneous objects
    break;
  }

  return datatype;
}

// This is a recursion.
std::vector<std::string> traverse_ntuples(TList *keys) {
  std::vector<std::string> result;

  for (const auto &&obj : *keys) {
    auto key = dynamic_cast<TKey *>(obj);
    std::string name = key->GetName();
    std::string class_name = key->GetClassName();

    if (class_name.compare("TDirectoryFile") == 0) {
      auto sub_obj = dynamic_cast<TDirectoryFile *>(key->ReadObj());
      std::vector<std::string> sub_result =
          traverse_ntuples(sub_obj->GetListOfKeys());

      for (auto &&sub_dir : sub_result) {
        result.insert(result.end(), name + "/" + sub_dir);
      }

    } else if (class_name.compare("TTree") == 0) {
      result.insert(result.end(), name);

    } else {
      std::cout << "Unknown datatype: " << class_name << ". Skip." << std::endl;
    }
  }

  return result;
}

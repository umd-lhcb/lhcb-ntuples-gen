// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Mon Jul 01, 2019 at 03:58 PM -0400

#include <TFile.h>
#include <TLeaf.h>
#include <TList.h>
#include <TObjArray.h>
#include <TTree.h>
#include <fstream>
#include <iostream>
#include <iterator>
#include <set>
#include <string>

const std::set<std::string> BLACKLISTED = {"GetIntegratedLuminosity"};
const std::string INDENT = "    ";

////////////////////////////////////////////////////////////////////////////////
// Declarations
////////////////////////////////////////////////////////////////////////////////

bool in_blacklist(std::string);

TList *get_top_trees(TFile *);
TObjArray *get_branches(TTree *);
std::string get_branch_datatype(TBranch *);

////////////////////////////////////////////////////////////////////////////////
// Main
////////////////////////////////////////////////////////////////////////////////

int main(int argc, char **argv) {
  char *input_filename = argv[1];
  std::string output_filename = argv[2];
  std::string subfolder;
  if (argc > 3) {
    subfolder = argv[3];
  } else {
    subfolder = "";
  }

  TFile *ntuple = new TFile(input_filename, "read");
  std::ofstream output_file;
  output_file.open(output_filename);

  // Get top-level tree/folder names
  for (const auto &&obj : *get_top_trees(ntuple)) {
    std::string name_top = obj->GetName();
    if (!in_blacklist(name_top)) {
      name_top += subfolder;

      output_file << name_top << ":" << std::endl;

      TTree *tree = (TTree *)ntuple->Get(name_top.c_str());
      for (const auto &&branch : *get_branches(tree)) {
        const std::string name_branch = branch->GetName();
        const std::string datatype = get_branch_datatype((TBranch *)branch);

        output_file << INDENT << name_branch << ": " << datatype << std::endl;
      }

      output_file << std::endl;
    }
  }

  delete ntuple;
  return 0;
}

////////////////////////////////////////////////////////////////////////////////
// Helpers
////////////////////////////////////////////////////////////////////////////////

bool in_blacklist(std::string name) {
  std::set<std::string>::iterator it = BLACKLISTED.find(name);
  if (it != BLACKLISTED.end()) {
    return true;
  } else {
    return false;
  }
}

////////////////////////////////////////////////////////////////////////////////
// TTree/TBranch/TFolder handlers
////////////////////////////////////////////////////////////////////////////////

TList *get_top_trees(TFile *ntuple) { return ntuple->GetListOfKeys(); }
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

/*
 *void get_folders(TFolder *folder) {
 *  TCollection *folders = folder->GetListOfFolders();
 *  TIter nextobj(folders);  // For some reason, this segfaults
 *  TObject *obj;
 *
 *  while ((obj = (TObject *)nextobj())) {
 *    std::cout << obj->GetName() << std::endl;
 *  }
 *}
 */

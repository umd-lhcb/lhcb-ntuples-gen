// Author: Yipeng Sun <syp at umd dot edu>
// License: BSD 2-clause
// Last Change: Fri Jun 28, 2019 at 05:56 AM -0400

#include <TFile.h>
#include <TList.h>
#include <TObjArray.h>
#include <TTree.h>
#include <iostream>
#include <iterator>
#include <set>
#include <string>

const std::set<std::string> BLACKLISTED = {"GetIntegratedLuminosity"};

////////////////////////////////////////////////////////////////////////////////
// Declarations
////////////////////////////////////////////////////////////////////////////////

bool in_blacklist(std::string);

TList *get_top_trees(TFile *);
TObjArray *get_branches(TTree *);

////////////////////////////////////////////////////////////////////////////////
// Main
////////////////////////////////////////////////////////////////////////////////

int main(int argc, char **argv) {
  char *input_file = argv[1];
  char *output_file = argv[2];
  std::string subfolder = argv[3];

  TFile *ntuple = new TFile(input_file, "read");

  // Get top-level tree/folder names
  for (const auto &&obj : *get_top_trees(ntuple)) {
    std::string name = obj->GetName();
    if (!in_blacklist(name)) {
      name += subfolder;

      TTree *tree = (TTree *)ntuple->Get(name.c_str());
      for (const auto &&branch : *get_branches(tree)) {
        std::cout << branch->GetName() << '\n';
      }
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

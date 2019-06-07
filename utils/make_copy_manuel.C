#include "TFile.h"
#include "TTree.h"

//function that will make a copy of the first 10 entries in Manuel's file
void make_copy_manuel() {

  //read in the .root file to make smaller
  TFile *bigfile = new TFile("src/lhcb-ntuples-gen/2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.root");

  //define tree within the original .root file
  TTree *bigtree = (TTree*)bigfile->Get("TupleY/DecayTree");

  //make a new file which will be the smaller .root file
  TFile *smallfile = new TFile("small_YCands.root","RECREATE");

  //define tree to be first 10 entries in original tree
  TTree *smalltree = bigtree->CloneTree(10);

  smallfile->Write();

  delete bigfile;
  delete smallfile;
}

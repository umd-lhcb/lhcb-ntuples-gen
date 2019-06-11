#include "TFile.h"
#include "TTree.h"

//for crossmatching of Manuel's and Phoebe's files, must have the following
//file1="src/lhcb-ntuples-gen/2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.root"
//file2="src/lhcb-ntuples-gen/2012-b2D0MuXB2DMuNuForTauMuLine/data/sample/YCan
//ds_sample-mag_down-data.root"

void crossmatch_phoebe(const char *file1, const char *file2) {

  //read in the .root files
  TFile *f1 = new TFile(file1);
  TFile *f2 = new TFile(file2);

  //define the trees within each file
  TTree *t1 = (TTree*)f1->Get("TupleY/DecayTree");
  TTree *t2 = (TTree*)f2->Get("YCands/DecayTree");

  //make a new file and a new tree which will have same form as t2
  //new file will be a smaller matched root file
  TFile *newfile = new TFile("small_matched_phoebe.root","RECREATE");
  TTree *MatchTree = t2->CloneTree(0);

  //set branch status of each tree to only read in eventNumber and runNumber
  t1->SetBranchStatus("*",0);
  t1->SetBranchStatus("runNumber",1);
  t1->SetBranchStatus("eventNumber",1);

  t2->SetBranchStatus("*",0);
  t2->SetBranchStatus("runNumber",1);
  t2->SetBranchStatus("eventNumber",1);

  //initialize the values to be read in from each file
  UInt_t run1, run2;
  ULong64_t event1, event2;

  //set address of values to read in
  t1->SetBranchAddress("runNumber",&run1);
  t1->SetBranchAddress("eventNumber",&event1);
  t2->SetBranchAddress("runNumber",&run2);
  t2->SetBranchAddress("eventNumber",&event2);

  //read all entries and cross match
  Int_t nentries1 = (Int_t)t1->GetEntries();
  Int_t nentries2 = (Int_t)t2->GetEntries();

  //here only match first ten entries instead of whole file (will save time)
  //for (Int_t i=0; i<nentries1; i++) {
  for (Int_t i=0; i<10; i++) {
    t1->GetEntry(i);

    for (Int_t j=0; j<nentries2; j++) {
      t2->GetEntry(j);
      if (run1 == run2 && event1 == event2) {
        //get the entry for t2 for ALL branches (i.e. set getall=1)
        t2->GetEntry(j,1);

      	//fill the new tree with values from t2 matching the given condition
        MatchTree->Fill();

      }

    }
  }

  //write the tree to the new .ROOT file
  newfile->Write();

  delete f1;
  delete f2;
  delete newfile;

}
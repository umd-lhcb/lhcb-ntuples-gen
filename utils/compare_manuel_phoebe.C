#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TH1D.h"

//function that will compare the two .root files one param at a time
//must have run crossmatch_phoebe.C first to make second file (file2)
//first file (file1) will be copy of YCands.root but only with first 10 events
//must have run make_copy_manuel.C to make first file (file1)

//file1 and file2 must be full path to the files in quotes ("...")

void compare_manuel_phoebe(const char *file1, const char *file2) {

  //read in the .root files
  TFile *f1 = new TFile(file1);
  TFile *f2 = new TFile(file2);

  //define the trees within each file
  TTree *t1 = (TTree*)f1->Get("DecayTree");
  TTree *t2 = (TTree*)f2->Get("DecayTree");

  //initialize the values to be read in from each file
  UInt_t run1, run2;
  ULong64_t event1, event2;
  Double_t D0_P1, D0_P2;

  //set address of values to read in
  t1->SetBranchAddress("runNumber",&run1);
  t1->SetBranchAddress("eventNumber",&event1);
  t2->SetBranchAddress("runNumber",&run2);
  t2->SetBranchAddress("eventNumber",&event2);

  //set address for each file of value to compare
  t1->SetBranchAddress("D0_P",&D0_P1);
  t2->SetBranchAddress("D0_P",&D0_P2);

  //make a new canvas to plot histogram on
  TCanvas *ct = new TCanvas("ct","D0 Momentum Difference",0,0,600,600);
  ct->cd();

  TH1D *hD0_diff = new TH1D("hD0_diff","D0 Momentum Differences",500,-150.0,150.0);

  //read all entries and cross match
  Int_t nentries1 = (Int_t)t1->GetEntries();
  Int_t nentries2 = (Int_t)t2->GetEntries();

  for (Int_t i=0; i<nentries1; i++) {
    t1->GetEntry(i);

    for (Int_t j=0; j<nentries2; j++) {
      t2->GetEntry(j);
      if (run1 == run2 && event1 == event2) {
        //fill histogram with difference of values
        Double_t D0_Pdiff = D0_P1 - D0_P2;
        hD0_diff->Fill(D0_Pdiff);

      }

    }
  }
  //draw and save the histogram
  hD0_diff->Draw();
  ct->SaveAs("D0_Pdiff_manuel_phoebe.png");

}
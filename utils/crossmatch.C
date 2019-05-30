#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TH1D.h"


void crossmatch() {
	//read in the .root files
	TFile *f1 = new TFile("BDslnu_small.root");
	TFile *f2 = new TFile("BDslnu_small2.root");

	//define the trees within each file
	TTree *t1 = (TTree*)f1->Get("DecayTree");
	TTree *t2 = (TTree*)f2->Get("DecayTree");

	//initialize the values to be read in from each file
	UInt_t run1, run2;
	ULong64_t event1, event2;
	Double_t Bplus_P1, Bplus_P2;
	//Double_t BPlus_Pdiff;

	//set address of values to read in
	t1->SetBranchAddress("runNumber",&run1);
	t1->SetBranchAddress("eventNumber",&event1);
	t1->SetBranchAddress("Bplus_P",&Bplus_P1);
	t2->SetBranchAddress("runNumber",&run2);
	t2->SetBranchAddress("eventNumber",&event2);
	t2->SetBranchAddress("Bplus_P",&Bplus_P2);

	//make a new canvas to plot histogram on
	TCanvas *ct = new TCanvas("ct","Bplus Momentum Difference",0,0,600,600);
	ct->cd();

	TH1D *hBplus_diff = new TH1D("hBplus_diff","Bplus Momentum Differences",1000,-0.1,0.1);

	//read all entries and cross match
	Int_t nentries1 = (Int_t)t1->GetEntries();
	Int_t nentries2 = (Int_t)t2->GetEntries();

	for (Int_t i=0; i<nentries1; i++) {
		t1->GetEntry(i);

		for (Int_t j=0; j<nentries2; j++) {
			t2->GetEntry(j);
			if (run1 == run2 && event1 == event2) {
				Double_t Bplus_Pdiff = Bplus_P1 - Bplus_P2;
				hBplus_diff->Fill(Bplus_Pdiff);

			}

		}
	}

	hBplus_diff->Draw();
	ct->SaveAs("BPlus_Pdiff.png");

}
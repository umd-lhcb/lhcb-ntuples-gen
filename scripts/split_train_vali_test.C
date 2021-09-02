// Split ntuple into training, validation, and test samples
// The split is controlled with the split="X:Y" parameter
// where X, Y, and 100-X-Y are the percentages of the
// original sample saved in the training, validation, and
// test samples, respectively

#include <iostream>

#include "TApplication.h"
#include "TEntryList.h"
#include "TFile.h"
#include "TRandom3.h"
#include "TString.h"
#include "TTree.h"

using namespace std;

void split_train_vali_test(TString input = "l0hadron_emu_tm.root",
                           TString split = "35:35") {
  TFile *inputFile = TFile::Open(input);
  TTree *inputTree = (TTree *)inputFile->Get("TupleB0/DecayTree");

  TString trainName = input;
  trainName.ReplaceAll(".root", "_train.root");
  auto  trainFile = TFile::Open(trainName, "RECREATE");
  auto *trainList = new TEntryList();

  TString validName = input;
  validName.ReplaceAll(".root", "_valid.root");
  auto  validFile = TFile::Open(validName, "RECREATE");
  auto *validList = new TEntryList();

  TString testName = input;
  testName.ReplaceAll(".root", "_test.root");
  auto  testFile = TFile::Open(testName, "RECREATE");
  auto *testList = new TEntryList();

  // Parsing the string to find the probabilities for the split
  TString strain = split;
  strain.Remove(strain.First(":"), strain.Length());
  float   ptrain = strain.Atof() / 100.;
  TString svalid = split;
  svalid.Remove(0, svalid.First(":") + 1);
  float pvalid   = svalid.Atof() / 100.;
  int   perctest = 100 - 100 * (pvalid + ptrain);

  // Filling the TEntryList based on a Uniform distribution
  long nEntries = inputTree->GetEntries();
  cout << endl
       << "Splitting the " << nEntries << " entries in " << input
       << " into training:validation:test as " << split << ":" << perctest
       << endl
       << endl;
  TRandom3 rand(42);
  float    prob;
  for (long entry = 0; entry < nEntries; entry++) {
    prob = rand.Uniform(0, 1);
    if (prob <= ptrain)
      trainList->Enter(entry);
    else if (prob <= ptrain + pvalid)
      validList->Enter(entry);
    else
      testList->Enter(entry);
  }

  // Saving ntuples
  inputTree->SetEntryList(trainList);
  trainFile->cd();
  trainFile->mkdir("TupleB0/");
  trainFile->cd("TupleB0/");
  auto trainTree = inputTree->CopyTree("");
  trainFile->Write();
  cout << "Wrote " << trainName << " with " << trainTree->GetEntries()
       << " entries" << endl;
  trainFile->Close();

  inputTree->SetEntryList(validList);
  validFile->cd();
  validFile->mkdir("TupleB0/");
  validFile->cd("TupleB0/");
  auto validTree = inputTree->CopyTree("");
  validFile->Write();
  cout << "Wrote " << validName << " with " << validTree->GetEntries()
       << " entries" << endl;
  validFile->Close();

  inputTree->SetEntryList(testList);
  testFile->mkdir("TupleB0/");
  testFile->cd("TupleB0/");
  testFile->cd();
  auto testTree = inputTree->CopyTree("");
  testFile->Write();
  cout << "Wrote " << testName << " with " << testTree->GetEntries()
       << " entries" << endl
       << endl;
  testFile->Close();

  gApplication->Terminate();
}

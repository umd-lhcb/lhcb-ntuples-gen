#include "TFile.h"
#include "TTree.h"
#include "TDirectory.h"
#include "TStopwatch.h"
#include <vector>

//for crossmatching of Manuel's and Phoebe's files, must have the following
//file1="src/lhcb-ntuples-gen/2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.root"
//file2="src/lhcb-ntuples-gen/2012-b2D0MuXB2DMuNuForTauMuLine/data/sample/YCan
//ds_sample-mag_down-data.root"

#define infile1 \
  "src/lhcb-ntuples-gen/2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.root"
#define infile2 \
  "src/lhcb-ntuples-gen/2012-b2D0MuXB2DMuNuForTauMuLine/data/sample/YCands_" \
  "sample-mag_down-data.root"

void extract_unique_id(TFile *file);
std::vector<std::vector<ULong64_t>> convert_to_vec(TFile *file);
void crossmatch_phoebe_fast(TFile *file1, TFile *file2);

int extract_cm_phoebe() {

  //read in the .root files
  TFile *f1 = new TFile(infile1);
  TFile *f2 = new TFile(infile2);

  //extract the unique IDs and duplicate IDs from Manuel's file
  //save unique IDs in one .root file and duplicate in another .root file
  extract_unique_id(f1);
  
  //read in the unique and duplicate .root files just created
  TFile *uid = new TFile("unique_id_YCands.root");
  TFile *did = new TFile("duplicate_id_YCands.root");

  //convert the eventNumber and runNumber values from each file into vectors
  //vectors have the following form
  /*
          column 1        column 2
  row 1   eventNumber_0   runNumber_0
  row 2   eventNumber_1   runNumber_1
  row 3   eventNumber_2   runNumber_2
  ...     ...             ...
  row n   eventNumber_n   runNumber_n
  */
  //here n is the number of entries in the TFile fed into convert_to_vec
  std::vector<std::vector<ULong64_t>> unique_vec = convert_to_vec(uid);
  std::vector<std::vector<ULong64_t>> dupli_vec = convert_to_vec(did);

  //crossmatch Manuel and Phoebe's files, only for unique IDs in Manuel's file
  crossmatch_phoebe_fast(uid, f2);

  return 0;
}


void extract_unique_id(TFile *file) {

  TStopwatch timer;
  timer.Start();

  //define the tree within the file twice
  TTree *tree = (TTree*)file->Get("TupleY/DecayTree");
  TTree *dtree = tree->CloneTree();

  //make a new file and new tree which will have same form as tree/dtree
  //new file will have same directory structure as DecayTree
  TFile *newfile = new TFile("unique_id_YCands.root","RECREATE");
  TDirectory *cdnew = newfile->mkdir("TupleY");
  newfile->cd("TupleY");
  TTree *MatchTree = tree->CloneTree(0);

  //make another new file for the duplicate events with this same form
  TFile *dupfile = new TFile("duplicate_id_YCands.root","RECREATE");
  TDirectory *cddup = dupfile->mkdir("TupleY");
  dupfile->cd("TupleY");
  TTree *DupliTree = tree->CloneTree(0);

  //set branch status of the trees to only read in eventNumber and runNumber
  tree->SetBranchStatus("*",0);
  tree->SetBranchStatus("runNumber",1);
  tree->SetBranchStatus("eventNumber",1);

  dtree->SetBranchStatus("*",0);
  dtree->SetBranchStatus("runNumber",1);
  dtree->SetBranchStatus("eventNumber",1);

  //initialize the values to be read in from the file
  UInt_t run, drun;
  ULong64_t event, devent;

  //set address of values to read in
  tree->SetBranchAddress("runNumber",&run);
  tree->SetBranchAddress("eventNumber",&event);

  dtree->SetBranchAddress("runNumber",&drun);
  dtree->SetBranchAddress("eventNumber",&devent);

  //find number of entries within the file
  Int_t nentries = (Int_t)tree->GetEntries();

  //define an integer to keep track of how many times an event is in the file
  Int_t sum = 0;

  //loop through the file to determine all unique event identifiers
  //i.e. find unique combinations of eventNumber and runNumber
  for (Int_t i=0; i<nentries; i++) {
    tree->GetEntry(i);

    for (Int_t j=0; j<nentries; j++) {
      dtree->GetEntry(j);

      if (run == drun && event == devent) {
        sum++;
      } else {
        sum = sum;
      }
    }
    if (sum == 1) {
      //if only one unique event id in file then get the entry from file1
      dtree->GetEntry(i,1);

      //fill new tree with events having unique identifiers
      //DOES NOT FILL EVENTS THAT HAVE DUPLICATES
      MatchTree->Fill();
    } else {
      //if more than one unique id in file then get the entry
      dtree->GetEntry(i,1);

      //fill the tree for duplicates with the duplicates
      DupliTree->Fill();
    }
    sum = 0;
  }

  //write the trees to the new .root files
  newfile->Write();
  dupfile->Write();

  timer.Stop();

  //print out the real time and the CPU time taken to make the new file
  cout << " Total CPU Time to Extract = " << timer.CpuTime() << endl;
  cout << " Total Real Time to Extract = " << timer.RealTime() << endl;

  delete file;
  delete newfile;
  delete dupfile;
}


std::vector<std::vector<ULong64_t>> convert_to_vec(TFile *file) {

  //define the vector to read to
  std::vector<std::vector<ULong64_t>> vec;

  //define the tree within the file
  TTree *tree = (TTree*)file->Get("TupleY/DecayTree");

  //set branch status of tree to only read in eventNumber and runNumber
  tree->SetBranchStatus("*",0);
  tree->SetBranchStatus("runNumber",1);
  tree->SetBranchStatus("eventNumber",1);

  //initialize values to be read from file
  UInt_t run;
  ULong64_t event;

  //set address of values to read in
  tree->SetBranchAddress("runNumber",&run);
  tree->SetBranchAddress("eventNumber",&event);

  //get total number of entries in file
  Int_t nentries = (Int_t)tree->GetEntries();

  //resize the vector so that it can take the necessary number of values
  //vector will have "nentries" number of rows and 2 columns
  vec.resize(nentries, std::vector<ULong64_t>(2));

  for (Int_t i=0; i<nentries; i++) {
    tree->GetEntry(i);

    //initialize the eventNumber and runNumber within the vector
    if (i == 0) {
      vec[i][0] = event;
      vec[i][1] = run;
    } else {
      //check for duplicates, if duplicates only assign first entry to vec
      if (vec[i][0] != vec[i-1][0] || vec[i][1] != vec[i-1][1]) {
        vec[i][0] = event;
        vec[i][1] = run;
      }
    }
  }
  return vec;
}


void crossmatch_phoebe_fast(TFile *file1, TFile *file2) {

  TStopwatch timer;
  timer.Start();

  //define the trees within each file
  TTree *t1 = (TTree*)file1->Get("TupleY/DecayTree");
  TTree *t2 = (TTree*)file2->Get("YCands/DecayTree");

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
        //get the new matched entry for t2
        t2->GetEntry(j,1);

      	//fill the new tree with values from t2 matching the given condition
        MatchTree->Fill();
      }
    }
  }

  //write the tree to the new .root file
  newfile->Write();

  timer.Stop();

  //print out the real time and the CPU time taken to make the new file
  cout << " Total CPU Time to Crossmatch = " << timer.CpuTime() << endl;
  cout << " Total Real Time to Crossmatch = " << timer.RealTime() << endl;

  delete file1;
  delete file2;
  delete newfile;
}

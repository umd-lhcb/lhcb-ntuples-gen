#include "TFile.h"
#include "TTree.h"
#include "TDirectory.h"
#include "TStopwatch.h"
#include "TBranch.h"
#include "TCanvas.h"
#include "TH1D.h"
#include <vector>

//==========================================
//THIS IS THE FINALIZED VERSION OF THIS CODE
//final of my (Ben's) versions for GitHub
//==========================================

//=======================================================================
//This macro will do the following:
//1. Extract the unique and duplicate event IDs from Manuel's file
//2. Save the unique and duplicate extracted IDs to their own respective
//   .root files
//3. Read in these two .root files and convert the event IDs into vectors
//   following the format described below
//4. Crossmatch Manuel and Phoebe's ntuples ONLY for the unique ID events
//5. Compare a single branch present in both Manuel and Phoebe's ntuples
//   (as of now this branch must be of type Double_t but this will be
//   changed after implementation with Yipeng's code)
//=======================================================================

//for crossmatching of Manuel's and Phoebe's files, must have the following
//file1="src/lhcb-ntuples-gen/2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.root"
//file2="src/lhcb-ntuples-gen/2012-b2D0MuXB2DMuNuForTauMuLine/data/sample/YCan
//ds_sample-mag_down-data.root"


//These definitions will need to change depending upon the directory
//structure of one's own computer!
#define infile1 \
  "src/lhcb-ntuples-gen/2012-b2D0MuXB2DMuNuForTauMuLine/gen/YCands.root"
#define infile2 \
  "src/lhcb-ntuples-gen/2012-b2D0MuXB2DMuNuForTauMuLine/data/sample/YCands_" \
  "sample-mag_down-data.root"


void extract_unique_id(TFile *file);
std::vector<std::vector<ULong64_t>> convert_to_vec(TFile *file);
void crossmatch_phoebe_fast(TFile *file1, TFile *file2);
void compare_branch(TFile *file1, TFile *file2, const char *branch_name);


int histo_make_compare() {

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

  //open the file that is Phoebe's ntuple crossmatched with Manuel's ntuple
  TFile *match_phoebe = new TFile("matched_phoebe.root");
  
  //must redefine the unique IDs file or else the compare_branch function
  //will not work, not deleting file yields a plot but no results on plot
  //hence keep the code this way with a redefinition (even though it's ugly)
  TFile *uid2 = new TFile("unique_id_YCands.root");

  //compare Manuel and Phoebe's branches, output saved in histogram
  compare_branch(uid2, match_phoebe, "muplus_P");

  //must again redefine files or I get a warning about a potential memory leak
  //redefinitions must occur after every call to "compare_branch"
  TFile *uid3 = new TFile("unique_id_YCands.root");
  TFile *match_phoebe3 = new TFile("matched_phoebe.root");
  compare_branch(uid3, match_phoebe3, "muplus_PX");

  TFile *uid4 = new TFile("unique_id_YCands.root");
  TFile *match_phoebe4 = new TFile("matched_phoebe.root");
  compare_branch(uid4, match_phoebe4, "muplus_PY");

  TFile *uid5 = new TFile("unique_id_YCands.root");
  TFile *match_phoebe5 = new TFile("matched_phoebe.root");
  compare_branch(uid5, match_phoebe5, "muplus_PZ");

  TFile *uid6 = new TFile("unique_id_YCands.root");
  TFile *match_phoebe6 = new TFile("matched_phoebe.root");
  compare_branch(uid6, match_phoebe6, "Kplus_P");

  TFile *uid7 = new TFile("unique_id_YCands.root");
  TFile *match_phoebe7 = new TFile("matched_phoebe.root");
  compare_branch(uid7, match_phoebe7, "Kplus_PX");

  TFile *uid8 = new TFile("unique_id_YCands.root");
  TFile *match_phoebe8 = new TFile("matched_phoebe.root");
  compare_branch(uid8, match_phoebe8, "Kplus_PY");

  TFile *uid9 = new TFile("unique_id_YCands.root");
  TFile *match_phoebe9 = new TFile("matched_phoebe.root");
  compare_branch(uid9, match_phoebe9, "Kplus_PZ");

  TFile *uid10 = new TFile("unique_id_YCands.root");
  TFile *match_phoebe10 = new TFile("matched_phoebe.root");
  compare_branch(uid10, match_phoebe10, "D0_P");

  TFile *uid11 = new TFile("unique_id_YCands.root");
  TFile *match_phoebe11 = new TFile("matched_phoebe.root");
  compare_branch(uid11, match_phoebe11, "D0_MM");

  TFile *uid12 = new TFile("unique_id_YCands.root");
  TFile *match_phoebe12 = new TFile("matched_phoebe.root");
  compare_branch(uid12, match_phoebe12, "Dst_2010_minus_P");

  TFile *uid13 = new TFile("unique_id_YCands.root");
  TFile *match_phoebe13 = new TFile("matched_phoebe.root");
  compare_branch(uid13, match_phoebe13, "Dst_2010_minus_MM");

  //compare_branch(uid2, match_phoebe, "piminus_P");
  //compare_branch(uid2, match_phoebe, "piminus0_P");

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
  cout << " Total CPU Time = " << timer.CpuTime() << endl;
  cout << " Total Real Time = " << timer.RealTime() << endl;

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
  TFile *newfile = new TFile("matched_phoebe.root","RECREATE");
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
  for (Int_t i=0; i<nentries1; i++) {
  //for (Int_t i=0; i<10; i++) {
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
  cout << " Total CPU Time = " << timer.CpuTime() << endl;
  cout << " Total Real Time = " << timer.RealTime() << endl;

  delete file1;
  delete file2;
  delete newfile;
}

void compare_branch(TFile *file1, TFile *file2, const char *branch_name) {
  
  //define the trees for each file
  //file1 must be the unique IDs file and file2 must be the crossmatched file
  //input branch name can only be of type Double_t
  TTree *t1 = (TTree*)file1->Get("TupleY/DecayTree");
  TTree *t2 = (TTree*)file2->Get("DecayTree");

  //get the branch for the given branch name
  TBranch *testb1 = t1->GetBranch(branch_name);
  TBranch *testb2 = t2->GetBranch(branch_name);

  //test if given branch exists in both files
  //if it does not exist in both files then exit program
  if (!testb1 || !testb2) {
    cout << "The given branch name is not a branch in one or both files." 
    << endl;

    cout << "Try running the program again stating a diffrent branch name." 
    << endl;

    cout << "The program has terminated." << endl;

    exit(0);
  } else {
    cout << "The given branch is a branch in both files." << endl;

    cout << "Further analysis to come..." << endl;

    //initialize the values to be read in from each file
    UInt_t run1, run2;
    ULong64_t event1, event2;
    Double_t branch1, branch2;

    //set address of values to read in
    t1->SetBranchAddress("runNumber",&run1);
    t1->SetBranchAddress("eventNumber",&event1);
    t2->SetBranchAddress("runNumber",&run2);
    t2->SetBranchAddress("eventNumber",&event2);

    //set address for each file of value to compare
    t1->SetBranchAddress(branch_name,&branch1);
    t2->SetBranchAddress(branch_name,&branch2);

    //define 2nd halves of inputs to TH1D and SaveAs
    const char *title2 = " Difference";
    const char *file_name2 = "_diff_manuel_phoebe.png";

    //define title of the histogram
    char title[100];
    strcpy(title,branch_name);
    strcat(title,title2);

    //define the file name to have histogram saved to
    char file_name[100];
    strcpy(file_name,branch_name);
    strcat(file_name,file_name2);

    //define inputs to TH1d and SaveAs for 2nd histogram
    const char *title3 = " Difference (Normalized)";
    const char *file_name3 = "_diff_norm_manuel_phoebe.png";

    //define title of 2nd histogram
    char title_norm[100];
    strcpy(title_norm,branch_name);
    strcat(title_norm,title3);

    //define file name of 2nd histogram
    char file_norm[100];
    strcpy(file_norm,branch_name);
    strcat(file_norm,file_name3);

    //make a new canvas to plot histogram on
    TCanvas *ct = new TCanvas("ct",title,0,0,600,600);
    ct->cd();

    TH1D *h_diff = new TH1D("h_diff",title,500,-150.0,150.0);

    //read all entries and cross match
    Int_t nentries1 = (Int_t)t1->GetEntries();
    Int_t nentries2 = (Int_t)t2->GetEntries();

    for (Int_t i=0; i<nentries1; i++) {
      t1->GetEntry(i);

      for (Int_t j=0; j<nentries2; j++) {
        t2->GetEntry(j);
        if (run1 == run2 && event1 == event2) {
          //fill histogram with difference of values
          Double_t diff = branch1 - branch2;
          h_diff->Fill(diff);
        }
      }
    }
    //draw and save the histogram in current directory
    h_diff->Draw();
    ct->SaveAs(file_name);

    //make a new canvas to plot 2nd histogram on
    TCanvas *ct2 = new TCanvas("ct2",title_norm,0,0,600,600);
    ct2->cd();

    TH1D *h_norm = new TH1D("h_norm",title_norm,500,-1.0,1.0);

    for (Int_t i=0; i<nentries1; i++) {
      t1->GetEntry(i);

      for (Int_t j=0; j<nentries2; j++) {
        t2->GetEntry(j);
        if (run1 == run2 && event1 == event2) {
          //fill 2nd histogram with normalized difference
          Double_t diff_norm = (branch1 - branch2) / branch2;
          h_norm->Fill(diff_norm);
        }
      }
    }
    //draw and save the histogram in current directory
    h_norm->Draw();
    ct2->SaveAs(file_norm);

    //close the TCanvas's
    ct->Close();
    ct2->Close();
  }
  delete file1;
  delete file2;
}
#include "TFile.h"
#include "TTree.h"
#include "TDirectory.h"
#include "TStopwatch.h"
#include "TTreeReader.h"
#include "TBranch.h"
#include "TCanvas.h"
#include "TH1D.h"
#include <vector>
#include <string>

//=========================================================================
// This macro will do the following:
// 1. Extract the unique event IDs from two ntuples
// 2. Save the unique extracted IDs to their own respective ntuples
// 3. Read in one ntuple and convert the event IDs into a vector following
//    the format described below
// 4. Crossmatch this ntuple vector and the second UID ntuple ONLY for the
//    unique ID events (do this by looping over unique ID vector for first
//    file, then loop over second UID ntuple)
// 5. Compare a single branch present in both ntuples (as of now this
//    branch must be of type Double_t but this will be changed after
//    implementation with Yipeng's code)
//=========================================================================

/*
Vectors of the event IDs have the following form

        column 1        column 2
row 1   eventNumber_0   runNumber_0
row 2   eventNumber_1   runNumber_1
row 3   eventNumber_2   runNumber_2
...     ...             ...
row n   eventNumber_n   runNumber_n

Here n is the number of entries in the file fed into convert_to_vec
*/

std::string extract_uid(std::string file, std::string tree,
                        std::string outfile);
std::string get_tree_name(std::string tree);
std::vector<std::vector<ULong64_t>> convert_to_vec(std::string file_name,
                                                   std::string tree_name);
std::string crossmatch(std::vector<std::vector<ULong64_t>> uids,
                       std::string file, std::string tree,
                       std::string outfile);
void compare_branch(std::string file1, std::string file2,
                    std::string tree1, std::string tree2, 
                    std::string branch_name1, std::string branch_name2,
                    std::string out_tuple);



int ntuple_validate(std::string infile1, std::string infile2,
                    std::string intree1, std::string intree2,
                    std::string branch_name1, std::string branch_name2,
                    std::string out_tuple) {

  // The two .root files read in are the two files we want to compare
  // Specifically, infile1 must be the file to be validated and infile2 is
  // the file to validate against (although vice-versa should be fine also)
  // The branch to compare must be listed as "branch_name1" in "infile1"
  // and as "branch_name2" in "infile2"
  // The "out_tuple" read in is used to define the output .root files
  // For example, if one wants the output crossmatch file to be named
  // "mc_crossmatch.root" then the given input to "out_tuple" must be "mc"

  // Define the output UID file names
  size_t pos_dot1 = infile1.find(".");
  size_t pos_dot2 = infile2.find(".");

  std::string uid_outfile1 = infile1;
  uid_outfile1 = uid_outfile1.erase(pos_dot1,std::string::npos);
  uid_outfile1 = uid_outfile1 + "_uid.root";

  std::string uid_outfile2 = infile2;
  uid_outfile2 = uid_outfile2.erase(pos_dot2,std::string::npos);
  uid_outfile2 = uid_outfile2 + "_uid.root";

  // Extract the unique IDs from each given .root file
  std::string uid_infile1 = extract_uid(infile1, intree1, uid_outfile1);
  std::string uid_infile2 = extract_uid(infile2, intree2, uid_outfile2);

  // If input tree name for "intree1/2" have a directory structure then
  // save only the actual tree name (not full path to tree name)
  // This must be done because the saved output file will not have a
  // directory structure for the tree, it will just be the tree name
  std::string uid_tree1 = get_tree_name(intree1);
  std::string uid_tree2 = get_tree_name(intree2);

  // Save the extracted unique IDs as a vector
  std::vector<std::vector<ULong64_t>> uid_vec = convert_to_vec(uid_infile1,
                                                               uid_tree1);

  std::string cm_outfile = out_tuple + "_crossmatch.root";

  // Crossmatch the first UID file with second input file
  std::string cm_file = crossmatch(uid_vec, uid_infile2, uid_tree2,
                                   cm_outfile);

  // Compare the branches between the UID file for "infile1" and the
  // crossmatched UID file for "infile2"
  compare_branch(uid_infile1, cm_file, uid_tree1, uid_tree2,
                 branch_name1, branch_name2, out_tuple);

  return 0;
}



std::string extract_uid(std::string file, std::string tree,
                        std::string outfile) {
  TStopwatch timer;
  timer.Start();

  // Initialize ntuple files
  TFile *tp1 = new TFile(file.c_str(), "READ");
  TFile *tp2 = new TFile(file.c_str(), "READ");
  TFile *tp_out = new TFile(outfile.c_str(), "RECREATE");

  TTree *readTree = (TTree*)tp1->Get(tree.c_str());

  // Initialize output tree
  TTree *outtree = readTree->CloneTree(0);

  // Initialize readers for file1.
  TTreeReader reader1(tree.c_str(), tp1);
  TTreeReaderValue<UInt_t> runNumber1_reader(reader1, "runNumber");
  TTreeReaderValue<ULong64_t> eventNumber1_reader(reader1, "eventNumber");

  // Initialize branch value storage in loop
  UInt_t runNumber1;
  UInt_t runNumber2;
  ULong64_t eventNumber1;
  ULong64_t eventNumber2;

  // Loop over ntuples and find unique events
  while (reader1.Next()) {
    int num_of_occurrence = 0;

    runNumber1 = *runNumber1_reader;
    eventNumber1 = *eventNumber1_reader;

    // NOTE: A reader can only be consumed once. So we need to recreate new
    // readers inside the loop
    TTreeReader reader2(tree.c_str(), tp2);
    TTreeReaderValue<UInt_t> runNumber2_reader(reader2, "runNumber");
    TTreeReaderValue<ULong64_t> eventNumber2_reader(reader2, "eventNumber");

    while (reader2.Next()) {
      runNumber2 = *runNumber2_reader;
      eventNumber2 = *eventNumber2_reader;

      if (runNumber1 == runNumber2 and eventNumber1 == eventNumber2) {
        num_of_occurrence++;
      }
    }

    // Get unique ID events and all their branches, save to output tree
    if (num_of_occurrence == 1) {
      readTree->GetEntry(reader1.GetCurrentEntry(),1);
      outtree->Fill();
    }  // Ignore duplicated events for now
  }

  tp_out->Write();
  tp_out->Close();

  delete tp1;
  delete tp2;
  delete tp_out;

  timer.Stop();

  // Print out the real time and the CPU time taken to make the new file
  cout << "\n" << endl;
  cout << " Extracting UID ..." << endl;
  cout << " Total CPU Time = " << timer.CpuTime() << endl;
  cout << " Total Real Time = " << timer.RealTime() << endl;

  return outfile;
}


std::string get_tree_name(std::string tree) {
  // Find the position of the last "/" in the given tree name
  size_t pos_slash = tree.find_last_of("/");

  // If there is a directory structure then keep only the tree name itself,
  // if not then do not change the tree name
  if (pos_slash != std::string::npos) {
    std::string tree_name = tree;
    tree_name = tree_name.erase(0,pos_slash+1);
    return tree_name;

  } else {
    std::string tree_name = tree;
    return tree_name;
  }
}


std::vector<std::vector<ULong64_t>> convert_to_vec(std::string file_name,
                                                   std::string tree_name) {

  // Define the vector to write the event IDs to
  std::vector<std::vector<ULong64_t>> vec;

  // Initialize given file
  TFile *file = new TFile(file_name.c_str(), "READ");

  TTree *tree = (TTree*)file->Get(tree_name.c_str());

  // Get total number of entries in the file
  Int_t nentries = (Int_t)tree->GetEntries();

  // Resize the output vector to be the right size
  // Vector will have "nentries" number of rows and 2 columns
  vec.resize(nentries, std::vector<ULong64_t>(2));

  // Initialize reader for the given file
  TTreeReader file_reader(tree_name.c_str(), file);
  TTreeReaderValue<UInt_t> runNumber_reader(file_reader, "runNumber");
  TTreeReaderValue<ULong64_t> eventNumber_reader(file_reader, "eventNumber");

  // Initialize branch values
  UInt_t run;
  ULong64_t event;

  // Loop over the file and save the eventNumber and runNumber to the vector
  while (file_reader.Next()) {
    run = *runNumber_reader;
    event = *eventNumber_reader;

    vec[file_reader.GetCurrentEntry()][0] = event;
    vec[file_reader.GetCurrentEntry()][1] = run;
  }

  delete file;

  return vec;
}


std::string crossmatch(std::vector<std::vector<ULong64_t>> uids,
                       std::string file, std::string tree,
                       std::string outfile) {

  TStopwatch timer;
  timer.Start();

  // Initialize ntuple files
  TFile *f_in = new TFile(file.c_str(), "READ");
  TFile *f_out = new TFile(outfile.c_str(), "RECREATE");

  TTree *readTree = (TTree*)f_in->Get(tree.c_str());

  // Initialize output tree
  TTree *outtree = readTree->CloneTree(0);

  // Initialize branch values for looping
  UInt_t runNumber1;
  UInt_t runNumber2;
  ULong64_t eventNumber1;
  ULong64_t eventNumber2;

  // Loop over unique event ID vector and match with input file
  for (Int_t i=0; i<uids.size(); i++) {
    eventNumber1 = uids[i][0];
    runNumber1 = uids[i][1];

    // Initilaize readers for (file)
    // NOTE: A reader can only be consumed once. So we need to recreate new
    // readers inside the loop
    TTreeReader reader(tree.c_str(), f_in);
    TTreeReaderValue<UInt_t> runNumber2_reader(reader, "runNumber");
    TTreeReaderValue<ULong64_t> eventNumber2_reader(reader, "eventNumber");

    while (reader.Next()) {
      runNumber2 = *runNumber2_reader;
      eventNumber2 = *eventNumber2_reader;

      if (runNumber1 == runNumber2 and eventNumber1 == eventNumber2) {
        readTree->GetEntry(reader.GetCurrentEntry(),1);
        outtree->Fill();
      }
    }
  }

  // Write the tree to the new .root file
  f_out->Write();
  f_out->Close();

  delete f_in;
  delete f_out;

  timer.Stop();

  // Print out the real time and the CPU time taken to make the new file
  cout << "\n" << endl;
  cout << " Crossmatching ..." << endl;
  cout << " Total CPU Time = " << timer.CpuTime() << endl;
  cout << " Total Real Time = " << timer.RealTime() << endl;

  return outfile;
}


void compare_branch(std::string file1, std::string file2,
                    std::string tree1, std::string tree2,
                    std::string branch_name1, std::string branch_name2,
                    std::string out_tuple) {
  // Initialize ntuple files
  TFile *f1 = new TFile(file1.c_str(), "READ");
  TFile *f2 = new TFile(file2.c_str(), "READ");

  TTree *t1 = (TTree*)f1->Get(tree1.c_str());
  TTree *t2 = (TTree*)f2->Get(tree2.c_str());

  // Get branch names within each file to see whether to continue analysis
  TBranch *testb1 = t1->GetBranch(branch_name1.c_str());
  TBranch *testb2 = t2->GetBranch(branch_name2.c_str());

  // Throw message and exit program if branches not in file
  if (!testb1 || !testb2) {
    cout << "\n" << endl;

    cout << "The given branch names are not branches in one or both files."
    << endl;

    cout << "Try running the program again stating different branch names."
    << endl;

    cout << "The program has terminated.\n" << endl;

    exit(0);
  } else {
    cout << "\n" << endl;

    cout << "The given branches are actual branches in their respective files."
    << endl;

    cout << "Further analysis to come ...\n" << endl;
  }
  
  // Initialize branch values for looping
  UInt_t runNumber1;
  UInt_t runNumber2;
  ULong64_t eventNumber1;
  ULong64_t eventNumber2;
  Double_t branch1;
  Double_t branch2;

  // Initialize readers for file1
  TTreeReader reader1(tree1.c_str(), f1);
  TTreeReaderValue<UInt_t> runNumber1_reader(reader1, "runNumber");
  TTreeReaderValue<ULong64_t> eventNumber1_reader(reader1, "eventNumber");
  TTreeReaderValue<Double_t> branch1_reader(reader1, branch_name1.c_str());

  // Define title and file name of first (non-normalized) histogram
  std::string title1 = branch_name1 + " " + out_tuple + " Difference";
  std::string file_name1 = branch_name1 + "_" + out_tuple + "_diff.png";

  // Make canvas to plot first histogram
  TCanvas *ct = new TCanvas("ct",title1.c_str(),0,0,600,600);
  ct->cd();

  TH1D *h_diff = new TH1D("h_diff",title1.c_str(),500,-75.0,75.0);

  while (reader1.Next()) {
    runNumber1 = *runNumber1_reader;
    eventNumber1 = *eventNumber1_reader;
    //branch1 = *branch1_reader;

    // NOTE: A reader can only be consumed once. So we need to recreate new
    // readers inside the loop
    TTreeReader reader2(tree2.c_str(), f2);
    TTreeReaderValue<UInt_t> runNumber2_reader(reader2, "runNumber");
    TTreeReaderValue<ULong64_t> eventNumber2_reader(reader2, "eventNumber");
    TTreeReaderValue<Double_t> branch2_reader(reader2, branch_name2.c_str());

    while (reader2.Next()) {
      runNumber2 = *runNumber2_reader;
      eventNumber2 = *eventNumber2_reader;
      //branch2 = *branch2_reader;

      if (runNumber1 == runNumber2 and eventNumber1 == eventNumber2) {
        branch1 = *branch1_reader;
        branch2 = *branch2_reader;

        Double_t diff = branch1 - branch2;
        h_diff->Fill(diff);
      }
    }
  }
  // Draw and save the histogram in the current directory
  h_diff->Draw();
  ct->SaveAs(file_name1.c_str());

  // Initialize readers for file1 for the normalized histograms
  // Must use a different reader name, so use reader3 for file1 and
  // reader4 for file2
  TTreeReader reader3(tree1.c_str(), f1);
  TTreeReaderValue<UInt_t> runNumber3_reader(reader3, "runNumber");
  TTreeReaderValue<ULong64_t> eventNumber3_reader(reader3, "eventNumber");
  TTreeReaderValue<Double_t> branch3_reader(reader3, branch_name1.c_str());

  // Define title and file name of second (normalized) histogram
  std::string title2 = branch_name1 + " " + out_tuple + " Difference (Norm)";
  std::string file_name2 = branch_name1 + "_" + out_tuple + "_diff_norm.png";

  // Make canvas to plot the second histogram
  TCanvas *ct2 = new TCanvas("ct2",title2.c_str(),0,0,600,600);
  ct2->cd();

  TH1D *h_norm = new TH1D("h_norm",title2.c_str(),500,-1.0,1.0);

  while (reader3.Next()) {
    runNumber1 = *runNumber3_reader;
    eventNumber1 = *eventNumber3_reader;
    //branch1 = *branch3_reader;

    // NOTE: A reader can only be consumed once. So we need to create new
    // readers inside the loop
    TTreeReader reader4(tree2.c_str(), f2);
    TTreeReaderValue<UInt_t> runNumber4_reader(reader4, "runNumber");
    TTreeReaderValue<ULong64_t> eventNumber4_reader(reader4, "eventNumber");
    TTreeReaderValue<Double_t> branch4_reader(reader4, branch_name2.c_str());

    while (reader4.Next()) {
      runNumber2 = *runNumber4_reader;
      eventNumber2 = *eventNumber4_reader;
      //branch2 = *branch4_reader;

      if (runNumber1 == runNumber2 and eventNumber1 == eventNumber2) {
        branch1 = *branch3_reader;
        branch2 = *branch4_reader;

        Double_t diff_norm = (branch1 - branch2) / branch2;
        h_norm->Fill(diff_norm);
      }
    }
  }
  // Draw and save the histogram in the current directory
  h_norm->Draw();
  ct2->SaveAs(file_name2.c_str());

  // Close the TCanvas's
  ct->Close();
  ct2->Close();

  delete f1;
  delete f2;
}


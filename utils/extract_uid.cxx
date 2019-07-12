// Author: Ben Flaggs, Yipeng Sun
// License: BSD 2-clause
// Last Change: Fri Jul 12, 2019 at 02:14 AM -0400

#include <TFile.h>
#include <TStopwatch.h>
#include <TTree.h>
#include <TTreeReader.h>
#include <iostream>
#include <string>

using namespace std;

void extract_uid(string file1, string file2, string output, string tree1,
                 string tree2) {
  TStopwatch timer;
  timer.Start();

  // initialize ntuple files
  TFile *tp1 = new TFile(file1.c_str(), "read");
  TFile *tp2 = new TFile(file2.c_str(), "read");
  TFile *tp_out = new TFile(output.c_str(), "recreate");

  // initialize output tree
  TTree tree("uid", "uid");

  // initialize readers for file1.
  TTreeReader reader1(tree1.c_str(), tp1);
  TTreeReaderValue<UInt_t> runNumber1_reader(reader1, "runNumber");
  TTreeReaderValue<ULong64_t> eventNumber1_reader(reader1, "eventNumber");

  // initialize branch value storage in loop
  UInt_t runNumber1;
  UInt_t runNumber2;
  ULong64_t eventNumber1;
  ULong64_t eventNumber2;

  // initialize output branches
  tree.Branch("runNumber", &runNumber1);
  tree.Branch("eventNumber", &eventNumber1);

  while (reader1.Next()) {
    int num_of_occurrence = 0;

    runNumber1 = *runNumber1_reader;
    eventNumber1 = *eventNumber1_reader;

    // NOTE: a reader can only be consumed once. So we need to recreate new
    // readers inside the loop
    TTreeReader reader2(tree2.c_str(), tp2);
    TTreeReaderValue<UInt_t> runNumber2_reader(reader2, "runNumber");
    TTreeReaderValue<ULong64_t> eventNumber2_reader(reader2, "eventNumber");

    while (reader2.Next()) {
      runNumber2 = *runNumber2_reader;
      eventNumber2 = *eventNumber2_reader;

      if (runNumber1 == runNumber2 and eventNumber1 == eventNumber2) {
        num_of_occurrence++;
      }
    }

    if (num_of_occurrence == 1) {
      tree.Fill();
    }  // ignore duplicated events for now
  }

  tp_out->Write();
  tp_out->Close();

  delete tp1;
  delete tp2;
  delete tp_out;

  timer.Stop();

  // print out the real time and the CPU time taken to make the new file
  cout << " Total CPU Time = " << timer.CpuTime() << endl;
  cout << " Total Real Time = " << timer.RealTime() << endl;
}

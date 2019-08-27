// Author: Ben Flaggs, Yipeng Sun
// License: BSD 2-clause
// Last Change: Tue Aug 27, 2019 at 03:05 PM -0400

#include <TCanvas.h>
#include <TFile.h>
#include <TH1D.h>
#include <TROOT.h>
#include <TTreeReader.h>

#include <iostream>
#include <memory>
#include <string>

using namespace std;

const string file_extension = ".png";

void make_histo_float(string input_filename, string output_dir, string suffix,
                      string tree_name, string branch_name, int nbinsx,
                      double xlow, double xup) {
  auto file = std::make_unique<TFile>(input_filename.c_str());
  auto canvas =
      std::make_unique<TCanvas>("canvas", branch_name.c_str(), 0, 0, 600, 600);
  auto histo =
      std::make_unique<TH1D>("histo", branch_name.c_str(), nbinsx, xlow, xup);

  // Don't display canvas on-screen
  gROOT->SetBatch(kTRUE);

  TTreeReader             reader(tree_name.c_str(), file.get());
  TTreeReaderValue<float> branch(reader, branch_name.c_str());

  while (reader.Next()) {
    auto value = *branch;
    histo->Fill(value);
  }

  histo->Draw();
  canvas->SaveAs((output_dir + branch_name + suffix + file_extension).c_str());
}

// Author: Ben Flaggs, Yipeng Sun
// License: BSD 2-clause
// Last Change: Sun Aug 25, 2019 at 11:37 PM -0400

#include <TFile.h>
#include <TH1D.h>
#include <TCanvas.h>
#include <TTreeReader.h>
#include <TROOT.h>

#include <iostream>
#include <string>

using namespace std;

const string file_extension = ".png";

void make_histo_float(string input_filename, string output_dir, string suffix,
    string tree_name, string branch_name,
    int nbinsx, double xlow, double xup) {
  TFile *file = new TFile(input_filename.c_str());

  TCanvas *canvas = new TCanvas("canvas", branch_name.c_str(), 0, 0, 600, 600);
  TH1D *histo = new TH1D("histo", branch_name.c_str(), nbinsx, xlow, xup);

  // Don't display canvas on-screen
  gROOT->SetBatch(kTRUE);

  TTreeReader reader(tree_name.c_str(), file);
  TTreeReaderValue<float> branch(reader, branch_name.c_str());

  while (reader.Next()) {
    auto value = *branch;
    histo->Fill(value);
  }

  histo->Draw();
  canvas->SaveAs((output_dir + branch_name + suffix + file_extension).c_str());

  delete canvas;
  delete histo;
  delete file;
}

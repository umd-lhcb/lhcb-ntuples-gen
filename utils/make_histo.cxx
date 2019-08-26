// Author: Ben Flaggs, Yipeng Sun
// License: BSD 2-clause
// Last Change: Sun Aug 25, 2019 at 10:13 PM -0400

#include <TFile.h>
#include <TH1D.h>
#include <TCanvas.h>
#include <TTreeReader.h>

#include <iostream>
#include <string>

using namespace std;

const string file_extension = ".png";

void make_histo(string input_filename, string output_dir,
    string tree_name, string branch_name,
    int nbinsx, double xlow, double xup) {
  TFile *file = new TFile(input_filename.c_str());

  TCanvas *canvas = new TCanvas("canvas", branch_name.c_str(), 0, 0, 600, 600);
  canvas->cd();

  TH1D *histo = new TH1D("histo", branch_name.c_str(), nbinsx, xlow, xup);

  TTreeReader reader(tree_name.c_str(), file);
  TTreeReaderValue<double> branch(reader, branch_name.c_str());

  while (reader.Next()) {
    auto value = static_cast<double>(*branch);
    histo->Fill(value);
  }

  canvas->SaveAs((output_dir + branch_name + file_extension).c_str());

  delete file;
  delete histo;
  delete canvas;
}

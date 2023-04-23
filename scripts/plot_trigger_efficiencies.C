// Plot trigger efficiencies with weights
// Take a look at here on how to use this macro:
//   https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/f0aef2913520fb9ff49a949493b8ac69fd72d3bd/studies/trigger_emulation-l0_hadron_tos_xgb_debug/plot_l0hadron_xgb_eff.py

#include <iostream>
#include <vector>

#include "TApplication.h"
#include "TCanvas.h"
#include "TChain.h"
#include "TGraphAsymmErrors.h"
#include "TH1D.h"
#include "TString.h"
#include "TStyle.h"

using namespace std;

void    setStyle(float lMargin, float tMargin);
TString varToHuman(TString var);
TString varToPlain(TString var);

void plot_trigger_wefficiencies(TString ntpName, TString var,
                                vector<TString> trigs, TString basecut,
                                float minx = 0., float maxx = 20.,
                                int nbins = 40, TString outFolder = "./") {
  // Loading ntuple
  TChain ntp("TupleB0/DecayTree");
  ntp.Add(ntpName);

  // Setting up style
  float lMargin = 0.1, tMargin = 0.06;
  setStyle(lMargin, tMargin);
  TCanvas can("can", "", 1000, 840);
  can.cd();
  can.SetGrid();

  ntpName.Remove(0, ntpName.Last('/') + 1);
  ntpName.ReplaceAll("l0hadron_full_", "");
  ntpName.ReplaceAll(".root", "");
  TH1D haxis("haxis", "", nbins, minx, maxx);
  haxis.GetYaxis()->SetRangeUser(0, 1 + trigs.size() * 0.08);
  haxis.GetYaxis()->SetTitle("L0Hadron efficiency");
  haxis.GetXaxis()->SetTitle(varToHuman(var));
  TString title = ntpName;
  if (basecut != "1") title += " [" + basecut + "]";
  haxis.SetTitle(title);
  haxis.GetYaxis()->CenterTitle(true);
  haxis.GetXaxis()->CenterTitle(true);
  haxis.Draw();

  double  legX(lMargin + 0.05), legY = 1 - tMargin - 0.01, legSingle = 0.048;
  double  legW = 0.5, legH = legSingle * trigs.size();
  TLegend leg(legX, legY - legH, legX + legW, legY);
  leg.SetTextSize(0.035);

  // Calculating and drawing efficiencies for each cut
  vector<TGraphAsymmErrors*> graphs;
  vector<int>                colors({1, kBlue - 7, 2, 8});
  for (unsigned ind = 0; ind < trigs.size(); ind++) {
    TH1D*   histo[2];
    TString hname, totCut, pname;
    hname    = "den";
    totCut   = basecut;
    histo[0] = new TH1D(hname, "", nbins, minx, maxx);
    ntp.Project(hname, var, totCut);
    hname    = "num";
    totCut   = "(" + basecut + ")*(" + trigs[ind] + ")";
    histo[1] = new TH1D(hname, "", nbins, minx, maxx);
    ntp.Project(hname, var, totCut);

    // Adding overflow bins
    for (unsigned his(0); his < 2; his++) {
      double valLastbin = histo[his]->GetBinContent(nbins) +
                          histo[his]->GetBinContent(nbins + 1);
      histo[his]->SetBinContent(nbins, valLastbin);
    }

    graphs.push_back(new TGraphAsymmErrors(histo[1], histo[0]));
    TString opts = "";
    opts         = "P same";
    graphs[ind]->SetMarkerColor(colors[ind]);
    graphs[ind]->SetLineColor(colors[ind]);
    if (ind == 0) {
      graphs[ind]->SetMarkerSize(1.4);
      graphs[ind]->SetMarkerStyle(21);
    } else {
      graphs[ind]->SetMarkerSize(1.2);
      graphs[ind]->SetMarkerStyle(20);
    }

    leg.AddEntry(graphs[ind], varToHuman(trigs[ind]));

    graphs[ind]->Draw(opts);
    for (unsigned his(0); his < 2; his++) histo[his]->Delete();
  }
  leg.Draw();

  TString pname = outFolder + "/" + varToPlain(var) + "-" + ntpName + "-Cut_" +
                  varToPlain(basecut) + ".png";
  can.SaveAs(pname);

  for (unsigned ind = 0; ind < trigs.size(); ind++) graphs[ind]->Delete();

  gApplication->Terminate();
}

TString varToHuman(TString var) {
  var.ReplaceAll("k_", "K ");
  var.ReplaceAll("d0_", "D^{0} ");
  var.ReplaceAll("PT", "p_{T}");
  var.ReplaceAll("/1000", " [GeV]");
  var.ReplaceAll("/1000000", " [GeV^{2}]");
  var.ReplaceAll("l0_hadron_prob", "XGB prob.");
  var.ReplaceAll("l0_hadron_tos_emu_no_bdt", "E_{trig} emu no BDT");
  var.ReplaceAll("l0_hadron_tos_emu", "XGB bool");
  var.ReplaceAll("FitVar_El", "E_{#mu} ");
  var.ReplaceAll("FitVar_Mmiss2", "m_{miss}^{2} ");
  var.ReplaceAll("FitVar_q2", "q^{2} ");
  var.ReplaceAll("b0_ISOLATION_BDT", "BDT_{iso} ");

  return var;
}

TString varToPlain(TString var) {
  var.ReplaceAll("/", "_div");
  var.ReplaceAll(">", "_g");
  var.ReplaceAll(">=", "_geq");
  var.ReplaceAll("<", "_l");
  var.ReplaceAll("<=", "_leq");
  var.ReplaceAll("==", "_eq");
  var.ReplaceAll("(", "-");
  var.ReplaceAll(")", "-");
  var.ReplaceAll(" ", "_");
  var.ReplaceAll(",", "-");
  var.ReplaceAll("&&", "_AND_");
  var.ReplaceAll("||", "_OR_");

  return var;
}

void setStyle(float lMargin, float tMargin) {
  gStyle->SetOptStat(0);  // No Stats box
  gStyle->SetTitleOffset(1, "x");
  gStyle->SetTitleOffset(1, "y");
  gStyle->SetPadRightMargin(0.039);
  gStyle->SetPadBottomMargin(0.11);
  gStyle->SetPadTopMargin(tMargin);
  gStyle->SetPadLeftMargin(lMargin);
  gStyle->SetTitleFontSize(0.036);     // Set top title size
  gStyle->SetTitleSize(0.045, "xyz");  // Set the 2 axes title size
  gStyle->SetLabelSize(0.038, "xyz");  // Set the 2 axes label size
}

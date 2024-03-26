#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include <map>
#include <iostream>
#include <vector>
#include "TCut.h"
#include "TCanvas.h"
#include "TEventList.h"
#include "TTreeFormula.h"
#include "RooAddPdf.h"
#include "RooAbsPdf.h"
#include "RooPlot.h"
#include "RooRealVar.h"
#include "RooGaussian.h"
#include "RooCBShape.h"
#include "RooDataSet.h"
#include "RooDataHist.h"
#include "RooExponential.h"
#include "RooStats/SPlot.h"
#include "RooTreeDataStore.h"
// 
// 
// int main()

int sWeightJpsiK(){
  TCut cutstring = "muplus_PT > 500 && muminus_PT > 500 && K_PT > 500 && Bplus_DIRA_OWNPV > 0.9995 && Bplus_MINIPCHI2 < 12 && Bplus_ENDVERTEX_CHI2 < 18 && muplus_MINIPCHI2 > 4 && muminus_MINIPCHI2 > 4&& Jpsi_FDCHI2_OWNPV > 25 && Jpsi_MM > 3060 && Jpsi_MM < 3140 && K_PIDK > 4 && muminus_PIDmu > 2 && muplus_PIDmu > 2&& (Bplus_Hlt2Topo2BodyBBDTDecision_TOS || Bplus_Hlt2Topo3BodyBBDTDecision_TOS) && Bplus_Hlt1TrackAllL0Decision_TOS > 0.5 && Bplus_M > 5150 && Bplus_M < 5350";
  
  std::map<string,double> mins;
  std::map<string,double> maxs;
  
  std::vector<TString> floatvars;
  
  
  TFile *f1 = new TFile("JpsiKData.root");
  TTree *tree = (TTree*) f1->Get("DecayTree");    
  
  
  TEventList list("list","list");
  tree->Draw(">>list",cutstring);
  RooRealVar Bplus_M("Bplus_M","M_{J/#psi K} (MeV / c^{2})",5150,5350);
  TTreeFormula ttf("ttf","Bplus_M",tree);
  
  /*
  TH1F hist("hist","",150,5150,5350);
  tree->Draw("Bplus_M>>hist",cutstring);
  RooDataHist unbinned("unbinned","unbinned",Bplus_M,&hist);
  */
  
//   TTreeFormula ttf("ttf","Bplus_M",tree);
///*

  RooDataSet unbinned("unbinned","unbinned",Bplus_M);
  for(int i=0;i<list.GetN();i++){
//   for(int i=0;i<100e3;i++){
    tree->GetEntry(list.GetEntry(i));
    Bplus_M=ttf.EvalInstance();
    unbinned.add(Bplus_M);   
  }
  RooRealVar peak("peak","peak",5270,5290);
  RooRealVar width1("width1","width1",15,30);
  RooRealVar width2("width2","width2",0,15);
  RooRealVar alpha("alpha","alpha",0.5,2);
  RooRealVar nsigma("nsigma","nsigma",3,150);
  RooCBShape g1("g1","g1",Bplus_M,peak,width1,alpha,nsigma);
  RooGaussian g2("g2","g2",Bplus_M,peak,width2);
  RooRealVar frac("frac","frac",0.6,0,1);
  RooAddPdf signal("signal","signal",RooArgSet(g1,g2),RooArgSet(frac));
  RooRealVar expc("expc","expc",-0.05,0.);
  RooExponential bkg("bkg","bkg",Bplus_M,expc);
  
  
  
  RooRealVar peaktail("peaktail","peaktail",5120,5170);
  RooRealVar widthtail("widthtail","widthtail",20,50);
  RooGaussian gtail("gtail","gtail",Bplus_M,peaktail,widthtail);
  
  RooRealVar signalyield("signalyield","signalyield",0,1.5e6);
  RooRealVar bkgyield("bkgyield","bkgyield",0,200000);
  RooRealVar tailyield("tailyield","tailyield",0,10e3);
  RooAddPdf model("model","model",RooArgSet(signal,bkg,gtail),RooArgSet(signalyield,bkgyield,tailyield));
  model.fitTo(unbinned)  ;
  
  //
  
  RooPlot *frame = Bplus_M.frame();
  frame->SetTitle("");
  unbinned.plotOn(frame);
  model.plotOn(frame);
  
  model.plotOn(frame,RooFit::Components("signal"),RooFit::LineStyle(kDashed),RooFit::LineColor(kRed));
  model.plotOn(frame,RooFit::Components("bkg"),RooFit::LineStyle(kDashed),RooFit::LineColor(kBlack));
  TCanvas c;
  frame->Draw();
  c.SaveAs("JpsiKfit.pdf");
  c.SaveAs("JpsiKfit.eps");

  RooStats::SPlot *splot = new RooStats::SPlot("splot","splot",unbinned,&model,RooArgList(signalyield,bkgyield));
  
  TFile *outfile = new TFile("JpsiKDataWeighted.root","recreate");
  TTree * outtree = tree->CopyTree(cutstring);
//   unbinned.store()->Print();
  Double_t sWeight;
  
  TBranch *sBranch = outtree->Branch("sWeight",&sWeight);
  for(int i=0;i<outtree->GetEntries();i++){
    sWeight = unbinned.store()->get(i)->getRealValue("signalyield_sw");
    sBranch->Fill();
  }
  outfile->Write();
  return 0;
    
}

#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include <memory>
#include <cstdlib> 
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TH3.h"
#include "TCanvas.h"
#include "TChain.h"
#include "TChainElement.h"
#include "TEventList.h"
#include "TEntryList.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TMath.h"
#include "TCut.h"
#include "TTree.h"
#include "TTreeFormula.h"
#include "TString.h"
#include "TApplication.h"

// TString name = "reweighting_v2";
// TString name = "reweighting_Sim0X_v1";
// TString name = "reweighting_Sim0X_PV";
// TString name = "Sim08to9Kin_v1TOS";
// TString name = "Sim08to9KinNonTIS_v2";
// TString name = "Sim08to9HadCorr_v2";
// TString name = "Sim08to9PythiaMuTIS";

// TString name = "reweighting_JpsiKBoth_v1_L0Corr";
// TString name = "reweighting_IP_v2";


// TString name = "reweighting_89_JpsiK_v2_finer";

// TString name = "reweighting_69_JpsiK";


TString name = "reweighting_JpsiK";

int reweight(TString filename,TString treename);
void weight3D( std::string,int, float, float, std::string,int, float, float, std::string,int, float, float);

int reweight(TString filename,TString treename){
  std::cout << "processing " << filename << " with tree " << treename << std::endl;
  int nWeights = 2;
  int nCats=3;
  TFile *fweight= new TFile("JpsiKWeights.root");
  
  
  TFile *file = new TFile(filename,"update");
  TTree *tree = (TTree*) file->Get(treename);

  
  
  tree->SetAlias("Bplus_TRUEP_X","Bplus_PX");
  tree->SetAlias("Bplus_TRUEP_Y","Bplus_PY");
  tree->SetAlias("Bplus_TRUEP_Z","Bplus_PZ");
  tree->SetAlias("Bplus_TRUEPT","Bplus_PT");
  
  
  
  std::vector< std::vector<TH3F*> > hists;
  std::vector<TTreeFormula*> xvarTTFs;
  std::vector<TTreeFormula*> yvarTTFs;
  std::vector<TTreeFormula*> zvarTTFs;
  std::vector<TTreeFormula*> catTTFs;  
  
  
  
  for(int i =1;i<nWeights+1;i++){
    std::vector<TH3F*>tmphists;
    for(int j=0;j<nCats;j++){
//     TString weightname = TString::Format("weighting_%i",i);
    TString weightname = "weighting_"+TString::Format("%i",i)+"_category_"+TString::Format("%i",j);
//     std::cout << "weightname " << weightname << std::endl;
    tmphists.push_back((TH3F*)fweight->Get(weightname));
    }
    hists.push_back(tmphists);
//     std::cout << "got histograms" << std::endl;
    TString variables = hists[i-1][0]->GetTitle();
    TObjArray *terms = variables.Tokenize(":");
    TIterator *itString = terms->MakeIterator();
    TObjString *_string;
    TString varnames[4];
    int ivar = 0;
      do {
  //       std::cout<< "loopStart" << std::endl;
	_string= (TObjString*) itString->Next();
  //       _string->Print();	
// 	std::cout << _string->String() << std::endl;
	varnames[ivar]=_string->String();
	ivar++;
    }
    while(_string!=(TObjString*)terms->Last());
//     std::cout << "xvarname " << varnames[2] << std::endl;
    xvarTTFs.push_back(new TTreeFormula ((TString)"TTF_"+varnames[2],varnames[2],tree));
    yvarTTFs.push_back(new TTreeFormula ((TString)"TTF_"+varnames[1],varnames[1],tree));
    zvarTTFs.push_back(new TTreeFormula ((TString)"TTF_"+varnames[0],varnames[0],tree));
//     catTTFs.push_back(new TTreeFormula ((TString)"TTF_"+varnames[3],varnames[3],tree));
  }
  
  
  for(int k=0;k<nCats;k++){
//     hists[k][0];
    
    TString variables = hists[0][k]->GetTitle();
    TObjArray *terms = variables.Tokenize(":");
    TIterator *itString = terms->MakeIterator();
    TObjString *_string;
    TString varnames[4];
    int ivar = 0;
      do {
  //       std::cout<< "loopStart" << std::endl;
	_string= (TObjString*) itString->Next();
  //       _string->Print();	
// 	std::cout << _string->String() << std::endl;
	varnames[ivar]=_string->String();
	ivar++;
    }
    while(_string!=(TObjString*)terms->Last());
//     std::cout << varnames[3] << std::endl;
    catTTFs.push_back(new TTreeFormula ((TString)"TTF_"+varnames[3],varnames[3],tree));
  }
  
  Float_t weight;
  TBranch *br = tree->Branch(name,&weight);
  for(int j=0;j<tree->GetEntries();j++){
   tree->GetEntry(j);
   weight = 1.;
   for(int i =1;i<nWeights+1;i++){
      float _x = xvarTTFs[i-1]->EvalInstance();
      float _y = yvarTTFs[i-1]->EvalInstance();
      float _z = zvarTTFs[i-1]->EvalInstance();
      
      int cat=0;
      for(int k =0;k<nCats;k++){
	if(catTTFs[k]->EvalInstance()){
	  cat=k;
	  break;
	}
      }
      Int_t binx = hists[i-1][cat]->GetXaxis()->FindFixBin(_x);
      Int_t biny = hists[i-1][cat]->GetYaxis()->FindFixBin(_y);
      Int_t binz = hists[i-1][cat]->GetZaxis()->FindFixBin(_z);
      
	
      weight = weight* hists[i-1][cat]->GetBinContent(binx,biny,binz);
   }
   br->Fill();
    
  }
  file->Write();
  return 0;
}


int ApplyJpsiKWeight(){
    
    std::vector<std::string> files;
    std::vector<std::string> trees;

    files.push_back("Somepath/DstMu.root");
    trees.push_back("DecayTree");
    files.push_back("Somepath/DstTau.root");
    trees.push_back("DecayTree");
    files.push_back("Somepath/DstD.root");
    trees.push_back("DecayTree");
    files.push_back("Somepath/Dstst.root");
    trees.push_back("DecayTree");
    files.push_back("Somepath/DststHigher.root");
    trees.push_back("DecayTree");
    files.push_back("Somepath/Bs_Dstst.root");
    trees.push_back("DecayTree");
    files.push_back("Somepath/DstDsTau.root");
    trees.push_back("DecayTree");
    files.push_back("Somepath/DststTau.root");
    trees.push_back("DecayTree");

    
    for(int i=0;i<files.size();i++){
        reweight(files[i],trees[i]);
    }
    return 0;
}

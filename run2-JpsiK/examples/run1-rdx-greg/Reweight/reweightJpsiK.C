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
#include "TArrayD.h"

TTree*data, *pdf;
TEventList *dataList,*pdfList;
TFile *file;
TString cutstring;
TString lastWeight;
TString dataWeightName;
int nWeightings;
std::vector<std::string> categories;

void weight3D( std::string,int, float, float, std::string,int, float, float, std::string,int, float, float);

int reweightJpsiK(){
   categories.push_back("Bplus_L0MuonDecision_TIS > 0.5");
   categories.push_back("Bplus_L0Global_TIS > 0.5 && Bplus_L0MuonDecision_TIS < 0.5");
   categories.push_back("Bplus_L0Global_TIS < 0.5 ");

 
  TFile *f1 = new TFile("JpsiKDataWeighted.root");
  data=(TTree*)f1->Get("DecayTree");
  TFile *f2 = new TFile("JpsiKSim09.root");
  pdf=(TTree*)f2->Get("DecayTree");
  TString outputfile = "JpsiKWeights.root";
  
  
  file = new TFile(outputfile,"recreate");  
  cutstring = "((muplus_PT > 500 && muminus_PT > 500 && K_PT > 500 &&  Bplus_DIRA_OWNPV > 0.9995 && Bplus_MINIPCHI2 < 12 && Bplus_ENDVERTEX_CHI2 < 18 && muplus_MINIPCHI2 > 4 && muminus_MINIPCHI2 > 4&& Jpsi_FDCHI2_OWNPV > 25 && Jpsi_MM > 3060 && Jpsi_MM < 3140 && (Bplus_Hlt2Topo2BodyBBDTDecision_TOS || Bplus_Hlt2Topo3BodyBBDTDecision_TOS) && Bplus_Hlt1TrackAllL0Decision_TOS > 0.5) && nSPDHits < 600 ) && (Bplus_L0Global_TIS > 0.5 || Bplus_L0DiMuonDecision_TOS > 0.5)";



  dataWeightName="sWeight";
  lastWeight="PIDweight_v1*TrackEff*(1.*(Bplus_L0Global_TIS > 0.5) + DimuonWeight_v2*(Bplus_L0Global_TIS<0.5))";
  
  
  nWeightings=0;
   
  dataList=new TEventList("dlist");
  pdfList=new TEventList("pdfList"); 
  data->Draw(">>dlist");
  pdf->Draw(">>pdfList");
//   /*
  data->SetAlias("Bplus_TRUEP_X","Bplus_PX");
  data->SetAlias("Bplus_TRUEP_Y","Bplus_PY");
  data->SetAlias("Bplus_TRUEP_Z","Bplus_PZ");
  data->SetAlias("Bplus_TRUEPT","Bplus_PT");
  
  
  pdf->SetAlias("Bplus_TRUEP_X","Bplus_PX");
  pdf->SetAlias("Bplus_TRUEP_Y","Bplus_PY");
  pdf->SetAlias("Bplus_TRUEP_Z","Bplus_PZ");
  pdf->SetAlias("Bplus_TRUEPT","Bplus_PT");

  
  
  weight3D("Bplus_OWNPV_X",1,-0.3,10.8,"Bplus_OWNPV_NDOF",20,1,200,"nTracks",20,0,450);
  weight3D("(1.0/2.0)*log((sqrt(Bplus_TRUEP_X^2 + Bplus_TRUEP_Y^2 + Bplus_TRUEP_Z^2)+Bplus_TRUEP_Z)/(sqrt(Bplus_TRUEP_X^2 + Bplus_TRUEP_Y^2 + Bplus_TRUEP_Z^2)-Bplus_TRUEP_Z)) ",9,2.,5.,"Bplus_TRUEPT",20,0,25e3,"nTracks",20,0,450);
 
  
  
  file->Write();
  return 0;
}


void weight3D(std::string var1name, int bins1, float min1, float max1, std::string var2name, int bins2, float min2, float max2, std::string var3name, int bins3, float min3, float max3){
  int nCategories = categories.size();
  TH3F *hMC[nCategories];
  for(int i =0;i<nCategories;i++){
    hMC[i]=new TH3F(TString::Format("hMC_%i",i),"",bins1,min1,max1,bins2,min2,max2,bins3,min3,max3);
    if(var2name=="SV_transverse_residual"){
//       TArrayD xbins = * hMC[i]->GetXaxis()->GetXbins();
//       TArrayD zbins = * hMC[i]->GetZaxis()->GetXbins();
//       Double_t *xbins = (Double_t*) hMC[i]->GetXaxis()->GetXbins()->GetArray();
//       std::cout << "xbins[0] " << xbins[0] << std::endl;
//       std::cout << "xbins[3] " << xbins[3] << std::endl;
//       TArrayD ybins = * hMC[i]->GetYaxis()->GetXbins();
//       std::cout << "xbins size " << xbins.GetSize() << " zbins " << zbins.GetSize() << std::endl;
      Double_t ybins[25] = {0.,0.005,0.01,0.015,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065,0.07,0.075,0.08,0.085,0.09,0.095,0.1,0.2,0.5,1.,2.};
      Double_t xbins[bins1+1];
      for(int i=0;i<bins1+1;i++){
	xbins[i]=min1 + (max1-min1) * (float)i / (float)bins1;
      }
      Double_t zbins[bins3+1];
      for(int i=0;i<bins3+1;i++){
	zbins[i]=min3 + (max3-min3) * (float)i / (float)bins3;
      }
//       hMC[i]=new TH3F(TString::Format("hMC_%i_2",i),"",bins1+1,xbins.GetArray(),24,ybins,bins3+1,zbins.GetArray());
//       hMC[i]=new TH3F(TString::Format("hMC_%i_2",i),"",24,ybins,24,ybins,24,ybins);
      hMC[i]=new TH3F(TString::Format("hMC_%i_2",i),"",bins1,xbins,24,ybins,bins3,zbins);
//       TFile *ftest = new TFile("test.root","recreate");
//       ftest->WriteTObject(hMC[i]);
//       TH1F test("test","",24,ybins);
//       test.Fill(0.05);
//       test.Fill(0.6);
//       ftest->WriteTObject(&test);
//       ftest->Write();
//       ftest->Close();
//       return;
    }
  }
  TString weightname = TString::Format("reweight_%i",nWeightings);
  TString nString = TString::Format("_%i",nWeightings);
    
//     TFile *ftmp = new TFile(FriendFiles[i]);
  TString friendname = "weights";
  if(nWeightings > 0.5)
    friendname= friendname+nString;
  std::cout << "getting friend tree " << friendname << std::endl;
  TTree *tmpfriend;
  if(nWeightings < 0.5)
    tmpfriend=pdf;
  else
  tmpfriend = (TTree*)file->Get(friendname);    
  TTreeFormula weightTTF("weightTTF",lastWeight,tmpfriend);
//     TTreeFormula OtherWeightTTF("OWeightTTF",OtherWeight,tmptree);
  TTreeFormula cutTTF("cutTTF",cutstring,pdf);
  TTreeFormula *catTTF[nCategories];
  for(int i =0;i<nCategories;i++){
    catTTF[i]=new TTreeFormula(TString::Format("catTTF_%i",i),(TString)categories[i],pdf);
  }
  TTreeFormula var1MC ("var1f",(TString)var1name,pdf);
  TTreeFormula var2MC ("var2f",(TString)var2name,pdf);
  TTreeFormula var3MC ("var3f",(TString)var3name,pdf);
  
//   for(int j=0;j<pdfList->GetN();j++){
//     pdf->GetEntry(pdfList->GetEntry(j));
  for(int j=0;j<pdf->GetEntries();j++){
//   for(int j=0;j<10e3;j++){
    pdf->GetEntry(j);
    tmpfriend->GetEntry(j);
    if(cutTTF.EvalInstance()){
      float _weight =weightTTF.EvalInstance();
      float _x = var1MC.EvalInstance();
      float _y = var2MC.EvalInstance();
      float _z = var3MC.EvalInstance();
      int cat=0;
      for(int k =0;k<nCategories;k++){
	if(catTTF[k]->EvalInstance()){
	  cat=k;
	  break;
	}
      }
      hMC[cat]->Fill(_x,_y,_z,_weight);
//       hMC.Fill(_x,_y,_z,1.);
    }
  }
  
  for(int i =0;i<nCategories;i++){
    std::cout << "category " << i << " " << hMC[i]->Integral() << std::endl;;
  }
//   weightTTF.Delete();
//   cutTTF.Delete();
//   var1MC.Delete();
//   var2MC.Delete();
//   var3MC.Delete();
//   delete tmpfriend;
//   ftmp2->Close();
//     ftmp->Close();
//     break;
//   file->ReOpen("read");
//   data = (TChain*) file->Get(category+ "_data");

  TH3F *hdata[nCategories];
  for(int i =0;i<nCategories;i++){
    hdata[i]=new TH3F(TString::Format("hdata_%i",i),"",bins1,min1,max1,bins2,min2,max2,bins3,min3,max3);
    
    if(var2name=="SV_transverse_residual"){
      Double_t ybins[25] = {0.,0.005,0.01,0.015,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065,0.07,0.075,0.08,0.085,0.09,0.095,0.1,0.2,0.5,1.,2.};
      Double_t xbins[bins1+1];
      for(int i=0;i<bins1+1;i++){
	xbins[i]=min1 + (max1-min1) * (float)i / (float)bins1;
      }
      Double_t zbins[bins3+1];
      for(int i=0;i<bins3+1;i++){
	zbins[i]=min3 + (max3-min3) * (float)i / (float)bins3;
      }
      hdata[i]=new TH3F(TString::Format("hdata_%i_2",i),"",bins1,xbins,24,ybins,bins3,zbins);
    }
  }
//   data->SetDirectory(0);
//   hdata.SetDirectory(0);
//   std::cout << "draw : " << data->Draw((TString)var3name+":"+var2name+":"+var1name+">>+hdata",cutstring) << std::endl;
//   dataTree->Draw((TString)var3name+":"+var2name+":"+var1name+">>+hdata",cutstring);
  
  TTreeFormula var1data ("var1d",(TString)var1name,data);
  TTreeFormula var2data ("var2d",(TString)var2name,data);
  TTreeFormula var3data ("var3d",(TString)var3name,data);
  TTreeFormula dataWeight ("dataWeight",(TString)dataWeightName,data);
  TTreeFormula cutTTFdata("cutTTFdata",cutstring,data);
  
  
  TTreeFormula *catTTFData[nCategories];
  for(int i =0;i<nCategories;i++){
    catTTFData[i]=new TTreeFormula(TString::Format("catTTF_%i",i),(TString)categories[i],data);
  }
  
  for(int i=0;i<dataList->GetN();i++){
//   for(int i=0;i<10e3;i++){
      data->GetEntry(dataList->GetEntry(i));
      if(cutTTFdata.EvalInstance()){
	float var1=var1data.EvalInstance();
	float var2=var2data.EvalInstance();
	float var3=var3data.EvalInstance();
	int cat=0;
	for(int i =0;i<nCategories;i++){
	  if(catTTFData[i]->EvalInstance()){
	    cat=i;
	    break;
	  }
	}
	hdata[cat]->Fill(var1,var2,var3,dataWeight.EvalInstance());    
      }
  }
  
  
  nWeightings++;
  
  weightname = TString::Format("reweight_%i",nWeightings);
  nString = TString::Format("_%i",nWeightings);
  
  TH3F *ratio[nCategories];
  for(int i =0;i<nCategories;i++){
    std::cout << "category " << i << " category string " << categories[i] << " MC integral " << hMC[i]->Integral() << " data integral " << hdata[i]->Integral() << std::endl;
    hdata[i]->SetDirectory(0);
    hMC[i]->SetDirectory(0);
    hdata[i]->Scale(1./hdata[i]->Integral());
    hMC[i]->Scale(1./hMC[i]->Integral());
    
    if(var2name=="SV_transverse_residual"){
      Double_t ybins[25] = {0.,0.005,0.01,0.015,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065,0.07,0.075,0.08,0.085,0.09,0.095,0.1,0.2,0.5,1.,2.};
      Double_t xbins[bins1+1];
      for(int i=0;i<bins1+1;i++){
	xbins[i]=min1 + (max1-min1) * (float)i / (float)bins1;
      }
      Double_t zbins[bins3+1];
      for(int i=0;i<bins3+1;i++){
	zbins[i]=min3 + (max3-min3) * (float)i / (float)bins3;
      }
      ratio[i]=new TH3F("weighting"+nString+"_category_"+TString::Format("%i",i),(TString)var3name+":"+var2name+":"+var1name+":"+categories[i],bins1,xbins,24,ybins,bins3,zbins);
    }
    else
     ratio[i]=new TH3F("weighting"+nString+"_category_"+TString::Format("%i",i),(TString)var3name+":"+var2name+":"+var1name+":"+categories[i],bins1,min1,max1,bins2,min2,max2,bins3,min3,max3);
     
    ratio[i]->Divide(hdata[i], hMC[i],1.,1.);
    std::cout << "ratio integral " << ratio[i]->Integral() << std::endl;
//     ratio[i]->SetName("weighting"+nString+"_category_"+TString::Format("%i",i));
//     ratio[i]->SetTitle((TString)var3name+":"+var2name+":"+var1name+":"+categories[i]);
    file->WriteTObject(ratio[i]);
  }
  
  file->ReOpen("update");
//   TTree *tmpfriend = (TTree*)file->Get(FriendNames[i]);
  TTree *newfriend = new TTree((TString)"weights"+nString,"");
//     FriendNames[i] = FriendNames[i]+nString;
//   std::cout << "new FriendName " << FriendNames[i]+nString << std::endl;
//     TTree *newfriend = new TTree(FriendNames[i]+nString,"");
  Double_t _weight;
//     newfriend->Branch(weightname,&_weight);
  TBranch *br = newfriend->Branch(weightname,&_weight);
  
  
  
 
  for(int j=0;j<pdf->GetEntries();j++){
//   for(int j=0;j<100;j++){
    pdf->GetEntry(j);
    tmpfriend->GetEntry(j);
//       if(cutTTF.EvalInstance()){
      _weight =weightTTF.EvalInstance();
      float _x = var1MC.EvalInstance();
      float _y = var2MC.EvalInstance();
      float _z = var3MC.EvalInstance();
      int cat=0;
      for(int k =0;k<nCategories;k++){
	if(catTTF[k]->EvalInstance()){
	  cat=k;
	  break;
	}
      }
      
      Int_t binx = ratio[cat]->GetXaxis()->FindFixBin(_x);
      Int_t biny = ratio[cat]->GetYaxis()->FindFixBin(_y);
      Int_t binz = ratio[cat]->GetZaxis()->FindFixBin(_z);
      
      _weight = _weight * ratio[cat]->GetBinContent(binx,biny,binz);
      newfriend->Fill();
//       std::cout << "branch filled " << std::endl;
//       }
  }

  weightTTF.Delete();
  cutTTF.Delete();
  var1MC.Delete();
  var2MC.Delete();
  var3MC.Delete();
  file->Write();
//   delete tmptree;
//     delete tmpfriend;
//   ftmp2->Close();
//     ftmp->Close();
//     break;

  lastWeight=weightname;
  
  
  return;
}

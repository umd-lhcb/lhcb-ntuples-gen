{
  
  TFile *f1 = new TFile("JpsiKDataWeighted.root");
  TTree *data=(TTree*)f1->Get("DecayTree");
  TFile *f2 = new TFile("JpsiKSim09.root");
  TTree *mc=(TTree*)f2->Get("DecayTree");
  TString MCweight="(PIDweight_v1*TrackEff*reweighting_JpsiK09Multi_v4*(abs(reweighting_JpsiK09Multi_v4)<10))";
  
  
  TString cutstringData = "(muplus_PT > 500 && muminus_PT > 500 && K_PT > 500 && Bplus_DIRA_OWNPV > 0.9995 && Bplus_MINIPCHI2 < 12 && Bplus_ENDVERTEX_CHI2 < 18 && muplus_MINIPCHI2 > 4 && muminus_MINIPCHI2 > 4&& Jpsi_FDCHI2_OWNPV > 25 && Jpsi_MM > 3060 && Jpsi_MM < 3140 && K_PIDK > 4 && muminus_PIDmu > 2 && muplus_PIDmu > 2&& (Bplus_Hlt2Topo2BodyBBDTDecision_TOS || Bplus_Hlt2Topo3BodyBBDTDecision_TOS) && Bplus_Hlt1TrackAllL0Decision_TOS > 0.5 && Bplus_L0HadronDecision_Dec > 0.5)";
  TString cutstringMC = "(muplus_PT > 500 && muminus_PT > 500 && K_PT > 500 &&  Bplus_DIRA_OWNPV > 0.9995 && Bplus_MINIPCHI2 < 12 && Bplus_ENDVERTEX_CHI2 < 18 && muplus_MINIPCHI2 > 4 && muminus_MINIPCHI2 > 4&& Jpsi_FDCHI2_OWNPV > 25 && Jpsi_MM > 3060 && Jpsi_MM < 3140 && (Bplus_Hlt2Topo2BodyBBDTDecision_TOS || Bplus_Hlt2Topo3BodyBBDTDecision_TOS) && Bplus_Hlt1TrackAllL0Decision_TOS > 0.5 && Bplus_L0HadronDecision_Dec > 0.5 )";
  
  
  
  TH1F allPT("allPT","",20,800,5000);
  allPT.Sumw2(true);
  TH1F TOSPT("TOSPT","",20,800,5000);
  TH1F allPTMC("allPTMC","",20,800,5000);
  TH1F TOSPTMC("TOSPTMC","",20,800,5000);
  data->Draw("sqrt(muplus_PT*muminus_PT)>>allPT",cutstringData+"&&muminus_L0MuonDecision_TOS > -0.5");
  data->Draw("sqrt(muplus_PT*muminus_PT)>>TOSPT",cutstringData+"&&Jpsi_L0DiMuonDecision_TOS > 0.5");
  TH1F dataEff = TOSPT / allPT;
  
  mc->Draw("sqrt(muplus_PT*muminus_PT)>>allPTMC","("+cutstringMC+"&&muminus_L0MuonDecision_TOS > -0.5"+")*"+MCweight);
  mc->Draw("sqrt(muplus_PT*muminus_PT)>>TOSPTMC","("+cutstringMC+"&&Jpsi_L0DiMuonDecision_TOS > 0.5"+")*"+MCweight);
  TH1F mcEff = TOSPTMC / allPTMC;
  dataEff.SetLineColor(kBlack);
  mcEff.SetLineColor(kRed);
  dataEff.Draw();
  mcEff.Draw("same");
  
  TH1F ratioH=dataEff/mcEff;
  ratioH.SetName("DimuonRatio");
  ratioH.Draw();
  allPT.DrawNormalized("same");
  TFile *fout = new TFile("DimuonCorrection.root","recreate");
  fout->WriteTObject(&ratioH);
  fout->Write();
  fout->Close();
  
}

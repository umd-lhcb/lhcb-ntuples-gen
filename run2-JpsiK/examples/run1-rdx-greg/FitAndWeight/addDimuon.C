{
  TFile *f1 = new TFile("DimuonCorrection.root");
  TH1F *ratioH = (TH1F*) f1->Get("DimuonRatio");
  
  TFile *f2 = new TFile("JpsiKDataWeighted.root","update");
  TTree *tree = (TTree*)f2->Get("DecayTree");
  
  TTreeFormula ptsq("ptsq","sqrt(muplus_PT*muminus_PT)",tree);
  Float_t weight;
  TBranch *br = tree->Branch("DimuonWeight",&weight);
  for(int i=0;i<tree->GetEntries();i++){
    tree->GetEntry(i);
    Float_t _pt = ptsq.EvalInstance();
    int binx = ratioH->GetXaxis()->FindFixBin(_pt);       
    weight=ratioH->GetBinContent(binx);
    if(weight<0.1)weigh=1.;
    br->Fill();
  }
  f2->Write();
  f2->Close();
  
}


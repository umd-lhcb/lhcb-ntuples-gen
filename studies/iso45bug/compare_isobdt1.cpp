using namespace std;

// naively expect VELO to be most iso on avg, then upstream, then long, so expect scores to go
// long > up > VELO
void compare_isobdt1() {
    gStyle->SetOptStat(0);
    TChain c("TupleB0/DecayTree", "c");
    c.Add("../../ntuples/glacier_links/0.9.12-all_years/2016/data/data-std-MagDown/*-dv.root");
    TH1D velo("velo","Least iso track BDT scores for diff. track types, D*#mu Data", 40, -2.1, 0.9);
    velo.SetLineColor(kRed);
    TH1D up("up","Least iso track BDT scores for diff. track types, D*#mu Data", 40, -2.1, 0.9);
    up.SetLineColor(kBlue);
    TH1D lng("lng","Least iso track BDT scores for diff. track types, D*#mu Data", 40, -2.1, 0.9);
    lng.SetLineColor(kBlack);
    c.Draw("b0_ISOLATION_BDT>>velo","b0_ISOLATION_Type==1");
    TString velo_descrip = "VELO: " + to_string(int(velo.GetEntries()));
    c.Draw("b0_ISOLATION_BDT>>up","b0_ISOLATION_Type==4");
    TString up_descrip = "Upstream: " + to_string(int(up.GetEntries()));
    c.Draw("b0_ISOLATION_BDT>>lng","b0_ISOLATION_Type==3");
    TString lng_descrip = "Long: " + to_string(int(lng.GetEntries()));
    TCanvas cv("cv","cv");
    TLegend l(0.1,0.7,0.3,0.9);
    l.SetHeader("Track Type: Events");
    l.AddEntry(&velo, velo_descrip);
    l.AddEntry(&up, up_descrip);
    l.AddEntry(&lng, lng_descrip);
    velo.DrawNormalized("histsame");
    up.DrawNormalized("histsame");
    lng.DrawNormalized("histsame");
    l.Draw();
    cv.SaveAs("compare_isobdt1.png");
}
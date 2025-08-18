# Copied (by Alex Fernez) with modifications to allow it to work for our tuples, from https://gitlab.cern.ch/lhcb-slb/B02DplusTauNu/-/blob/master/emulate_L0TIS/create_histos.py
# Minor differences from RD+: I apply tracking and kin/occ reweight to all MC (they just used JpsiK MC with kin/occ reweight as a secondary check) and stricter PID for JpsiK (for MC applied with weights for DLLK>4, DLLmu>2, cuts for isMuon),
# and for the portability check I compare JpsiK real TIS to D*(mu/tau)nu real TIS whereas they compared to D(mu/tau)nu. Notably too, their performance plots were only for 2015, and they only produced these TIS effs for 2015 and 2016, whereas I do performance plots and measurements for all of 2016-18.
# Our cuts (eg. on JpsiK mass) may be slightly different, but I've used the same trigger path ((L0 B Global TIS || L0 Muon TOS*) && HLT1 TrackMu TOS && HLT2 DiMuonHeavy TOS) and also required nspdhits<450
# * Muon TOS modified to only accept muons with pT above 2GeV, to account for poor trigger modeling in MC at low mu pT

# script should simply be run as: 
# python -u measure_and_validate_L0GlobalTIS.py 2>&1 | tee measure_and_validate_L0GlobalTIS.log
# (above will create a log file) I've hardcoded the input/output locations

import ROOT
import numpy as np
import os
import os.path as op
from math import log, sqrt
ROOT.gErrorIgnoreLevel = ROOT.kFatal ## Suppressing output
ROOT.gROOT.ProcessLine('.x ../../include/functor/rdp/RooIpatia2.cxx++') # very similiar to Hypatia... (identical, as far as I can tell)
# ROOT.gROOT.ProcessLine('.x ../../include/functor/rdp/lhcbStyle.C') # style is annoying me, so gonna skip this
# ROOT.gStyle.SetMarkerSize(0)
ROOT.gStyle.SetOptStat(0)

nbins_pz = 4
nbins_pt = 8
nbins_list = [nbins_pz,nbins_pt]

# SPD_cut = 450

fitplots_path = './fitplots'
os.system(f'mkdir -p {fitplots_path}')
perfplots_path = './perfplots'
os.system(f'mkdir -p {perfplots_path}')

years = []
# years.append("2015")
years.append("2016")
years.append("2017")
years.append("2018")


# Input files
f_Jpsi_data = [] # python always closes the files and makes the trees inside them unreadable if you don't keep the file objects active somehow
t_Jpsi_data = []
f_Jpsi_MC = []
t_Jpsi_MC = []
f_Jpsi_MC_untriggered = []
t_Jpsi_MC_untriggered = []
f_Dstmu_MC = [] # all D*lnu is untriggered; only use real TIS eff for portability check
t_Dstmu_MC = []
f_Dsttau_MC = []
t_Dsttau_MC = []
for year in years:
    for pol in ['mu', 'md']:
        f_Jpsi_data.append(ROOT.TFile(f'../../ntuples/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/JpsiK-data/step2/JpsiK--25_05_07--std--data--{year}--{pol}.root'))
        t_Jpsi_data.append(f_Jpsi_data[-1].Get("tree"))
        f_Jpsi_MC.append(ROOT.TFile(f'../../ntuples/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/JpsiK-mc/step2/JpsiK--25_05_11--mc--12143001--{year}--{pol}.root'))
        t_Jpsi_MC.append(f_Jpsi_MC[-1].Get("tree"))
        f_Jpsi_MC_untriggered.append(ROOT.TFile(f'../../ntuples/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/JpsiK-mc/step2-notrigger/JpsiK--25_05_12--mc--12143001--{year}--{pol}.root'))
        t_Jpsi_MC_untriggered.append(f_Jpsi_MC_untriggered[-1].Get("tree"))
        if not (year=='2016' and pol=='mu'):
            f_Dstmu_MC.append(ROOT.TFile(f'../../ntuples/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/Dstlnu-mc/step2-notrigger/Dst--25_05_13--mc--11574021--{year}--{pol}.root'))
            t_Dstmu_MC.append(f_Dstmu_MC[-1].Get("tree"))
            f_Dsttau_MC.append(ROOT.TFile(f'../../ntuples/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/Dstlnu-mc/step2-notrigger/Dst--25_05_13--mc--11574011--{year}--{pol}.root'))
            t_Dsttau_MC.append(f_Dsttau_MC[-1].Get("tree"))


# Get B log(pz), log(pT) binning scheme from (triggered) Jpsi MC
print('Computing binning schemes...')
Jpsi_MC_N_TOSTIS_list = []
for ivar in range(2): Jpsi_MC_N_TOSTIS_list.append([])
for ev in t_Jpsi_MC[0]:
    # if ev.nspdhits<SPD_cut: # should be redundant for step2 JpsiK data/MC
    Jpsi_MC_N_TOSTIS_list[0].append(log(ev.b_pz))
    Jpsi_MC_N_TOSTIS_list[1].append(log(ev.b_pt))
Jpsi_MC_N_TOSTIS_array = []
for ivar in range(2): Jpsi_MC_N_TOSTIS_array.append(np.array(Jpsi_MC_N_TOSTIS_list[ivar]))
binning_list = []
for ivar in range(2):
    binning_list.append([min(Jpsi_MC_N_TOSTIS_array[ivar])-2.])
    for ibin in range(nbins_list[ivar]-1): binning_list[ivar].append(np.percentile(Jpsi_MC_N_TOSTIS_array[ivar],100./nbins_list[ivar]*(1+ibin)))
    binning_list[ivar].append(max(Jpsi_MC_N_TOSTIS_array[ivar])+2.)
binning_array = []
for ivar in range(2): binning_array.append(np.array(binning_list[ivar],'d'))

# Lists of datasets
JpsiKmass = ROOT.RooRealVar("Bp_M","M(J/#psi K)",5150,5450,'MeV/c^{2}')
Jpsi_data_N_TOSTIS = []
Jpsi_data_N_TOSnoTIS = []
list_of_datasets = [Jpsi_data_N_TOSTIS,Jpsi_data_N_TOSnoTIS]
for ilist in range(len(list_of_datasets)):
    for iyear in range(len(years)):
        list_of_datasets[ilist].append([])
        for ipzbin in range(nbins_pz):
            list_of_datasets[ilist][iyear].append([])
            for iptbin in range(nbins_pt):
                list_of_datasets[ilist][iyear][ipzbin].append(ROOT.RooDataSet("d"+str(ilist)+str(iyear)+str(ipzbin)+str(iptbin),"d"+str(ilist)+str(iyear)+str(ipzbin)+str(iptbin),ROOT.RooArgSet(JpsiKmass)))


# Lists of yield histograms
Jpsi_MC_N_TOSTIS = []
Jpsi_MC_N_TOSnoTIS = []
Jpsi_MC_N_TIS = []
Jpsi_MC_N_noTIS = []
Dstmu_MC_N_TIS = []
Dstmu_MC_N_noTIS = []
Dsttau_MC_N_TIS = []
Dsttau_MC_N_noTIS = []
list_of_histos = [Jpsi_MC_N_TOSTIS, Jpsi_MC_N_TOSnoTIS, Jpsi_MC_N_TIS, Jpsi_MC_N_noTIS, Dstmu_MC_N_TIS, Dstmu_MC_N_noTIS, Dsttau_MC_N_TIS, Dsttau_MC_N_noTIS]
for ilist in range(len(list_of_histos)):
    for iyear in range(len(years)):
        list_of_histos[ilist].append(ROOT.TH2F("h"+str(ilist)+str(iyear),"",nbins_list[0],binning_array[0],nbins_list[1],binning_array[1]))
        list_of_histos[ilist][iyear].Sumw2()

# Filling of the histograms
for iyear in range(len(years)):
    print(f'\n-- Filling in {years[iyear]} datasets --\n')
    print('Filling JpsiK data...')
    for ev in t_Jpsi_data[iyear]:
        # if ev.nspdhits<SPD_cut:
        if ev.l0_mu_tos_pt:
            ipzbin = Jpsi_MC_N_TOSTIS[0].GetXaxis().FindBin(log(ev.b_pz))-1
            iptbin = Jpsi_MC_N_TOSTIS[0].GetYaxis().FindBin(log(ev.b_pt))-1
            JpsiKmass.setVal(ev.b_m)
            if ev.b_l0_global_tis: list_of_datasets[0][iyear][ipzbin][iptbin].add(ROOT.RooArgSet(JpsiKmass))
            else: list_of_datasets[1][iyear][ipzbin][iptbin].add(ROOT.RooArgSet(JpsiKmass))
    print('Filling JpsiK MC...') # note: can use reco momentum here, but need to use true momentum for D*lnu (to avoid RFA)
    for ev in t_Jpsi_MC[iyear]:
        # if ev.nspdhits<SPD_cut:
        if ev.l0_mu_tos_pt:
            if ev.b_l0_global_tis: list_of_histos[0][iyear].Fill(log(ev.b_pz),log(ev.b_pt),min(100.0,ev.w)) # w = wtrk * wpid_k (for DLLk>4) * wpid_mu (for DLLmu>2) * wpid_amu (for DLLamu>2) * mu_ismu * amu_ismu * wjk_occ * wjk_kin
            else: list_of_histos[1][iyear].Fill(log(ev.b_pz),log(ev.b_pt),min(100.0,ev.w))
    print('Filling untriggered JpsiK MC...')
    for ev in t_Jpsi_MC_untriggered[iyear]:
        # if ev.nspdhits<SPD_cut:
        if ev.b_l0_global_tis: list_of_histos[2][iyear].Fill(log(ev.b_pz),log(ev.b_pt),min(100.0,ev.w))
        else: list_of_histos[3][iyear].Fill(log(ev.b_pz),log(ev.b_pt),min(100.0,ev.w))
    print('Filling Dstmunu MC...') # note: store momenta in GeV in these tuples
    for ev in t_Dstmu_MC[iyear]:
        if ev.tis_measure_ok: # ev.nspdhits<450 and ev.b_true_pz>0 -- and ev.B0_BKGCAT==50? RD+ used this commented out cut, prob for makeshift truthmatching; I'll ignore (we do full truthmatching). no trigger path requirements here, looking for real TIS eff
            if ev.b_l0_global_tis: list_of_histos[4][iyear].Fill(log(ev.b_true_pz*1000),log(ev.b_true_pt*1000),min(100.0,ev.w_w_ubdt)) # missing wff (would need to reprocess 2016 step1), but shouldn't matter much
            else: list_of_histos[5][iyear].Fill(log(ev.b_true_pz*1000),log(ev.b_true_pt*1000),min(100.0,ev.w_w_ubdt)) # w_w_ubdt = wpid_mu_ubdt (for DLLmu > 2.0 & DLLe < 1.0 & IsMuon == 1.0 & UBDT > 0.25) * wpid_k (for DLLK > 4.0 & IsMuon == 0.0) * wpid_pi (DLLK < 2.0 & IsMuon == 0.0) * wtrk * wjk
    print('Filling Dsttaunu MC...')
    for ev in t_Dsttau_MC[iyear]:
        if ev.tis_measure_ok: # and ev.B0_BKGCAT==50
            if ev.b_l0_global_tis: list_of_histos[6][iyear].Fill(log(ev.b_true_pz*1000),log(ev.b_true_pt*1000),min(100.0,ev.w_w_ubdt))
            else: list_of_histos[7][iyear].Fill(log(ev.b_true_pz*1000),log(ev.b_true_pt*1000),min(100.0,ev.w_w_ubdt))


# Lists of efficiency histograms
Jpsi_data_eff = []
Jpsi_MC_eff = []
Jpsi_MC_true_eff = []
Dstmu_MC_true_eff = []
Jpsi_data_eff_lin = []
Jpsi_MC_eff_lin = []
Jpsi_MC_true_eff_lin = []
Dstmu_MC_true_eff_lin = []
Dsttau_MC_true_eff = []
Dsttau_MC_true_eff_lin = []

for iyear in range(len(years)):
    Jpsi_data_eff.append(ROOT.TH2F("Jpsi_data_eff"+str(iyear),"J/#psiK Data log(pz) vs log(pT)",nbins_list[0],binning_array[0],nbins_list[1],binning_array[1]))
    Jpsi_MC_eff.append(ROOT.TH2F("Jpsi_MC_eff"+str(iyear),"J/#psiK MC log(pz) vs log(pT)",nbins_list[0],binning_array[0],nbins_list[1],binning_array[1]))
    Jpsi_MC_true_eff.append(ROOT.TH2F("Jpsi_MC_true_eff"+str(iyear),"J/#psiK Untriggered MC log(pz) vs log(pT)",nbins_list[0],binning_array[0],nbins_list[1],binning_array[1]))
    Dstmu_MC_true_eff.append(ROOT.TH2F("Dstmu_MC_true_eff"+str(iyear),"D*#mu#nu Untriggered MC log(pz) vs log(pT)",nbins_list[0],binning_array[0],nbins_list[1],binning_array[1]))
    Dsttau_MC_true_eff.append(ROOT.TH2F("Dsttau_MC_true_eff"+str(iyear),"D*#tau#nu Untriggered MC log(pz) vs log(pT)",nbins_list[0],binning_array[0],nbins_list[1],binning_array[1]))
    Jpsi_data_eff_lin.append(ROOT.TH1F("Jpsi_data_eff"+str(iyear)+"_lin","J/#psiK Data Combined Bins",nbins_pz*nbins_pt,0,nbins_pz*nbins_pt))
    Jpsi_MC_eff_lin.append(ROOT.TH1F("Jpsi_MC_eff"+str(iyear)+"_lin","J/#psiK MC log(pz) vs log(pT)",nbins_pz*nbins_pt,0,nbins_pz*nbins_pt))
    Jpsi_MC_true_eff_lin.append(ROOT.TH1F("Jpsi_MC_true_eff"+str(iyear)+"_lin","J/#psiK Untriggered MC Combined Bins",nbins_pz*nbins_pt,0,nbins_pz*nbins_pt))
    Dstmu_MC_true_eff_lin.append(ROOT.TH1F("Dstmu_MC_true_eff"+str(iyear)+"_lin","D*#mu#nu Untriggered MC Combined Bins",nbins_pz*nbins_pt,0,nbins_pz*nbins_pt))
    Dsttau_MC_true_eff_lin.append(ROOT.TH1F("Dsttau_MC_true_eff"+str(iyear)+"_lin","D*#tau#nu Untriggered MC Combined Bins",nbins_pz*nbins_pt,0,nbins_pz*nbins_pt))


# Invariant mass model
Bp_mass = ROOT.RooRealVar("Bp_mass","#mu_{B^{+}}",5279.32,5278.0,5280.64)
Bp_width = ROOT.RooRealVar("Bp_width","#sigma_{B^{+}}",10,4,18)
Bp_lambda = ROOT.RooRealVar("Bp_lambda","lambda",-3.3,-6,-1)
Bp_zeta = ROOT.RooRealVar("zeta","zeta",1e-10)
Bp_beta = ROOT.RooRealVar("beta","beta",1e-10)
Bp_a1 = ROOT.RooRealVar("Bp_a1","a1",2.0,0,5)
Bp_n1 = ROOT.RooRealVar("Bp_n1","n1",3.4,0,15)
Bp_a2 = ROOT.RooRealVar("Bp_a2","a2",2.2,0,5)
Bp_n2 = ROOT.RooRealVar("Bp_n2","n2",3.5,0,20)

# for var in [Bp_lambda,Bp_a1,Bp_n1,Bp_a2,Bp_n2]: var.setConstant() # these are the params that vary the most... uncomment this if you want to fix them

def set_constant_param_vals_tostis(iyear): # set best guesses (averaged from a semi-successful set of fits) for params that vary the most (and potentially set to be "constant")- separate tostis from tosnotis too
    if years[iyear]=='2016':
        Bp_lambda.setVal(-3.260716275862069)
        Bp_a1.setVal(2.0936025379310346)
        Bp_n1.setVal(3.2627817410255173)
        Bp_a2.setVal(2.3535740413793103)
        Bp_n2.setVal(3.1700217836626208)
    elif years[iyear]=='2017':
        Bp_lambda.setVal(-3.286724429530201)
        Bp_a1.setVal(1.9615280402684563)
        Bp_n1.setVal(3.513258043624161)
        Bp_a2.setVal(2.0823326174496644)
        Bp_n2.setVal(3.2216234389261746)
    elif years[iyear]=='2018':
        Bp_lambda.setVal(-3.4439811034482757)
        Bp_a1.setVal(2.0249021379310346)
        Bp_n1.setVal(3.429166126245517)
        Bp_a2.setVal(2.194366903448276)
        Bp_n2.setVal(3.589092989076386)
    else: return

def set_constant_param_vals_tosnotis(iyear):
    if years[iyear]=='2016':
        Bp_lambda.setVal(-3.194743287671233)
        Bp_a1.setVal(2.1391474657534246)
        Bp_n1.setVal(3.316903508330137)
        Bp_a2.setVal(2.4136346575342467)
        Bp_n2.setVal(3.267227214448904)
    elif years[iyear]=='2017':
        Bp_lambda.setVal(-3.1885289864864865)
        Bp_a1.setVal(2.078512)
        Bp_n1.setVal(3.7031106162162164)
        Bp_a2.setVal(2.2064143243243244)
        Bp_n2.setVal(3.5622785668918917)
    elif years[iyear]=='2018':
        Bp_lambda.setVal(-3.454392191780822)
        Bp_a1.setVal(2.096195410958904)
        Bp_n1.setVal(3.567812294128767)
        Bp_a2.setVal(2.231838904109589)
        Bp_n2.setVal(3.693241242931767)
    else: return

Bp_pdf = ROOT.RooIpatia2("Bp_pdf","Bp_pdf",JpsiKmass,Bp_lambda,Bp_zeta,Bp_beta,Bp_width,Bp_mass,Bp_a1,Bp_n1,Bp_a2,Bp_n2)
Bp_yield = ROOT.RooRealVar("Bp_yield","N_{B^{+}}",2e+05,0.,1e+07)

bkg_coef = ROOT.RooRealVar("bkg_coef","c_{bkg}",0,-0.1,0.1)
bkg_pdf = ROOT.RooExponential("bkg_pdf","bkg_pdf",JpsiKmass,bkg_coef)
bkg_yield = ROOT.RooRealVar("bkg_yield","N_{bkg}",8e+04,0.,1.e+06)
# bkg_lin = ROOT.RooRealVar("bkg_lin","lin",0.0,-0.1,0.1) # try different bkg model
# bkg_pdf = ROOT.RooPolynomial("bkg_pdf","bkg_pdf",JpsiKmass,ROOT.RooArgList(bkg_lin))

model = ROOT.RooAddPdf("model","model",ROOT.RooArgList(Bp_pdf,bkg_pdf),ROOT.RooArgList(Bp_yield,bkg_yield))


# Per-bin fits to data
def stat_syst(a,sa,b,sb):
    return 1./(a+b)**2*sqrt(b**2*sa**2+a**2*sb**2)

def evaluate_bin(xbin_,ybin_,hTIS_,hnoTIS_,heff_):
    NTIS_ = hTIS_.GetBinContent(xbin_,ybin_)
    NnoTIS_ = hnoTIS_.GetBinContent(xbin_,ybin_)
    NTIS_err_ = hTIS_.GetBinError(xbin_,ybin_)
    NnoTIS_err_ = hnoTIS_.GetBinError(xbin_,ybin_)
    val_ = NTIS_/(NTIS_+NnoTIS_)
    err_ = stat_syst(NTIS_,NTIS_err_,NnoTIS_,NnoTIS_err_)
    heff_.SetBinContent(xbin_,ybin_,val_)
    heff_.SetBinError(xbin_,ybin_,err_)

# fitresults = ROOT.TFile("../gen/measure_L0GlobalTIS_JpsiData_Bp_fitresults.root", "recreate")
for iyear in range(len(years)):
    print(f'Working on {years[iyear]} fits:')
    for ipzbin in range(nbins_pz):
        for iptbin in range(nbins_pt):
            print(f'\n\n  Fitting {years[iyear]} JpsiK TISTOS data Bp mass for bin {ipzbin},{iptbin}\n\n')
            set_constant_param_vals_tostis(iyear)
            tostis_res = model.fitTo(list_of_datasets[0][iyear][ipzbin][iptbin],ROOT.RooFit.NumCPU(8),ROOT.RooFit.Save(True))
            # tostis_res.Write(f'Bp_fit_tostis_JpsiData{years[iyear]}_pz{ipzbin}_pt{iptbin}')
            tostis_frame = JpsiKmass.frame(ROOT.RooFit.Title('TOSTIS B^{+} #rightarrow J/#psiK data, B^{+} mass fit for B_logpz bin ' + f'{ipzbin}' + ' B_logpt bin ' + f'{iptbin}'))
            list_of_datasets[0][iyear][ipzbin][iptbin].plotOn(tostis_frame, ROOT.RooFit.LineColor(ROOT.kBlack), ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
            model.plotOn(tostis_frame, ROOT.RooFit.LineColor(ROOT.kBlue))
            # model.plotOn(tostis_frame, ROOT.RooFit.LineColor(ROOT.kRed), ROOT.RooFit.Components(ROOT.RooArgSet(Bp_pdf))) # broken for some reason... whatever
            # model.plotOn(tostis_frame, ROOT.RooFit.LineColor(ROOT.kViolet), ROOT.RooFit.Components(ROOT.RooArgSet(bkg_pdf)))
            ctostis = ROOT.TCanvas("ctostis", "ctostis")
            tostis_frame.Draw()
            ctostis.SaveAs(f'{fitplots_path}/tostis_bpmassfit{years[iyear]}_jpsikdata_logpz{ipzbin}_logpt{iptbin}.png')
            S_TOSTIS = Bp_yield.getVal()
            SE_TOSTIS = Bp_yield.getError()

            print(f'\n\n  Fitting {years[iyear]} JpsiK TOSnoTIS data Bp mass for bin {ipzbin},{iptbin}\n\n')
            set_constant_param_vals_tosnotis(iyear)
            tosnotis_res = model.fitTo(list_of_datasets[1][iyear][ipzbin][iptbin],ROOT.RooFit.NumCPU(8))
            # tosnotis_res.Write(f'Bp_fit_tosnotis_JpsiData{years[iyear]}_pz{ipzbin}_pt{iptbin}')
            tosnotis_frame = JpsiKmass.frame(ROOT.RooFit.Title('TOSnoTIS B^{+} #rightarrow J/#psiK data, B^{+} mass fit for B_logpz bin ' + f'{ipzbin}' + ' B_logpt bin ' + f'{iptbin}'))
            list_of_datasets[0][iyear][ipzbin][iptbin].plotOn(tosnotis_frame, ROOT.RooFit.LineColor(ROOT.kBlack), ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
            model.plotOn(tosnotis_frame, ROOT.RooFit.LineColor(ROOT.kBlue))
            # model.plotOn(tosnotis_frame, ROOT.RooFit.LineColor(ROOT.kRed), ROOT.RooFit.Components(ROOT.RooArgSet(Bp_pdf)))
            # model.plotOn(tosnotis_frame, ROOT.RooFit.LineColor(ROOT.kViolet), ROOT.RooFit.Components(ROOT.RooArgSet(bkg_pdf)))
            ctosnotis = ROOT.TCanvas("ctosnotis", "ctosnotis")
            tosnotis_frame.Draw()
            ctosnotis.SaveAs(f'{fitplots_path}/tosnotis_bpmassfit{years[iyear]}_jpsikdata_logpz{ipzbin}_logpt{iptbin}.png')
            S_TOSnoTIS = Bp_yield.getVal()
            SE_TOSnoTIS = Bp_yield.getError()
            
            # print(f'  evaluating JpsiK data TOSTIS/TOS')
            eff_val = S_TOSTIS/(S_TOSTIS+S_TOSnoTIS)
            eff_err = stat_syst(S_TOSTIS,SE_TOSTIS,S_TOSnoTIS,SE_TOSnoTIS)
            Jpsi_data_eff[iyear].SetBinContent(ipzbin+1,iptbin+1,eff_val)
            Jpsi_data_eff[iyear].SetBinError(ipzbin+1,iptbin+1,eff_err)
            # print(f'  evaluating JpsiK MC TOSTIS/TOS')
            evaluate_bin(ipzbin+1,iptbin+1,Jpsi_MC_N_TOSTIS[iyear],Jpsi_MC_N_TOSnoTIS[iyear],Jpsi_MC_eff[iyear])
            # print(f'  evaluating JpsiK MC TIS/all')
            evaluate_bin(ipzbin+1,iptbin+1,Jpsi_MC_N_TIS[iyear],Jpsi_MC_N_noTIS[iyear],Jpsi_MC_true_eff[iyear])
# fitresults.Close()
print()
for iyear in range(len(years)):
    for ipzbin in range(nbins_pz):
        for iptbin in range(nbins_pt):
            # print(f'Evaluating {years[iyear]} Dst(mu/tau)nu TIS/all for bin {ipzbin},{iptbin}')
            evaluate_bin(ipzbin+1,iptbin+1,Dstmu_MC_N_TIS[iyear],Dstmu_MC_N_noTIS[iyear],Dstmu_MC_true_eff[iyear])
            evaluate_bin(ipzbin+1,iptbin+1,Dsttau_MC_N_TIS[iyear],Dsttau_MC_N_noTIS[iyear],Dsttau_MC_true_eff[iyear])


# Creation of 1-D histograms, used to check the performances
for iyear in range(len(years)):
    for ipzbin in range(nbins_pz):
        for iptbin in range(nbins_pt):
            iglobalbin = ipzbin*nbins_pt+iptbin+1
            Jpsi_data_eff_lin[iyear].SetBinContent(iglobalbin,Jpsi_data_eff[iyear].GetBinContent(ipzbin+1,iptbin+1))
            Jpsi_MC_eff_lin[iyear].SetBinContent(iglobalbin,Jpsi_MC_eff[iyear].GetBinContent(ipzbin+1,iptbin+1))
            Jpsi_MC_true_eff_lin[iyear].SetBinContent(iglobalbin,Jpsi_MC_true_eff[iyear].GetBinContent(ipzbin+1,iptbin+1))
            Jpsi_data_eff_lin[iyear].SetBinError(iglobalbin,Jpsi_data_eff[iyear].GetBinError(ipzbin+1,iptbin+1))
            Jpsi_MC_eff_lin[iyear].SetBinError(iglobalbin,Jpsi_MC_eff[iyear].GetBinError(ipzbin+1,iptbin+1))
            Jpsi_MC_true_eff_lin[iyear].SetBinError(iglobalbin,Jpsi_MC_true_eff[iyear].GetBinError(ipzbin+1,iptbin+1))
            Dstmu_MC_true_eff_lin[iyear].SetBinContent(iglobalbin,Dstmu_MC_true_eff[iyear].GetBinContent(ipzbin+1,iptbin+1))
            Dsttau_MC_true_eff_lin[iyear].SetBinContent(iglobalbin,Dsttau_MC_true_eff[iyear].GetBinContent(ipzbin+1,iptbin+1))
            Dstmu_MC_true_eff_lin[iyear].SetBinError(iglobalbin,Dstmu_MC_true_eff[iyear].GetBinError(ipzbin+1,iptbin+1))
            Dsttau_MC_true_eff_lin[iyear].SetBinError(iglobalbin,Dsttau_MC_true_eff[iyear].GetBinError(ipzbin+1,iptbin+1))

for iyear in range(len(years)):
    Jpsi_data_eff[iyear].SetLineColor(ROOT.kRed)
    Jpsi_MC_eff[iyear].SetLineColor(ROOT.kGreen+3)
    Jpsi_MC_true_eff[iyear].SetLineColor(ROOT.kBlack)
    Dstmu_MC_true_eff[iyear].SetLineColor(ROOT.kBlue)
    Dsttau_MC_true_eff[iyear].SetLineColor(ROOT.kOrange+2)
    Jpsi_data_eff_lin[iyear].SetLineColor(ROOT.kRed)
    Jpsi_MC_eff_lin[iyear].SetLineColor(ROOT.kGreen+3)
    Jpsi_MC_true_eff_lin[iyear].SetLineColor(ROOT.kBlack)
    Dstmu_MC_true_eff_lin[iyear].SetLineColor(ROOT.kBlue)
    Dsttau_MC_true_eff_lin[iyear].SetLineColor(ROOT.kOrange+2)
    for h_ in [Jpsi_data_eff[iyear],Jpsi_MC_eff[iyear],Jpsi_MC_true_eff[iyear],Dstmu_MC_true_eff[iyear],Dsttau_MC_true_eff[iyear]]:
        h_.GetXaxis().SetTitle("log(PZ)")
        h_.GetYaxis().SetTitle("log(PT)")
        # h_.SetMarkerSize(0)
    for h_ in [Jpsi_data_eff_lin[iyear],Jpsi_MC_eff_lin[iyear],Jpsi_MC_true_eff_lin[iyear],Dstmu_MC_true_eff_lin[iyear],Dsttau_MC_true_eff_lin[iyear]]:
        h_.GetXaxis().SetTitle("Bin number")
        h_.GetYaxis().SetTitle("Efficiency")
        # h_.SetMarkerSize(0)


# plot legend in upper left (effs should all rise as func of B pz, pT). histos is map from histo name -> TH1 object
def plot(histos, title, outpng):
    print(f'Plotting Performance Plot: {title}')
    c = ROOT.TCanvas("c","c")

    high, low = None, None
    for hn in histos:
        h = histos[hn]
        hmax = h.GetBinContent(h.GetMaximumBin())
        hmin = h.GetBinContent(h.GetMinimumBin())
        if high==None or hmax>high: high = hmax
        if low==None or hmin<low: low = hmin
    rng = high-low
    high = high + 0.1*rng
    low = low - 0.1*rng
    print(f'   ((low,high)=({low},{high}))')
    leg = ROOT.TLegend(0.1, 0.79, 0.4, 0.92)
    for hn in histos:
        h = histos[hn]
        h.SetMaximum(high)
        h.SetMinimum(low)
        h.SetTitle(title)
        leg.AddEntry(h, hn, "l")
        h.Draw("e1same")
    leg.Draw()

    # c.Print(f"../gen/Performance_plots_{years[iyear]}.root")
    c.Print(f"{perfplots_path}/{outpng}")


for iyear in range(len(years)):
    plot({f'JpsiK Data{years[iyear]} (TISTOS)': Jpsi_data_eff_lin[iyear], f'JpsiK MC{years[iyear]} (TISTOS)': Jpsi_MC_eff_lin[iyear]}, f'{years[iyear]} JpsiK Data vs MC Eff Check', f'{years[iyear]}_JpsiK_Data-MC_eff.png')
    plot({f'JpsiK MC{years[iyear]} (TISTOS)': Jpsi_MC_eff_lin[iyear], f'JpsiK MC{years[iyear]} (real TIS)': Jpsi_MC_true_eff_lin[iyear]}, f'{years[iyear]} JpsiK MC: TISTOS Method Eff Check', f'{years[iyear]}_JpsiKMC_TISTOS-TIS_eff.png')
    plot({f'JpsiK MC{years[iyear]} (real TIS)': Jpsi_MC_true_eff_lin[iyear], f'DstMuNu MC{years[iyear]} (real TIS)': Dstmu_MC_true_eff_lin[iyear], f'DstTauNu MC{years[iyear]} (real TIS)': Dsttau_MC_true_eff_lin[iyear]}, f'{years[iyear]} TIS Portability Eff Check', f'{years[iyear]}_JpsiKMC-DstlnuMC_eff.png')
    Jpsi_data_eff_pz = Jpsi_data_eff[iyear].ProjectionX()
    Jpsi_MC_eff_pz = Jpsi_MC_eff[iyear].ProjectionX()
    plot({f'JpsiK Data{years[iyear]} (TISTOS)': Jpsi_data_eff_pz, f'JpsiK MC{years[iyear]} (TISTOS)': Jpsi_MC_eff_pz}, f'{years[iyear]} JpsiK Data vs MC Eff (proj->log(PZ)) Check', f'{years[iyear]}_JpsiK_Data-MC_pz.png')
    Jpsi_MC_eff_pz = Jpsi_MC_eff[iyear].ProjectionX()
    Jpsi_MC_true_eff_pz = Jpsi_MC_true_eff[iyear].ProjectionX()
    plot({f'JpsiK MC{years[iyear]} (TISTOS)': Jpsi_MC_eff_pz, f'JpsiK MC{years[iyear]} (real TIS)': Jpsi_MC_true_eff_pz}, f'{years[iyear]} JpsiK MC: TISTOS Method Eff (proj->log(PZ)) Check', f'{years[iyear]}_JpsiKMC_TISTOS-TIS_pz.png')
    Dstmu_MC_true_eff_pz = Dstmu_MC_true_eff[iyear].ProjectionX()
    Dsttau_MC_true_eff_pz = Dsttau_MC_true_eff[iyear].ProjectionX()
    Jpsi_MC_true_eff_pz = Jpsi_MC_true_eff[iyear].ProjectionX()
    plot({f'JpsiK MC{years[iyear]} (real TIS)': Jpsi_MC_true_eff_pz, f'DstMuNu MC{years[iyear]} (real TIS)': Dstmu_MC_true_eff_pz, f'DstTauNu MC{years[iyear]} (real TIS)': Dsttau_MC_true_eff_pz}, f'{years[iyear]} TIS Portability Eff (proj->log(PZ)) Check', f'{years[iyear]}_JpsiKMC-DstlnuMC_pz.png')
    Jpsi_data_eff_pt = Jpsi_data_eff[iyear].ProjectionY()
    Jpsi_MC_eff_pt = Jpsi_MC_eff[iyear].ProjectionY()
    plot({f'JpsiK Data{years[iyear]} (TISTOS)': Jpsi_data_eff_pt, f'JpsiK MC{years[iyear]} (TISTOS)': Jpsi_MC_eff_pt}, f'{years[iyear]} JpsiK Data vs MC Eff (proj->log(PT)) Check', f'{years[iyear]}_JpsiK_Data-MC_pt.png')
    Jpsi_MC_eff_pt = Jpsi_MC_eff[iyear].ProjectionY()
    Jpsi_MC_true_eff_pt = Jpsi_MC_true_eff[iyear].ProjectionY()
    plot({f'JpsiK MC{years[iyear]} (TISTOS)': Jpsi_MC_eff_pt, f'JpsiK MC{years[iyear]} (real TIS)': Jpsi_MC_true_eff_pt}, f'{years[iyear]} JpsiK MC: TISTOS Method Eff (proj->log(PT)) Check', f'{years[iyear]}_JpsiKMC_TISTOS-TIS_pt.png')
    Dstmu_MC_true_eff_pt = Dstmu_MC_true_eff[iyear].ProjectionY()
    Dsttau_MC_true_eff_pt = Dsttau_MC_true_eff[iyear].ProjectionY()
    Jpsi_MC_true_eff_pt = Jpsi_MC_true_eff[iyear].ProjectionY()
    plot({f'JpsiK MC{years[iyear]} (real TIS)': Jpsi_MC_true_eff_pt, f'DstMuNu MC{years[iyear]} (real TIS)': Dstmu_MC_true_eff_pt, f'DstTauNu MC{years[iyear]} (real TIS)': Dsttau_MC_true_eff_pt}, f'{years[iyear]} TIS Portability Eff (proj->log(PT)) Check', f'{years[iyear]}_JpsiKMC-DstlnuMC_pt.png')

foutput = ROOT.TFile("L0TIS_efficiency_2D.root","recreate")
eff_histos = []
for iyear in range(len(years)):
    eff_histos.append(Jpsi_data_eff[iyear].Clone())
    eff_histos[iyear].Write()
foutput.Close()

print(f'\nNote: binning used everywhere is (log(Bpz), log(Bpt)): {binning_array}')
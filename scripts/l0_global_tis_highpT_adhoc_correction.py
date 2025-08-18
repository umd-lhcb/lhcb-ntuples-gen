# B L0 Global TIS, measured in JpsiK data, doesn't accurately reflect the trigger eff pdf as a function of B (true, for rdx) log(pT), especially at high
# pT. The idea here is: leave measured trigger weights for all but the highest log(pT) reweighting bins alone, but for this highest bin, add an additional
# correction weight that captures the high pT rdx trigger eff dependence
# Algorithm looks like:
#  - Find the mean of log(pT) in this bin (for a given log(pz) bin i) for step1 (untriggered) D*munu fullsim MC, call this mean m_i and the correpsonding efficiency of the bin (from JpsiK data measurement) e_i
#    - note: the trigger eff weights are found in (non-uniform) bins of B log(pz) (4 bins) x log(pT) (8 bins)
#  - For each year, take (all, polarities combined) the D*munu step1 fullsim MC and create 4 (1 for each log(pz) bin) histograms (say, 20 bins) of the trigger eff in this highest log(pT) bin
#  - Fit linear functions f_i(log(pT))=a_i(log(pT)-m_i)+e_i to these histograms
#  - The fit slope coefficient a_i along with (m_i,e_i) will determine the additional ad-hoc weight for this log(pz) bin i, highest log(pT) bin: w_i=f_i(log(pT))/e_i (to be applied in the L0 Global TIS emulation procedure)

# hard-coded everything: just run as python l0_global_tis_highpT_adhoc_correction.py

# Author: Alex Fernez

import ROOT
from glob import glob

ROOT.gErrorIgnoreLevel = ROOT.kFatal
ROOT.gStyle.SetOptStat(0)

nbins = 20

yr_idxs = {2016: 0, 2017: 1, 2018: 2}
adhoc_rwgt = {yr: {} for yr in yr_idxs} # fill with pzbin -> [m_i, e_i, a_i]
# pjkstep2 = '../ntuples/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/JpsiK-data/step2'
# pjks = {2016: [f'{pjkstep2}/JpsiK--25_05_07--std--data--2016--md.root', f'{pjkstep2}/JpsiK--25_05_07--std--data--2016--mu.root'],
#         2017: [f'{pjkstep2}/JpsiK--25_05_07--std--data--2017--md.root', f'{pjkstep2}/JpsiK--25_05_07--std--data--2017--mu.root'],
#         2018: [f'{pjkstep2}/JpsiK--25_05_07--std--data--2018--md.root', f'{pjkstep2}/JpsiK--25_05_07--std--data--2018--mu.root']}
# cjks = {yr: ROOT.TChain('tree', f'JpsiKData{yr}') for yr in pjks}
# for yr,paths in pjks.items():
#     for pjk in paths: cjks[yr].Add(pjk) # JpsiK step2 data should already have cuts applied (eg. nspdhits<450, l0 = l0_mu_tos_pt || b_l0_global_tis)
# pdststep2 = '../ntuples/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/Dstlnu-mc/step2-notrigger'
# pdsts = {2016: [f'{pdststep2}/Dst--25_05_13--mc--11574021--2016--md.root', f'{pdststep2}/Dst--25_05_13--mc--11574021--2016--mu.root'],
#          2017: [f'{pdststep2}/Dst--25_05_13--mc--11574021--2017--md.root', f'{pdststep2}/Dst--25_05_13--mc--11574021--2017--mu.root'],
#          2018: [f'{pdststep2}/Dst--25_05_13--mc--11574021--2018--md.root', f'{pdststep2}/Dst--25_05_13--mc--11574021--2018--mu.root']}
# wdst = '1' # 'TMath::Min(w_w_ubdt, 10.0)' # don't bother with FFs (would have to reprocess 2016), but try other MC weights (PID, trk, kin/occ)
pdsts = {2016: ['../ntuples/glacier_links/0.9.4-trigger_emulation/Dst_D0-mc/Dst_D0--21_04_21--mc--MC_2016_Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8_Sim09j_Trig0x6139160F_Reco16_Turbo03a_Filtered_11574021_D0TAUNU.SAFESTRIPTRIG.DST.root'],
         2017: glob('../ntuples/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/Dstlnu-mc/2017/norm_DstMu/*/*-dv.root'),
         2018: glob('../ntuples/0.9.13-JpsiK_and_Dstlnu_fullsim_for_L0emu_initrwgt/Dstlnu-mc/2018/norm_DstMu/*/*-dv.root')}
cdsts = {yr: ROOT.TChain('TupleB0/DecayTree', f'DstmunuMCnotrig{yr}') for yr in pdsts}
for yr,paths in pdsts.items():
    for pdst in paths: cdsts[yr].Add(pdst)
pwtrig = ROOT.TFile('../run2-JpsiK/measure_tis/L0TIS_efficiency_2D.root')
wtrigs = {yr: pwtrig.Get(f'Jpsi_data_eff{yr_idxs[yr]}') for yr in yr_idxs} # yr -> TH2

## helper (from ChatGPT!)
def extract_th2_bins(th2):
    x_axis = th2.GetXaxis()
    y_axis = th2.GetYaxis()
    x_bins_low = []
    for i in range(1, x_axis.GetNbins()+2): x_bins_low.append(x_axis.GetBinLowEdge(i))
    y_bins_low = []
    for i in range(1, y_axis.GetNbins()+2): y_bins_low.append(y_axis.GetBinLowEdge(i))
    return x_bins_low, y_bins_low

# get the JpsiK data high log(pT) bin means
# wtrig_binnings = {yr: extract_th2_bins(wtrig) for yr,wtrig in wtrigs.items()} # log(pz) x log(pT)
# # print(wtrig_binnings)
# jpsi_highlogpT_means = {yr: {} for yr in yr_idxs}
# for yr,cjk in cjks.items():
#     for pzidx in range(len(wtrig_binnings[yr][0])-1):
#         hall = ROOT.TH1D(f'highlogpT_{yr}_{pzidx}', f'J#psi K {yr} Data B log(p_{{T}}): high log(p_{{T}}), log(p_{{z}}) bin {pzidx}', 1, wtrig_binnings[yr][1][-2], wtrig_binnings[yr][1][-1])
#         cjk.Draw(f'log(b_pt)>>highlogpT_{yr}_{pzidx}', f'log(b_pt)>{wtrig_binnings[yr][1][-2]} && log(b_pt)<{wtrig_binnings[yr][1][-1]} && ' + \
#                                                        f'log(b_pz)>{wtrig_binnings[yr][0][pzidx]} && log(b_pz)<{wtrig_binnings[yr][0][pzidx+1]}')
#         jpsi_highlogpT_means[yr][pzidx] = hall.GetMean()

# create D*munu (true) log(pT) trigger effs distributions for high log(pT) bin and given log(pz) bin, and fit a line fixed to m_i, e_i
wtrig_binnings = {yr: extract_th2_bins(wtrig) for yr,wtrig in wtrigs.items()} # log(pz) x log(pT)
for yr,cdst in cdsts.items():
    for pzidx in range(len(wtrig_binnings[yr][0])-1):
        hall = ROOT.TH1D(f'highlogpT_{yr}_{pzidx}', f'D*#mu#nu {yr} Fullsim MC B L0Global TIS eff vs true log(p_{{T}}): high log(p_{{T}}), log(p_{{z}}) bin {pzidx}', nbins, wtrig_binnings[yr][1][-2], wtrig_binnings[yr][1][-1])
        htis = ROOT.TH1D(f'tis_highlogpT_{yr}_{pzidx}', f'D*#mu#nu {yr} Fullsim MC B L0Global TIS eff vs true log(p_{{T}}): high log(p_{{T}}), log(p_{{z}}) bin {pzidx}', nbins, wtrig_binnings[yr][1][-2], wtrig_binnings[yr][1][-1])
        cdst.Draw(f'log(b0_TRUEPT)>>highlogpT_{yr}_{pzidx}', f'log(b0_TRUEPT)>{wtrig_binnings[yr][1][-2]} && log(b0_TRUEPT)<{wtrig_binnings[yr][1][-1]} && ' + \
                                                             f'log(b0_TRUEP_Z)>{wtrig_binnings[yr][0][pzidx]} && log(b0_TRUEP_Z)<{wtrig_binnings[yr][0][pzidx+1]}')
        cdst.Draw(f'log(b0_TRUEPT)>>tis_highlogpT_{yr}_{pzidx}', f'log(b0_TRUEPT)>{wtrig_binnings[yr][1][-2]} && log(b0_TRUEPT)<{wtrig_binnings[yr][1][-1]} && ' + \
                                                                 f'log(b0_TRUEP_Z)>{wtrig_binnings[yr][0][pzidx]} && log(b0_TRUEP_Z)<{wtrig_binnings[yr][0][pzidx+1]} && b0_L0Global_TIS')  
        mean = hall.GetMean()
        eff_highpt = wtrigs[yr].GetBinContent(pzidx+1,len(wtrig_binnings[yr][1])-1)
        htis.Sumw2()
        hall.Sumw2()
        htis.Divide(hall)
        htis.GetXaxis().SetTitle('True log(p_{T})')
        htis.GetYaxis().SetTitle('Efficiency')
        htis.SetLineColor(ROOT.kBlack)
        # fit the linear function
        print(f'\nCheck {yr} eff is reasonable for high log(pT), log(pz) {pzidx} bin: {eff_highpt} (center is {mean})')
        lin = ROOT.TF1(f'linear_highlogpT_tiseff_{yr}_{pzidx}', f'[0]*(x-{mean})+{eff_highpt}', wtrig_binnings[yr][1][-2], wtrig_binnings[yr][1][-1])
        htis.Fit(lin)
        slope = lin.GetParameter(0)
        adhoc_rwgt[yr][pzidx+1] = [mean, eff_highpt, slope] # use the ROOT bin numbering
        lin.SetLineColor(ROOT.kBlue)
        # draw the fixed point, for reference
        fixedpt = ROOT.TGraph()
        fixedpt.AddPoint(mean, eff_highpt)
        fixedpt.SetMarkerColor(ROOT.kRed)
        fixedpt.SetMarkerSize(1.35)
        fixedpt.SetMarkerStyle(4)
        c = ROOT.TCanvas('c', 'c')
        htis.Draw('e1')
        lin.Draw('same')
        fixedpt.Draw('psame')
        c.SaveAs(f'../gen/l0_global_tis_eff-{yr}-dstmunu_fullsim-highlogpT_logpz{pzidx}-adhoc_correction.png')

print(f'Results:\n{adhoc_rwgt}')

# overall eff correction?
# print(f'\n\nComparing overall L0GlobalTIS effs: JpsiK Data vs (fullsim, untriggered) Dstmunu MC:\n')
# for yr,cjk in cjks.items():
#     wtrig = wtrigs[yr]
#     wsum = 0
#     for ev in cjk:
#         pzbin = wtrig.GetXaxis().FindBin(ROOT.TMath.Log(ev.b_pz))
#         ptbin = wtrig.GetYaxis().FindBin(ROOT.TMath.Log(ev.b_pt))
#         wsum += wtrig.GetBinContent(pzbin,ptbin)
#     print(f'{yr} JpsiK Data (TISTOS) eff: {wsum/cjk.GetEntries()}')
# for yr,cdst in cdsts.items():
#     print(f'{yr} Dstmunu (fullsim, MC) MC (real) eff: {cdst.GetEntries("b0_L0Global_TIS")/cdst.GetEntries()}')
#     wtrig = wtrigs[yr]
#     wsum = 0
#     for ev in cdst:
#         pzbin = wtrig.GetXaxis().FindBin(ROOT.TMath.Log(1000*ev.b_true_pz))
#         ptbin = wtrig.GetYaxis().FindBin(ROOT.TMath.Log(1000*ev.b_true_pt))
#         wsum += wtrig.GetBinContent(pzbin,ptbin)
#     print(f'{yr} Dstmunu (fullsim, MC) MC (meas in JpsiK data) eff: {wsum/cdst.GetEntries()}')
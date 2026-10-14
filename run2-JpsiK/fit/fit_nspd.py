#!/usr/bin/env python3
#
# Author: Lucas Meyer Garcia
# Find correction for nSPDHits distribution in MC from B -> J/Psi K
# To be applied AFTER initial reweighting

from argparse import ArgumentParser
import ROOT
import yaml

ROOT.gROOT.SetBatch(True)
ROOT.EnableImplicitMT(16)

global_config = ROOT.RooAbsReal.defaultIntegratorConfig()
global_config.getConfigSection('RooIntegrator1D').setRealValue('maxSteps', 100)


def parse_input():
    parser = ArgumentParser(
        description=
        'generate weights for sequential 2D reweighting using hep_ml, mimicking original gen_weights.py.'
    )
    parser.add_argument(
        '-d',
        '--dataNtp',
        required=True,
        nargs='+',
        help='specify data input ntuples, which must contain sWeight branches.'
    )
    parser.add_argument('-m',
                        '--mcNtp',
                        required=True,
                        nargs='+',
                        help='specify MC input ntuples.')
    parser.add_argument(
        '-o',
        '--output',
        required=True,
        help='specify output ntuple, which contains histograms.')
    parser.add_argument('-t',
                        '--tree',
                        default='tree',
                        help='specify the tree name in the input ntuple.')

    return parser.parse_args()


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()

    c = ROOT.TCanvas('c', 'c', 960, 720)
    var_name = 'nspdhits'
    nspdhits = ROOT.RooRealVar('nspdhits', 'nspdhits', 0, 900)
    nspdhits.setRange('fit_full', 30, 870)

    # Read data events
    # We just want a histogram here to build the RooDataHist, so it's easier with RDataFrame
    data_weight_name = 'sw_sig'
    print(f'Opening tree "{args.tree}" in data file(s) {args.dataNtp}',
          flush=True)
    data_files = ROOT.std.vector('string')(
        args.dataNtp)  # Maybe not needed in root 6.32
    df_data = ROOT.RDataFrame(args.tree, data_files)
    h_data = df_data.Histo1D(
        ('h_nspdhits_data', 'nSPDHits;nSPDHits;Events', 90, 0, 900), var_name,
        data_weight_name)
    datahist_data = ROOT.RooDataHist('datahist', 'datahist', nspdhits,
                                     h_data.GetValue())

    # Read MC events
    # Here we want to build a RooKeysPdf with the MC nSPDHits distribution,
    # so let RooDataSet read the TFile
    print(f'INFO Opening tree "{args.tree}" in MC file(s) {args.mcNtp}',
          flush=True)
    chain_mc = ROOT.TChain(args.tree)
    for filename in args.mcNtp:
        chain_mc.Add(filename)

    mc_cut = ''
    mc_weight_name = 'w'
    w = ROOT.RooRealVar(mc_weight_name, mc_weight_name, 0, 1000)
    print(f'INFO Creating MC dataset', flush=True)
    dataset_mc = ROOT.RooDataSet('dataset_mc', 'dataset_mc', chain_mc,
                                 ROOT.RooArgSet(nspdhits, w), mc_cut,
                                 mc_weight_name)

    print(f'INFO Creating MC PDF', flush=True)
    keys = ROOT.RooKeysPdf('model_nspdhits_mc', 'model_nspdhits_mc', nspdhits,
                           dataset_mc, ROOT.RooKeysPdf.NoMirror, 1.2)

    # Plot MC PDF
    print(f'INFO Plotting MC dataset and PDF', flush=True)
    frame_mc = nspdhits.frame(ROOT.RooFit.Range(0, 900))
    dataset_mc.plotOn(frame_mc, ROOT.RooFit.Binning(90, 0, 900))
    keys.plotOn(frame_mc, ROOT.RooFit.NormRange('fit_full'))
    frame_mc.Draw()
    c.SaveAs(args.output + '/nSPD_mc.pdf')

    # Build model
    l = ROOT.RooRealVar('lambda', 'lambda', 50.0, 0.0, 200.0)
    poisson = ROOT.RooPoisson('poisson', 'Poisson', nspdhits, l)

    nspdhits.setBins(10000, 'cache')  # Binning used for the FFT calculation
    conv = ROOT.RooFFTConvPdf('model_nspdhits_mc_shifted',
                              'model_nspdhits_mc_shifted', nspdhits, keys,
                              poisson)

    # Fit
    conv.chi2FitTo(datahist_data, ROOT.RooFit.Range('fit_full'),
                   ROOT.RooFit.NumCPU(4), ROOT.RooFit.Strategy(2))

    l_first_val = l.getVal()

    # Plot results
    frame = nspdhits.frame(ROOT.RooFit.Range(0, 900))
    datahist_data.plotOn(frame, ROOT.RooFit.Name('data'))
    keys.plotOn(frame, ROOT.RooFit.NormRange('fit_full'),
                ROOT.RooFit.LineColor(ROOT.kBlue),
                ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.Name('mc'))
    conv.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kRed),
                ROOT.RooFit.Name('fit'))
    frame.Draw()

    legend = ROOT.TLegend(0.65, 0.70, 0.88, 0.88)
    legend.AddEntry(frame.findObject('data'), 'Data', 'PE')
    legend.AddEntry(frame.findObject('mc'), 'MC', 'L')
    legend.AddEntry(frame.findObject('fit'), 'MC #otimes Poisson', 'L')
    legend.Draw()

    c.SaveAs(args.output + '/nSPD_fit.pdf')

    # Define Poisson with nSPDHits-dependant parameter
    a = ROOT.RooRealVar('a', 'a', 1.0, 0.1, 5.)
    # b = ROOT.RooRealVar('b', 'b', l_first_val, 0., 100.)
    b = ROOT.RooRealVar('b', 'b', 0.)  # Fit prefers no constant term
    poisson_nd = ROOT.RooGenericPdf(
        'poisson_nd',
        'TMath::PoissonI(nspdhits, TMath::Max(a * TMath::Floor(nspdhits) + b, 0.0) )',
        ROOT.RooArgList(nspdhits, a, b))

    conv_nd = ROOT.RooFFTConvPdf('model_nspdhits_mc_shifted_nd',
                                 'model_nspdhits_mc_shifted_nd', nspdhits,
                                 keys, poisson_nd)
    conv_nd.setBufferFraction(0.0)

    # Fit with nSPDHits-dependant Poisson parameter
    print(f'\n\nINFO Fitting with nSPDHits-dependant Poisson parameter\n\n',
          flush=True)
    conv_nd.chi2FitTo(datahist_data, ROOT.RooFit.Range('fit_full'),
                      ROOT.RooFit.Strategy(2), ROOT.RooFit.NumCPU(4))

    frame_nd = nspdhits.frame(ROOT.RooFit.Range(0, 900))
    datahist_data.plotOn(frame_nd, ROOT.RooFit.Name('data'))
    keys.plotOn(frame_nd, ROOT.RooFit.NormRange('fit_full'),
                ROOT.RooFit.LineColor(ROOT.kBlue),
                ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.Name('mc'))
    conv_nd.plotOn(frame_nd, ROOT.RooFit.LineColor(ROOT.kRed),
                   ROOT.RooFit.Name('fit'))

    frame_nd.Draw()

    legend_nd = ROOT.TLegend(0.65, 0.70, 0.88, 0.88)
    legend_nd.AddEntry(frame_nd.findObject('data'), 'Data', 'PE')
    legend_nd.AddEntry(frame_nd.findObject('mc'), 'MC', 'L')
    legend_nd.AddEntry(frame_nd.findObject('fit'), 'MC #otimes Poisson', 'L')
    legend_nd.Draw()

    c.SaveAs(args.output + '/nSPD_fit_ND.pdf')

    # SAve fit results in yaml file
    results = {'slope': a.getVal(), 'offset': b.getVal()}
    with open(args.output + '/nspd_params.yml', 'w') as f:
        yaml.dump(results, f)

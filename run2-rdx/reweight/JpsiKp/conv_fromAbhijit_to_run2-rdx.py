import ROOT
import glob

# Calculate nbins and ranges of each axis
def histo_axes_info(histo):
    bx = histo.GetNbinsX()
    by = histo.GetNbinsY()
    x1 = histo.GetXaxis().GetBinLowEdge(1)
    x2 = histo.GetXaxis().GetBinLowEdge(bx+1)
    y1 = histo.GetYaxis().GetBinLowEdge(1)
    y2 = histo.GetYaxis().GetBinLowEdge(by+1)
    return [[x1,x2,bx], [y1,y2,by]]

# Input files
# Three histograms: 1. Regular binning, 2. Rectangular binning, 3. Adaptive binning
# Rectangular binning worked well for us. The others we plan to use for systematics
files = glob.glob('fromAbhijit/*.root', recursive=True); files.sort()
for file in files:
    year = file.split("_")[3][:-5]
    # h_kinematic
    lfile = ROOT.TFile(file)
    h_kinematic = lfile.Get("h_rectangularbinn")
    print (year, "h_kinematic", histo_axes_info(h_kinematic))

    # h_occupancy
    #bfile = ROOT.TFile("../JpsiK/root-run2-JpsiK/run2-JpsiK-2016-md-B-ndof_ntracks__pt_eta.root")
    #h_occupancy = bfile.Get("h_occupancy")
    h_occupancy = ROOT.TH2F("h_occupancy", "h_occupancy", 20, 1.0, 1000.0, 20, 0.0, 1800.0)
    h_occupancy.GetXaxis().SetTitle("B PV ndf")
    h_occupancy.GetYaxis().SetTitle("nTracks")
    h_occupancy_axes_info = histo_axes_info(h_occupancy)
    print (year, "h_occupancy", h_occupancy_axes_info)
    for i in range(h_occupancy_axes_info[0][2]):
        for j in range(h_occupancy_axes_info[1][2]):
            h_occupancy.SetBinContent(i+1, j+1, 1.0)

    # Write histograms
    for polarity in ['mu', 'md']:
        ofile = ROOT.TFile("root-run2-JpsiKp/run2-JpsiKp-" + year + "-" + polarity + "-B-ndof_ntracks__p_pt.root", "RECREATE")
        h_kinematic.Write("h_kinematic"); h_occupancy.Write("h_occupancy"); ofile.Close()
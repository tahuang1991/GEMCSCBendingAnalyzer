import ROOT
import os
import time
from plot_functions import *

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetStatW(0.15)
ROOT.gStyle.SetStatH(0.25)

ROOT.gStyle.SetOptStat(111110)

#ROOT.gStyle.SetErrorX(0)
#ROOT.gStyle.SetErrorY(0)

ROOT.gStyle.SetTitleStyle(0)
ROOT.gStyle.SetTitleAlign(13) ## coord in top left
ROOT.gStyle.SetTitleX(0.)
ROOT.gStyle.SetTitleY(1.)
ROOT.gStyle.SetTitleW(1)
ROOT.gStyle.SetTitleH(0.058)
ROOT.gStyle.SetTitleBorderSize(0)

ROOT.gStyle.SetPadLeftMargin(0.126)
ROOT.gStyle.SetPadRightMargin(0.10)
ROOT.gStyle.SetPadTopMargin(0.06)
ROOT.gStyle.SetPadBottomMargin(0.13)

ROOT.gStyle.SetPaintTextFormat(".4f")

ROOT.gStyle.SetMarkerStyle(1)

import numpy as np

color = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen+2, ROOT.kMagenta+2,ROOT.kCyan+2 ]
marker = [20,21,22,23,33]
def setcolortables():
     red = np.array([ 0.0, 1.0, 1.0], dtype=np.double)
     green = np.array([ 0.0, 1.0, 0.0], dtype=np.double)
     blue = np.array([ 1.0, 1.0, 0.0], dtype=np.double)
     stop = np.array([ 0.0, 0.5, 1.0], dtype=np.double)
     #print "red ",red
     ROOT.TColor.CreateGradientColorTable(3, stop, red, green, blue, 40)
     
def cloneDummyHistogram(Histogram):
    dummyhist = Histogram.Clone()
    dummyhist.SetName("dummy")
    for xbin in xrange(dummyhist.GetNbinsX()):
        dummyhist.SetBinContent(xbin+1, 0.0)
        dummyhist.SetBinError(xbin+1, 0.0)
    return dummyhist
    
def getTefficiency(ch, todraw, dencut, numcut, xbins):
    hden = ROOT.TH1F("hden","hden", len(xbins)-1, xbins)
    hnum = ROOT.TH1F("hnum","hnum", len(xbins)-1, xbins)
    print " dencut, ",dencut," numcut ",numcut
    ch.Draw(todraw+">>hden", dencut)
    ch.Draw(todraw+">>hnum", numcut)
    Teff = ROOT.TEfficiency(hnum, hden)
    ROOT.SetOwnership(Teff, False)
    return Teff
    
    
#_____________________________________________________________
branch_list=["lumi","run","event","muonpt","muoneta","muonphi","muoncharge","muonendcap","has_TightID","isGood_GE11","has_GE11","has_ME11","rechit_phi_GE11",
"prop_phi_GE11","rechit_phi_ME11","prop_phi_ME11","muonPx","muonPy","muonPz","muondxy","muondz","muon_ntrackhit","muon_nChameber","muon_chi2","muonPFIso","muonTkIso", "muon_nChamber","has_MediumID","has_LooseID", 
"rechit_eta_ME11", "rechit_x_ME11", "rechit_y_ME11", "rechit_r_ME11", "prop_eta_ME11","prop_x_ME11", "prop_y_ME11", "prop_r_ME11", "rechit_prop_dR_ME11","chamber_ME11", "roll_GE11", "chamber_GE11", "rechit_eta_GE11", "rechit_x_GE11",
"rechit_y_GE11", "rechit_r_GE11", "prop_eta_GE11", "prop_x_GE11", "prop_y_GE11","prop_r_GE11","rechit_prop_dR_GE11","has_cscseg_st",
"cscseg_phi_st","cscseg_eta_st","cscseg_x_st","cscseg_y_st","cscseg_z_st","cscseg_prop_dR_st",
"cscseg_chamber_st","cscseg_ring_st","has_csclct_st","csclct_phi_st","csclct_eta_st","csclct_x_st", "csclct_y_st", "csclct_r_st","csclct_chamber_st","csclct_ring_st",
"csclct_prop_dR_st", "csclct_keyStrip_st", "csclct_keyWG_st","csclct_matchWin_st","csclct_pattern_st", "has_propME11", "ring_ME11",
"chamber_propME11","ring_propME11","has_propGE11","roll_propGE11","chamber_propGE11",  "dphi_CSCL1_GE11L1",
"dphi_fitCSCL1_GE11L1","dphi_CSCSeg_GE11Rechit","dphi_keyCSCRechit_GE11Rechit","dphi_CSCRechits_GE11Rechit","dphi_propCSC_propGE11"]
chain = ROOT.TChain("SliceTestAnalysis/MuonData")
#chain.Add('/eos/uscms/store/user/mkhurana/GEMCSCBending_2018C/out_ana_10*.root')
#chain.Add("slicetest_ana.root")
#chain.Add("2018C_out_ana_v2.root")
#chain.Add("out_ana_all_2018C.root")
chain.Add("GEMCSCBending_2018C_v11.root")
#chain.Add("GEMCSCAan_Run2018D_ZMu_323470-323470_all.root")
#chain.Add("GEMCSCBending_doublemuon_2018C_v1.root")
#plotdir = "GEMCSCBending_2018C_doubleMuon_singlemuon_plots/"
#plotdir = "GEMCSCBending_2018C_doubleMuon_singlemuon_plots_alignment/"
#plotdir = "GEMCSCBending_2018C_v11_plots_prop_rechit_dphi_normalized/"
#plotdir = "GEMCSCAan_Run2018D_ZMu_323470_324200_prop_rechit_dphi_normalized/"
plotdir = "GEMCSCBending_2018C_singlemuon_plots_residual_wholechamber/"
os.system("mkdir -p "+plotdir)




#plot_muons(chain, "has_TightID", plotdir)
#plot_deltaR(chain, "has_TightID && muonpt>10","muon p_{T}> 30, tight ID", plotdir)
plot_dPhiGEMMuon(chain, "has_MediumID && muonpt>20", "RecoMuon: Medium ID, p_{T}>20 GeV", plotdir)
#plot_GEMHitsVsChamber(chain, "has_MediumID && muonpt>20", "muon: medium ID", plotdir)
#plot_CSCHits(chain, "has_TightID && muonpt>10", "muon p_{T}> 10, tight ID",plotdir)
#plot_GEMdXVsRoll(chain, "has_TightID && muonpt>25", "muon tight ID, p_{T}>25", plotdir)
#plot_GEMHits(chain, "has_TightID && muonpt>10", "muon p_{T}> 10, tight ID",plotdir)
#plot_GEMRechitVsMuon(chain, "has_TightID && muonpt>25"," tight ID,muon p_{T}>25 " , plotdir)
#plot_GEMPhiVsCSCPhi(chain, "has_TightID && muonpt>30", "muon p_{T}> 30, tight ID", plotdir)
#plot_deltaPhi(chain, "has_TightID", "tight ID",plotdir)
#plot_deltaPhi(chain, "has_TightID", "tight ID",plotdir)
#plot_deltaPhiVspt(chain, "has_TightID ", "muon tight ID", plotdir)
#plot_GEMalignment(chain, "has_MediumID && muonpt>25", "medium ID",plotdir)

ptbin = [10.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 80.0, 100.0, 150.0, 200.0]
myptbin = np.asarray(ptbin)


#plot_GEMHitEff_ptbin(chain, "has_TightID && muoneta < 0 && run == 319347", "Muon tight ID", plotdir)
#plot_GEMHitEff_phi(chain,  "has_TightID && muonpt>=25 && muoneta < 0 && hasGEMdata>0", "Muon tight ID, p_{T}^{reco}>25", os.path.join(plotdir, "GEMRechit_Eff_phibin_pt25_"))
##strip
#plot_GEMHitEff_phi(chain,  "has_TightID && muonpt>=25 && muoneta < 0 && run == 319347", "Muon tight ID, p_{T}^{reco}>25", os.path.join(plotdir, "GEMRechit_Eff_stripbin_pt25_run319347_"))
#plot_ME11CSCHitEff(chain, "prop_phi_ME11", "has_TightID && muonpt>=25 && muoneta < 0", 72, -3.1415, 3.1415,  "global #phi", "Muon tight ID, p_{T}^{reco}>25",  os.path.join(plotdir, "ME11Rechit_eff_phibin_pt25_"))
#plot_ME11CSCHitEff(chain, "chamber_propME11", "has_TightID && muonpt>=25 && muoneta < 0", 36, 1.0, 37.0,  "ME11, chamber", "Muon tight ID, p_{T}^{reco}>25",  os.path.join(plotdir, "ME11Rechit_eff_chamberbin_pt25_"))
#plot_CSCSegmentEff(chain, "prop_chamber_st", "has_TightID && muonpt>=25 && muoneta < 0", 36, 1.0, 37.0, "MEX1, chamber", "Muon tight ID, p_{T}^{reco}>25", os.path.join(plotdir, "CSCsegment_eff_chamberbin_pt25_"))

#plot_residual_1D(chain, "has_TightID && muonpt>=25", "residual [cm]", 50, -5.0, 5.0, "tight ID, p_{T}^{reco}>25", os.path.join(plotdir, "GEMalignment_residual_1D"))
#plot_residual_1D_v2(chain, "has_TightID && muonpt>=15", "residual [cm]", 50, -5.0, 5.0, "tight ID, p_{T}^{reco}>15", os.path.join(plotdir, "GEMalignment_residual_vfat6"))
